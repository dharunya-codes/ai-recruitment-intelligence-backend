from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.resumes import _get_company_resume
from app.database.database import get_db
from app.models.report import Report
from app.models.resume import Resume
from app.models.user import User
from app.schemas.report import ReportResponse, ReportsResponse
from app.services.audit_service import record_audit_event
from app.services.report_service import ReportService
from app.utils.security import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


def _response(report: Report) -> ReportResponse:
    data = report.report_data if isinstance(report.report_data, dict) else {}
    gen_status = str(data.get("generation_status", "completed"))
    return ReportResponse(
        id=report.id,
        resume_id=report.resume_id,
        report_type=report.report_type,
        generation_status=gen_status,
        report_data=data,
        created_at=report.created_at,
    )


def _format_reports_response(resume_id: int, reports: list[Report]) -> ReportsResponse:
    return ReportsResponse(
        resume_id=resume_id,
        reports={rep.report_type: _response(rep) for rep in reports},
    )


@router.post("/{resume_id}/generate", response_model=ReportsResponse)
def generate_reports(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    service = ReportService(db)
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        existing = service.get_reports(resume.id, "candidate")
        if existing:
            return _format_reports_response(resume.id, existing)
        service.generate_candidate_report(resume.id)
        record_audit_event(db, "REPORT_GENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
        reports = service.get_reports(resume.id, "candidate")
        return _format_reports_response(resume.id, reports)

    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume = _get_company_resume(resume_id, current_user.company_id, db)
    existing = service.get_reports(resume.id)
    types_present = {r.report_type.lower() for r in existing}
    if {"company", "candidate"}.issubset(types_present) or {"hr", "candidate"}.issubset(types_present):
        return _format_reports_response(resume.id, existing)

    service.generate_company_report(resume.id)
    service.generate_candidate_report(resume.id)
    record_audit_event(db, "REPORT_GENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
    all_reps = service.get_reports(resume.id)
    return _format_reports_response(resume.id, all_reps)


@router.post("/{resume_id}/regenerate", response_model=ReportsResponse)
def regenerate_reports(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    service = ReportService(db)
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        service.generate_candidate_report(resume.id)
        record_audit_event(db, "REPORT_REGENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
        reports = service.get_reports(resume.id, "candidate")
        return _format_reports_response(resume.id, reports)

    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume = _get_company_resume(resume_id, current_user.company_id, db)
    service.generate_company_report(resume.id)
    service.generate_candidate_report(resume.id)
    record_audit_event(db, "REPORT_REGENERATED", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
    all_reps = service.get_reports(resume.id)
    return _format_reports_response(resume.id, all_reps)


@router.get("/{resume_id}", response_model=ReportsResponse)
def get_reports(
    resume_id: int,
    report_type: str | None = Query(default=None, pattern="^(?i)(CANDIDATE|HR|candidate|company)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportsResponse:
    service = ReportService(db)
    if current_user.role == "CANDIDATE":
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == current_user.id).first()
        if resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        if report_type and report_type.lower() in {"hr", "company"}:
            raise HTTPException(status_code=404, detail="Report not found")
        reports = service.get_reports(resume.id, "candidate")
        return _format_reports_response(resume.id, reports)

    if current_user.role not in {"HR", "COMPANY_ADMIN"} or current_user.company_id is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume = _get_company_resume(resume_id, current_user.company_id, db)
    reports = service.get_reports(resume.id, report_type)
    return _format_reports_response(resume.id, reports)