from fastapi import APIRouter
from ...models.declaration import (
    ValidateDeclarationsRequest,
    ValidateDeclarationsResponse,
)
from ...services.rule_engine import rule_engine

router = APIRouter(prefix="/rules", tags=["Rules"])

@router.post("/validate", response_model=ValidateDeclarationsResponse)
async def validate_declarations(request: ValidateDeclarationsRequest):
    """
    Statutory Legal Metrology (Packaged Commodities) Rules 2011 Engine.
    Evaluates mandatory statutory declarations, numeral heights, and MRP syntax.
    """
    return rule_engine.validate(
        declarations=request.declarations,
        product_metadata=request.productMetadata,
    )
