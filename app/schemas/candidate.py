from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CandidateRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=200)


class CandidateProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateResumeResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int | None
    file_name: str
    target_role: str | None
    score_type: str | None
    created_at: datetime


class CandidateAnalysisRequest(BaseModel):
    target_role: str = Field(..., min_length=2, max_length=200)
    job_description: str | None = Field(default=None, max_length=100000)


class CandidateAnalysisResponse(BaseModel):
    resume_id: int
    target_role: str
    score_type: str
    requirements_source: str
    overall_match_score: float | None
    required_score: float | None
    preferred_score: float | None
    score_status: str
    detected_skills: list[str]
    matched_requirements: list[dict[str, Any]]
    weak_requirements: list[dict[str, Any]]
    missing_requirements: list[dict[str, Any]]
    requirement_analysis: list[dict[str, Any]]
    category_breakdown: dict[str, Any]
    counts: dict[str, int]
    skill_gap: dict[str, Any]