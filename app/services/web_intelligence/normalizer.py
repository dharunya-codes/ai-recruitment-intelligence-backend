from __future__ import annotations

from typing import Any

from app.schemas.web_intelligence import ExternalCandidate, ExternalJob
from app.services.skill_extractor import extract_skills
from app.services.web_intelligence.compliance import sanitize_public_candidate_profile


def normalize_external_job(raw: dict[str, Any], default_source: str = "PUBLIC_SOURCE") -> ExternalJob:
    """Normalize heterogeneous public job payloads into standard ExternalJob."""
    job_id = str(raw.get("id") or raw.get("source_id") or raw.get("job_id") or "job_unknown")
    source = str(raw.get("source") or default_source)
    title = str(raw.get("title") or raw.get("job_title") or "Untitled Position").strip()
    company = str(raw.get("company") or raw.get("company_name") or "Unknown Company").strip()
    location = str(raw.get("location") or raw.get("city") or "Remote").strip()
    employment_type = str(raw.get("employment_type") or raw.get("type") or "Full-time").strip()
    description = str(raw.get("description") or raw.get("job_description") or raw.get("summary") or "").strip()

    # Normalize skills: if provided use them, else extract from title and description
    skills = raw.get("skills") or raw.get("required_skills")
    if isinstance(skills, list):
        normalized_skills = [str(s).strip() for s in skills if str(s).strip()]
    else:
        normalized_skills = extract_skills(f"{title} {description}")

    url = str(raw.get("url") or raw.get("link") or raw.get("job_url") or f"https://example.com/jobs/{job_id}")
    posted_at = str(raw.get("posted_at") or raw.get("date_posted") or raw.get("created_at") or "")

    return ExternalJob(
        id=job_id,
        source=source,
        title=title,
        company=company,
        location=location,
        employment_type=employment_type,
        description=description,
        skills=normalized_skills,
        url=url,
        posted_at=posted_at or None,
    )


def normalize_external_candidate(raw: dict[str, Any], default_source: str = "PUBLIC_SOURCE") -> ExternalCandidate:
    """Normalize heterogeneous public candidate payloads into standard ExternalCandidate with privacy sanitization."""
    sanitized = sanitize_public_candidate_profile(raw)

    source = str(sanitized.get("source") or default_source)
    source_id = str(sanitized.get("source_id") or sanitized.get("id") or "cand_unknown")
    name = str(sanitized.get("name") or sanitized.get("full_name") or "Public Candidate Profile").strip()
    headline = str(sanitized.get("headline") or sanitized.get("title") or sanitized.get("summary") or "").strip()
    location = str(sanitized.get("location") or sanitized.get("city") or "Global").strip()

    public_skills = sanitized.get("public_skills") or sanitized.get("skills")
    if isinstance(public_skills, list):
        normalized_skills = [str(s).strip() for s in public_skills if str(s).strip()]
    else:
        normalized_skills = extract_skills(f"{headline} {' '.join(sanitized.get('projects', []))}")

    experience = sanitized.get("experience") or []
    if isinstance(experience, str):
        experience = [experience]
    elif not isinstance(experience, list):
        experience = []

    projects = sanitized.get("projects") or []
    if isinstance(projects, str):
        projects = [projects]
    elif not isinstance(projects, list):
        projects = []

    education = sanitized.get("education") or []
    if isinstance(education, str):
        education = [education]
    elif not isinstance(education, list):
        education = []

    profile_url = str(sanitized.get("profile_url") or sanitized.get("url") or f"https://example.com/profiles/{source_id}")

    return ExternalCandidate(
        source=source,
        source_id=source_id,
        name=name,
        headline=headline,
        location=location,
        public_skills=normalized_skills,
        experience=[str(e) for e in experience],
        projects=[str(p) for p in projects],
        education=[str(ed) for ed in education],
        profile_url=profile_url,
    )
