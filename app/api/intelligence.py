from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.candidate import _get_candidate_resume
from app.api.resumes import _get_company_resume
from app.database.database import get_db
from app.models.assessment import Assessment
from app.models.analysis_snapshot import AnalysisSnapshot
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.user import User
from app.models.verification import VerificationQuestion
from app.schemas.intelligence import CareerQuestionRequest, CareerQuestionResponse, IntelligenceResponse, MultiJobRequest, MultiJobResponse
from app.services.action_priority_service import build_actions
from app.services.analysis_cache_service import analysis_cache, make_analysis_cache_key
from app.services.career_intelligence_service import build_career_intelligence
from app.services.career_question_service import answer_career_question
from app.services.candidate_readiness_service import build_readiness_profile
from app.services.evidence_consistency_service import analyze_evidence_consistency
from app.services.improvement_plan_service import build_improvement_plan
from app.services.multi_job_analysis_service import analyze_resume_against_jobs
from app.services.evidence_builder_service import build_evidence_recommendations
from app.services.project_recommendation_service import recommend_projects
from app.services.progress_service import compare_snapshots
from app.services.role_roadmap_service import build_role_roadmap
from app.services.resume_quality_service import analyze_resume_quality
from app.services.skill_priority_engine import build_advanced_gaps, build_skill_priorities, transferable_skills
from app.utils.security import get_candidate_user, get_company_user, get_current_user

router = APIRouter(tags=["Candidate Intelligence", "Career Intelligence"])


def _assessment_data(resume_id: int, db: Session) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    assessment = db.query(Assessment).filter(Assessment.resume_id == resume_id).order_by(Assessment.id.desc()).first()
    if assessment is None:
        return {"status": "NOT_AVAILABLE", "score": None, "strengths": [], "areas_for_improvement": []}, []
    results: list[dict[str, Any]] = []
    for question in assessment.assessment_questions:
        answer = max(question.candidate_answers, key=lambda item: item.id, default=None)
        if answer is not None:
            results.append({"skill": question.skill, "score": answer.score or 0, "status": answer.evaluation_status or "NOT_EVALUATED", "missing_points": json.loads(answer.missing_points or "[]")})
    return {
        "status": assessment.status or "NOT_STARTED",
        "score": assessment.score,
        "strengths": json.loads(assessment.strengths or "[]"),
        "areas_for_improvement": json.loads(assessment.areas_for_improvement or "[]"),
    }, results


def _verification_data(resume_id: int, db: Session) -> list[dict[str, Any]]:
    return [
        {"skill": item.skill, "status": item.status or "PENDING", "evidence_status": item.evidence_status or "NOT_VERIFIED"}
        for item in db.query(VerificationQuestion).filter(VerificationQuestion.resume_id == resume_id).all()
    ]


def _intelligence_data(resume, db: Session) -> dict[str, Any]:
    analysis = resume.analysis_data or {}
    verification = _verification_data(resume.id, db)
    assessment, assessment_results = _assessment_data(resume.id, db)
    quality = analyze_resume_quality(resume.extracted_text or "")
    priorities = build_skill_priorities(
        analysis.get("requirement_analysis", []),
        {item["skill"]: item["evidence_status"] for item in verification},
        {item["skill"]: item["score"] for item in assessment_results},
    )
    advanced_gaps = build_advanced_gaps(
        analysis.get("requirement_analysis", []),
        {item["skill"]: item["evidence_status"] for item in verification},
    )
    readiness = build_readiness_profile(analysis, verification, assessment, quality)
    plan = build_improvement_plan(priorities, assessment.get("areas_for_improvement", []), quality)
    consistency = analyze_evidence_consistency(analysis.get("requirement_analysis", []), verification, assessment_results)
    return {
        "readiness": readiness,
        "resume_quality": quality,
        "skill_priorities": priorities,
        "advanced_gaps": advanced_gaps,
        "transferability": transferable_skills(analysis.get("detected_skills", [])),
        "improvement_plan": plan,
        "evidence_consistency": consistency,
        "assessment_feedback": [
            {
                **item,
                "recommended_focus": (
                    f"Review {item['skill']} concepts: {', '.join(item['missing_points'])}."
                    if item["missing_points"]
                    else f"Practice explaining {item['skill']} with a concrete example."
                ),
            }
            for item in assessment_results
            if item["score"] <= 6
        ],
    }


def _candidate_intelligence(resume_id: int, db: Session, user: User) -> dict[str, Any]:
    resume = _get_candidate_resume(resume_id, user, db)
    if not resume.analysis_data:
        raise HTTPException(status_code=422, detail="Analyze the resume before requesting intelligence")
    return _intelligence_data(resume, db)


def _build_career_data(resume, db: Session) -> dict[str, Any]:
    data = _intelligence_data(resume, db)
    analysis = resume.analysis_data or {}
    verification = _verification_data(resume.id, db)
    verification_gaps = [item["skill"] for item in verification if item["status"] != "ANSWERED"]
    assessment_gaps = [item["skill"] for item in data["assessment_feedback"]]
    career = build_career_intelligence(
        target_role=resume.target_role or "Target role",
        analysis=analysis,
        priorities=data["skill_priorities"],
        advanced_gaps=data["advanced_gaps"],
        verification_gaps=verification_gaps,
        assessment_gaps=assessment_gaps,
        resume_quality_issues=data["resume_quality"],
    )
    return {
        "career_intelligence": career,
        "actions": build_actions(data["skill_priorities"], data["resume_quality"], verification_gaps, assessment_gaps),
        "projects": recommend_projects(resume.target_role or "Target role", data["advanced_gaps"]),
        "evidence_builder": build_evidence_recommendations(data["advanced_gaps"]),
        "roadmap": build_role_roadmap(resume.target_role or "Target role", analysis.get("requirement_analysis", [])),
        "progress": compare_snapshots([
            snapshot.analysis_data
            for snapshot in db.query(AnalysisSnapshot).filter(AnalysisSnapshot.resume_id == resume.id, AnalysisSnapshot.candidate_user_id == resume.candidate_user_id).order_by(AnalysisSnapshot.id).all()
        ]),
    }


def _career_data(resume, db: Session) -> dict[str, Any]:
    verification_state = _verification_data(resume.id, db)
    assessment_state, assessment_results = _assessment_data(resume.id, db)
    key = make_analysis_cache_key(
        owner_scope=resume.candidate_user_id or f"company:{resume.job_id}",
        resume_text=resume.extracted_text or "",
        job_context={
            "analysis": resume.analysis_data or {},
            "verification": verification_state,
            "assessment": assessment_state,
            "assessment_results": assessment_results,
        },
        target_role=resume.target_role,
    )
    return analysis_cache.get_or_compute(key, lambda: _build_career_data(resume, db))


@router.get("/candidate/analysis/{resume_id}/readiness", response_model=IntelligenceResponse, summary="Get candidate readiness dimensions")
def candidate_readiness(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    data = _candidate_intelligence(resume_id, db, current_user)
    return IntelligenceResponse(resume_id=resume_id, data={"dimensions": data["readiness"], "assessment_feedback": data["assessment_feedback"]})


@router.get("/candidate/analysis/{resume_id}/improvement-plan", response_model=IntelligenceResponse, summary="Get candidate improvement plan")
def candidate_improvement_plan(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    return IntelligenceResponse(resume_id=resume_id, data=_candidate_intelligence(resume_id, db, current_user)["improvement_plan"])


@router.get("/candidate/analysis/{resume_id}/resume-quality", response_model=IntelligenceResponse, summary="Get objective resume quality findings")
def candidate_resume_quality(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    return IntelligenceResponse(resume_id=resume_id, data={"findings": _candidate_intelligence(resume_id, db, current_user)["resume_quality"]})


@router.get("/candidate/analysis/{resume_id}/skill-priorities", response_model=IntelligenceResponse, summary="Get explainable skill priorities")
def candidate_skill_priorities(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    data = _candidate_intelligence(resume_id, db, current_user)
    return IntelligenceResponse(resume_id=resume_id, data={"priorities": data["skill_priorities"], "advanced_gaps": data["advanced_gaps"], "transferability": data["transferability"]})


@router.get("/candidate/analysis/{resume_id}/career-intelligence", response_model=IntelligenceResponse, summary="Get personalized candidate career intelligence")
def candidate_career_intelligence(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    if not resume.analysis_data:
        raise HTTPException(status_code=422, detail="Analyze the resume before requesting career intelligence")
    return IntelligenceResponse(resume_id=resume_id, data=_career_data(resume, db)["career_intelligence"])


@router.get("/candidate/analysis/{resume_id}/actions", response_model=IntelligenceResponse, summary="Get prioritized candidate actions")
def candidate_actions(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    return IntelligenceResponse(resume_id=resume_id, data={"actions": _career_data(resume, db)["actions"]})


@router.get("/candidate/analysis/{resume_id}/projects", response_model=IntelligenceResponse, summary="Get role-aware project recommendations")
def candidate_projects(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    return IntelligenceResponse(resume_id=resume_id, data={"projects": _career_data(resume, db)["projects"]})


@router.get("/candidate/analysis/{resume_id}/evidence-builder", response_model=IntelligenceResponse, summary="Get resume evidence recommendations")
def candidate_evidence_builder(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    return IntelligenceResponse(resume_id=resume_id, data={"recommendations": _career_data(resume, db)["evidence_builder"]})


@router.get("/candidate/analysis/{resume_id}/roadmap", response_model=IntelligenceResponse, summary="Get a supported role roadmap")
def candidate_roadmap(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    return IntelligenceResponse(resume_id=resume_id, data=_career_data(resume, db)["roadmap"])


@router.get("/candidate/analysis/{resume_id}/progress", response_model=IntelligenceResponse, summary="Compare candidate analysis snapshots")
def candidate_progress(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> IntelligenceResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    return IntelligenceResponse(resume_id=resume_id, data=_career_data(resume, db)["progress"])


@router.post("/candidate/analysis/{resume_id}/career-question", response_model=CareerQuestionResponse, summary="Answer a supported career intelligence question")
def candidate_career_question(resume_id: int, payload: CareerQuestionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> CareerQuestionResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    data = _career_data(resume, db)["career_intelligence"]
    return CareerQuestionResponse(resume_id=resume_id, data=answer_career_question(payload.question_type, data))


@router.get("/analysis/{resume_id}/career-intelligence", response_model=IntelligenceResponse, summary="Get authorized HR career intelligence")
def hr_career_intelligence(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_company_user)) -> IntelligenceResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    if not resume.analysis_data:
        raise HTTPException(status_code=422, detail="Analysis is not available")
    return IntelligenceResponse(resume_id=resume_id, data=_career_data(resume, db)["career_intelligence"])


@router.get("/analysis/{resume_id}/evidence-consistency", response_model=IntelligenceResponse, summary="Compare resume, verification, and assessment evidence")
def evidence_consistency(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> IntelligenceResponse:
    if current_user.role == "CANDIDATE":
        data = _candidate_intelligence(resume_id, db, current_user)
    else:
        resume = _get_company_resume(resume_id, current_user.company_id, db)
        data = _intelligence_data(resume, db)
    return IntelligenceResponse(resume_id=resume_id, data={"items": data["evidence_consistency"]})


@router.post("/analysis/multi-job", response_model=MultiJobResponse, summary="Analyze one resume independently against authorized jobs")
def multi_job_analysis(payload: MultiJobRequest, db: Session = Depends(get_db), current_user: User = Depends(get_company_user)) -> MultiJobResponse:
    resume = _get_company_resume(payload.resume_id, current_user.company_id, db)
    jobs = []
    for job in db.query(Job).filter(Job.id.in_(payload.job_ids), Job.company_id == current_user.company_id).all():
        requirements = db.query(JobRequirement).filter(JobRequirement.job_id == job.id).order_by(JobRequirement.id).all()
        jobs.append((job, requirements))
    return MultiJobResponse(resume_id=resume.id, analyses=analyze_resume_against_jobs(resume.extracted_text or "", jobs))