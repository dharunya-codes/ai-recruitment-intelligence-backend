from typing import Optional, Dict, Any
from pydantic import BaseModel
from .product import Product
from .inspection import Inspection, ComplianceResult

class Officer(BaseModel):
    id: str
    name: str
    designation: str
    badgeNumber: str
    department: str
    jurisdiction: str
    role: Optional[str] = "ENFORCEMENT_OFFICER"
    avatarUrl: Optional[str] = None

class InspectionReport(BaseModel):
    certificateNumber: str
    inspectionId: str
    issuedDate: str
    officer: Officer
    product: Product
    inspection: Inspection
    complianceResult: ComplianceResult
    findingsSummary: str
    statutoryRemedy: str
    showCauseNoticeRequired: bool
    seizureRecommended: bool
    legalNoticeRef: Optional[str] = None

class UploadImageResponse(BaseModel):
    fileId: str
    imageUrl: str
    filename: str
    format: Optional[str] = None
    resolution: Optional[Dict[str, Any]] = None
