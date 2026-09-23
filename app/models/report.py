from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    report_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="reports")
    job: Mapped["Job"] = relationship(back_populates="reports")
    resume: Mapped["Resume"] = relationship(back_populates="reports")
