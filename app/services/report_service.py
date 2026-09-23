from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.evidence import SkillEvidence
from app.models.job import Job
from app.models.report import Report
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.verification import VerificationQuestion
from app.services.action_priority_service import build_actions
from app.services.answer_evaluation_service import evaluate_answer
from app.services.candidate_readiness_service import build_readiness_profile
from app.services.career_intelligence_service import build_career_intelligence
from app.services.gap_engine import generate_skill_gap_summary
from app.services.genai_service import GenAIService
from app.services.improvement_plan_service import build_improvement_plan
from app.services.matching_engine import MATCHED, MISSING, WEAK, match_resume_to_requirements
from app.services.project_recommendation_service import recommend_projects
from app.services.resume_quality_service import analyze_resume_quality
from app.services.role_catalog import extract_custom_role_expectations, role_expectations
from app.services.role_roadmap_service import build_role_roadmap
from app.services.scoring_engine import calculate_candidate_score
from app.services.skill_extractor import extract_skills
from app.services.skill_priority_engine import build_advanced_gaps, build_skill_priorities


def _json_object(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return default


def _format_datetime(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


class ReportService:
    """
    Orchestrates candidate intelligence pipelines into structured, explainable reports.
    Source of truth remains deterministic backend analysis; GenAI generates grounded summaries.
    """

    def __init__(self, db: Session, genai_service: GenAIService | None = None) -> None:
        self.db = db
        self.genai = genai_service or GenAIService()

    def _get_resume(self, resume_id: int) -> Resume:
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume

    def _collect_pipeline_data(self, resume: Resume) -> dict[str, Any]:
        candidate = resume.candidate
        job = resume.job
        extracted_text = resume.extracted_text or ""

        # 1. Matching & Scoring
        if job is not None:
            requirements = (
                self.db.query(JobRequirement)
                .filter(JobRequirement.job_id == job.id)
                .order_by(JobRequirement.id)
                .all()
            )
            matches = match_resume_to_requirements(extracted_text, requirements)
            score_data = calculate_candidate_score(matches)
            gap_summary = generate_skill_gap_summary(matches)
            target_role = job.title
            job_info = {
                "id": job.id,
                "title": job.title,
                "department": getattr(job, "department", "General") or "General",
                "location": getattr(job, "location", "Remote") or "Remote",
                "employment_type": getattr(job, "employment_type", "FULL_TIME") or "FULL_TIME",
                "description": job.description,
            }
        else:
            analysis_data = dict(resume.analysis_data or {})
            target_role = resume.target_role or "Target Role"
            job_info = {
                "id": None,
                "title": target_role,
                "department": "General",
                "location": "Remote",
                "employment_type": "FULL_TIME",
                "description": resume.target_job_description or "Role-based evaluation",
            }
            if analysis_data and "requirement_analysis" in analysis_data:
                matches = analysis_data.get("requirement_analysis", [])
                score_data = {
                    "overall_match_score": analysis_data.get("overall_match_score"),
                    "required_score": analysis_data.get("required_score"),
                    "preferred_score": analysis_data.get("preferred_score"),
                    "score_status": analysis_data.get("score_status", "CALCULATED"),
                    "counts": analysis_data.get("counts", {}),
                    "category_breakdown": analysis_data.get("category_breakdown", {}),
                    "requirement_analysis": matches,
                }
                gap_summary = analysis_data.get("skill_gap") or generate_skill_gap_summary(matches)
            else:
                # Standalone fallback expectations
                expectations = role_expectations(target_role) or extract_custom_role_expectations(target_role)
                req_objects = [
                    type("Req", (), {"id": i + 1, "requirement": s, "category": "SKILL", "importance": "REQUIRED"})()
                    for i, s in enumerate(expectations.get("skills", []))
                ]
                matches = match_resume_to_requirements(extracted_text, req_objects)
                score_data = calculate_candidate_score(matches)
                gap_summary = generate_skill_gap_summary(matches)

        requirement_analysis = score_data.get("requirement_analysis", matches)

        # 2. Skill Evidence (Resume Evidence - strictly separated)
        db_evidence = (
            self.db.query(SkillEvidence)
            .filter(SkillEvidence.resume_id == resume.id)
            .order_by(SkillEvidence.id)
            .all()
        )
        evidence_by_skill = {item.skill.casefold(): item for item in db_evidence}

        structured_evidence: list[dict[str, Any]] = []
        for match in requirement_analysis:
            skill_name = str(match.get("requirement", ""))
            db_ev = evidence_by_skill.get(skill_name.casefold())
            status = str(match.get("match_status", "MISSING")).upper()
            evidence_text = match.get("evidence_text") or (db_ev.evidence_text if db_ev else None)
            is_matched = status == MATCHED
            is_weak = status == WEAK
            lowered_text = (evidence_text or "").casefold()

            project_ev = db_ev.project_evidence if db_ev else bool("project" in lowered_text or "built" in lowered_text or "developed" in lowered_text)
            internship_ev = db_ev.internship_evidence if db_ev else bool("intern" in lowered_text or "internship" in lowered_text)
            cert_ev = db_ev.certification_evidence if db_ev else bool("certif" in lowered_text)

            strength = "STRONG" if is_matched else ("WEAK" if is_weak else "MISSING")
            structured_evidence.append({
                "skill": skill_name,
                "resume_mention": is_matched or is_weak,
                "project_evidence": project_ev,
                "internship_evidence": internship_ev,
                "certification_evidence": cert_ev,
                "evidence_text": evidence_text,
                "evidence_strength": strength,
                "verification_status": db_ev.verification_status if db_ev and db_ev.verification_status else ("not_required" if is_matched else "needs_verification"),
            })

        # Categorized skills
        strong_skills = [item for item in structured_evidence if item["evidence_strength"] == "STRONG"]
        moderate_skills = [item for item in structured_evidence if item["evidence_strength"] == "MODERATE"]
        weak_skills = [item for item in structured_evidence if item["evidence_strength"] == "WEAK"]
        missing_skills = [item for item in structured_evidence if item["evidence_strength"] == "MISSING"]
        needs_verification = [item for item in structured_evidence if item["evidence_strength"] in {"WEAK", "MISSING"}]

        # 3. Verification Questions and Answers
        db_verification = (
            self.db.query(VerificationQuestion)
            .filter(VerificationQuestion.resume_id == resume.id)
            .order_by(VerificationQuestion.id)
            .all()
        )
        verification_questions: list[dict[str, Any]] = []
        verification_answers: list[dict[str, Any]] = []
        candidate_reported_evidence: list[dict[str, Any]] = []
        verified_skills: list[str] = []
        verification_by_skill: dict[str, str] = {}

        for vq in db_verification:
            is_answered = bool(vq.answer and vq.answer.strip())
            ev_status = vq.evidence_status or ("CANDIDATE_VERIFIED" if vq.candidate_reported_evidence else "NOT_VERIFIED")
            q_data = {
                "id": vq.id,
                "skill": vq.skill,
                "question": vq.question,
                "answer": vq.answer,
                "status": vq.status or ("ANSWERED" if is_answered else "PENDING"),
                "candidate_reported_evidence": vq.candidate_reported_evidence,
                "evidence_status": ev_status,
            }
            verification_questions.append(q_data)
            if is_answered:
                verification_answers.append(q_data)
                if vq.candidate_reported_evidence:
                    candidate_reported_evidence.append({
                        "skill": vq.skill,
                        "evidence": vq.candidate_reported_evidence,
                        "source": "candidate-reported; not resume evidence",
                    })
                    verified_skills.append(vq.skill)
            verification_by_skill[vq.skill] = ev_status

        if not db_verification:
            verification_status = "not_required" if not weak_skills else "not_completed"
        elif len(verification_answers) == len(db_verification):
            verification_status = "completed"
        elif verification_answers:
            verification_status = "partially_verified"
        else:
            verification_status = "pending"

        # 4. Assessment & Answers
        assessment = (
            self.db.query(Assessment)
            .filter(Assessment.resume_id == resume.id)
            .order_by(Assessment.id.desc())
            .first()
        )
        assessment_questions_data: list[dict[str, Any]] = []
        assessment_answers_data: list[dict[str, Any]] = []
        assessment_feedback: list[str] = []
        assessment_areas_to_improve: list[str] = []
        assessment_by_skill: dict[str, float] = {}

        paste_detected = False
        typing_duration = 0
        started_at: datetime | None = None
        submitted_at: datetime | None = None

        if assessment is not None:
            assessment_status = assessment.status or "NOT_STARTED"
            assessment_score = assessment.score
            for q in assessment.assessment_questions:
                ans = max(q.candidate_answers, key=lambda a: a.id, default=None) if q.candidate_answers else None
                ans_text = ans.answer if ans else None
                score_val = ans.score if ans else None
                fb_text = ans.feedback if ans else None

                if ans:
                    if ans.paste_attempt_detected:
                        paste_detected = True
                    if ans.typing_duration:
                        typing_duration += ans.typing_duration
                    if ans.started_at and (started_at is None or ans.started_at < started_at):
                        started_at = ans.started_at
                    if ans.submitted_at and (submitted_at is None or ans.submitted_at > submitted_at):
                        submitted_at = ans.submitted_at
                    if score_val is not None and q.skill:
                        assessment_by_skill[q.skill] = score_val
                    if fb_text:
                        assessment_feedback.append(fb_text)

                q_entry = {
                    "id": q.id,
                    "question": q.question,
                    "skill": q.skill,
                    "question_type": q.question_type or "TECHNICAL",
                    "difficulty": q.difficulty or "MEDIUM",
                    "answer": ans_text,
                    "score": score_val,
                    "feedback": fb_text,
                }
                assessment_questions_data.append(q_entry)
                if ans_text:
                    assessment_answers_data.append(q_entry)

            stored_strengths = _json_object(assessment.strengths, [])
            stored_improvements = _json_object(assessment.areas_for_improvement, [])
            assessment_feedback = list(dict.fromkeys(assessment_feedback + stored_strengths))
            assessment_areas_to_improve = list(dict.fromkeys(stored_improvements))
        else:
            assessment_status = "not_completed"
            assessment_score = None

        integrity_data = {
            "paste_attempt_detected": paste_detected,
            "typing_duration": typing_duration if typing_duration > 0 else None,
            "started_at": _format_datetime(started_at),
            "submitted_at": _format_datetime(submitted_at),
            "note": "Paste attempt detected during assessment." if paste_detected else "Standard input profile observed.",
        }

        # 5. Skill Gaps & Priorities
        skill_priorities = build_skill_priorities(requirement_analysis, verification_by_skill, assessment_by_skill)
        advanced_gaps = build_advanced_gaps(requirement_analysis, verification_by_skill)
        gap_items: list[dict[str, Any]] = []
        for item in gap_summary.get("priority_gaps", []):
            gap_items.append({
                "skill": item.get("requirement"),
                "category": item.get("category", "SKILL"),
                "importance": item.get("importance", "REQUIRED"),
                "match_status": item.get("match_status", "MISSING"),
                "priority": item.get("priority", "HIGH"),
                "reason": "Required or preferred role competency with limited or missing resume evidence.",
            })

        # 6. Resume Quality
        quality_findings = analyze_resume_quality(extracted_text)
        resume_quality_data = {
            "findings_count": len(quality_findings),
            "findings": quality_findings,
            "clarity": "HIGH" if not quality_findings else "NEEDS_REVIEW",
            "completeness": "HIGH" if len(extracted_text.strip()) >= 300 else "LOW",
        }

        # 7. Suggestions & Improvements
        improvement_suggestions = [f["recommendation"] for f in quality_findings if f.get("recommendation")]
        for m in missing_skills[:3]:
            improvement_suggestions.append(f"Add demonstrable experience or project work demonstrating {m['skill']}.")
        for w in weak_skills[:2]:
            improvement_suggestions.append(f"Strengthen evidence for {w['skill']} with specific metrics or tooling used.")
        improvement_suggestions = list(dict.fromkeys(improvement_suggestions)) or [
            "Keep role-relevant project evidence specific, quantifiable, and outcome-focused."
        ]

        # 8. Career Intelligence, Recommended Projects, Roadmap & Action Priorities
        verification_gaps = [q["skill"] for q in verification_questions if q["status"] != "ANSWERED"]
        assessment_gaps = [q["skill"] for q in assessment_questions_data if (q.get("score") or 0) <= 6 and q.get("skill")]
        career_intel = build_career_intelligence(
            target_role=target_role,
            analysis={
                "matched_requirements": [m for m in requirement_analysis if m.get("match_status") == MATCHED],
                "counts": score_data.get("counts", {}),
                "requirements_source": "COMPANY_JD" if job is not None else "ROLE_BASED_EXPECTATIONS",
            },
            priorities=skill_priorities,
            advanced_gaps=advanced_gaps,
            verification_gaps=verification_gaps,
            assessment_gaps=assessment_gaps,
            resume_quality_issues=quality_findings,
        )
        rec_projects = recommend_projects(target_role, advanced_gaps)
        roadmap_data = build_role_roadmap(target_role, requirement_analysis)
        action_priorities_data = build_actions(skill_priorities, quality_findings, verification_gaps, assessment_gaps)

        # 9. Score Breakdown
        cat_breakdown = score_data.get("category_breakdown", {})
        overall_score = score_data.get("overall_match_score")
        score_breakdown = {
            "required_skills": score_data.get("required_score", overall_score),
            "preferred_skills": score_data.get("preferred_score", overall_score),
            "experience": cat_breakdown.get("EXPERIENCE", {}).get("score", overall_score),
            "education": cat_breakdown.get("EDUCATION", {}).get("score", 85.0 if overall_score else None),
            "project_relevance": cat_breakdown.get("PROJECT", {}).get("score", overall_score),
            "evidence_strength": overall_score,
            **cat_breakdown,
        }

        # 10. GenAI Context
        context = {
            "candidate": {
                "id": candidate.id if candidate else None,
                "name": candidate.name if candidate else "Candidate",
                "email": candidate.email if candidate else None,
                "phone": candidate.phone if candidate else None,
            },
            "job": job_info,
            "resume": {
                "id": resume.id,
                "file_name": resume.file_name,
                "created_at": _format_datetime(resume.created_at),
            },
            "resume_text": extracted_text,
            "resume_analysis": {
                "overall_match_score": overall_score,
                "required_score": score_data.get("required_score"),
                "preferred_score": score_data.get("preferred_score"),
                "score_status": score_data.get("score_status"),
                "counts": score_data.get("counts", {}),
                "matched_requirements": [m for m in requirement_analysis if m.get("match_status") == MATCHED],
                "weak_requirements": [m for m in requirement_analysis if m.get("match_status") == WEAK],
                "missing_requirements": [m for m in requirement_analysis if m.get("match_status") == MISSING],
                "score_breakdown": score_breakdown,
                "skill_gap": gap_summary,
            },
            "evidence": structured_evidence,
            "skills": {
                "strong": [s["skill"] for s in strong_skills],
                "moderate": [s["skill"] for s in moderate_skills],
                "weak": [s["skill"] for s in weak_skills],
                "missing": [s["skill"] for s in missing_skills],
                "needs_verification": [s["skill"] for s in needs_verification],
            },
            "verification": verification_questions,
            "assessment": {
                "status": assessment_status,
                "score": assessment_score,
                "total_questions": len(assessment_questions_data),
                "answered": len(assessment_answers_data),
                "feedback": assessment_feedback,
                "strengths": stored_strengths if assessment else [],
                "areas_for_improvement": assessment_areas_to_improve,
                "integrity": integrity_data,
            },
            "skill_gaps": gap_items,
            "resume_quality": resume_quality_data,
            "improvement_suggestions": improvement_suggestions,
            "career_intelligence": career_intel,
            "recommended_projects": rec_projects,
            "roadmap": roadmap_data,
            "action_priorities": action_priorities_data,
        }

        return context

    def generate_company_report(self, resume_id: int) -> Report:
        """Generate and persist the comprehensive Company recruitment intelligence report."""
        resume = self._get_resume(resume_id)
        context = self._collect_pipeline_data(resume)

        ai_summary, gen_status = self.genai.generate_company_ai_summary(context)

        report_data = {
            "report_type": "company",
            "generation_status": gen_status,
            "candidate": context["candidate"],
            "resume": context["resume"],
            "job": context["job"],
            "match_analysis": {
                "overall_score": context["resume_analysis"]["overall_match_score"],
                "score_breakdown": context["resume_analysis"]["score_breakdown"],
                "explanation": (
                    f"Candidate matches {context['resume_analysis']['counts'].get('matched', 0)} of "
                    f"{context['resume_analysis']['counts'].get('total', 0)} required role criteria. "
                    "All metrics derived deterministically from resume and job requirements."
                ),
            },
            "skills": {
                "strong": [item for item in context["evidence"] if item["evidence_strength"] == "STRONG"],
                "moderate": [item for item in context["evidence"] if item["evidence_strength"] == "MODERATE"],
                "weak": [item for item in context["evidence"] if item["evidence_strength"] == "WEAK"],
                "missing": [item for item in context["evidence"] if item["evidence_strength"] == "MISSING"],
                "needs_verification": [item for item in context["evidence"] if item["evidence_strength"] in {"WEAK", "MISSING"}],
            },
            "evidence": context["evidence"],
            "verification": {
                "status": "completed" if all(q["status"] == "ANSWERED" for q in context["verification"]) and context["verification"] else ("pending" if context["verification"] else "not_required"),
                "questions": context["verification"],
                "answers": [q for q in context["verification"] if q["status"] == "ANSWERED"],
                "candidate_reported_evidence": [
                    {
                        "skill": q["skill"],
                        "evidence": q["candidate_reported_evidence"],
                        "source": "candidate-reported; not resume evidence",
                    }
                    for q in context["verification"]
                    if q.get("candidate_reported_evidence")
                ],
            },
            "assessment": {
                "status": context["assessment"]["status"],
                "score": context["assessment"]["score"],
                "questions": [q for q in context["assessment"].get("questions", [])] or [
                    {
                        "question": q["question"],
                        "skill": q["skill"],
                        "question_type": q["question_type"],
                        "difficulty": q["difficulty"],
                        "answer": q["answer"],
                        "score": q["score"],
                        "feedback": q["feedback"],
                    }
                    for q in context.get("assessment_questions", [])
                ],
                "answers": [q for q in context["assessment"].get("questions", []) if q.get("answer")] or [],
                "feedback": context["assessment"]["feedback"],
                "integrity": context["assessment"]["integrity"],
            },
            "skill_gaps": context["skill_gaps"],
            "resume_quality": context["resume_quality"],
            "improvement_areas": context["improvement_suggestions"],
            "ai_summary": ai_summary,
            # Backward compatibility fields
            "role": context["job"]["title"],
            "match_score": context["resume_analysis"]["overall_match_score"],
            "matched_requirements": context["resume_analysis"]["matched_requirements"],
            "weak_requirements": context["resume_analysis"]["weak_requirements"],
            "missing_requirements": context["resume_analysis"]["missing_requirements"],
            "evidence_summary": [
                {"skill": e["skill"], "evidence_strength": e["evidence_strength"], "evidence_text": e["evidence_text"], "source": "resume"}
                for e in context["evidence"]
            ],
            "verification_summary": [
                {"skill": v["skill"], "status": v["status"], "candidate_reported_evidence": v["candidate_reported_evidence"], "source": "candidate-reported; not resume evidence"}
                for v in context["verification"]
            ],
            "assessment_summary": context["assessment"],
            "final_summary": (
                "This report is decision support based on the submitted resume, verification responses, "
                "and assessment responses. HR remains the final decision-maker."
            ),
        }

        return self._save_or_update_report(resume, "HR", report_data)

    def generate_candidate_report(self, resume_id: int) -> Report:
        """Generate and persist the comprehensive Candidate career intelligence report."""
        resume = self._get_resume(resume_id)
        context = self._collect_pipeline_data(resume)

        ai_summary, gen_status = self.genai.generate_candidate_ai_summary(context)

        report_data = {
            "report_type": "candidate",
            "generation_status": gen_status,
            "candidate": context["candidate"],
            "resume": context["resume"],
            "job": context["job"],
            "match_analysis": {
                "overall_score": context["resume_analysis"]["overall_match_score"],
                "score_breakdown": context["resume_analysis"]["score_breakdown"],
                "explanation": (
                    f"Your profile demonstrates {context['resume_analysis']['counts'].get('matched', 0)} of "
                    f"{context['resume_analysis']['counts'].get('total', 0)} target skills and competencies."
                ),
            },
            "skill_analysis": {
                "strong": [item for item in context["evidence"] if item["evidence_strength"] == "STRONG"],
                "moderate": [item for item in context["evidence"] if item["evidence_strength"] == "MODERATE"],
                "weak": [item for item in context["evidence"] if item["evidence_strength"] == "WEAK"],
                "missing": [item for item in context["evidence"] if item["evidence_strength"] == "MISSING"],
                "needs_verification": [item for item in context["evidence"] if item["evidence_strength"] in {"WEAK", "MISSING"}],
            },
            "evidence_analysis": context["evidence"],
            "verification_results": {
                "questions": context["verification"],
                "answers": [q for q in context["verification"] if q["status"] == "ANSWERED"],
                "verified_skills": [q["skill"] for q in context["verification"] if q.get("candidate_reported_evidence")],
                "candidate_reported_evidence": [
                    {
                        "skill": q["skill"],
                        "evidence": q["candidate_reported_evidence"],
                        "source": "candidate-reported; not resume evidence",
                    }
                    for q in context["verification"]
                    if q.get("candidate_reported_evidence")
                ],
            },
            "assessment_result": {
                "status": context["assessment"]["status"],
                "score": context["assessment"]["score"],
                "feedback": context["assessment"]["feedback"],
                "areas_to_improve": context["assessment"]["areas_for_improvement"],
                "questions": context["assessment"].get("questions", []),
                "integrity": context["assessment"]["integrity"],
            },
            "resume_quality": context["resume_quality"],
            "skill_gaps": context["skill_gaps"],
            "improvement_suggestions": context["improvement_suggestions"],
            "career_intelligence": context["career_intelligence"],
            "recommended_projects": context["recommended_projects"],
            "roadmap": context["roadmap"],
            "action_priorities": context["action_priorities"],
            "ai_summary": ai_summary,
            # Backward compatibility fields
            "strong_skills": [s["skill"] for s in context["evidence"] if s["evidence_strength"] == "STRONG"],
            "weak_skills": [s["skill"] for s in context["evidence"] if s["evidence_strength"] == "WEAK"],
            "missing_skills": [s["skill"] for s in context["evidence"] if s["evidence_strength"] == "MISSING"],
            "verification_summary": [
                {"skill": v["skill"], "status": v["status"], "candidate_reported_evidence": v["candidate_reported_evidence"], "source": "candidate-reported; not resume evidence"}
                for v in context["verification"]
            ],
            "assessment_summary": context["assessment"],
            "assessment_strengths": context["assessment"].get("strengths", []),
            "assessment_improvement_areas": context["assessment"].get("areas_for_improvement", []),
            "resume_improvements": context["improvement_suggestions"],
            "project_improvements": context["improvement_suggestions"],
            "executive_summary": (
                f"For {context['job']['title']}, available resume evidence demonstrates "
                f"{context['resume_analysis']['counts'].get('matched', 0)} of {context['resume_analysis']['counts'].get('total', 0)} requirements."
            ),
        }

        return self._save_or_update_report(resume, "CANDIDATE", report_data)

    def _save_or_update_report(self, resume: Resume, report_type: str, report_data: dict[str, Any]) -> Report:
        """Persist report avoiding uncontrolled duplicates; supports both canonical and legacy types."""
        # Find existing by exact or case-insensitive / alias match
        type_aliases = [report_type, report_type.upper(), report_type.lower()]
        if report_type.lower() in {"company", "hr"}:
            type_aliases.extend(["company", "HR", "COMPANY", "hr"])
        elif report_type.lower() in {"candidate"}:
            type_aliases.extend(["candidate", "CANDIDATE"])

        existing = (
            self.db.query(Report)
            .filter(Report.resume_id == resume.id, Report.report_type.in_(type_aliases))
            .first()
        )

        if existing is not None:
            existing.report_data = report_data
            existing.report_type = report_type
            self.db.commit()
            self.db.refresh(existing)
            return existing

        report = Report(
            candidate_id=resume.candidate_id,
            job_id=resume.job_id,
            resume_id=resume.id,
            report_type=report_type,
            report_data=report_data,
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def generate_all_reports(self, resume_id: int, report_types: tuple[str, ...] = ("company", "candidate")) -> dict[str, Report]:
        """Generate requested report types and return map with both canonical and uppercase aliases."""
        reports: dict[str, Report] = {}
        for r_type in report_types:
            normalized = r_type.lower()
            if normalized in {"company", "hr"}:
                rep = self.generate_company_report(resume_id)
                reports["company"] = rep
                reports["HR"] = rep
            elif normalized in {"candidate"}:
                rep = self.generate_candidate_report(resume_id)
                reports["candidate"] = rep
                reports["CANDIDATE"] = rep
        return reports

    def get_reports(self, resume_id: int, report_type: str | None = None) -> list[Report]:
        """Fetch generated reports for a resume, filtering by type if specified."""
        query = self.db.query(Report).filter(Report.resume_id == resume_id)
        if report_type:
            normalized = report_type.lower()
            if normalized in {"company", "hr"}:
                query = query.filter(Report.report_type.in_(["company", "HR", "COMPANY", "hr"]))
            elif normalized in {"candidate"}:
                query = query.filter(Report.report_type.in_(["candidate", "CANDIDATE"]))
            else:
                query = query.filter(Report.report_type == report_type)
        return query.order_by(Report.id).all()
