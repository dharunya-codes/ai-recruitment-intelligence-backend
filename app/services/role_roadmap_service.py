from __future__ import annotations

from typing import Any


def build_role_roadmap(role: str, requirements: list[dict[str, Any]]) -> dict[str, Any]:
    skills = [str(item.get("requirement")) for item in requirements if item.get("category") == "SKILL"]
    if not skills:
        return {"role": role, "stages": []}
    return {"role": role, "stages": [{"stage": "FOUNDATION", "skills": skills[:2]}, {"stage": "CORE_SKILLS", "skills": skills[2:]}, {"stage": "PRACTICAL_EVIDENCE", "skills": [item for item in skills if item in {"SIEM", "Docker", "Python", "SQL"}]}, {"stage": "VERIFICATION", "skills": skills}, {"stage": "ASSESSMENT", "skills": skills}, {"stage": "RESUME_REFINEMENT", "skills": skills}]}