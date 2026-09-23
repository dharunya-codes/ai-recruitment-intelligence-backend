from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.schemas.job_requirement import (
    JDUploadRequest,
    JobRequirementResponse,
    JobRequirementsResponse,
)
from app.services.jd_parser import parse_jd
from app.services.requirement_extractor import extract_requirements
from app.utils.security import get_company_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_company_job(job_id: int, company_id: int, db: Session) -> Job:
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.company_id == company_id)
        .first()
    )
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


@router.post(
    "/{job_id}/jd",
    response_model=JobRequirementsResponse,
)
def submit_job_description(
    job_id: int,
    payload: JDUploadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> JobRequirementsResponse:
    job = get_company_job(job_id, current_user.company_id, db)
    normalized_description = parse_jd(payload.description)
    extracted_requirements = extract_requirements(normalized_description)

    db.query(JobRequirement).filter(JobRequirement.job_id == job.id).delete(
        synchronize_session=False
    )
    job.description = payload.description
    requirements = [
        JobRequirement(
            job_id=job.id,
            requirement=item["requirement"],
            category=item["category"],
            importance=item["importance"],
        )
        for item in extracted_requirements
    ]
    db.add_all(requirements)
    db.commit()

    return JobRequirementsResponse(
        job_id=job.id,
        requirements=[JobRequirementResponse.model_validate(item) for item in requirements],
    )


@router.get(
    "/{job_id}/requirements",
    response_model=JobRequirementsResponse,
)
def get_job_requirements(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> JobRequirementsResponse:
    job = get_company_job(job_id, current_user.company_id, db)
    requirements = (
        db.query(JobRequirement)
        .filter(JobRequirement.job_id == job.id)
        .order_by(JobRequirement.id)
        .all()
    )
    return JobRequirementsResponse(
        job_id=job.id,
        requirements=requirements,
    )


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> Job:
    job = Job(
        company_id=current_user.company_id,
        title=payload.title,
        department=payload.department,
        location=payload.location,
        employment_type=payload.employment_type,
        description=payload.description,
        minimum_experience=payload.minimum_experience,
        education=payload.education,
        certifications=payload.certifications,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[JobResponse])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> list[Job]:
    return (
        db.query(Job)
        .filter(Job.company_id == current_user.company_id)
        .order_by(Job.id)
        .all()
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> Job:
    return get_company_job(job_id, current_user.company_id, db)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> Job:
    job = get_company_job(job_id, current_user.company_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> dict[str, str]:
    job = get_company_job(job_id, current_user.company_id, db)
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}