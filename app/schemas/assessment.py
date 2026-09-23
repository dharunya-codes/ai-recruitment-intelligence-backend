from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AssessmentQuestionResponse(BaseModel):
    id: int
    question: str
    skill: str | None
    question_type: str | None
    difficulty: str | None


class AssessmentResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int | None
    resume_id: int
    score: float | None
    status: str
    created_at: datetime
    question_count: int
    questions: list[AssessmentQuestionResponse]


class AssessmentAnswerRequest(BaseModel):
    answer: str | None = Field(default=None, max_length=10000)
    started_at: datetime | None = None
    submitted_at: datetime | None = None
    typing_duration: int | None = Field(default=None, ge=0)
    paste_attempt_detected: bool | None = None


class AssessmentAnswerResponse(BaseModel):
    id: int
    question_id: int
    assessment_id: int
    status: str
    score: float | None
    feedback: str | None


class AssessmentStatusResponse(BaseModel):
    assessment_id: int
    status: str
    total_questions: int
    answered: int
    unanswered: int


class AssessmentQuestionResult(BaseModel):
    question_id: int
    question: str
    skill: str | None
    question_type: str | None
    score: float
    max_score: int
    evaluation_status: str
    feedback: str
    strengths: list[str]
    missing_points: list[str]


class CategoryScore(BaseModel):
    score: float
    answered: int
    total: int


class AssessmentResultResponse(BaseModel):
    assessment_id: int
    status: str
    score: float
    total_questions: int
    answered: int
    unanswered: int
    category_scores: dict[str, CategoryScore]
    question_results: list[AssessmentQuestionResult]
    strengths: list[str]
    areas_for_improvement: list[str]