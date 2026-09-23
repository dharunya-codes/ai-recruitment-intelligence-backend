from typing import Optional
from pydantic import BaseModel
from .common import BoundingBox, RuleReference, SeverityLevel, ViolationStatus

class Violation(BaseModel):
    id: str
    inspectionId: str
    title: str
    severity: SeverityLevel
    declarationKey: str
    detectedValue: str
    expectedValue: str
    explanation: str
    applicableRule: RuleReference
    evidenceImageUrl: Optional[str] = None
    boundingBox: Optional[BoundingBox] = None
    recommendedAction: str
    status: ViolationStatus = ViolationStatus.OPEN
    identifiedDate: str
