from __future__ import annotations

from app.services.gap_engine import generate_skill_gap_summary
from app.services.scoring_engine import calculate_candidate_score


def _match(
    requirement: str,
    importance: str,
    status: str,
    category: str = "SKILL",
    evidence: str | None = "evidence",
) -> dict[str, object]:
    return {
        "requirement_id": 1,
        "requirement": requirement,
        "category": category,
        "importance": importance,
        "match_status": status,
        "evidence_text": evidence,
    }


def test_basic_scoring() -> None:
    result = calculate_candidate_score(
        [
            _match("Python", "REQUIRED", "MATCHED"),
            _match("SQL", "REQUIRED", "MATCHED"),
            _match("Docker", "REQUIRED", "MISSING", evidence=None),
        ]
    )
    assert result["overall_match_score"] == 66.67
    assert result["required_score"] == 66.67


def test_weak_requirement_scoring() -> None:
    result = calculate_candidate_score(
        [_match("Python", "REQUIRED", "MATCHED"), _match("Java", "REQUIRED", "WEAK")]
    )
    assert result["overall_match_score"] == 75.0


def test_preferred_weighting() -> None:
    result = calculate_candidate_score(
        [_match("Python", "REQUIRED", "MATCHED"), _match("AWS", "PREFERRED", "MATCHED")]
    )
    assert result["overall_match_score"] == 100.0
    assert result["preferred_score"] == 100.0


def test_required_and_preferred_weighting() -> None:
    result = calculate_candidate_score(
        [
            _match("Python", "REQUIRED", "MATCHED"),
            _match("Docker", "REQUIRED", "MISSING", evidence=None),
            _match("AWS", "PREFERRED", "MATCHED"),
        ]
    )
    assert result["overall_match_score"] == 60.0


def test_no_requirements_returns_null_scores() -> None:
    result = calculate_candidate_score([])
    assert result["overall_match_score"] is None
    assert result["required_score"] is None
    assert result["preferred_score"] is None
    assert result["score_status"] == "NO_REQUIREMENTS"


def test_required_and_preferred_scores_are_separate() -> None:
    result = calculate_candidate_score(
        [
            _match("Python", "REQUIRED", "MATCHED"),
            _match("SQL", "REQUIRED", "WEAK"),
            _match("Docker", "REQUIRED", "MISSING", evidence=None),
            _match("AWS", "PREFERRED", "MATCHED"),
            _match("Azure", "PREFERRED", "WEAK"),
        ]
    )
    assert result["required_score"] == 50.0
    assert result["preferred_score"] == 75.0


def test_category_breakdown_uses_status_values() -> None:
    result = calculate_candidate_score(
        [
            _match("Python", "REQUIRED", "MATCHED"),
            _match("SQL", "REQUIRED", "WEAK"),
            _match("Docker", "REQUIRED", "MISSING", evidence=None),
        ]
    )
    assert result["category_breakdown"] == {
        "SKILL": {"score": 50.0, "matched": 1, "weak": 1, "missing": 1, "total": 3}
    }


def test_requirement_contributions_are_explainable() -> None:
    result = calculate_candidate_score([_match("Python", "REQUIRED", "MATCHED")])
    contribution = result["requirement_analysis"][0]
    assert contribution["status_value"] == 1.0
    assert contribution["importance_weight"] == 1.0
    assert contribution["weighted_value"] == 1.0


def test_gap_engine_generates_strengths_and_priorities() -> None:
    result = generate_skill_gap_summary(
        [
            _match("Python", "REQUIRED", "MATCHED"),
            _match("Java", "REQUIRED", "WEAK"),
            _match("Docker", "REQUIRED", "MISSING", evidence=None),
            _match("AWS", "PREFERRED", "MISSING", evidence=None),
        ]
    )
    assert [item["requirement"] for item in result["strengths"]] == ["Python"]
    assert [item["requirement"] for item in result["weak_areas"]] == ["Java"]
    assert [item["requirement"] for item in result["missing_requirements"]] == ["Docker", "AWS"]
    priorities = {item["requirement"]: item["priority"] for item in result["priority_gaps"]}
    assert priorities == {"Java": "MEDIUM", "Docker": "HIGH", "AWS": "LOW"}
    assert result["weak_areas"][0]["reason"] == "Limited supporting evidence found."
