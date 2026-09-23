from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class AnalysisSnapshot(Base):
    __tablename__ = "analysis_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    target_role: Mapped[str] = mapped_column(String(200), nullable=False)
    overall_score: Mapped[float | None] = mapped_column(nullable=True)
    analysis_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)