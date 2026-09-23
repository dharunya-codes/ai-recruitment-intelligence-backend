from __future__ import annotations

from typing import Any


QUESTION_TYPES = {"WHAT_SHOULD_I_IMPROVE", "WHAT_SKILL_IS_MISSING", "WHY_IS_MY_MATCH_SCORE_LOW", "WHAT_EVIDENCE_IS_MISSING", "WHAT_SHOULD_I_PRACTICE", "WHAT_PROJECT_SHOULD_I_BUILD", "WHAT_SHOULD_I_VERIFY"}


def answer_career_question(question_type: str, intelligence: dict[str, Any]) -> dict[str, Any]:
    if question_type not in QUESTION_TYPES:
        return {"status": "INSUFFICIENT_DATA", "answer": "This question type is not supported by the career intelligence service.", "supporting_evidence": [], "related_skills": [], "recommended_actions": []}
    gaps = intelligence.get("priority_gaps", [])
    if question_type == "WHAT_SKILL_IS_MISSING":
        answer = "The highest-priority gaps are: " + ", ".join(gaps) if gaps else "No priority gaps were identified in the available analysis."
    elif question_type == "WHAT_EVIDENCE_IS_MISSING":
        answer = "Evidence needs strengthening for: " + ", ".join(intelligence.get("evidence_gaps", [])) if intelligence.get("evidence_gaps") else "No evidence gaps were identified."
    elif question_type == "WHAT_SHOULD_I_VERIFY":
        answer = "Next verification focus: " + ", ".join(intelligence.get("verification_gaps", [])) if intelligence.get("verification_gaps") else "No incomplete verification items were identified."
    else:
        answer = "Start with the listed priority gaps and the next actions derived from your analysis."
    return {"status": "ANSWERED", "answer": answer, "supporting_evidence": intelligence.get("evidence_gaps", []), "related_skills": gaps, "recommended_actions": intelligence.get("next_actions", [])}