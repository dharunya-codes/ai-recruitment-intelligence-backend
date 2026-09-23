from fastapi import APIRouter
from ...models.dashboard import DashboardStats
from ...services.store import store

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """
    Retrieve executive KPI metrics:
    - Total inspections count & compliance rate
    - Inspection distribution (compliant, non-compliant, pending)
    - Monthly compliance trends
    - Most prevalent violation categories
    - Recent inspections stream
    """
    return store.get_dashboard_stats()
