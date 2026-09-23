from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.jobs import get_company_job
from app.database.database import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.schemas.analysis import RequirementMatch, ResumeAnalysisResponse
from app.schemas.resume import ResumeResponse, ResumeTextResponse
from app.services.matching_engine import MISSING, MATCHED, match_resume_to_requirements
from app.services.gap_engine import generate_skill_gap_summary
from app.services.resume_parser import (
    extract_candidate_info,
    extract_text_from_docx,
    extract_text_from_pdf,
)
from app.services.skill_extractor import extract_skills
from app.services.scoring_engine import calculate_candidate_score
from app.services.audit_service import record_audit_event
from app.utils.security import get_company_user

router = APIRouter(tags=["Resumes", "Analysis"])

UPLOAD_DIRECTORY = Path("uploads") / "resumes"
MAX_RESUME_SIZE = 10 * 1024 * 1024
MAX_EXTRACTED_TEXT_SIZE = 200_000
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def _resume_response(resume: Resume) -> ResumeResponse:
    return ResumeResponse(
        id=resume.id,
        candidate_id=resume.candidate_id,
        job_id=resume.job_id,
        file_name=resume.file_name,
        candidate_name=resume.candidate.name,
        candidate_email=resume.candidate.email,
        candidate_phone=resume.candidate.phone,
        created_at=resume.created_at,
    )


def _get_company_resume(resume_id: int, company_id: int, db: Session) -> Resume:
    resume = (
        db.query(Resume)
        .join(Job, Resume.job_id == Job.id)
        .filter(Resume.id == resume_id, Job.company_id == company_id)
        .first()
    )
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


def _validate_upload(filename: str, content_type: str | None, content: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported")
    if content_type and content_type not in {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/octet-stream",
    }:
        raise HTTPException(status_code=400, detail="Unsupported resume content type")
    if extension == ".pdf" and not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Invalid PDF file")
    if extension == ".docx" and not content.startswith(b"PK"):
        raise HTTPException(status_code=400, detail="Invalid DOCX file")
    return extension


def _find_or_create_candidate(
    info: dict[str, str | None],
    db: Session,
) -> Candidate:
    email = info["email"]
    phone = info["phone"]
    candidate = None
    if email:
        candidate = db.query(Candidate).filter(Candidate.email == email).first()
    if candidate is None and phone:
        candidate = db.query(Candidate).filter(Candidate.phone == phone).first()
    if candidate is not None:
        return candidate

    stored_email = email or f"unknown-{uuid.uuid4().hex}@local.invalid"
    candidate = Candidate(
        name=info["name"] or "Unknown Candidate",
        email=stored_email,
        phone=phone,
    )
    db.add(candidate)
    db.flush()
    return candidate


@router.post("/jobs/{job_id}/resumes", response_model=ResumeResponse, status_code=201)
def upload_resume(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> ResumeResponse:
    job = get_company_job(job_id, current_user.company_id, db)
    original_name = Path(file.filename or "resume").name
    content = file.file.read(MAX_RESUME_SIZE + 1)
    if len(content) > MAX_RESUME_SIZE:
        raise HTTPException(status_code=413, detail="Resume file exceeds the 10 MB limit")
    extension = _validate_upload(original_name, file.content_type, content)

    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{extension}"
    stored_path = UPLOAD_DIRECTORY / stored_name
    stored_path.write_bytes(content)
    try:
        extracted_text = (
            extract_text_from_pdf(stored_path)
            if extension == ".pdf"
            else extract_text_from_docx(stored_path)
        )
        if not re.search(r"\S", extracted_text):
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from resume",
            )
        if len(extracted_text) > MAX_EXTRACTED_TEXT_SIZE:
            raise HTTPException(status_code=400, detail="Extracted resume content is too large")
        info = extract_candidate_info(extracted_text)
        candidate = _find_or_create_candidate(info, db)
        resume = Resume(
            candidate_id=candidate.id,
            job_id=job.id,
            file_name=original_name,
            file_path=stored_path.as_posix(),
            extracted_text=extracted_text,
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        record_audit_event(db, "RESUME_UPLOAD", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
        return _resume_response(resume)
    except HTTPException:
        stored_path.unlink(missing_ok=True)
        db.rollback()
        raise
    except Exception as exc:
        stored_path.unlink(missing_ok=True)
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not process resume") from exc


@router.get("/jobs/{job_id}/resumes", response_model=list[ResumeResponse])
def list_job_resumes(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> list[ResumeResponse]:
    job = get_company_job(job_id, current_user.company_id, db)
    resumes = db.query(Resume).filter(Resume.job_id == job.id).order_by(Resume.id).all()
    return [_resume_response(resume) for resume in resumes]


@router.get("/resumes/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> ResumeResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    return _resume_response(resume)


@router.get("/resumes/{resume_id}/text", response_model=ResumeTextResponse)
def get_resume_text(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> ResumeTextResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    return ResumeTextResponse(
        resume_id=resume.id,
        extracted_text=resume.extracted_text or "",
    )


@router.get("/resumes/{resume_id}/analysis", response_model=ResumeAnalysisResponse)
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> ResumeAnalysisResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    requirements = (
        db.query(JobRequirement)
        .filter(JobRequirement.job_id == resume.job_id)
        .order_by(JobRequirement.id)
        .all()
    )
    matches = match_resume_to_requirements(resume.extracted_text or "", requirements)
    def response_match(item: dict[str, object]) -> RequirementMatch:
        status_value = str(item["match_status"])
        importance = str(item["importance"] or "REQUIRED")
        return RequirementMatch(
            **item,
            verification_required=status_value == "WEAK"
            or importance == "REQUIRED" and status_value == MISSING,
        )

    matched = [response_match(item) for item in matches if item["match_status"] == MATCHED]
    weak = [response_match(item) for item in matches if item["match_status"] == "WEAK"]
    missing = [response_match(item) for item in matches if item["match_status"] == MISSING]
    score = calculate_candidate_score(matches)
    skill_gap = generate_skill_gap_summary(matches)

    return ResumeAnalysisResponse(
        resume_id=resume.id,
        job_id=resume.job_id,
        candidate_id=resume.candidate_id,
        candidate_name=resume.candidate.name,
        detected_skills=extract_skills(resume.extracted_text or ""),
        matched_requirements=matched,
        weak_requirements=weak,
        missing_requirements=missing,
        **score,
        skill_gap=skill_gap,
    )