from __future__ import annotations

import re
from collections.abc import Iterable

from app.services.skill_extractor import find_skill_alias

MATCHED = "MATCHED"
WEAK = "WEAK"
MISSING = "MISSING"

SUPPORTING_CONTEXT = (
    "project",
    "developed",
    "built",
    "implemented",
    "created",
    "worked",
    "experience",
    "internship",
    "deployed",
    "used",
    "designed",
    "application",
    "applications",
    "certification",
    "certifications",
)
STOP_WORDS = {
    "a", "an", "and", "are", "be", "for", "in", "of", "on", "or", "the",
    "to", "with", "will", "using", "use", "should", "must", "have", "has",
    "years", "year", "experience", "required", "preferred", "is", "as",
}


def _sentences(text: str) -> Iterable[str]:
    return (part.strip() for part in re.split(r"[.!?\n]+", text) if part.strip())


def _contains_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"(?<![\w+#]){re.escape(phrase)}(?![\w+#])", text, re.IGNORECASE) is not None


def _evidence_sentence(text: str, requirement: str) -> str | None:
    for line in text.splitlines():
        clean_line = line.strip()
        if clean_line and _contains_phrase(clean_line, requirement):
            return clean_line
    for sentence in _sentences(text):
        if _contains_phrase(sentence, requirement):
            return sentence
    if _contains_phrase(text, requirement):
        match = re.search(re.escape(requirement), text, flags=re.IGNORECASE)
        if match:
            start = max(0, text.rfind("\n", 0, match.start()) + 1)
            end = text.find("\n", match.end())
            return text[start:] if end == -1 else text[start:end]
    return None


def _content_tokens(text: str) -> set[str]:
    return {
        token.casefold()
        for token in re.findall(r"[A-Za-z][A-Za-z+#'-]*", text)
        if token.casefold() not in STOP_WORDS and len(token) > 2
    }


def _tokens_overlap(left: set[str], right: set[str]) -> int:
    return sum(
        1
        for left_token in left
        if any(
            left_token == right_token
            or len(left_token) >= 5
            and len(right_token) >= 5
            and (left_token.startswith(right_token) or right_token.startswith(left_token))
            for right_token in right
        )
    )


def _context_is_supporting(sentence: str) -> bool:
    lowered = sentence.casefold()
    return any(marker in lowered for marker in SUPPORTING_CONTEXT)


def _match_status(category: str, requirement: str, evidence: str | None, resume_text: str) -> str:
    if evidence is None:
        return MISSING
    if category == "RESPONSIBILITY":
        requirement_tokens = _content_tokens(requirement)
        evidence_tokens = _content_tokens(evidence)
        overlap = _tokens_overlap(requirement_tokens, evidence_tokens)
        return MATCHED if overlap >= max(2, len(requirement_tokens) // 2) else WEAK
    if category == "EXPERIENCE":
        return MATCHED if _context_is_supporting(evidence) else WEAK
    if category in {"EDUCATION", "CERTIFICATION"}:
        return MATCHED if _context_is_supporting(evidence) or category == "EDUCATION" and "education" in evidence.casefold() else WEAK
    return MATCHED if _context_is_supporting(evidence) else WEAK


def _requirement_evidence(requirement: str, category: str, resume_text: str) -> str | None:
    if category == "SKILL":
        alias = find_skill_alias(resume_text, requirement)
        if alias is None:
            return None
        return _evidence_sentence(resume_text, alias) or alias
    if category == "RESPONSIBILITY":
        requirement_tokens = _content_tokens(requirement)
        for sentence in _sentences(resume_text):
            if _tokens_overlap(requirement_tokens, _content_tokens(sentence)) >= max(
                2, len(requirement_tokens) // 2
            ):
                return sentence
        return None
    return _evidence_sentence(resume_text, requirement)


def match_resume_to_requirements(resume_text: str, requirements: Iterable[object]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for requirement in requirements:
        name = str(requirement.requirement)
        category = str(requirement.category)
        evidence = _requirement_evidence(name, category, resume_text)
        results.append(
            {
                "requirement_id": requirement.id,
                "requirement": name,
                "category": category,
                "importance": requirement.importance,
                "match_status": _match_status(category, name, evidence, resume_text),
                "evidence_text": evidence,
            }
        )
    return results