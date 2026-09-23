from __future__ import annotations

import fitz
from fastapi.testclient import TestClient

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
from app.services.web_intelligence.base_source import BaseJobSource
from app.services.web_intelligence.normalizer import normalize_external_candidate, normalize_external_job
from app.services.web_intelligence.source_manager import SourceManager

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


def _register_and_login_candidate(name: str, email: str) -> tuple[dict[str, str], int]:
    client.post("/candidate/auth/register", json={"name": name, "email": email, "password": "StrongPassword123"})
    login = client.post("/candidate/auth/login", json={"email": email, "password": "StrongPassword123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, login.json()


def _register_and_login_hr(email: str, company_name: str) -> tuple[dict[str, str], int]:
    client.post(
        "/auth/register",
        json={"name": "HR Manager", "email": email, "password": "StrongPassword123", "role": "HR", "company_name": company_name},
    )
    login = client.post("/auth/login", json={"email": email, "password": "StrongPassword123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, login.json()


def test_unauthenticated_requests_rejected() -> None:
    _clear_db()
    # Unauthenticated job search
    assert client.post("/candidate/web-intelligence/jobs/search", json={"query": "Python"}).status_code == 401

    # Unauthenticated job comparison
    assert client.post(
        "/candidate/web-intelligence/jobs/compare",
        json={"resume_id": 1, "job_title": "Python Developer", "job_description": "Python, SQL"},
    ).status_code == 401

    # Unauthenticated candidate discovery
    assert client.post("/jobs/1/candidate-discovery", json={}).status_code == 401


def test_candidate_job_search_and_validation() -> None:
    _clear_db()
    headers, _ = _register_and_login_candidate("Candidate One", "cand1@example.com")

    # Valid search
    resp = client.post(
        "/candidate/web-intelligence/jobs/search",
        json={"query": "Python Developer", "location": "Coimbatore", "limit": 5},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "Python Developer"
    assert data["location"] == "Coimbatore"
    assert data["total_results"] >= 1
    first_job = data["results"][0]
    assert first_job["source"] == "MOCK_PUBLIC_JOB_SOURCE"
    assert "Python" in first_job["title"]
    assert "skills" in first_job
    assert "url" in first_job

    # Invalid empty query
    empty_resp = client.post(
        "/candidate/web-intelligence/jobs/search",
        json={"query": "", "limit": 5},
        headers=headers,
    )
    assert empty_resp.status_code == 422

    # Invalid oversized query
    long_resp = client.post(
        "/candidate/web-intelligence/jobs/search",
        json={"query": "A" * 150, "limit": 5},
        headers=headers,
    )
    assert long_resp.status_code == 422

    # Limit bounding
    bounded_resp = client.post(
        "/candidate/web-intelligence/jobs/search",
        json={"query": "Developer", "limit": 2},
        headers=headers,
    )
    assert bounded_resp.status_code == 200
    assert len(bounded_resp.json()["results"]) <= 2


def test_candidate_job_comparison_and_isolation() -> None:
    _clear_db()

    # Candidate A
    headers_a, _ = _register_and_login_candidate("Alice", "alice@example.com")
    resume_a_text = """
    Alice Software Developer
    Email: alice@example.com
    Summary: Software Developer with project experience in Python, SQL, REST API, Git, and Docker.
    Experience:
    - Software Engineer: Worked on Python backend services and designed SQL database schemas.
    Projects:
    - Backend Microservice: Built and developed REST API services using Python and Docker with SQL databases.
    """
    upload_a = client.post(
        "/candidate/resumes",
        files={"file": ("alice_resume.pdf", _pdf_bytes(resume_a_text), "application/pdf")},
        headers=headers_a,
    )
    resume_id_a = upload_a.json()["id"]

    # Candidate B
    headers_b, _ = _register_and_login_candidate("Bob", "bob@example.com")

    # Compare Candidate A's resume against discovered job
    job_desc = "We need a Senior Python Developer with Python, REST API, SQL, Docker, and Kubernetes experience."
    comp_resp = client.post(
        "/candidate/web-intelligence/jobs/compare",
        json={
            "resume_id": resume_id_a,
            "job_title": "Senior Python Developer",
            "job_description": job_desc,
            "job_source_url": "https://demo-public-jobs.halo.local/jobs/101",
        },
        headers=headers_a,
    )
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert comp_data["resume_id"] == resume_id_a
    assert comp_data["job_title"] == "Senior Python Developer"
    assert comp_data["match_score"] is not None
    assert "Python" in comp_data["strong_skills"]
    assert "Kubernetes" in comp_data["missing_skills"]
    assert "score_breakdown" in comp_data
    assert "evidence" in comp_data
    assert "improvement_suggestions" in comp_data

    # Candidate isolation: Candidate B cannot compare Candidate A's resume
    isolated_resp = client.post(
        "/candidate/web-intelligence/jobs/compare",
        json={
            "resume_id": resume_id_a,
            "job_title": "Senior Python Developer",
            "job_description": job_desc,
        },
        headers=headers_b,
    )
    assert isolated_resp.status_code == 404

    # Verify original resume was not altered
    get_resume = client.get(f"/candidate/resumes/{resume_id_a}", headers=headers_a)
    assert get_resume.status_code == 200
    assert get_resume.json()["id"] == resume_id_a


def test_recruiter_candidate_discovery_and_isolation() -> None:
    _clear_db()

    # Company 1
    headers_hr1, _ = _register_and_login_hr("hr1@company1.com", "Company One")
    job_resp1 = client.post("/jobs", json={"title": "Cyber Security Engineer", "description": "Security role"}, headers=headers_hr1)
    job_id_1 = job_resp1.json()["id"]
    client.post(
        f"/jobs/{job_id_1}/jd",
        json={"description": "Required: Linux, Networking, Cyber Security, SIEM, Python. Preferred: Incident Response."},
        headers=headers_hr1,
    )

    # Company 2
    headers_hr2, _ = _register_and_login_hr("hr2@company2.com", "Company Two")

    # Run discovery for Company 1 Job
    disc_resp = client.post(
        f"/jobs/{job_id_1}/candidate-discovery",
        json={"location": "India", "skills_filter": ["Linux", "SIEM", "Python"], "limit": 5},
        headers=headers_hr1,
    )
    assert disc_resp.status_code == 200
    disc_data = disc_resp.json()
    assert disc_data["job_id"] == job_id_1
    assert disc_data["candidates_count"] >= 1
    cand1 = disc_data["results"][0]
    assert cand1["source"] == "MOCK_PUBLIC_CANDIDATE_SOURCE"
    assert "match_analysis" in cand1
    assert "Linux" in cand1["match_analysis"]["matched_requirements"]
    assert cand1["match_analysis"]["match_score"] is not None
    assert cand1["match_analysis"]["public_evidence_summary"] is not None

    # Isolation: Company 2 HR cannot run discovery on Company 1 Job
    unauth_disc = client.post(
        f"/jobs/{job_id_1}/candidate-discovery",
        json={"limit": 5},
        headers=headers_hr2,
    )
    assert unauth_disc.status_code == 404


def test_normalizer_and_privacy_sanitizer() -> None:
    raw_job = {
        "source_id": "job_custom_99",
        "job_title": "Lead Software Architect",
        "company_name": "Innovate Ltd",
        "city": "Remote",
        "job_description": "Python, AWS, and Docker lead developer position.",
    }
    normalized_job = normalize_external_job(raw_job)
    assert normalized_job.id == "job_custom_99"
    assert normalized_job.title == "Lead Software Architect"
    assert normalized_job.company == "Innovate Ltd"
    assert "Python" in normalized_job.skills

    # Candidate privacy normalization (stripping private emails and phone numbers)
    raw_cand = {
        "id": "cand_custom_88",
        "name": "Jane Public",
        "headline": "Fullstack Developer. Reach me at secret.email@domain.com or (555) 123-4567",
        "public_skills": ["Python", "JavaScript"],
        "email": "should_be_stripped@domain.com",
        "phone": "+1 555-987-6543",
    }
    normalized_cand = normalize_external_candidate(raw_cand)
    assert normalized_cand.source_id == "cand_custom_88"
    assert "secret.email@domain.com" not in normalized_cand.headline
    assert "[REDACTED_EMAIL]" in normalized_cand.headline
    assert "[REDACTED_PHONE]" in normalized_cand.headline
    assert not hasattr(normalized_cand, "email")
    assert not hasattr(normalized_cand, "phone")


def test_source_manager_failure_isolation() -> None:
    class FailingJobSource(BaseJobSource):
        @property
        def source_name(self) -> str:
            return "PUBLIC_TECH_CAREERS"

        def is_enabled(self) -> bool:
            return True

        def search_jobs(self, query: str, location: str | None = None, company: str | None = None, limit: int = 10):
            raise ConnectionError("Simulated remote source network error")

    sm = SourceManager()
    sm.register_job_source(FailingJobSource())

    # Search should still succeed by using working mock source despite failing source
    results = sm.search_jobs("Python Developer")
    assert len(results) >= 1
    assert results[0].title == "Python Developer"


def test_web_search_caching() -> None:
    _clear_db()
    headers, _ = _register_and_login_candidate("Cache Candidate", "cache_cand@example.com")

    resp1 = client.post("/candidate/web-intelligence/jobs/search", json={"query": "Python Developer", "limit": 5}, headers=headers)
    assert resp1.status_code == 200

    resp2 = client.post("/candidate/web-intelligence/jobs/search", json={"query": "Python Developer", "limit": 5}, headers=headers)
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()
    assert analysis_cache.stats()["hits"] >= 1
