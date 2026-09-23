from __future__ import annotations

import re
from typing import Any

from app.services.requirement_extractor import extract_requirements
from app.services.skill_extractor import extract_skills
from app.services.web_intelligence.role_keywords import get_role_expansion, get_role_technologies


def extract_web_requirements(job_title: str, job_description: str) -> dict[str, Any]:
    """Extract structured role and skill requirements from JD specifically formatted for web intelligence."""
    extracted_reqs = extract_requirements(job_description or "")
    extracted_skills_list = extract_skills(job_description or "")

    required_skills: list[str] = []
    preferred_skills: list[str] = []
    technologies: list[str] = []
    certifications: list[str] = []
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
        elif cat == "EXPERIENCE":
            if not experience:
                experience = req_text
        elif cat == "EDUCATION":
            if not education:
                education = req_text
        elif cat == "CERTIFICATION":
            if req_text not in certifications:
                certifications.append(req_text)

    # Fallback to skills extractor if needed
    for s in extracted_skills_list:
        if s not in required_skills and s not in preferred_skills:
            if len(required_skills) < 5:
                required_skills.append(s)
            else:
                preferred_skills.append(s)

    # Detect known technologies from text
    known_techs = [
        "FastAPI", "Django", "Flask", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Git", "GraphQL", "REST API",
        "React", "Node.js", "TypeScript", "Python", "Java", "Go", "Pandas", "PyTorch", "TensorFlow", "Power BI", "Tableau"
    ]
    jd_lower = (job_description or "").lower()
    for tech in known_techs:
        if re.search(r"\b" + re.escape(tech.lower()) + r"\b", jd_lower):
            if tech not in technologies:
                technologies.append(tech)

    # Role keywords expansion
    role_keywords = get_role_expansion(job_title)

    return {
        "role": job_title or "Software Engineer",
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "technologies": technologies or required_skills[:4],
        "experience": experience,
        "education": education,
        "certifications": certifications,
        "role_keywords": role_keywords[:6],
    }
