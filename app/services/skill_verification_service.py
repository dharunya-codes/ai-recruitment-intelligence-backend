from __future__ import annotations

from collections.abc import Iterable

from app.services.matching_engine import MISSING, WEAK
from app.services.skill_priority_engine import classify_priority

PENDING = "PENDING"
ANSWERED = "ANSWERED"
NOT_VERIFIED = "NOT_VERIFIED"
CANDIDATE_VERIFIED = "CANDIDATE_VERIFIED"
NO_SUPPORTING_EVIDENCE = "NO_SUPPORTING_EVIDENCE"

PROJECT_INDICATORS = ("project", "built", "developed", "created", "implemented")
EXPERIENCE_INDICATORS = ("internship", "experience", "worked", "employment")
ANSWER_EVIDENCE_INDICATORS = (
    "project",
    "built",
    "developed",
    "created",
    "implemented",
    "application",
    "system",
)


def _value(item: object, key: str) -> object:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key)


def _priority(importance: str, status: str) -> str | None:
    if importance == "REQUIRED" and status == MISSING:
        return "HIGH"
    if importance == "REQUIRED" and status == WEAK:
        return "MEDIUM"
    if importance == "PREFERRED" and status == WEAK:
        return "LOW"
    return None


def _question_type(status: str, resume_text: str) -> str:
    lowered = resume_text.casefold()
    if status == MISSING:
        return "KNOWLEDGE_VERIFICATION"
    if any(marker in lowered for marker in PROJECT_INDICATORS):
        return "PROJECT_USAGE"
    if any(marker in lowered for marker in EXPERIENCE_INDICATORS):
        return "EXPERIENCE_USAGE"
    return "SKILL_USAGE"


def _question(skill: str, question_type: str, status: str) -> str:
    if question_type == "PROJECT_USAGE":
        return f"You mentioned {skill}. Describe a project where you used {skill}. What did you implement?"
    if question_type == "EXPERIENCE_USAGE":
        return f"You mentioned {skill}. Describe how you used {skill} in an internship, work experience, or academic project."
    if question_type == "KNOWLEDGE_VERIFICATION":
        return f"{skill} is listed as a required skill for this role. Explain how {skill} works and describe a practical situation where you would use it."
    return f"You mentioned {skill} in your resume. Describe how you have used {skill}."


def generate_verification_questions(
    requirement_matches: Iterable[object],
    resume_text: str,
) -> list[dict[str, object]]:
    eligible: list[tuple[int, object, str]] = []
    for match in requirement_matches:
        status = str(_value(match, "match_status")).upper()
        importance = str(_value(match, "importance") or "REQUIRED").upper()
        legacy_priority = _priority(importance, status)
        if legacy_priority:
            priority, _ = classify_priority(importance=importance, match_status=status)
            priority = legacy_priority
            priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[priority]
            eligible.append((priority_order, match, priority))

    eligible.sort(key=lambda item: item[0])
    questions: list[dict[str, object]] = []
    for _, match, priority in eligible[:5]:
        status = str(_value(match, "match_status")).upper()
        skill = str(_value(match, "requirement"))
        question_type = _question_type(status, resume_text)
        questions.append(
            {
                "skill": skill,
                "question": _question(skill, question_type, status),
                "priority": priority,
                "question_type": question_type,
                "match_status": status,
                "importance": str(_value(match, "importance") or "REQUIRED").upper(),
            }
        )
    return questions


def extract_candidate_reported_evidence(answer: str) -> str | None:
    lowered = answer.casefold()
    if any(indicator in lowered for indicator in ANSWER_EVIDENCE_INDICATORS):
        return answer
    return None