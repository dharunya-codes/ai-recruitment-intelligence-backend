from __future__ import annotations

from typing import Any


def build_career_intelligence(
    *,
    target_role: str,
    analysis: dict[str, Any],
    priorities: list[dict[str, Any]],
    advanced_gaps: list[dict[str, Any]],
    verification_gaps: list[str],
    assessment_gaps: list[str],
    resume_quality_issues: list[dict[str, Any]],
) -> dict[str, Any]:
    matched = [item["requirement"] for item in analysis.get("matched_requirements", [])]
    priority_gaps = [item["skill"] for item in priorities if item["priority"] in {"CRITICAL", "HIGH"}]
    evidence_gaps = [item["skill"] for item in advanced_gaps if item["status"] in {"MISSING", "WEAK_EVIDENCE"}]
    alignment = "STRONG" if len(matched) >= max(1, int(analysis.get("counts", {}).get("total", 0) * 0.75)) else "MODERATE" if matched else "LIMITED"
    return {
        "target_role": target_role,
        "role_type": "ROLE_BASED_EXPECTATIONS" if analysis.get("requirements_source") in ("ROLE_BASED_EXPECTATIONS", "CUSTOM_ROLE") else "COMPANY_JD",
        "role_alignment": {"status": alignment, "reason": f"{len(matched)} requirement(s) are currently supported by the analysis."},
        "top_supported_skills": matched[:5],
        "priority_gaps": priority_gaps,
        "evidence_gaps": evidence_gaps,
        "verification_gaps": verification_gaps,
        "assessment_gaps": assessment_gaps,
        "resume_quality_issues": resume_quality_issues,
        "next_actions": [
            f"Strengthen evidence for {skill}." for skill in priority_gaps[:3]
        ],
        "advanced_gap_details": advanced_gaps,
    }