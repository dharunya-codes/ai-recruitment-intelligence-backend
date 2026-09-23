from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent

logger = logging.getLogger(__name__)


def record_audit_event(
    db: Session,
    event_type: str,
    *,
    user_id: int | None = None,
    role: str | None = None,
    resource_type: str | None = None,
    resource_id: int | None = None,
    success: bool = True,
) -> None:
    try:
        db.add(AuditEvent(event_type=event_type, user_id=user_id, role=role, resource_type=resource_type, resource_id=resource_id, success=success))
        db.commit()
    except Exception:
        db.rollback()
        logger.warning("Audit event could not be persisted: %s", event_type)