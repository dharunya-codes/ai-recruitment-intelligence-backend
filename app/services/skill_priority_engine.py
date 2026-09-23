from __future__ import annotations

from typing import Any


def classify_priority(
    *,
    importance: str | None,
    match_status: str | None,
    verification_status: str | None = None,
    assessment_score: float | None = None,
) -> tuple[str, str]:
    importance = (importance or "REQUIRED").upper()
    match_status = (match_status or "MISSING").upper()
    verification_status = (verification_status or "").upper()
    if importance == "REQUIRED" and match_status == "MISSING":
        return "CRITICAL", "Required skill is missing from the available resume evidence."
    if importance == "REQUIRED" and match_status == "WEAK":
        return "HIGH", "Required skill is present but has limited supporting resume evidence."
    if match_status == "WEAK" and verification_status in {"", "PENDING", "NOT_VERIFIED"}:
        return "HIGH", "Skill has weak evidence and remains unverified."
    if assessment_score is not None and assessment_score <= 6:
        return "HIGH", "Assessment performance indicates that this skill needs further practice."
    if importance == "PREFERRED" and match_status in {"MISSING", "WEAK"}:
        return "MEDIUM", "Preferred skill is not strongly demonstrated in the available evidence."
    if match_status == "MATCHED":
        return "LOW", "Skill has supporting resume evidence and does not require immediate attention."
    return "MEDIUM", "Available evidence indicates a useful area for review."


def build_skill_priorities(
    requirement_analysis: list[dict[str, Any]],
    verification_by_skill: dict[str, str] | None = None,
    assessment_by_skill: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    verification_by_skill = verification_by_skill or {}
    assessment_by_skill = assessment_by_skill or {}
    results = []
    for item in requirement_analysis:
        skill = str(item.get("requirement", ""))
        priority, reason = classify_priority(
            importance=item.get("importance"),
            match_status=item.get("match_status"),
            verification_status=verification_by_skill.get(skill),
            assessment_score=assessment_by_skill.get(skill),
        )
        results.append({"skill": skill, "priority": priority, "reason": reason})
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(results, key=lambda item: (order[item["priority"]], item["skill"].casefold()))


def build_advanced_gaps(
    requirement_analysis: list[dict[str, Any]],
    verification_by_skill: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    verification_by_skill = verification_by_skill or {}
    gaps = []
    for item in requirement_analysis:
        skill = str(item.get("requirement", ""))
        match_status = str(item.get("match_status", "MISSING")).upper()
        verification = verification_by_skill.get(skill, "NOT_VERIFIED").upper()
        if match_status == "MISSING":
            status = "MISSING"
            reason = "Required or preferred by the analyzed role but not detected in the resume."
        elif verification == "CANDIDATE_VERIFIED":
            status = "CANDIDATE_VERIFIED"
            reason = "Candidate-reported verification evidence is available; it remains separate from resume evidence."
        elif match_status == "WEAK":
            status = "WEAK_EVIDENCE"
            reason = "The resume mentions this requirement but contains limited supporting evidence."
        else:
            status = "STRONG_EVIDENCE"
            reason = "The resume contains supporting evidence for this requirement."
        gaps.append({"skill": skill, "status": status, "reason": reason})
    return gaps


def transferable_skills(skills: list[str]) -> list[dict[str, Any]]:
    rules = {
        "python": ("Security Automation", "Python is a technical foundation for automation-related tasks."),
        "linux": ("Systems Operations", "Linux supports operating-system and systems operations work."),
        "sql": ("Data Analysis", "SQL is used to retrieve and analyze structured data."),
        "javascript": ("Web Development", "JavaScript is a foundation for browser-based web development."),
    }
    results = []
    for skill in skills:
        rule = rules.get(skill.casefold())
        if rule:
            results.append({"skill": skill, "transferable_to": [rule[0]], "reason": rule[1]})
    return results