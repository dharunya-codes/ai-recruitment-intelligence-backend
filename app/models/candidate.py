from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    resumes: Mapped[list["Resume"]] = relationship(back_populates="candidate")
    verification_questions: Mapped[list["VerificationQuestion"]] = relationship(back_populates="candidate")
    assessments: Mapped[list["Assessment"]] = relationship(back_populates="candidate")
    reports: Mapped[list["Report"]] = relationship(back_populates="candidate")
    user: Mapped["User | None"] = relationship()
