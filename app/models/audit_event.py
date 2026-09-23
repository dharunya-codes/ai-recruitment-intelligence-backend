from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(String(60), index=True)
    user_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    role: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resource_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    resource_id: Mapped[int | None] = mapped_column(nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)