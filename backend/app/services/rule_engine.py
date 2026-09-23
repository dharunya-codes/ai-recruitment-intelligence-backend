import re
import uuid
from typing import List, Dict, Any, Tuple, Optional

from ..models.declaration import (
    DeclarationField,
    ComplianceSummary,
    ValidateDeclarationsResponse,
)
from ..models.violation import Violation
from ..models.common import (
    ComplianceStatus,
    DeclarationStatus,
    SeverityLevel,
    ViolationStatus,
)
from ..data.lmpc_rules import LMPC_RULES

class LegalMetrologyRuleEngine:
    """
    Statutory Compliance Validation Engine enforcing:
    - Legal Metrology (Packaged Commodities) Rules, 2011 (LMPC Rules)
    - Legal Metrology Act, 2009 (Sections 18, 36, 39)
    """

    MANDATORY_DECLARATIONS = [
        "generic_name",
        "net_quantity",
        "mrp",
        "unit_sale_price",
        "mfg_date",
        "manufacturer_details",
        "country_of_origin",
        "consumer_care",
        "batch_number",
    ]

    def validate(
        self,
        declarations: List[DeclarationField],
        product_metadata: Optional[Dict[str, Any]] = None,
        inspection_id: Optional[str] = None,
    ) -> ValidateDeclarationsResponse:
        current_insp_id = inspection_id or "INSP-CURRENT"
        violations: List[Violation] = []
        updated_declarations: List[DeclarationField] = []

        dec_map: Dict[str, DeclarationField] = {d.key: d for d in declarations}

        # Validate each present declaration
        for decl in declarations:
            d = decl.model_copy()
            rule_violations = self._validate_individual_declaration(d, product_metadata, current_insp_id)
            if rule_violations:
                violations.extend(rule_violations)
            updated_declarations.append(d)

        # Check for missing mandatory declarations
        for key in self.MANDATORY_DECLARATIONS:
            if key not in dec_map or not dec_map[key].extractedValue:
                # If key is missing or extractedValue is None
                already_in_list = any(d.key == key for d in updated_declarations)
                if not already_in_list:
                    missing_field = self._create_missing_declaration(key)
                    updated_declarations.append(missing_field)
                
                # Check if violation already generated
                if not any(v.declarationKey == key for v in violations):
                    v = self._create_missing_violation(key, current_insp_id)
                    if v:
                        violations.append(v)

        # Compute summary
        total_req = len(self.MANDATORY_DECLARATIONS)
        compliant_count = sum(1 for d in updated_declarations if d.status == DeclarationStatus.COMPLIANT)
        warning_count = sum(1 for d in updated_declarations if d.status == DeclarationStatus.WARNING)
        violation_count = sum(1 for d in updated_declarations if d.status == DeclarationStatus.VIOLATION)
        missing_count = sum(1 for d in updated_declarations if d.status == DeclarationStatus.MISSING or not d.extractedValue)
        detected_count = len(updated_declarations) - missing_count

        summary = ComplianceSummary(
            totalRequired=total_req,
            detectedCount=detected_count,
            compliantCount=compliant_count,
            warningCount=warning_count,
            violationCount=violation_count,
            missingCount=missing_count,
        )

        # Compute compliance score (0-100)
        # Deduct 25 for HIGH severity, 15 for MEDIUM, 8 for LOW
        deductions = 0
        for v in violations:
            if v.severity == SeverityLevel.HIGH:
                deductions += 25
            elif v.severity == SeverityLevel.MEDIUM:
                deductions += 15
            elif v.severity == SeverityLevel.LOW:
                deductions += 8

        score = max(0.0, min(100.0, float(100 - deductions)))

        # Determine overall status
        if score >= 90 and violation_count == 0 and missing_count == 0:
            overall_status = ComplianceStatus.COMPLIANT
        elif score < 60 or any(v.severity == SeverityLevel.HIGH for v in violations):
            overall_status = ComplianceStatus.NON_COMPLIANT
        else:
            overall_status = ComplianceStatus.NEEDS_REVIEW

        return ValidateDeclarationsResponse(
            overallStatus=overall_status,
            complianceScore=score,
            violations=violations,
            declarations=updated_declarations,
            summary=summary,
        )

    def _validate_individual_declaration(
        self,
        d: DeclarationField,
        product_metadata: Optional[Dict[str, Any]],
        inspection_id: str,
    ) -> List[Violation]:
        violations: List[Violation] = []

        # Rule 6(11): Unit Sale Price
        if d.key == "unit_sale_price":
            if not d.extractedValue:
                d.status = DeclarationStatus.VIOLATION
                d.notes = "Statutory declaration completely missing on package label."
                violations.append(
                    Violation(
                        id=f"VIOL-{uuid.uuid4().hex[:8].upper()}",
                        inspectionId=inspection_id,
                        title="Omission of Mandatory Unit Sale Price (USP)",
                        severity=SeverityLevel.HIGH,
                        declarationKey="unit_sale_price",
                        detectedValue="NOT DETECTED (Missing on label)",
                        expectedValue="₹ ... per g / kg / ml adjacent to MRP",
                        explanation="Under Rule 6(11) of the Legal Metrology (Packaged Commodities) Rules, 2011, pre-packaged commodities exceeding 100g/100ml must declare the Unit Sale Price rounded to two decimal places.",
                        applicableRule=LMPC_RULES["RULE_6_11"],
                        recommendedAction="Issue Statutory Notice under Section 36(1). Compounding penalty of ₹25,000 applicable.",
                        status=ViolationStatus.OPEN,
                        identifiedDate="2026-03-08",
                    )
                )

        # Rule 6(1)(c) & Rule 5: Net Quantity & Numeral Height
        elif d.key == "net_quantity":
            if d.numeralHeightMm and d.requiredHeightMm:
                if d.numeralHeightMm < d.requiredHeightMm:
                    d.status = DeclarationStatus.WARNING
                    d.notes = f"Numeral font height measured at {d.numeralHeightMm}mm, violating Rule 5 Table-I minimum of {d.requiredHeightMm}mm."
                    violations.append(
                        Violation(
                            id=f"VIOL-{uuid.uuid4().hex[:8].upper()}",
                            inspectionId=inspection_id,
                            title="Non-Standard Net Quantity Numeral Font Height",
                            severity=SeverityLevel.MEDIUM,
                            declarationKey="net_quantity",
                            detectedValue=f"Measured Numeral Height: {d.numeralHeightMm} mm",
                            expectedValue=f"Minimum {d.requiredHeightMm} mm as per Table-I",
                            explanation="As mandated by Table-I under Rule 5 of LMPC Rules 2011, numerals in net quantity declaration must satisfy statutory millimeter height thresholds.",
                            applicableRule=LMPC_RULES["RULE_6_1_C"],
                            recommendedAction="Order immediate recall/rectification of non-compliant packaging batch.",
                            status=ViolationStatus.OPEN,
                            identifiedDate="2026-03-08",
                            boundingBox=d.boundingBox,
                        )
                    )

        # Rule 6(1)(e): Consumer Care
        elif d.key == "consumer_care":
            val = d.extractedValue or ""
            has_email = "@" in val
            has_phone = bool(re.search(r"\d{4,}", val))
            if has_phone and not has_email:
                d.status = DeclarationStatus.WARNING
                d.notes = "Consumer care telephone provided, but grievance email address is omitted."
                violations.append(
                    Violation(
                        id=f"VIOL-{uuid.uuid4().hex[:8].upper()}",
                        inspectionId=inspection_id,
                        title="Incomplete Consumer Grievance Redressal Declaration",
                        severity=SeverityLevel.LOW,
                        declarationKey="consumer_care",
                        detectedValue=f"Provided: {val} (Email omitted)",
                        expectedValue="Both telephone number and email address are required under Rule 6(1)(e)",
                        explanation="Rule 6(1)(e) requires every package to bear the name, address, telephone number, and e-mail address of the consumer redressal cell.",
                        applicableRule=LMPC_RULES["RULE_6_1_E"],
                        recommendedAction="Issue 14-day compliance correction directive under Rule 32.",
                        status=ViolationStatus.UNDER_REVIEW,
                        identifiedDate="2026-03-08",
                    )
                )

        return violations

    def _create_missing_declaration(self, key: str) -> DeclarationField:
        rule_map = {
            "unit_sale_price": ("Rule 6(11)", "Unit Sale Price (USP)", "₹ xx.xx per g / ml"),
            "country_of_origin": ("Rule 6(10)", "Country of Origin", "Conspicuous country name"),
            "consumer_care": ("Rule 6(1)(e)", "Consumer Care Helpline & Redressal", "Telephone, email, and postal address"),
            "mfg_date": ("Rule 6(1)(d)", "Month & Year of Manufacture", "MM/YYYY format"),
            "mrp": ("Rule 6(1)(da)", "Maximum Retail Price (MRP)", "MRP ₹ xx.xx incl. of all taxes"),
            "net_quantity": ("Rule 6(1)(c) & Rule 5", "Net Quantity & Numeral Height", "Metric unit with compliant numeral height"),
            "generic_name": ("Rule 6(1)(b)", "Generic / Common Name", "Generic name on PDP"),
            "manufacturer_details": ("Rule 6(1)(a)", "Manufacturer / Packer Address", "Complete address with PIN"),
            "batch_number": ("Rule 6(1)(g)", "Batch / Lot Number", "Distinct lot identification"),
        }
        rule_ref, label, fmt = rule_map.get(key, ("Rule 6", key.replace("_", " ").title(), "Standard format"))
        return DeclarationField(
            id=f"dec-missing-{key}",
            key=key,
            label=label,
            ruleRef=rule_ref,
            extractedValue=None,
            expectedFormat=fmt,
            status=DeclarationStatus.MISSING,
            confidence=0.0,
            notes="Mandatory declaration was not detected on the packaging.",
        )

    def _create_missing_violation(self, key: str, inspection_id: str) -> Optional[Violation]:
        if key == "unit_sale_price":
            return Violation(
                id=f"VIOL-{uuid.uuid4().hex[:8].upper()}",
                inspectionId=inspection_id,
                title="Omission of Mandatory Unit Sale Price (USP)",
                severity=SeverityLevel.HIGH,
                declarationKey="unit_sale_price",
                detectedValue="NOT DETECTED (Missing on label)",
                expectedValue="₹ ... per g / kg / ml adjacent to MRP",
                explanation="Under Rule 6(11) of the Legal Metrology (Packaged Commodities) Rules, 2011, pre-packaged commodities exceeding 100g must declare the Unit Sale Price rounded to two decimal places.",
                applicableRule=LMPC_RULES["RULE_6_11"],
                recommendedAction="Issue Statutory Notice under Section 36(1). Compounding penalty of ₹25,000 applicable.",
                status=ViolationStatus.OPEN,
                identifiedDate="2026-03-08",
            )
        elif key == "country_of_origin":
            return Violation(
                id=f"VIOL-{uuid.uuid4().hex[:8].upper()}",
                inspectionId=inspection_id,
                title="Missing Country of Origin on Package",
                severity=SeverityLevel.HIGH,
                declarationKey="country_of_origin",
                detectedValue="NOT DECLARED on primary display panel",
                expectedValue="Country of Origin prominently displayed on PDP",
                explanation="Rule 6(10) strictly provides that every package shall declare the country of origin.",
                applicableRule=LMPC_RULES["RULE_6_10"],
                recommendedAction="Issue notice under Section 36(1) of Legal Metrology Act, 2009.",
                status=ViolationStatus.OPEN,
                identifiedDate="2026-03-08",
            )
        return None

rule_engine = LegalMetrologyRuleEngine()
