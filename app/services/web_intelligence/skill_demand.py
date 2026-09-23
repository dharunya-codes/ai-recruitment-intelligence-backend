from __future__ import annotations

from collections import Counter
from typing import Any


def aggregate_skill_demand(target_role: str, jobs: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate observed skill frequencies across discovered public jobs."""
    skill_counter: Counter[str] = Counter()

    for job in jobs:
        reqs = job.get("required_skills", [])
        prefs = job.get("preferred_skills", [])
        # Deduplicate per job so 1 job counts once per skill
        job_skills = set(reqs + prefs)
        for s in job_skills:
            if s and isinstance(s, str):
                skill_counter[s.strip()] += 1

    total_jobs = len(jobs)
    skill_demand = []

    for skill, count in skill_counter.most_common():
        pct = round((count / total_jobs) * 100.0, 1) if total_jobs > 0 else 0.0
        skill_demand.append(
            {
                "skill": skill,
                "job_count": count,
                "frequency_percentage": pct,
            }
        )

    return {
        "role": target_role,
        "total_jobs_discovered": total_jobs,
        "label": "Observed requirements in discovered jobs",
        "skill_demand": skill_demand,
    }
