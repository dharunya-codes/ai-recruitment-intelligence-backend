from typing import List
from pydantic import BaseModel
from .common import SeverityLevel
from .inspection import Inspection

class ComplianceOverTimeItem(BaseModel):
    month: str
    compliant: int
    nonCompliant: int
    total: int

class ViolationCategoryItem(BaseModel):
    category: str
    count: int
    percentage: float
    color: str

class DashboardStats(BaseModel):
    totalInspections: int
    compliantCount: int
    nonCompliantCount: int
    pendingReviewCount: int
    complianceRate: float
    recentInspections: List[Inspection]
    complianceOverTime: List[ComplianceOverTimeItem]
    violationCategories: List[ViolationCategoryItem]

class InspectionTrendItem(BaseModel):
    date: str
    compliant: int
    nonCompliant: int
    needsReview: int

class ViolationByCategoryItem(BaseModel):
    category: str
    count: int

class FrequentRuleItem(BaseModel):
    rule: str
    title: str
    count: int
    severity: SeverityLevel

class CategoryComplianceItem(BaseModel):
    category: str
    complianceRate: float
    totalInspected: int

class AnalyticsData(BaseModel):
    inspectionsTrend: List[InspectionTrendItem]
    violationsByCategory: List[ViolationByCategoryItem]
    mostFrequentRules: List[FrequentRuleItem]
    categoryCompliance: List[CategoryComplianceItem]
