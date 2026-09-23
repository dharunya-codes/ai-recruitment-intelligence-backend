import threading
from typing import Dict, List, Optional
from copy import deepcopy

from ..models.product import Product
from ..models.inspection import Inspection, ComplianceResult
from ..models.violation import Violation
from ..models.dashboard import DashboardStats, AnalyticsData
from ..data.seed_data import (
    SEED_PRODUCTS,
    SEED_INSPECTIONS,
    SEED_VIOLATIONS,
    SEED_COMPLIANCE_RESULTS,
    SEED_DASHBOARD_STATS,
    SEED_ANALYTICS,
)

class DataStore:
    """Thread-safe in-memory store for LM-Inspect AI entities."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.products: Dict[str, Product] = {p.id: deepcopy(p) for p in SEED_PRODUCTS}
        self.inspections: List[Inspection] = [deepcopy(i) for i in SEED_INSPECTIONS]
        self.violations: List[Violation] = [deepcopy(v) for v in SEED_VIOLATIONS]
        self.compliance_results: Dict[str, ComplianceResult] = {
            k: deepcopy(v) for k, v in SEED_COMPLIANCE_RESULTS.items()
        }
        self.dashboard_stats: DashboardStats = deepcopy(SEED_DASHBOARD_STATS)
        self.analytics_data: AnalyticsData = deepcopy(SEED_ANALYTICS)

    def get_inspections(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Inspection]:
        with self._lock:
            items = list(self.inspections)
            
            if status and status != "All":
                normalized = status.upper().replace("-", "_").replace(" ", "_")
                items = [
                    i for i in items
                    if i.status.value.replace("-", "_") == normalized
                ]
                
            if category and category != "All Categories":
                items = [i for i in items if i.category == category]
                
            if search and search.strip():
                q = search.lower().strip()
                items = [
                    i for i in items
                    if (
                        q in i.productName.lower()
                        or q in i.brand.lower()
                        or q in i.sku.lower()
                        or q in i.inspectionNumber.lower()
                        or q in i.manufacturer.lower()
                    )
                ]
                
            return items

    def get_inspection_by_id(self, inspection_id: str) -> Optional[Inspection]:
        with self._lock:
            for insp in self.inspections:
                if insp.id == inspection_id:
                    return deepcopy(insp)
            return None

    def add_inspection(self, inspection: Inspection) -> None:
        with self._lock:
            self.inspections.insert(0, deepcopy(inspection))
            self.dashboard_stats.totalInspections += 1
            if inspection.status.value == "COMPLIANT":
                self.dashboard_stats.compliantCount += 1
            elif inspection.status.value == "NON-COMPLIANT":
                self.dashboard_stats.nonCompliantCount += 1
            else:
                self.dashboard_stats.pendingReviewCount += 1
                
            total = self.dashboard_stats.totalInspections
            compliant = self.dashboard_stats.compliantCount
            self.dashboard_stats.complianceRate = round((compliant / total) * 100, 1) if total > 0 else 0
            self.dashboard_stats.recentInspections = self.inspections[:5]

    def get_compliance_result(self, inspection_id: str) -> Optional[ComplianceResult]:
        with self._lock:
            if inspection_id in self.compliance_results:
                return deepcopy(self.compliance_results[inspection_id])
            # Fallback to default mock result if exists
            if "INSP-2026-0842" in self.compliance_results:
                return deepcopy(self.compliance_results["INSP-2026-0842"])
            return None

    def save_compliance_result(self, result: ComplianceResult) -> None:
        with self._lock:
            self.compliance_results[result.inspectionId] = deepcopy(result)
            for v in result.violations:
                if not any(item.id == v.id for item in self.violations):
                    self.violations.insert(0, deepcopy(v))

    def get_violations(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        inspection_id: Optional[str] = None,
    ) -> List[Violation]:
        with self._lock:
            items = list(self.violations)
            if severity and severity != "ALL":
                items = [v for v in items if v.severity.value == severity]
            if status and status != "ALL":
                items = [v for v in items if v.status.value == status]
            if inspection_id:
                items = [v for v in items if v.inspectionId == inspection_id]
            return items

    def get_product(self, product_id: str) -> Optional[Product]:
        with self._lock:
            if product_id in self.products:
                return deepcopy(self.products[product_id])
            for p in self.products.values():
                if p.name.lower() == product_id.lower() or p.sku.lower() == product_id.lower():
                    return deepcopy(p)
            return None

    def add_product(self, product: Product) -> None:
        with self._lock:
            self.products[product.id] = deepcopy(product)

    def get_dashboard_stats(self) -> DashboardStats:
        with self._lock:
            stats = deepcopy(self.dashboard_stats)
            stats.recentInspections = self.inspections[:5]
            return stats

    def get_analytics_data(self) -> AnalyticsData:
        with self._lock:
            return deepcopy(self.analytics_data)

store = DataStore()
