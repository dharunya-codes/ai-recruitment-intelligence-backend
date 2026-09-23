from __future__ import annotations

from typing import Any


def compare_snapshots(snapshots: list[dict[str, Any]]) -> dict[str, Any]:
    if len(snapshots) < 2:
        return {"progress_status": "INSUFFICIENT_HISTORY", "improved": [], "remaining_gaps": [], "new_gaps": [], "evidence_changes": [], "assessment_changes": []}
    previous, current = snapshots[-2], snapshots[-1]
    old = {item["requirement"]: item["match_status"] for item in previous.get("requirement_analysis", [])}
    new = {item["requirement"]: item["match_status"] for item in current.get("requirement_analysis", [])}
    improved = [skill for skill, status in new.items() if status == "MATCHED" and old.get(skill) != "MATCHED"]
    remaining = [skill for skill, status in new.items() if status != "MATCHED"]
    added = [skill for skill in new if skill not in old]
    return {"progress_status": "CHANGES_DETECTED" if improved or added or remaining != [skill for skill, status in old.items() if status != "MATCHED"] else "NO_CHANGES_DETECTED", "improved": improved, "remaining_gaps": remaining, "new_gaps": added, "evidence_changes": improved, "assessment_changes": []}