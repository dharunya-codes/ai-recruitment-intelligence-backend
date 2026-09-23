from __future__ import annotations

from typing import Any


PROJECT_RULES = {
    "docker": {"project_title": "Containerized service deployment", "difficulty": "INTERMEDIATE", "components": ["REST API", "Dockerfile", "documented deployment steps"]},
    "siem": {"project_title": "Security event monitoring lab", "difficulty": "INTERMEDIATE", "components": ["sample authentication logs", "event queries", "alert documentation"]},
    "python": {"project_title": "Python automation utility", "difficulty": "BEGINNER", "components": ["input validation", "error handling", "tests"]},
    "sql": {"project_title": "SQL reporting dataset", "difficulty": "BEGINNER", "components": ["relational tables", "joins", "documented queries"]},
    "linux": {"project_title": "Linux operations lab", "difficulty": "BEGINNER", "components": ["shell commands", "service inspection", "runbook"]},
    "incident response": {"project_title": "Incident response case study", "difficulty": "ADVANCED", "components": ["timeline", "evidence notes", "containment plan"]},
}


def recommend_projects(target_role: str, gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recommendations = []
    for gap in gaps:
        rule = PROJECT_RULES.get(str(gap.get("skill", "")).casefold())
        if not rule:
            continue
        recommendations.append({
            "project_title": rule["project_title"],
            "target_skills": [gap["skill"]],
            "difficulty": rule["difficulty"],
            "purpose": f"Generate practical {gap['skill']} evidence relevant to {target_role}.",
            "suggested_components": rule["components"],
            "evidence_to_document": f"Document the candidate's actual contribution, technologies, and outcome for {gap['skill']}.",
        })
    return recommendations