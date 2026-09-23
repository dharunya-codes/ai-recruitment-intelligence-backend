from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from app.services.matching_engine import MATCHED, MISSING, WEAK

STATUS_VALUES = {
    MATCHED: 1.0,
    WEAK: 0.5,
    MISSING: 0.0,
}
IMPORTANCE_WEIGHTS = {
    "REQUIRED": 1.0,
    "PREFERRED": 0.5,
}


def _value(item: object, key: str) -> object:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key)


def _score(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values) * 100, 2)


def calculate_candidate_score(requirement_matches: Iterable[object]) -> dict[str, object]:
    """Score demonstrated JD requirements, never candidate quality or hiring fitness."""
    requirement_analysis: list[dict[str, object]] = []
    required_values: list[float] = []
    preferred_values: list[float] = []
    category_values: dict[str, list[float]] = defaultdict(list)
    counts = {"matched": 0, "weak": 0, "missing": 0, "total": 0}

    for match in requirement_matches:
        status = str(_value(match, "match_status")).upper()
        importance = str(_value(match, "importance") or "REQUIRED").upper()
        status_value = STATUS_VALUES.get(status, 0.0)
        importance_weight = IMPORTANCE_WEIGHTS.get(importance, IMPORTANCE_WEIGHTS["REQUIRED"])
        weighted_value = status_value * importance_weight
        category = str(_value(match, "category"))

        requirement_analysis.append(
            {
                "requirement_id": _value(match, "requirement_id"),
                "requirement": _value(match, "requirement"),
                "category": category,
                "importance": importance,
                "match_status": status,
                "evidence_text": _value(match, "evidence_text"),
                "status_value": status_value,
                "importance_weight": importance_weight,
                "weighted_value": weighted_value,
            }
        )
        counts["total"] += 1
        counts[status.casefold()] = counts.get(status.casefold(), 0) + 1
        category_values[category].append(status_value)
        if importance == "PREFERRED":
            preferred_values.append(status_value)
        else:
            required_values.append(status_value)

    weighted_possible = sum(
        item["importance_weight"] for item in requirement_analysis
    )
    weighted_obtained = sum(item["weighted_value"] for item in requirement_analysis)
    overall_match_score = (
        round(weighted_obtained / weighted_possible * 100, 2)
        if weighted_possible
        else None
    )

    category_breakdown = {
        category: {
            "score": _score(values),
            "matched": sum(value == STATUS_VALUES[MATCHED] for value in values),
            "weak": sum(value == STATUS_VALUES[WEAK] for value in values),
            "missing": sum(value == STATUS_VALUES[MISSING] for value in values),
            "total": len(values),
        }
        for category, values in category_values.items()
    }

    return {
        "overall_match_score": overall_match_score,
        "required_score": _score(required_values),
        "preferred_score": _score(preferred_values),
        "score_status": "CALCULATED" if requirement_analysis else "NO_REQUIREMENTS",
        "counts": counts,
        "category_breakdown": category_breakdown,
        "requirement_analysis": requirement_analysis,
    }