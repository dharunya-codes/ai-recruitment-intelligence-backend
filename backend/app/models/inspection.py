from typing import Optional, List
from pydantic import BaseModel
from .common import BoundingBox, ComplianceStatus, ScanType
from .product import Product
from .declaration import DeclarationField, ComplianceSummary
from .violation import Violation

class Inspection(BaseModel):
    id: str
    inspectionNumber: str
    productId: str
    productName: str
    brand: str
    category: str
    manufacturer: str
    sku: str
    inspectionLocation: str
    inspectionDate: str
    inspectorId: str
    inspectorName: str
    scanType: ScanType
    status: ComplianceStatus
    complianceScore: float
    violationsCount: int
    detectedDeclarationsCount: int
    totalDeclarationsRequired: int
    imageUrl: str
    notes: Optional[str] = None

class AnalyzeProductRequest(BaseModel):
    productId: Optional[str] = None
    productName: str
    brand: str
    category: str
    manufacturer: str
    sku: str
    location: str
    scanType: ScanType = ScanType.FRONT_LABEL
    imageUrl: str
    fileId: Optional[str] = None

class AnalyzeProductResponse(BaseModel):
    inspectionId: str
    status: ComplianceStatus
    complianceScore: Optional[float] = None

class AnalysisMetadata(BaseModel):
    engineVersion: str
    modelConfidenceAvg: float
    processingTimeSeconds: float
    imageResolution: str
    ocrEngine: str
    rulesEngineVersion: str
    timestamp: str

class ComplianceResult(BaseModel):
    id: str
    inspectionId: str
    product: Product
    inspection: Inspection
    overallStatus: ComplianceStatus
    complianceScore: float
    summary: ComplianceSummary
    declarations: List[DeclarationField]
    violations: List[Violation]
    boundingBoxes: List[BoundingBox]
    analysisMetadata: AnalysisMetadata
