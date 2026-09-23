from __future__ import annotations

from typing import Any


def build_evidence_recommendations(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence_map = {
        "MISSING": [("PROJECT", "Document a project where this skill was actually used."), ("COURSEWORK", "Add relevant coursework only if it was completed and can be supported.")],
        "WEAK_EVIDENCE": [("PROJECT", "Add concrete project contribution and outcome details for this skill."), ("ASSESSMENT", "Use assessment performance as an additional, separate signal.")],
        "CANDIDATE_VERIFIED": [("VERIFICATION", "Keep the candidate-reported verification evidence separate from resume evidence.")],
    }
    return [{"skill": item["skill"], "current_status": item["status"], "recommended_evidence": [{"type": kind, "description": description} for kind, description in evidence_map.get(item["status"], [])]} for item in gaps if item["status"] != "STRONG_EVIDENCE"]