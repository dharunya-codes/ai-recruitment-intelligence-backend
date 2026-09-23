from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ComplianceStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON-COMPLIANT"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    PENDING = "PENDING"

class DeclarationStatus(str, Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    VIOLATION = "violation"
    MISSING = "missing"

class SeverityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ViolationStatus(str, Enum):
    OPEN = "OPEN"
    NOTICE_ISSUED = "NOTICE_ISSUED"
    RESOLVED = "RESOLVED"
    UNDER_REVIEW = "UNDER_REVIEW"

class ScanType(str, Enum):
    FRONT_LABEL = "Front Label"
    BACK_LABEL = "Back Label"
    SIDE_LABEL = "Side Label"
    PRODUCT_LISTING = "Product Listing"
    FULL_PRODUCT = "Full Product"

class BoundingBox(BaseModel):
    id: str
    x: float = Field(..., description="Percentage 0 - 100")
    y: float = Field(..., description="Percentage 0 - 100")
    width: float = Field(..., description="Percentage 0 - 100")
    height: float = Field(..., description="Percentage 0 - 100")
    label: str
    status: DeclarationStatus
    confidence: float

class RuleReference(BaseModel):
    ruleNumber: str
    actName: str
    clauseTitle: str
    description: str
    penalSection: str
    maximumFine: str
    gazetteNotification: Optional[str] = None
