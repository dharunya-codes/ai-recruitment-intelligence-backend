from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.candidate import _get_candidate_resume
from app.api.jobs import get_company_job
from app.database.database import get_db
from app.models.requirement import JobRequirement
from app.models.user import User
from app.schemas.web_intelligence import (
    CandidateGitHubRequestWeb,
    CandidateGitHubResponseWeb,
    CandidateJobComparisonRequest,
    CandidateJobComparisonResponse,
    CandidateJobMatchRequestWeb,
    CandidateJobMatchResponseWeb,
    CandidateJobSearchRequestWeb,
    CandidateJobSearchResponseWeb,
    CandidateMatchAnalysis,
    DiscoveredCandidateResult,
    JobSearchRequest,
    JobSearchResponse,
    RecruiterCandidateDiscoveryRequest,
    RecruiterCandidateDiscoveryResponse,
    RecruiterSearchRequest,
    RecruiterSearchResponse,
)
from app.services.analysis_cache_service import analysis_cache, make_web_search_cache_key
from app.services.gap_engine import generate_skill_gap_summary
from app.services.matching_engine import MATCHED, MISSING, WEAK, match_resume_to_requirements
from app.services.requirement_extractor import extract_requirements
from app.services.resume_quality_service import analyze_resume_quality
from app.services.scoring_engine import calculate_candidate_score
from app.services.skill_extractor import extract_skills
from app.services.web_intelligence import (
    LINKEDIN_POLICY_NOTICE,
    aggregate_skill_demand,
    extract_web_requirements,
    get_role_expansion,
    github_client,
    match_candidate_to_discovered_jobs,
    match_profiles_for_recruiter,
    public_job_search,
    public_profile_search,
    validate_source_url,
)
from app.services.web_intelligence.source_manager import source_manager
from app.utils.security import get_candidate_user, get_company_user

intelligence_router = APIRouter(prefix="/intelligence", tags=["Web Intelligence"])
candidate_web_router = APIRouter(prefix="/candidate/web-intelligence", tags=["Candidate Web Intelligence", "Web Intelligence"])
recruiter_web_router = APIRouter(prefix="/jobs", tags=["Recruiter Web Intelligence", "Web Intelligence"])


# =====================================================================
# 1. RECRUITER WEB INTELLIGENCE
# =====================================================================
@intelligence_router.post(
    "/recruiter/search",
    response_model=RecruiterSearchResponse,
    summary="Recruiter public candidate and project discovery from JD",
)
def recruiter_web_search(
    payload: RecruiterSearchRequest,
    current_user: User = Depends(get_company_user),
) -> RecruiterSearchResponse:
    # 1. Extract requirements from JD
    web_reqs = extract_web_requirements(payload.job_title, payload.job_description)

    # 2. Search GitHub public repositories & contributor evidence
    github_evidence = github_client.search_users_and_evidence(
        skills=web_reqs["required_skills"] + web_reqs["preferred_skills"],
        role=payload.job_title,
        limit=payload.limit,
    )

    # 3. Discover public technical profiles
    profiles = public_profile_search.search_profiles(
        job_title=payload.job_title,
        requirements=web_reqs["required_skills"],
        limit=payload.limit,
    )

    # 4. Match profiles against JD requirements
    matching_results = match_profiles_for_recruiter(profiles or github_evidence, web_reqs)

    # 5. Get source transparency statuses
    source_statuses = public_profile_search.get_source_statuses()

    return RecruiterSearchResponse(
        job_requirements=web_reqs,
        profiles=profiles,
        github_results=github_evidence,
        matching_results=matching_results,
        source_status=source_statuses,
        compliance_notice=(
            "Only permitted and authorized public-source data is used. "
            "GitHub public technical data is accessed through the GitHub API, "
            "while LinkedIn information is accessed only through permitted/authorized mechanisms."
        ),
    )


# =====================================================================
# 2. CANDIDATE WEB INTELLIGENCE
# =====================================================================
@intelligence_router.post(
    "/candidate/jobs/search",
    response_model=CandidateJobSearchResponseWeb,
    summary="Discover real public job opportunities for candidate target role",
)
def candidate_web_job_search(
    payload: CandidateJobSearchRequestWeb,
    current_user: User = Depends(get_candidate_user),
) -> CandidateJobSearchResponseWeb:
    expanded = get_role_expansion(payload.target_role)
    jobs = public_job_search.search_jobs(
        target_role=payload.target_role,
        location=payload.location,
        limit=payload.limit,
    )

    return CandidateJobSearchResponseWeb(
        target_role=payload.target_role,
        expanded_keywords=expanded,
        jobs=jobs,
    )


@intelligence_router.post(
    "/candidate/jobs/match",
    response_model=CandidateJobMatchResponseWeb,
    summary="Match candidate resume against discovered public jobs",
)
def candidate_web_job_match(
    payload: CandidateJobMatchRequestWeb,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_candidate_user),
) -> CandidateJobMatchResponseWeb:
    # Strict candidate ownership verification
    resume = _get_candidate_resume(payload.resume_id, current_user, db)

    # Discover jobs
    jobs = public_job_search.search_jobs(
        target_role=payload.target_role,
        location=payload.location,
        limit=payload.limit,
    )

    # Match candidate resume against discovered jobs
    resume_text = resume.extracted_text or ""
    match_data = match_candidate_to_discovered_jobs(resume_text, jobs)

    # Aggregate skill market view across discovered jobs
    demand_data = aggregate_skill_demand(payload.target_role, jobs)

    return CandidateJobMatchResponseWeb(
        target_role=payload.target_role,
        resume_id=resume.id,
        jobs=match_data["job_matches"],
        skill_matches=match_data["skill_matches"],
        skill_gaps=match_data["skill_gaps"],
        observed_skill_demand=demand_data["skill_demand"],
        market_summary_label="Observed requirements in discovered jobs",
    )


@intelligence_router.post(
    "/candidate/github",
    response_model=CandidateGitHubResponseWeb,
    summary="Candidate GitHub technical intelligence and project examples",
)
def candidate_web_github_intelligence(
    payload: CandidateGitHubRequestWeb,
    current_user: User = Depends(get_candidate_user),
) -> CandidateGitHubResponseWeb:
    data = github_client.get_role_projects(payload.target_role)
    return CandidateGitHubResponseWeb(**data)


# =====================================================================
# 3. BACKWARDS-COMPATIBLE LEGACY ROUTES
# =====================================================================
@candidate_web_router.post("/jobs/search", response_model=JobSearchResponse, summary="Discover public jobs from permitted sources")
def search_public_jobs(
    payload: JobSearchRequest,
    current_user: User = Depends(get_candidate_user),
) -> JobSearchResponse:
    cache_key = make_web_search_cache_key(
        search_type="job_search",
        query=payload.query,
        location=payload.location,
        company=payload.company,
        limit=payload.limit,
    )

    def compute_search() -> dict[str, Any]:
        results = source_manager.search_jobs(
            query=payload.query,
            location=payload.location,
            company=payload.company,
            source_filter=payload.source,
            limit=payload.limit,
        )
        return {
            "query": payload.query,
            "location": payload.location,
            "total_results": len(results),
            "results": [r.model_dump() for r in results],
        }

    data = analysis_cache.get_or_compute(cache_key, compute_search)
    return JobSearchResponse(**data)


@candidate_web_router.post("/jobs/compare", response_model=CandidateJobComparisonResponse, summary="Compare candidate resume against discovered public job")
def compare_candidate_job(
    payload: CandidateJobComparisonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_candidate_user),
) -> CandidateJobComparisonResponse:
    resume = _get_candidate_resume(payload.resume_id, current_user, db)

    if payload.job_source_url and not validate_source_url(payload.job_source_url):
        raise HTTPException(status_code=422, detail="Invalid job source URL format")

    extracted = extract_requirements(payload.job_description)
    if not extracted:
        raise HTTPException(status_code=422, detail="No extractable requirements found in the job description")

    requirements = [SimpleNamespace(id=index + 1, **item) for index, item in enumerate(extracted)]

    resume_text = resume.extracted_text or ""
    matches = match_resume_to_requirements(resume_text, requirements)
    score = calculate_candidate_score(matches)
    detected = extract_skills(resume_text)
    gap_summary = generate_skill_gap_summary(matches)
    quality_findings = analyze_resume_quality(resume_text)

    matched_reqs = [item for item in matches if item["match_status"] == MATCHED]
    weak_reqs = [item for item in matches if item["match_status"] == WEAK]
    missing_reqs = [item for item in matches if item["match_status"] == MISSING]

    strong_skills = [item["requirement"] for item in matched_reqs if item.get("category") == "SKILL"] or [item["requirement"] for item in matched_reqs]
    weak_skills = [item["requirement"] for item in weak_reqs if item.get("category") == "SKILL"] or [item["requirement"] for item in weak_reqs]
    missing_skills = [item["requirement"] for item in missing_reqs if item.get("category") == "SKILL"] or [item["requirement"] for item in missing_reqs]

    needs_verification = [item["requirement"] for item in weak_reqs if item.get("importance") == "REQUIRED"] or weak_skills

    evidence_list = [
        {
            "requirement": item.get("requirement"),
            "category": item.get("category"),
            "importance": item.get("importance"),
            "match_status": item.get("match_status"),
            "evidence_strength": "STRONG" if item.get("match_status") == MATCHED else ("WEAK" if item.get("match_status") == WEAK else "MISSING"),
            "resume_mention": item.get("match_status") in {MATCHED, WEAK},
            "project_evidence": bool("project" in (item.get("evidence_text") or "").casefold() or "built" in (item.get("evidence_text") or "").casefold()),
            "evidence_text": item.get("evidence_text"),
        }
        for item in score.get("requirement_analysis", [])
    ]

    cat_breakdown = score.get("category_breakdown", {})
    score_breakdown = {
        "required_skills": score.get("required_score"),
        "preferred_skills": score.get("preferred_score"),
        "experience": cat_breakdown.get("EXPERIENCE", {}).get("score", score.get("overall_match_score")),
        "education": cat_breakdown.get("EDUCATION", {}).get("score", 85.0),
        "project_relevance": score.get("overall_match_score"),
        "evidence_strength": score.get("overall_match_score"),
        **cat_breakdown,
    }

    suggestions = [f.get("recommendation") for f in quality_findings if f.get("recommendation")]
    for m in missing_skills[:3]:
        suggestions.append(f"Learn or demonstrate project work for {m}.")
    for w in weak_skills[:2]:
        suggestions.append(f"Add concrete implementation evidence for {w} to your resume.")

    return CandidateJobComparisonResponse(
        resume_id=resume.id,
        job_title=payload.job_title,
        job_source_url=payload.job_source_url,
        match_score=score.get("overall_match_score"),
        overall_match_score=score.get("overall_match_score"),
        required_score=score.get("required_score"),
        preferred_score=score.get("preferred_score"),
        score_status=score.get("score_status", "CALCULATED"),
        score_breakdown=score_breakdown,
        strong_skills=strong_skills,
        weak_skills=weak_skills,
        missing_skills=missing_skills,
        needs_verification=needs_verification,
        evidence=evidence_list,
        skill_gaps={
            "strong": strong_skills,
            "weak": weak_skills,
            "needs_verification": needs_verification,
            "missing": missing_skills,
        },
        improvement_suggestions=list(dict.fromkeys(suggestions)),
        detected_skills=detected,
        matched_requirements=matched_reqs,
        weak_requirements=weak_reqs,
        missing_requirements=missing_reqs,
    )


@recruiter_web_router.post("/{job_id}/candidate-discovery", response_model=RecruiterCandidateDiscoveryResponse, summary="Discover public candidate profiles for an authorized job")
def discover_candidates_for_job(
    job_id: int,
    payload: RecruiterCandidateDiscoveryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> RecruiterCandidateDiscoveryResponse:
    job = get_company_job(job_id, current_user.company_id, db)

    job_reqs = db.query(JobRequirement).filter(JobRequirement.job_id == job.id).order_by(JobRequirement.id).all()
    if not job_reqs and job.description:
        extracted = extract_requirements(job.description)
        job_reqs = [SimpleNamespace(id=i + 1, **item) for i, item in enumerate(extracted)]

    req_labels = [r.requirement for r in job_reqs] if job_reqs else []

    candidates = source_manager.search_candidates(
        job_title=job.title,
        requirements=req_labels,
        location=payload.location,
        skills_filter=payload.skills_filter,
        limit=payload.limit,
    )

    results: list[DiscoveredCandidateResult] = []

    for cand in candidates:
        profile_text = (
            f"{cand.name}\n"
            f"{cand.headline}\n"
            f"Skills: {', '.join(cand.public_skills)}\n"
            f"Projects: {' '.join(cand.projects)}\n"
            f"Experience: {' '.join(cand.experience)}\n"
            f"Education: {' '.join(cand.education)}"
        )

        if job_reqs:
            matches = match_resume_to_requirements(profile_text, job_reqs)
            score_data = calculate_candidate_score(matches)
            matched_items = [m["requirement"] for m in matches if m["match_status"] == MATCHED]
            weak_items = [m["requirement"] for m in matches if m["match_status"] == WEAK]
            missing_items = [m["requirement"] for m in matches if m["match_status"] == MISSING]
            match_score = score_data.get("overall_match_score")
        else:
            matched_items = list(cand.public_skills)
            weak_items = []
            missing_items = []
            match_score = 75.0 if cand.public_skills else 50.0

        evidence_summary = (
            f"Public projects and headline indicate alignment with {', '.join(matched_items[:3])}."
            if matched_items
            else "Public profile lists general technical background."
        )

        results.append(
            DiscoveredCandidateResult(
                source=cand.source,
                source_profile_url=cand.profile_url,
                name=cand.name,
                headline=cand.headline,
                location=cand.location,
                public_skills=cand.public_skills,
                match_analysis=CandidateMatchAnalysis(
                    match_score=match_score,
                    matched_requirements=matched_items,
                    weak_requirements=weak_items,
                    missing_requirements=missing_items,
                    public_evidence_summary=evidence_summary,
                ),
            )
        )

    return RecruiterCandidateDiscoveryResponse(
        job_id=job.id,
        job_title=job.title,
        candidates_count=len(results),
        results=results,
    )
