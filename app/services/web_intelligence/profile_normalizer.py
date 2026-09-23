from __future__ import annotations

from typing import Any

from app.services.web_intelligence.source_policy import (
    SOURCE_GITHUB,
    SOURCE_TYPE_API,
    sanitize_public_profile_text,
    validate_source_url,
)


def normalize_public_profile(raw_profile: dict[str, Any]) -> dict[str, Any]:
    """Normalize a raw public candidate profile record, sanitizing PII and validating URLs."""
    name = str(raw_profile.get("name") or raw_profile.get("username") or "Public Technical Contributor").strip()
    headline = str(raw_profile.get("headline") or raw_profile.get("bio") or "Open Source Software Contributor").strip()
    headline = sanitize_public_profile_text(headline)

    location = str(raw_profile.get("location") or "Global / Remote").strip()

    raw_skills = raw_profile.get("public_skills") or raw_profile.get("skills") or []
    cleaned_skills: list[str] = []
    for s in raw_skills:
        if isinstance(s, str) and s.strip():
            s_clean = s.strip()
            if s_clean not in cleaned_skills:
                cleaned_skills.append(s_clean)

    profile_url = str(raw_profile.get("profile_url") or raw_profile.get("url") or f"https://github.com/{name}")
    if not validate_source_url(profile_url):
        profile_url = f"https://github.com/{name}"

    source = raw_profile.get("source") or SOURCE_GITHUB
    source_type = raw_profile.get("source_type") or SOURCE_TYPE_API

    repositories = raw_profile.get("repositories", [])
    clean_repos = []
    for repo in repositories:
        repo_url = repo.get("url")
        if not validate_source_url(repo_url):
            repo_url = profile_url
        clean_repos.append(
            {
                "name": repo.get("name", "Project Repository"),
                "url": repo_url,
                "description": sanitize_public_profile_text(repo.get("description") or ""),
                "languages": repo.get("languages", []),
                "topics": repo.get("topics", []),
            }
        )

    return {
        "username": raw_profile.get("username") or name,
        "name": name,
        "headline": headline,
        "location": location,
        "public_skills": cleaned_skills,
        "repositories": clean_repos,
        "profile_url": profile_url,
        "source": source,
        "source_type": source_type,
    }
