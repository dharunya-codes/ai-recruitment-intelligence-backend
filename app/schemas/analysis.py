from __future__ import annotations

from pydantic import BaseModel


class RequirementMatch(BaseModel):
    requirement_id: int
    requirement: str
    category: str
    importance: str | None
    match_status: str
    evidence_text: str | None
    verification_required: bool = False


class RequirementScoreBreakdown(RequirementMatch):
    status_value: float
    importance_weight: float
    weighted_value: float


class CategoryScore(BaseModel):
    score: float | None
    matched: int
    weak: int
    missing: int
    total: int


class Strength(BaseModel):
    requirement: str
    category: str
    evidence: str | None


class WeakArea(BaseModel):
    requirement: str
    category: str
    reason: str
    evidence: str | None


class MissingRequirement(BaseModel):
    requirement: str
    category: str
    importance: str
    reason: str


class PriorityGap(BaseModel):
    requirement: str
    category: str
    importance: str
    match_status: str
    priority: str


class SkillGapResponse(BaseModel):
    strengths: list[Strength]
    weak_areas: list[WeakArea]
    missing_requirements: list[MissingRequirement]
    priority_gaps: list[PriorityGap]


class AnalysisCounts(BaseModel):
    matched: int
    weak: int
    missing: int
    total: int


class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    job_id: int
    candidate_id: int
    candidate_name: str
    detected_skills: list[str]
    matched_requirements: list[RequirementMatch]
    weak_requirements: list[RequirementMatch]
    missing_requirements: list[RequirementMatch]
    overall_match_score: float | None
    required_score: float | None
    preferred_score: float | None
    score_status: str
    counts: AnalysisCounts
    category_breakdown: dict[str, CategoryScore]
    requirement_analysis: list[RequirementScoreBreakdown]
    skill_gap: SkillGapResponse