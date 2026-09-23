from __future__ import annotations

from typing import Any


def analyze_evidence_consistency(
    requirement_analysis: list[dict[str, Any]],
    verification: list[dict[str, Any]],
    assessment_results: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    verification_by_skill = {str(item.get("skill", "")).casefold(): item for item in verification}
    assessment_by_skill: dict[str, list[float]] = {}
    for item in assessment_results or []:
        assessment_by_skill.setdefault(str(item.get("skill", "")).casefold(), []).append(float(item.get("score", 0)))
    results = []
    for requirement in requirement_analysis:
        skill = str(requirement.get("requirement", ""))
        resume_status = str(requirement.get("match_status", "MISSING")).upper()
        verification_item = verification_by_skill.get(skill.casefold())
        reported = verification_item and verification_item.get("evidence_status") == "CANDIDATE_VERIFIED"
        scores = assessment_by_skill.get(skill.casefold(), [])
        strong_assessment = bool(scores) and sum(scores) / len(scores) >= 8
        weak_assessment = bool(scores) and sum(scores) / len(scores) <= 4
        if resume_status in {"MATCHED", "WEAK"} and (reported or strong_assessment):
            conclusion = "Evidence sources are mutually supportive."
        elif resume_status == "MISSING" and not reported and not strong_assessment:
            conclusion = "Evidence is insufficient; additional verification may be useful."
        elif weak_assessment or (resume_status == "WEAK" and not reported):
            conclusion = "Evidence sources differ; additional verification may be useful."
        else:
            conclusion = "Evidence is available from more than one source."
        results.append({"skill": skill, "resume_status": resume_status, "verification_status": verification_item.get("evidence_status") if verification_item else "NOT_AVAILABLE", "assessment_signal": "STRONG" if strong_assessment else "WEAK" if weak_assessment else "NOT_AVAILABLE", "conclusion": conclusion})
    return results