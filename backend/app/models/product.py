from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .inspection import Inspection
    from .violation import Violation

class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    manufacturer: str
    packerOrImporter: Optional[str] = None
    sku: str
    barcode: Optional[str] = None
    packageType: str = "Packaged Commodity"
    declaredNetQuantity: Optional[str] = None
    declaredMRP: Optional[str] = None
    inspectionLocation: Optional[str] = None
    imageUrl: str
    createdAt: str

from .violation import Violation

class ProductDetailsResponse(BaseModel):
    product: Product
    inspections: List[dict] # Use dict or Inspection to avoid cyclic import
    violations: List[Violation]
