from __future__ import annotations

from typing import Any


def build_actions(
    priorities: list[dict[str, Any]],
    quality_findings: list[dict[str, Any]],
    verification_gaps: list[str],
    assessment_gaps: list[str],
) -> list[dict[str, Any]]:
    actions = []
    for item in priorities:
        if item["priority"] == "LOW":
            continue
        skill = item["skill"]
        actions.append({"action_id": f"skill-{skill.casefold().replace(' ', '-')}", "category": "SKILL", "priority": item["priority"], "skill": skill, "reason": item["reason"], "evidence": None, "recommended_action": f"Practice {skill} and document supported project evidence.", "status": "OPEN"})
    for finding in quality_findings:
        actions.append({"action_id": f"resume-{finding['category'].casefold()}", "category": "RESUME", "priority": finding["severity"], "skill": None, "reason": finding["finding"], "evidence": finding["evidence"], "recommended_action": finding["recommendation"], "status": "OPEN"})
    for skill in verification_gaps:
        actions.append({"action_id": f"verification-{skill.casefold().replace(' ', '-')}", "category": "VERIFICATION", "priority": "HIGH", "skill": skill, "reason": "Verification is incomplete for this analyzed skill.", "evidence": None, "recommended_action": f"Complete the verification question for {skill}.", "status": "OPEN"})
    for skill in assessment_gaps:
        actions.append({"action_id": f"assessment-{skill.casefold().replace(' ', '-')}", "category": "ASSESSMENT", "priority": "MEDIUM", "skill": skill, "reason": "Assessment feedback identifies concepts to practice.", "evidence": None, "recommended_action": f"Practice {skill} concepts identified in assessment feedback.", "status": "OPEN"})
    return actions