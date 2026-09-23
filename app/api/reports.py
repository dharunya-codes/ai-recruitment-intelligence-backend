from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.resumes import _get_company_resume
from app.database.database import get_db
from app.models.assessment import Assessment
from app.models.evidence import SkillEvidence
from app.models.report import Report
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.models.verification import VerificationQuestion
from app.schemas.report import ReportResponse, ReportsResponse
from app.services.gap_engine import generate_skill_gap_summary
from app.services.audit_service import record_audit_event
from app.services.genai_service import GenAIService
from app.services.matching_engine import match_resume_to_requirements
from app.services.scoring_engine import calculate_candidate_score
from app.utils.security import get_current_user
from app.utils.security import get_candidate_user

router = APIRouter(prefix="/reports", tags=["Reports"])


def _json_object(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return default


def _assessment_context(resume_id: int, db: Session) -> dict[str, Any]:
    assessment = (
        db.query(Assessment)
        .filter(Assessment.resume_id == resume_id)
        .order_by(Assessment.id.desc())
        .first()
    )
    if assessment is None:
        return {
            "status": "NOT_AVAILABLE",
            "score": None,
            "total_questions": 0,
            "answered": 0,
            "unanswered": 0,
            "category_scores": {},
            "strengths": [],
            "areas_for_improvement": [],
        }
    return {
        "status": assessment.status or "NOT_STARTED",
        "score": assessment.score,
        "total_questions": assessment.total_questions or len(assessment.assessment_questions),
        "answered": assessment.answered or 0,
        "unanswered": assessment.unanswered or 0,
        "category_scores": _json_object(assessment.category_scores, {}),
        "strengths": _json_object(assessment.strengths, []),
        "areas_for_improvement": _json_object(assessment.areas_for_improvement, []),
    }


def _build_context(resume, db: Session) -> dict[str, Any]:
    if resume.job_id is None and resume.analysis_data:
        analysis = resume.analysis_data
        verification = [
            {"skill": item.skill, "status": item.evidence_status or item.status, "candidate_reported_evidence": item.candidate_reported_evidence}
            for item in db.query(VerificationQuestion).filter(VerificationQuestion.resume_id == resume.id).order_by(VerificationQuestion.id).all()
        ]
        evidence = [
            {"skill": item.skill, "evidence_strength": item.evidence_strength, "evidence_text": item.evidence_text}
            for item in db.query(SkillEvidence).filter(SkillEvidence.resume_id == resume.id).order_by(SkillEvidence.id).all()
        ]
        return {
            "candidate": {"name": resume.candidate.name},
            "job": {"title": resume.target_role or "Target role", "description": resume.target_job_description},
            "resume_text": resume.extracted_text or "",
            "resume_analysis": analysis,
            "evidence": evidence,
            "verification": verification,
            "assessment": _assessment_context(resume.id, db),
        }
    requirements = (
        db.query(JobRequirement)
        .filter(JobRequirement.job_id == resume.job_id)
        .order_by(JobRequirement.id)
        .all()
    )
    matches = match_resume_to_requirements(resume.extracted_text or "", requirements)
    score = calculate_candidate_score(matches)
    analysis = {
        "overall_match_score": score.get("overall_match_score"),
        "required_score": score.get("required_score"),
        "preferred_score": score.get("preferred_score"),
        "score_status": score.get("score_status"),
        "counts": score.get("counts", {}),
        "matched_requirements": [item for item in matches if item["match_status"] == "MATCHED"],
        "weak_requirements": [item for item in matches if item["match_status"] == "WEAK"],
        "missing_requirements": [item for item in matches if item["match_status"] == "MISSING"],
        "skill_gap": generate_skill_gap_summary(matches),
    }
    verification = [
        {
            "skill": item.skill,
            "status": item.evidence_status or item.status,
            "candidate_reported_evidence": item.candidate_reported_evidence,
        }
        for item in db.query(VerificationQuestion)
        .filter(VerificationQuestion.resume_id == resume.id)
        .order_by(VerificationQuestion.id)
        .all()
    ]
    evidence = [
        {
            "skill": item.skill,
            "evidence_strength": item.evidence_strength,
            "evidence_text": item.evidence_text,
        }
        for item in db.query(SkillEvidence)
        .filter(SkillEvidence.resume_id == resume.id)
        .order_by(SkillEvidence.id)
        .all()
    ]
    return {
        "candidate": {"name": resume.candidate.name},
        "job": {"title": resume.job.title, "description": resume.job.description},
        "resume_text": resume.extracted_text or "",
        "resume_analysis": analysis,
        "evidence": evidence,
        "verification": verification,
        "assessment": _assessment_context(resume.id, db),
    }


def _response(report: Report) -> ReportResponse:
    data = report.report_data if isinstance(report.report_data, dict) else {}
    return ReportResponse(
        id=report.id,
        resume_id=report.resume_id,
        report_type=report.report_type,
        generation_status=str(data.get("generation_status", "UNKNOWN")),
        report_data=data,
        created_at=report.created_at,
    )


def _get_reports(resume_id: int, db: Session) -> list[Report]:
    return (
        db.query(Report)
        .filter(Report.resume_id == resume_id, Report.report_type.in_(["CANDIDATE", "HR"]))
        .order_by(Report.id)
        .all()
    )


def _generate_reports(resume_id: int, db: Session, report_types: tuple[str, ...] = ("CANDIDATE", "HR")) -> ReportsResponse:
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    context = _build_context(resume, db)
    generated = GenAIService().generate_reports(context)
    existing = {report.report_type: report for report in _get_reports(resume_id, db)}
    reports = {}
    generated_data = (("CANDIDATE", generated["candidate"]), ("HR", generated["hr"]))
    for report_type, report_data in generated_data:
        if report_type not in report_types:
            continue
        report = existing.get(report_type)
        if report is None:
            report = Report(
                candidate_id=resume.candidate_id,
                job_id=resume.job_id,
                resume_id=resume.id,
                report_type=report_type,
                report_data=report_data,
            )
            db.add(report)
        else:
            report.report_data = report_data
        reports[report_type] = report
    db.commit()
    for report in reports.values():
        db.refresh(report)
    return ReportsResponse(
        resume_id=resume.id,
        reports={key: _response(value) for key, value in reports.items()},
    )


@router.post("/{resume_id}/generate", response_model=ReportsResponse)
def generate_reports(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        existing = {report.report_type: report for report in _get_reports(resume.id, db) if report.report_type == "CANDIDATE"}
        if existing:
            return ReportsResponse(resume_id=resume.id, reports={"CANDIDATE": _response(existing["CANDIDATE"])})
        result = _generate_reports(resume.id, db, ("CANDIDATE",))
        record_audit_event(db, "REPORT_GENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
        return result
    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    existing = {report.report_type: report for report in _get_reports(resume.id, db)}
    if {"CANDIDATE", "HR"}.issubset(existing):
        return ReportsResponse(
            resume_id=resume.id,
            reports={key: _response(value) for key, value in existing.items()},
        )
    result = _generate_reports(resume.id, db)
    record_audit_event(db, "REPORT_GENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
    return result


@router.post("/{resume_id}/regenerate", response_model=ReportsResponse)
def regenerate_reports(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        result = _generate_reports(resume_id, db, ("CANDIDATE",))
        record_audit_event(db, "REPORT_REGENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume_id, success=True)
        return result
    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    _get_company_resume(resume_id, current_user.company_id, db)
    result = _generate_reports(resume_id, db)
    record_audit_event(db, "REPORT_REGENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume_id, success=True)
    return result


@router.get("/{resume_id}", response_model=ReportsResponse)
def get_reports(
    resume_id: int,
    report_type: str | None = Query(default=None, pattern="^(CANDIDATE|HR)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        if report_type == "HR":
            raise HTTPException(status_code=404, detail="Report not found")
        reports = [report for report in _get_reports(resume.id, db) if report.report_type == "CANDIDATE"]
        return ReportsResponse(resume_id=resume.id, reports={report.report_type: _response(report) for report in reports})
    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    reports = _get_reports(resume.id, db)
    if report_type:
        reports = [report for report in reports if report.report_type == report_type]
    return ReportsResponse(
        resume_id=resume.id,
        reports={report.report_type: _response(report) for report in reports},
    )