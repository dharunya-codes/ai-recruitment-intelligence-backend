from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VerificationQuestionResponse(BaseModel):
    id: int
    resume_id: int
    skill: str
    question: str
    priority: str
    question_type: str
    status: str
    evidence_status: str


class VerificationAnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1, max_length=10000)
    started_at: datetime | None = None
    submitted_at: datetime | None = None
    typing_duration: int | None = Field(default=None, ge=0)
    paste_attempt_detected: bool | None = None


class VerificationAnswerResponse(BaseModel):
    id: int
    skill: str
    status: str
    evidence_status: str
    candidate_reported_evidence: str | None
    resume_evidence_unchanged: bool = True
    resume_project_evidence: bool = False
    resume_internship_evidence: bool = False


class VerificationStatusItem(BaseModel):
    skill: str
    question: str
    status: str
    evidence_status: str
    candidate_reported_evidence: str | None


class VerificationStatusResponse(BaseModel):
    resume_id: int
    total_questions: int
    answered: int
    pending: int
    verification_items: list[VerificationStatusItem]