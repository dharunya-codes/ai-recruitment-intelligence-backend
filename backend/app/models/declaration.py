from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .common import BoundingBox, ComplianceStatus, DeclarationStatus, ScanType
from .violation import Violation

class ComplianceSummary(BaseModel):
    totalRequired: int
    detectedCount: int
    compliantCount: int
    warningCount: int
    violationCount: int
    missingCount: int

class DeclarationField(BaseModel):
    id: str
    key: str
    label: str
    ruleRef: str
    extractedValue: Optional[str] = None
    expectedFormat: str
    status: DeclarationStatus
    confidence: float
    boundingBox: Optional[BoundingBox] = None
    notes: Optional[str] = None
    numeralHeightMm: Optional[float] = None
    requiredHeightMm: Optional[float] = None

class ExtractDeclarationsRequest(BaseModel):
    fileId: Optional[str] = None
    imageUrl: str
    scanType: ScanType = ScanType.FRONT_LABEL
    ocrEngine: Optional[str] = None

class ExtractDeclarationsResponse(BaseModel):
    fileId: str
    rawOcrTokensCount: int
    extractedDeclarations: List[DeclarationField]
    boundingBoxes: List[BoundingBox]
    processingTimeMs: int
    confidenceScoreAvg: float

class ValidateDeclarationsRequest(BaseModel):
    declarations: List[DeclarationField]
    productMetadata: Optional[Dict[str, Any]] = None
    ruleSetVersion: Optional[str] = None

class ValidateDeclarationsResponse(BaseModel):
    overallStatus: ComplianceStatus
    complianceScore: float
    violations: List[Violation]
    declarations: List[DeclarationField]
    summary: ComplianceSummary
