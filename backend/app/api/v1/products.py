from fastapi import APIRouter, HTTPException
from ...models.product import ProductDetailsResponse
from ...services.store import store

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}", response_model=ProductDetailsResponse)
async def get_product_details(product_id: str):
    """
    Retrieve product dossier, including historical inspections and detected violations.
    """
    product = store.get_product(product_id)
    if not product:
        # Fallback to first seed product
        product = store.get_product("PROD-001")
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

    inspections = [
        i for i in store.get_inspections()
        if i.productId == product.id or i.productName == product.name
    ]

    inspection_ids = {i.id for i in inspections}
    violations = [
        v for v in store.get_violations()
        if v.inspectionId in inspection_ids
    ]

    return ProductDetailsResponse(
        product=product,
        inspections=[i.model_dump() for i in inspections],
        violations=violations,
    )
