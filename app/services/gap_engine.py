from __future__ import annotations

from collections.abc import Iterable

from app.services.matching_engine import MATCHED, MISSING, WEAK


def _value(item: object, key: str) -> object:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key)


def generate_skill_gap_summary(requirement_matches: Iterable[object]) -> dict[str, list[dict[str, object]]]:
    strengths: list[dict[str, object]] = []
    weak_areas: list[dict[str, object]] = []
    missing_requirements: list[dict[str, object]] = []
    priority_gaps: list[dict[str, object]] = []

    for match in requirement_matches:
        status = str(_value(match, "match_status")).upper()
        importance = str(_value(match, "importance") or "REQUIRED").upper()
        requirement = _value(match, "requirement")
        category = _value(match, "category")
        evidence = _value(match, "evidence_text")

        if status == MATCHED:
            strengths.append(
                {"requirement": requirement, "category": category, "evidence": evidence}
            )
            continue

        if status == WEAK:
            weak_areas.append(
                {
                    "requirement": requirement,
                    "category": category,
                    "reason": "Limited supporting evidence found.",
                    "evidence": evidence,
                }
            )
            priority = "MEDIUM" if importance == "REQUIRED" else "LOW"
        else:
            missing_requirements.append(
                {
                    "requirement": requirement,
                    "category": category,
                    "importance": importance,
                    "reason": "Not demonstrated in the submitted resume.",
                }
            )
            priority = "HIGH" if importance == "REQUIRED" else "LOW"

        priority_gaps.append(
            {
                "requirement": requirement,
                "category": category,
                "importance": importance,
                "match_status": status,
                "priority": priority,
            }
        )

    return {
        "strengths": strengths,
        "weak_areas": weak_areas,
        "missing_requirements": missing_requirements,
        "priority_gaps": priority_gaps,
    }