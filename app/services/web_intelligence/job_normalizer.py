from __future__ import annotations

import re
from typing import Any

from app.services.requirement_extractor import extract_requirements
from app.services.skill_extractor import extract_skills
from app.services.web_intelligence.source_policy import validate_source_url


def normalize_job_posting(raw_job: dict[str, Any], default_source: str = "Permitted Public Job Feed", default_source_type: str = "public_feed") -> dict[str, Any]:
    """Normalize a raw job record from any permitted public source into the standard HALO WebJob schema."""
    title = str(raw_job.get("title") or raw_job.get("job_title") or "Software Engineer").strip()
    company = str(raw_job.get("company") or raw_job.get("company_name") or "Tech Company").strip()
    location = str(raw_job.get("location") or "Remote").strip()
    employment_type = raw_job.get("employment_type") or raw_job.get("job_type") or "Full-time"
    description = str(raw_job.get("description") or raw_job.get("job_description") or "").strip()

    # Clean HTML tags if any present
    clean_desc = re.sub(r"<[^>]+>", " ", description)
    clean_desc = " ".join(clean_desc.split())

    # Summary
    summary = clean_desc[:280] + "..." if len(clean_desc) > 280 else clean_desc
    if not summary:
        summary = f"Job opportunity for {title} at {company}."

    # Extract requirements from job description
    extracted_reqs = extract_requirements(clean_desc) if clean_desc else []
    extracted_skills_list = extract_skills(clean_desc) if clean_desc else []

    required_skills: list[str] = []
    preferred_skills: list[str] = []
    experience: str | None = None
    education: str | None = None

    for item in extracted_reqs:
        cat = item.get("category", "")
        req_text = item.get("requirement", "")
        importance = item.get("importance", "REQUIRED")
        if cat == "SKILL":
            if importance == "REQUIRED":
                if req_text not in required_skills:
                    required_skills.append(req_text)
            else:
                if req_text not in preferred_skills:
                    preferred_skills.append(req_text)
        elif cat == "EXPERIENCE" and not experience:
            experience = req_text
        elif cat == "EDUCATION" and not education:
            education = req_text

    # Supplement with extracted skills if list was sparse
    for s in extracted_skills_list:
        if s not in required_skills and s not in preferred_skills:
            if len(required_skills) < 4:
                required_skills.append(s)
            else:
                preferred_skills.append(s)

    # If raw job has tags/skills explicitly supplied by the source
    raw_tags = raw_job.get("tags") or raw_job.get("skills") or []
    for tag in raw_tags:
        if isinstance(tag, str) and tag.strip():
            t_clean = tag.strip()
            if t_clean not in required_skills and t_clean not in preferred_skills:
                required_skills.append(t_clean)

    url = raw_job.get("url") or raw_job.get("job_url") or f"https://www.arbeitnow.com/jobs"
    if not validate_source_url(url):
        url = "https://www.arbeitnow.com/jobs"

    source = raw_job.get("source") or default_source
    source_type = raw_job.get("source_type") or default_source_type
    date_info = raw_job.get("posted_at") or raw_job.get("date_info") or raw_job.get("created_at") or "Recently posted"

    return {
        "job_title": title,
        "company": company,
        "location": location,
        "employment_type": employment_type,
        "required_skills": required_skills or ["Python", "SQL", "Git"],
        "preferred_skills": preferred_skills,
        "experience": experience,
        "education": education,
        "job_description_summary": summary,
        "source": source,
        "source_type": source_type,
        "job_url": url,
        "date_info": str(date_info),
    }
