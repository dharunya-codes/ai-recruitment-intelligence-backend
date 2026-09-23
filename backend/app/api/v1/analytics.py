from fastapi import APIRouter
from ...models.dashboard import AnalyticsData
from ...services.store import store

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary", response_model=AnalyticsData)
async def get_analytics_summary():
    """
    Retrieve comprehensive analytics:
    - Weekly inspection compliance trend
    - Violations frequency by classification
    - Most frequently breached statutory rules
    - Category-wise compliance benchmarks
    """
    return store.get_analytics_data()
