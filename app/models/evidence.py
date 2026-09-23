from __future__ import annotations

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class SkillEvidence(Base):
    __tablename__ = "skill_evidence"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    skill: Mapped[str] = mapped_column(String(150), nullable=False)
    resume_mention: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    project_evidence: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    internship_evidence: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    certification_evidence: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    evidence_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_strength: Mapped[str | None] = mapped_column(
        Enum(
            "STRONG",
            "MODERATE",
            "WEAK",
            "CANDIDATE_VERIFIED",
            "MISSING",
            name="evidence_strength",
            create_type=True,
        ),
        nullable=True,
    )
    verification_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    candidate_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    candidate_reported_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)

    resume: Mapped["Resume"] = relationship(back_populates="skill_evidence")
