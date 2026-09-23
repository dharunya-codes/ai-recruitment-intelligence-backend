from __future__ import annotations

from typing import Any


def match_profile_to_requirements(
    profile: dict[str, Any],
    job_requirements: dict[str, Any],
) -> dict[str, Any]:
    """Compare a discovered public candidate profile and public repositories against JD requirements."""
    required_skills = job_requirements.get("required_skills", [])
    preferred_skills = job_requirements.get("preferred_skills", [])
    all_jd_skills = list(dict.fromkeys(required_skills + preferred_skills))

    public_skills = profile.get("public_skills", [])
    repos = profile.get("repositories", [])
    profile_url = profile.get("profile_url", "")
    source = profile.get("source", "GitHub")
    source_type = profile.get("source_type", "github_api")

    matched_skills: list[str] = []
    supporting_projects: list[str] = []
    supporting_evidence: list[dict[str, Any]] = []

    # Check direct profile skills
    for skill in all_jd_skills:
        s_lower = skill.lower()
        if any(s_lower == ps.lower() or s_lower in ps.lower() for ps in public_skills):
            if skill not in matched_skills:
                matched_skills.append(skill)
                supporting_evidence.append(
                    {
                        "skill": skill,
                        "source": source,
                        "evidence": f"Public profile states expertise in {skill}.",
                        "url": profile_url,
                    }
                )

    # Check public repository evidence (topics, languages, descriptions)
    for repo in repos:
        r_name = repo.get("name", "")
        r_desc = (repo.get("description") or "").lower()
        r_langs = [l.lower() for l in repo.get("languages", [])]
        r_topics = [t.lower() for t in repo.get("topics", [])]
        r_url = repo.get("url") or profile_url

        repo_matched = False
        for skill in all_jd_skills:
            s_lower = skill.lower()
            if s_lower in r_desc or s_lower in r_langs or s_lower in r_topics or s_lower in r_name.lower():
                if skill not in matched_skills:
                    matched_skills.append(skill)
                supporting_evidence.append(
                    {
                        "skill": skill,
                        "source": source,
                        "evidence": f"Public repository '{r_name}' demonstrates {skill} ({repo.get('description') or 'open-source implementation'}).",
                        "url": r_url,
                    }
                )
                repo_matched = True

        if repo_matched and r_name not in supporting_projects:
            supporting_projects.append(r_name)

    # Missing or unverified skills from the JD
    missing_or_unverified = [s for s in required_skills if s not in matched_skills]

    # Calculate explainable score
    if all_jd_skills:
        match_score = round((len(matched_skills) / len(all_jd_skills)) * 100.0, 1)
    else:
        match_score = 75.0 if matched_skills else 50.0

    # Build human-readable explanation
    if matched_skills and supporting_projects:
        explanation = f"Public technical evidence demonstrates {', '.join(matched_skills[:3])} in repositories {', '.join(supporting_projects[:2])}."
        if missing_or_unverified:
            explanation += f" Direct public evidence for {', '.join(missing_or_unverified[:2])} was not observed."
    elif matched_skills:
        explanation = f"Public profile demonstrates alignment with {', '.join(matched_skills[:3])}."
        if missing_or_unverified:
            explanation += f" Direct public evidence for {', '.join(missing_or_unverified[:2])} was not observed."
    else:
        explanation = "Public profile lists general software engineering background without direct evidence for target skills."

    github_url = profile_url if "github.com" in profile_url else None

    return {
        "profile": profile.get("name") or profile.get("username", "Candidate"),
        "source": source,
        "source_type": source_type,
        "public_profile_url": profile_url,
        "github_url": github_url,
        "matched_skills": matched_skills,
        "supporting_projects": supporting_projects,
        "supporting_evidence": supporting_evidence,
        "missing_or_unverified": missing_or_unverified,
        "explanation": explanation,
        "match_score": match_score,
    }


def match_profiles_for_recruiter(
    profiles: list[dict[str, Any]],
    job_requirements: dict[str, Any],
) -> list[dict[str, Any]]:
    """Match all discovered public candidate profiles against recruiter JD requirements."""
    return [match_profile_to_requirements(p, job_requirements) for p in profiles]
