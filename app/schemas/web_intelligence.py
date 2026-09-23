from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# -------------------------------------------------------------
# Recruiter Web Intelligence Schemas
# -------------------------------------------------------------
class RecruiterSearchRequest(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200, description="Job title or role name")
    job_description: str = Field(..., min_length=10, max_length=50000, description="Full job description text")
    limit: int = Field(default=10, ge=1, le=30, description="Maximum number of candidate/project results")


class JobRequirementsWeb(BaseModel):
    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    experience: str | None = None
    education: str | None = None
    certifications: list[str] = Field(default_factory=list)
    role_keywords: list[str] = Field(default_factory=list)


class SupportingEvidenceItem(BaseModel):
    skill: str
    source: str
    evidence: str
    url: str


class DiscoveredCandidateProfileWeb(BaseModel):
    name: str
    headline: str
    profile_url: str
    source: str
    source_type: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_or_unverified: list[str] = Field(default_factory=list)
    public_evidence: list[SupportingEvidenceItem] = Field(default_factory=list)


class GitHubRepositoryInfo(BaseModel):
    name: str
    url: str
    description: str | None = None
    languages: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    stars: int | None = None


class GitHubCandidateResult(BaseModel):
    username: str
    profile_url: str
    repositories: list[GitHubRepositoryInfo] = Field(default_factory=list)
    matched_skills: list[str] = Field(default_factory=list)
    source: str = "GitHub"
    source_type: str = "github_api"


class RecruiterMatchingResult(BaseModel):
    profile: str
    source: str
    source_type: str
    public_profile_url: str
    github_url: str | None = None
    matched_skills: list[str] = Field(default_factory=list)
    supporting_projects: list[str] = Field(default_factory=list)
    supporting_evidence: list[SupportingEvidenceItem] = Field(default_factory=list)
    missing_or_unverified: list[str] = Field(default_factory=list)
    explanation: str
    match_score: float | None = None


class RecruiterSearchResponse(BaseModel):
    job_requirements: JobRequirementsWeb
    profiles: list[DiscoveredCandidateProfileWeb] = Field(default_factory=list)
    github_results: list[GitHubCandidateResult] = Field(default_factory=list)
    matching_results: list[RecruiterMatchingResult] = Field(default_factory=list)
    source_status: dict[str, Any] = Field(default_factory=dict)
    compliance_notice: str | None = None


# -------------------------------------------------------------
# Candidate Web Intelligence Schemas
# -------------------------------------------------------------
class CandidateJobSearchRequestWeb(BaseModel):
    target_role: str = Field(..., min_length=1, max_length=150, description="Target role name (e.g. Backend Developer)")
    location: str | None = Field(default=None, max_length=100, description="Optional target location")
    limit: int = Field(default=10, ge=1, le=30, description="Maximum number of public jobs to discover")


class DiscoveredWebJob(BaseModel):
    job_title: str
    company: str
    location: str
    employment_type: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience: str | None = None
    education: str | None = None
    job_description_summary: str
    source: str
    source_type: str
    job_url: str
    date_info: str | None = None


class CandidateJobSearchResponseWeb(BaseModel):
    target_role: str
    expanded_keywords: list[str] = Field(default_factory=list)
    jobs: list[DiscoveredWebJob] = Field(default_factory=list)


class CandidateJobMatchRequestWeb(BaseModel):
    resume_id: int = Field(..., description="ID of candidate's uploaded resume")
    target_role: str = Field(..., min_length=1, max_length=150, description="Target role name (e.g. Backend Developer)")
    location: str | None = Field(default=None, max_length=100, description="Optional location filter")
    limit: int = Field(default=10, ge=1, le=30, description="Maximum jobs to match against")


class SkillDemandItem(BaseModel):
    skill: str
    job_count: int
    frequency_percentage: float | None = None


class CandidateJobMatchResult(BaseModel):
    job_title: str
    company: str
    location: str
    employment_type: str | None = None
    job_url: str
    source: str
    source_type: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    related_skills: list[str] = Field(default_factory=list)
    experience_alignment: str
    skill_gap: list[str] = Field(default_factory=list)
    match_score: float
    match_explanation: str


class CandidateJobMatchResponseWeb(BaseModel):
    target_role: str
    resume_id: int
    jobs: list[CandidateJobMatchResult] = Field(default_factory=list)
    skill_matches: list[str] = Field(default_factory=list)
    skill_gaps: list[str] = Field(default_factory=list)
    observed_skill_demand: list[SkillDemandItem] = Field(default_factory=list)
    market_summary_label: str = "Observed requirements in discovered jobs"


class CandidateGitHubRequestWeb(BaseModel):
    target_role: str = Field(..., min_length=1, max_length=150, description="Target role for GitHub project discovery")


class CandidateGitHubProjectItem(BaseModel):
    name: str
    url: str
    description: str | None = None
    stars: int | None = None
    languages: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)


class CandidateGitHubResponseWeb(BaseModel):
    target_role: str
    projects: list[CandidateGitHubProjectItem] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    role_related_skills: list[str] = Field(default_factory=list)
    source: str = "GitHub"
    source_type: str = "github_api"


# -------------------------------------------------------------
# Backwards-Compatible Legacy Schemas
# -------------------------------------------------------------
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
