from __future__ import annotations

from typing import Any


def build_improvement_plan(
    priorities: list[dict[str, Any]],
    assessment_improvements: list[str],
    quality_findings: list[dict[str, Any]],
) -> dict[str, list[dict[str, str]]]:
    immediate: list[dict[str, str]] = []
    short_term: list[dict[str, str]] = []
    medium_term: list[dict[str, str]] = []
    for item in priorities:
        if item["priority"] == "CRITICAL":
            immediate.append({"skill": item["skill"], "action": f"Review {item['skill']} fundamentals and add supported evidence to the resume."})
        elif item["priority"] == "HIGH":
            short_term.append({"skill": item["skill"], "action": f"Build or document a small {item['skill']} exercise if supported by your experience."})
    for improvement in assessment_improvements:
        medium_term.append({"skill": "Assessment focus", "action": improvement})
    for finding in quality_findings:
        immediate.append({"skill": finding["category"], "action": finding["recommendation"]})
    return {"IMMEDIATE": immediate, "SHORT_TERM": short_term, "MEDIUM_TERM": medium_term}