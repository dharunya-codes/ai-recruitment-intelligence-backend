from __future__ import annotations

from typing import Any

from app.services.gap_engine import generate_skill_gap_summary
from app.services.matching_engine import MISSING, match_resume_to_requirements
from app.services.scoring_engine import calculate_candidate_score


def analyze_resume_against_jobs(resume_text: str, jobs: list[tuple[Any, list[Any]]]) -> list[dict[str, Any]]:
    results = []
    for job, requirements in jobs:
        matches = match_resume_to_requirements(resume_text, requirements)
        score = calculate_candidate_score(matches)
        results.append({
            "job_id": job.id,
            "job_title": job.title,
            "required_skill_coverage": score.get("required_score"),
            "preferred_skill_coverage": score.get("preferred_score"),
            "skill_gaps": [item["requirement"] for item in matches if item["match_status"] == MISSING],
            "evidence_strength": {item["requirement"]: item["match_status"] for item in matches},
            "analysis_status": score.get("score_status"),
            "skill_gap": generate_skill_gap_summary(matches),
        })
    return results