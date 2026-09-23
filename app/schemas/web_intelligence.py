from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class JobSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100, description="Job title, role, or keywords to search")
    location: str | None = Field(default=None, max_length=100, description="Optional target location or city")
    company: str | None = Field(default=None, max_length=100, description="Optional company name filter")
    source: str | None = Field(default=None, max_length=100, description="Optional source filter")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results to return")


class ExternalJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source: str
    title: str
    company: str
    location: str
    employment_type: str | None = None
    description: str
    skills: list[str] = Field(default_factory=list)
    url: str
    posted_at: str | None = None


class JobSearchResponse(BaseModel):
    query: str
    location: str | None = None
    total_results: int
    results: list[ExternalJob]


class CandidateJobComparisonRequest(BaseModel):
    resume_id: int
    job_title: str = Field(..., min_length=1, max_length=200, description="Title of the discovered public job")
    job_description: str = Field(..., min_length=10, max_length=100000, description="Full description text of the discovered job")
    job_source_url: str | None = Field(default=None, max_length=500, description="Optional URL of the source job posting")


class CandidateJobComparisonResponse(BaseModel):
    resume_id: int
    job_title: str
    job_source_url: str | None = None
    match_score: float | None = None
    overall_match_score: float | None = None
    required_score: float | None = None
    preferred_score: float | None = None
    score_status: str
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    strong_skills: list[str] = Field(default_factory=list)
    weak_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    needs_verification: list[str] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    skill_gaps: dict[str, Any] = Field(default_factory=dict)
    improvement_suggestions: list[str] = Field(default_factory=list)
    detected_skills: list[str] = Field(default_factory=list)
    matched_requirements: list[dict[str, Any]] = Field(default_factory=list)
    weak_requirements: list[dict[str, Any]] = Field(default_factory=list)
    missing_requirements: list[dict[str, Any]] = Field(default_factory=list)


class RecruiterCandidateDiscoveryRequest(BaseModel):
    location: str | None = Field(default=None, max_length=100, description="Optional location filter")
    skills_filter: list[str] = Field(default_factory=list, max_length=20, description="Optional list of skills to prioritize")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of candidate profiles to discover")


class ExternalCandidate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source: str
    source_id: str
    name: str
    headline: str
    location: str
    public_skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    profile_url: str


class CandidateMatchAnalysis(BaseModel):
    match_score: float | None = None
    matched_requirements: list[str] = Field(default_factory=list)
    weak_requirements: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    public_evidence_summary: str | None = None


class DiscoveredCandidateResult(BaseModel):
    source: str
    source_profile_url: str
    name: str
    headline: str
    location: str
    public_skills: list[str] = Field(default_factory=list)
    match_analysis: CandidateMatchAnalysis


class RecruiterCandidateDiscoveryResponse(BaseModel):
    job_id: int
    job_title: str
    candidates_count: int
    results: list[DiscoveredCandidateResult]
