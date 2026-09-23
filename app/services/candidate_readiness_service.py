from __future__ import annotations

from typing import Any


def build_readiness_profile(
    analysis: dict[str, Any],
    verification: list[dict[str, Any]],
    assessment: dict[str, Any],
    quality_findings: list[dict[str, Any]],
) -> dict[str, Any]:
    counts = analysis.get("counts", {})
    required_total = max(int(counts.get("total", 0)), 1)
    matched = int(counts.get("matched", 0))
    weak = int(counts.get("weak", 0))
    role_status = "STRONG" if matched / required_total >= 0.75 else "MODERATE" if matched else "LIMITED"
    evidence_status = "STRONG" if weak == 0 and matched else "MODERATE" if matched else "LIMITED"
    answered = sum(item.get("status") == "ANSWERED" for item in verification)
    verification_status = "FULLY_VERIFIED" if verification and answered == len(verification) else "PARTIALLY_VERIFIED" if answered else "NOT_VERIFIED"
    assessment_status = "COMPLETED" if assessment.get("status") == "EVALUATED" else "IN_PROGRESS" if assessment.get("status") in {"IN_PROGRESS", "SUBMITTED"} else "NOT_STARTED"
    quality_status = "STRONG" if not quality_findings else "NEEDS_ATTENTION"
    return {
        "role_alignment": {"status": role_status, "reason": f"{matched} of {counts.get('total', 0)} analyzed requirements are matched."},
        "skill_coverage": {"status": role_status, "reason": "Coverage is based on the existing deterministic requirement statuses."},
        "evidence_strength": {"status": evidence_status, "reason": f"{weak} requirement(s) have weak supporting resume evidence."},
        "verification": {"status": verification_status, "reason": f"{answered} of {len(verification)} verification item(s) are answered."},
        "assessment": {"status": assessment_status, "reason": "Assessment state is reported without changing its score."},
        "resume_quality": {"status": quality_status, "reason": f"{len(quality_findings)} objective resume quality finding(s) were detected."},
    }