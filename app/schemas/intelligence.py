from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class IntelligenceResponse(BaseModel):
    resume_id: int
    data: dict[str, Any]


class MultiJobRequest(BaseModel):
    resume_id: int = Field(..., gt=0)
    job_ids: list[int] = Field(..., min_length=1, max_length=20)


class MultiJobResponse(BaseModel):
    resume_id: int
    analyses: list[dict[str, Any]]


class CareerQuestionRequest(BaseModel):
    question_type: Literal[
        "WHAT_SHOULD_I_IMPROVE",
        "WHAT_SKILL_IS_MISSING",
        "WHY_IS_MY_MATCH_SCORE_LOW",
        "WHAT_EVIDENCE_IS_MISSING",
        "WHAT_SHOULD_I_PRACTICE",
        "WHAT_PROJECT_SHOULD_I_BUILD",
        "WHAT_SHOULD_I_VERIFY",
    ]


class CareerQuestionResponse(BaseModel):
    resume_id: int
    data: dict[str, Any]