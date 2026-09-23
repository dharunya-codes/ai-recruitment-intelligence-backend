from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


CORRECT_THRESHOLD = 0.80
PARTIAL_THRESHOLD = 0.30

_CONCEPT_ALIASES = {
    "log collection": ("log", "logs", "logging", "collect"),
    "event monitoring": ("event", "events", "monitor", "monitoring"),
    "correlation": ("correlate", "correlation", "correlates"),
    "alerts": ("alert", "alerts", "notification"),
    "authentication": ("authenticate", "authentication", "identity"),
    "authorization": ("authorize", "authorization", "permissions", "access control"),
}

_DEFAULT_CONCEPTS = {
    "SIEM": ("log collection", "event monitoring", "correlation", "alerts"),
    "SQL": ("query", "table", "filter", "join"),
    "Python": ("modules", "exceptions", "testing", "validation"),
    "Docker": ("image", "container", "build", "runtime"),
    "FastAPI": ("dependency injection", "validation", "request", "schema"),
    "Java": ("method", "parameters", "overloading", "overriding"),
}


@dataclass(frozen=True)
class EvaluationResult:
    score: float
    max_score: int
    evaluation_status: str
    feedback: str
    strengths: list[str]
    missing_points: list[str]


def normalize_text(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.casefold())
    normalized = re.sub(r"\b(logs|alerts|events)\b", lambda match: match.group(1)[:-1], normalized)
    return " ".join(normalized.split())


def expected_concepts_for_question(question: Any) -> list[str]:
    stored = getattr(question, "expected_concepts", None)
    if stored:
        try:
            concepts = json.loads(stored) if isinstance(stored, str) else stored
            if isinstance(concepts, list):
                return [str(concept) for concept in concepts]
        except (TypeError, json.JSONDecodeError):
            pass

    skill = str(getattr(question, "skill", ""))
    for name, concepts in _DEFAULT_CONCEPTS.items():
        if name.casefold() == skill.casefold():
            return list(concepts)
    question_text = normalize_text(str(getattr(question, "question", "")))
    return [word for word in ("purpose", "investigate", "explain", "design") if word in question_text] or ["relevant concept"]


def _concept_present(concept: str, answer: str) -> bool:
    normalized_concept = normalize_text(concept)
    if normalized_concept in answer:
        return True
    aliases = _CONCEPT_ALIASES.get(concept.casefold(), ())
    return any(normalize_text(alias) in answer for alias in aliases)


def evaluate_answer(question: Any, answer: Any) -> EvaluationResult:
    answer_text = answer if isinstance(answer, str) else getattr(answer, "answer", None)
    if not answer_text or not answer_text.strip():
        return EvaluationResult(0, 10, "NO_ANSWER", "No answer was submitted.", [], expected_concepts_for_question(question))

    concepts = expected_concepts_for_question(question)
    normalized_answer = normalize_text(answer_text)
    covered = [concept for concept in concepts if _concept_present(concept, normalized_answer)]
    coverage = len(covered) / len(concepts)
    score = round(coverage * 10, 2)
    if coverage >= CORRECT_THRESHOLD:
        evaluation_status = "CORRECT"
    elif coverage >= PARTIAL_THRESHOLD:
        evaluation_status = "PARTIAL"
    else:
        evaluation_status = "INCORRECT"

    skill = str(getattr(question, "skill", "the topic") or "the topic")
    strengths = [f"Mentioned {concept}" for concept in covered]
    missing = [concept for concept in concepts if concept not in covered]
    if evaluation_status == "CORRECT":
        feedback = f"The answer covers the main concepts expected for {skill}."
    elif evaluation_status == "PARTIAL":
        feedback = f"The answer covers some of the expected concepts for {skill}, but more detail is needed."
    else:
        feedback = f"The answer does not clearly cover the expected concepts for {skill}."
    return EvaluationResult(score, 10, evaluation_status, feedback, strengths, missing)