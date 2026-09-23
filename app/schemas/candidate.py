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
    role_source: str = "ROLE_CATALOG"
    analysis_type: str = "ROLE_COMPATIBILITY"
    match_score: float | None = None
    overall_match_score: float | None = None
    required_score: float | None = None
    preferred_score: float | None = None
    score_status: str
    detected_skills: list[str] = Field(default_factory=list)
    matched_requirements: list[dict[str, Any]] = Field(default_factory=list)
    weak_requirements: list[dict[str, Any]] = Field(default_factory=list)
    missing_requirements: list[dict[str, Any]] = Field(default_factory=list)
    requirement_analysis: list[dict[str, Any]] = Field(default_factory=list)
    category_breakdown: dict[str, Any] = Field(default_factory=dict)
    counts: dict[str, int] = Field(default_factory=dict)
    skill_gap: dict[str, Any] = Field(default_factory=dict)
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    strong_skills: list[str] = Field(default_factory=list)
    weak_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    needs_verification: list[str] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    skill_gaps: dict[str, Any] = Field(default_factory=dict)
    resume_quality: dict[str, Any] = Field(default_factory=dict)
    improvement_suggestions: list[str] = Field(default_factory=list)