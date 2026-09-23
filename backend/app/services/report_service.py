from datetime import datetime
from typing import Optional

from ..models.report import InspectionReport
from ..models.inspection import ComplianceResult
from ..models.common import ComplianceStatus
from ..data.seed_data import DEFAULT_OFFICER
from .store import store

class ReportService:
    """Service to generate statutory Form II Legal Metrology Inspection Reports."""

    def generate_report(self, inspection_id: str) -> Optional[InspectionReport]:
        compliance_result = store.get_compliance_result(inspection_id)
        if not compliance_result:
            return None

        clean_id = inspection_id.replace("INSP-", "")
        cert_num = f"LMPC/CERT/2026/{clean_id}"
        is_compliant = compliance_result.overallStatus == ComplianceStatus.COMPLIANT

        if is_compliant:
            findings = (
                "The inspected packaged commodity conforms with all mandatory statutory declarations "
                "under Rule 6 and satisfies numeral height standards under Rule 5 of the "
                "Legal Metrology (Packaged Commodities) Rules, 2011."
            )
            remedy = "No further legal action required. Certified as compliant for retail distribution."
        else:
            findings = (
                "The inspected packaged commodity exhibits non-compliance under Rule 6(11) "
                "(Omission of Unit Sale Price) and/or Rule 5 Table-I (Sub-standard numeral height "
                "for declared net weight)."
            )
            remedy = (
                "Issuance of Statutory Show-Cause Notice under Section 36(1) of Legal Metrology Act, 2009. "
                "The manufacturer/packer is required to submit explanation or apply for compounding within 15 days."
            )

        issued_date = datetime.now().strftime("%d %B %Y")
        
        return InspectionReport(
            certificateNumber=cert_num,
            inspectionId=inspection_id,
            issuedDate=issued_date,
            officer=DEFAULT_OFFICER,
            product=compliance_result.product,
            inspection=compliance_result.inspection,
            complianceResult=compliance_result,
            findingsSummary=findings,
            statutoryRemedy=remedy,
            showCauseNoticeRequired=not is_compliant,
            seizureRecommended=compliance_result.complianceScore < 50,
            legalNoticeRef=f"DO-CA/LMPC-ZONE4/SCN/2026/{clean_id}",
        )

report_service = ReportService()
