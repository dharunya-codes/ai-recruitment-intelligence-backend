from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True, index=True)
    candidate_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    target_role: Mapped[str | None] = mapped_column(String(200), nullable=True)
    target_job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    score_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    analysis_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="resumes")
    job: Mapped["Job"] = relationship(back_populates="resumes")
    skill_evidence: Mapped[list["SkillEvidence"]] = relationship(back_populates="resume")
    verification_questions: Mapped[list["VerificationQuestion"]] = relationship(back_populates="resume")
    assessments: Mapped[list["Assessment"]] = relationship(back_populates="resume")
    reports: Mapped[list["Report"]] = relationship(back_populates="resume")
