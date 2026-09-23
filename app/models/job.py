from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    department: Mapped[str | None] = mapped_column(String(150), nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    minimum_experience: Mapped[int | None] = mapped_column(nullable=True)
    education: Mapped[str | None] = mapped_column(String(255), nullable=True)
    certifications: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    company: Mapped["Company"] = relationship(back_populates="jobs")
    requirements: Mapped[list["JobRequirement"]] = relationship(back_populates="job")
    resumes: Mapped[list["Resume"]] = relationship(back_populates="job")
    assessments: Mapped[list["Assessment"]] = relationship(back_populates="job")
    reports: Mapped[list["Report"]] = relationship(back_populates="job")
