from typing import List, Optional
from fastapi import APIRouter, Query
from ...models.violation import Violation
from ...services.store import store

router = APIRouter(prefix="/violations", tags=["Violations"])

@router.get("", response_model=List[Violation])
async def get_violations(
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    inspectionId: Optional[str] = Query(None),
):
    """
    Retrieve statutory infractions registry, filterable by:
    - severity: HIGH, MEDIUM, LOW, ALL
    - status: OPEN, NOTICE_ISSUED, RESOLVED, UNDER_REVIEW, ALL
    - inspectionId: specific inspection reference
    """
    return store.get_violations(
        severity=severity,
        status=status,
        inspection_id=inspectionId,
    )
