from __future__ import annotations

from typing import Any

from app.services.skill_extractor import extract_skills


def match_resume_to_discovered_job(
    resume_text: str,
    candidate_skills: list[str],
    job: dict[str, Any],
) -> dict[str, Any]:
    """Compare candidate resume and skills against a discovered public job posting."""
    req_skills = job.get("required_skills", [])
    pref_skills = job.get("preferred_skills", [])
    all_job_skills = list(dict.fromkeys(req_skills + pref_skills))

    resume_lower = resume_text.lower()
    cand_skills_lower = {s.lower() for s in candidate_skills}

    matched_skills: list[str] = []
    missing_skills: list[str] = []
    related_skills: list[str] = []

    for skill in all_job_skills:
        s_lower = skill.lower()
        if s_lower in cand_skills_lower or s_lower in resume_lower:
            matched_skills.append(skill)
        else:
            # Check for partial / related overlap
            tokens = set(s_lower.split())
            if any(t in resume_lower for t in tokens if len(t) > 3):
                related_skills.append(skill)
            else:
                missing_skills.append(skill)

    # Calculate match score
    total_req = len(req_skills) if req_skills else 1
    req_matched = [s for s in req_skills if s in matched_skills]
    score = round((len(req_matched) / total_req) * 100.0, 1)

    # Experience alignment heuristic
    job_exp = job.get("experience")
    if job_exp:
        exp_alignment = f"Job requires {job_exp}. Verify years of professional experience in resume."
    else:
        exp_alignment = "Entry / Mid-level role alignment based on technical requirements."

    # Explanation
    if matched_skills and not missing_skills:
        explanation = f"Strong match: Candidate demonstrates all key required skills including {', '.join(matched_skills[:3])}."
    elif matched_skills and missing_skills:
        explanation = f"The candidate matches core skills ({', '.join(matched_skills[:3])}) but lacks direct evidence for {', '.join(missing_skills[:3])}."
    else:
        explanation = f"Low match: Candidate resume does not demonstrate key requirements for {job.get('job_title')}."

    return {
        "job_title": job.get("job_title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "employment_type": job.get("employment_type"),
        "job_url": job.get("job_url"),
        "source": job.get("source"),
        "source_type": job.get("source_type"),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "related_skills": related_skills,
        "experience_alignment": exp_alignment,
        "skill_gap": missing_skills,
        "match_score": score,
        "match_explanation": explanation,
    }


def match_candidate_to_discovered_jobs(
    resume_text: str,
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Match a candidate's resume across all discovered jobs and produce aggregate alignment."""
    extracted_skills = extract_skills(resume_text) if resume_text else []
    job_matches = [match_resume_to_discovered_job(resume_text, extracted_skills, j) for j in jobs]

    all_matched: list[str] = []
    all_gaps: list[str] = []

    for jm in job_matches:
        for ms in jm["matched_skills"]:
            if ms not in all_matched:
                all_matched.append(ms)
        for gs in jm["missing_skills"]:
            if gs not in all_gaps:
                all_gaps.append(gs)

    return {
        "job_matches": job_matches,
        "skill_matches": all_matched,
        "skill_gaps": all_gaps,
    }
