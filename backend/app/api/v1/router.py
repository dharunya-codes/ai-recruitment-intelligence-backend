from fastapi import APIRouter

from .images import router as images_router
from .inspections import router as inspections_router
from .declarations import router as declarations_router
from .rules import router as rules_router
from .violations import router as violations_router
from .products import router as products_router
from .dashboard import router as dashboard_router
from .analytics import router as analytics_router

api_v1_router = APIRouter()

api_v1_router.include_router(images_router)
api_v1_router.include_router(inspections_router)
api_v1_router.include_router(declarations_router)
api_v1_router.include_router(rules_router)
api_v1_router.include_router(violations_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(analytics_router)

@api_v1_router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "online",
        "service": "LM-Inspect AI API",
        "version": "1.0.0",
        "pipeline": {
            "ocr": "ready",
            "ai_models": "ready",
            "rule_engine": "ready",
        },
    }
