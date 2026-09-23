from __future__ import annotations

import fitz
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.database.database import SessionLocal
from app.main import app
from app.models.analysis_snapshot import AnalysisSnapshot
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.services.analysis_cache_service import analysis_cache
from app.services.rate_limit_service import rate_limiter
from app.services.web_intelligence import (
    aggregate_skill_demand,
    extract_web_requirements,
    get_role_expansion,
    github_client,
    linkedin_adapter,
    match_candidate_to_discovered_jobs,
    match_profiles_for_recruiter,
    normalize_public_profile,
    public_job_search,
    public_profile_search,
    validate_source_url,
)

client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _clear_db() -> None:
    analysis_cache.clear()
    rate_limiter.clear()
    db = SessionLocal()
    try:
        db.query(JobRequirement).delete()
        db.query(AnalysisSnapshot).delete()
        db.query(Resume).delete()
        db.query(Job).delete()
        db.query(Candidate).delete()
        db.query(User).delete()
        db.query(Company).delete()
        db.commit()
    finally:
        db.close()


def _register_and_login_candidate(name: str = "Engine Candidate", email: str = "cand_engine@example.com") -> tuple[dict[str, str], dict]:
    client.post(
        "/candidate/auth/register",
        json={"email": email, "name": name, "password": "StrongPassword123"},
    )
    login_resp = client.post(
        "/candidate/auth/login",
        json={"email": email, "password": "StrongPassword123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers, login_resp.json()


def _register_and_login_recruiter(company_name: str = "WebIntel Corp", email: str = "hr_engine@webintel.com") -> tuple[dict[str, str], dict]:
    client.post(
        "/auth/register",
        json={"company_name": company_name, "email": email, "name": "HR Engine Lead", "password": "StrongPassword123", "role": "HR"},
    )
    login_resp = client.post(
        "/auth/login",
        json={"email": email, "password": "StrongPassword123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers, login_resp.json()


def _upload_resume(headers: dict[str, str], text: str = "Experienced Python and FastAPI backend developer with SQL and PostgreSQL.") -> int:
    response = client.post(
        "/candidate/resumes",
        headers=headers,
        files={"file": ("resume.pdf", _pdf_bytes(text), "application/pdf")},
    )
    assert response.status_code == 201
    return response.json()["id"]


# =====================================================================
# 1. LINKEDIN ADAPTER & COMPLIANCE TESTS
# =====================================================================
def test_linkedin_not_configured_returns_graceful_status():
    status = linkedin_adapter.get_status()
    assert status["source"] == "LinkedIn"
    assert status["status"] == "not_configured"
    assert "Authorized LinkedIn access is not configured" in status["message"]
    assert status["is_configured"] is False

    # When unconfigured, search_profiles returns empty list with zero fabrication
    results = linkedin_adapter.search_profiles("Python Developer", ["Python", "FastAPI"])
    assert results == []


def test_linkedin_authorized_adapter_structure_and_normalization():
    raw_linkedin_data = {
        "firstName": {"localized": {"en_US": "Dev"}},
        "lastName": {"localized": {"en_US": "User"}},
        "headline": {"localized": {"en_US": "Senior Backend Architect at CloudCo (email: dev@cloudco.com)"}},
        "locationName": "San Francisco, CA",
        "publicProfileUrl": "https://www.linkedin.com/in/devuser-test",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
    }

    normalized = linkedin_adapter.normalize_profile(raw_linkedin_data)
    assert normalized["name"] == "Dev User"
    assert "dev@cloudco.com" not in normalized["headline"]
    assert normalized["source"] == "LinkedIn"
    assert normalized["source_type"] == "linkedin_authorized_api"
    assert normalized["public_skills"] == ["Python", "FastAPI", "PostgreSQL"]
    assert len(normalized["public_evidence"]) > 0
    assert normalized["public_evidence"][0]["source"] == "LinkedIn"


def test_linkedin_api_failure_and_rate_limit_handled_gracefully():
    with patch.object(linkedin_adapter, "is_configured", return_value=True):
        # Simulate network failure
        with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
            results = linkedin_adapter.search_profiles("Data Engineer", ["Python", "SQL"])
            assert results == []

        # Simulate 429 rate-limit response
        mock_resp = MagicMock()
        mock_resp.status = 429
        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = linkedin_adapter.search_profiles("Data Engineer", ["Python", "SQL"])
            assert results == []


# =====================================================================
# 2. PUBLIC PROFILE NORMALIZATION & PII SANITIZATION
# =====================================================================
def test_public_profile_normalization_and_pii_sanitization():
    raw_profile = {
        "username": "coder_jane",
        "name": "Jane Coder",
        "headline": "Lead Engineer. Contact: jane.coder@company.org or +1-555-123-4567.",
        "location": "Berlin, Germany",
        "public_skills": ["Python", "FastAPI", "Docker"],
        "profile_url": "https://github.com/coder_jane",
        "repositories": [
            {
                "name": "fastapi-service",
                "url": "https://github.com/coder_jane/fastapi-service",
                "description": "FastAPI REST microservice with Docker containerization.",
                "languages": ["Python"],
                "topics": ["fastapi", "docker"],
            }
        ],
    }

    norm = normalize_public_profile(raw_profile)
    assert norm["name"] == "Jane Coder"
    assert "jane.coder@company.org" not in norm["headline"]
    assert "+1-555-123-4567" not in norm["headline"]
    assert norm["source"] == "GitHub"
    assert norm["source_type"] == "github_api"
    assert len(norm["repositories"]) == 1


# =====================================================================
# 3. RECRUITER SEARCH & EXPLAINABLE MATCHING FLOW
# =====================================================================
def test_recruiter_web_intelligence_search_flow():
    _clear_db()
    hr_headers, _ = _register_and_login_recruiter()

    jd_text = (
        "We are looking for a Python Backend Developer with experience in FastAPI, "
        "REST APIs, SQL, PostgreSQL, Docker, and Redis. Minimum 3 years experience."
    )

    response = client.post(
        "/intelligence/recruiter/search",
        headers=hr_headers,
        json={
            "job_title": "Python Backend Developer",
            "job_description": jd_text,
            "limit": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()

    # 1. Job Requirements extraction
    reqs = data["job_requirements"]
    assert reqs["role"] == "Python Backend Developer"
    assert "Python" in reqs["required_skills"] or "FastAPI" in reqs["required_skills"]
    assert len(reqs["role_keywords"]) > 0

    # 2. Public candidate profiles
    assert "profiles" in data
    assert len(data["profiles"]) > 0
    first_prof = data["profiles"][0]
    assert "name" in first_prof
    assert "headline" in first_prof
    assert "profile_url" in first_prof
    assert validate_source_url(first_prof["profile_url"])
    assert first_prof["source"] in {"GitHub", "Public Web", "LinkedIn"}

    # 3. GitHub results
    assert "github_results" in data
    assert len(data["github_results"]) > 0
    first_gh = data["github_results"][0]
    assert "username" in first_gh
    assert "profile_url" in first_gh
    assert len(first_gh["repositories"]) > 0

    # 4. Matching results & Explainability
    assert "matching_results" in data
    assert len(data["matching_results"]) > 0
    first_match = data["matching_results"][0]
    assert "profile" in first_match
    assert "matched_skills" in first_match
    assert "supporting_projects" in first_match
    assert "supporting_evidence" in first_match
    assert len(first_match["supporting_evidence"]) > 0
    assert "explanation" in first_match
    assert "source" in first_match
    assert first_match["match_score"] is not None

    # 5. Source Status Transparency
    assert "source_status" in data
    assert "linkedin" in data["source_status"]
    assert "github" in data["source_status"]
    assert "public_web" in data["source_status"]
    assert data["source_status"]["linkedin"]["status"] in {"not_configured", "available"}

    # 6. Compliance Notice
    assert "compliance_notice" in data
    assert "LinkedIn" in data["compliance_notice"]


# =====================================================================
# 4. CANDIDATE JOB DISCOVERY & MATCHING TESTS
# =====================================================================
def test_candidate_web_intelligence_job_search():
    _clear_db()
    cand_headers, _ = _register_and_login_candidate(name="Job Searcher", email="cand_jobs@example.com")

    response = client.post(
        "/intelligence/candidate/jobs/search",
        headers=cand_headers,
        json={"target_role": "Data Analyst", "limit": 6},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["target_role"] == "Data Analyst"
    assert len(data["expanded_keywords"]) >= 2
    assert len(data["jobs"]) > 0
    first_job = data["jobs"][0]
    assert "job_title" in first_job
    assert "company" in first_job
    assert "location" in first_job
    assert "required_skills" in first_job
    assert "job_url" in first_job
    assert validate_source_url(first_job["job_url"])


def test_candidate_web_intelligence_job_match_and_skill_demand():
    _clear_db()
    cand_headers, _ = _register_and_login_candidate(name="Match Cand", email="cand_match@example.com")
    resume_id = _upload_resume(
        cand_headers,
        "Alice Backend Developer. Experience with Python, FastAPI, PostgreSQL, SQL, REST API and Git. Built web APIs.",
    )

    response = client.post(
        "/intelligence/candidate/jobs/match",
        headers=cand_headers,
        json={
            "resume_id": resume_id,
            "target_role": "Backend Developer",
            "limit": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["resume_id"] == resume_id
    assert data["target_role"] == "Backend Developer"
    assert len(data["jobs"]) > 0

    first_matched_job = data["jobs"][0]
    assert "matched_skills" in first_matched_job
    assert "missing_skills" in first_matched_job
    assert "match_score" in first_matched_job
    assert "match_explanation" in first_matched_job

    # Observed skill demand aggregation
    assert len(data["observed_skill_demand"]) > 0
    top_skill = data["observed_skill_demand"][0]
    assert "skill" in top_skill
    assert "job_count" in top_skill
    assert data["market_summary_label"] == "Observed requirements in discovered jobs"


def test_candidate_github_intelligence():
    _clear_db()
    cand_headers, _ = _register_and_login_candidate(name="GH Cand", email="cand_github@example.com")

    response = client.post(
        "/intelligence/candidate/github",
        headers=cand_headers,
        json={"target_role": "Backend Developer"},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["target_role"] == "Backend Developer"
    assert len(data["projects"]) > 0
    assert len(data["technologies"]) > 0
    assert len(data["role_related_skills"]) > 0
    assert data["source"] == "GitHub"
    assert data["source_type"] == "github_api"


# =====================================================================
# 5. SECURITY & ACCESS ISOLATION TESTS
# =====================================================================
def test_web_intelligence_security_and_isolation():
    _clear_db()
    cand_headers1, _ = _register_and_login_candidate(name="Cand 1", email="cand1@example.com")
    cand_headers2, _ = _register_and_login_candidate(name="Cand 2", email="cand2@example.com")
    hr_headers, _ = _register_and_login_recruiter(company_name="Security Org", email="hr_sec@example.com")

    resume_id1 = _upload_resume(cand_headers1, "Candidate 1 text with Python and FastAPI.")

    # Unauthenticated requests rejected
    assert client.post("/intelligence/recruiter/search", json={"job_title": "Python Dev", "job_description": "We need FastAPI and Python backend engineers."}).status_code == 401
    assert client.post("/intelligence/candidate/jobs/search", json={"target_role": "Python Dev"}).status_code == 401

    # Candidate cannot access recruiter endpoint
    recruiter_access = client.post(
        "/intelligence/recruiter/search",
        headers=cand_headers1,
        json={"job_title": "Python Dev", "job_description": "We need FastAPI and Python backend engineers."},
    )
    assert recruiter_access.status_code in {403, 404}

    # Candidate 2 cannot match candidate 1's resume
    cross_match = client.post(
        "/intelligence/candidate/jobs/match",
        headers=cand_headers2,
        json={"resume_id": resume_id1, "target_role": "Backend Developer"},
    )
    assert cross_match.status_code == 404
