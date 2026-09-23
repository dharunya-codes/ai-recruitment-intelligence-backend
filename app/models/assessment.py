from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    score: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_questions: Mapped[int | None] = mapped_column(nullable=True)
    answered: Mapped[int | None] = mapped_column(nullable=True)
    unanswered: Mapped[int | None] = mapped_column(nullable=True)
    category_scores: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    areas_for_improvement: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="assessments")
    job: Mapped["Job"] = relationship(back_populates="assessments")
    resume: Mapped["Resume"] = relationship(back_populates="assessments")
    assessment_questions: Mapped[list["AssessmentQuestion"]] = relationship(back_populates="assessment")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    skill: Mapped[str | None] = mapped_column(String(150), nullable=True)
    question_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expected_concepts: Mapped[str | None] = mapped_column(Text, nullable=True)

    assessment: Mapped["Assessment"] = relationship(back_populates="assessment_questions")
    candidate_answers: Mapped[list["CandidateAnswer"]] = relationship(back_populates="question")


class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("assessment_questions.id"), nullable=False)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluation_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    missing_points: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    typing_duration: Mapped[int | None] = mapped_column(nullable=True)
    paste_attempt_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    question: Mapped["AssessmentQuestion"] = relationship(back_populates="candidate_answers")
