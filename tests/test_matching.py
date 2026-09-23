from __future__ import annotations

from io import BytesIO
from types import SimpleNamespace

import fitz
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.services.matching_engine import match_resume_to_requirements
from app.services.skill_extractor import extract_skills

client = TestClient(app)


def _clear_phase7_data() -> None:
    db = SessionLocal()
    try:
        db.query(Resume).delete()
        db.query(Candidate).delete()
        db.query(JobRequirement).delete()
        db.query(Job).delete()
        db.query(User).delete()
        db.query(Company).delete()
        db.commit()
    finally:
        db.close()


def _register_and_login(email: str, company_name: str) -> dict[str, str]:
    registration = client.post(
        "/auth/register",
        json={
            "name": "Company User",
            "email": email,
            "password": "StrongPassword123",
            "role": "HR",
            "company_name": company_name,
        },
    )
    assert registration.status_code == 200
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "StrongPassword123"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _create_job(headers: dict[str, str]) -> int:
    response = client.post(
        "/jobs",
        json={"title": "Security Analyst", "description": "Initial description"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _upload(job_id: int, headers: dict[str, str], text: str):
    return client.post(
        f"/jobs/{job_id}/resumes",
        files={"file": ("candidate.pdf", _pdf_bytes(text), "application/pdf")},
        headers=headers,
    )


def _single_match(requirement: str, category: str, resume: str) -> dict[str, object]:
    row = SimpleNamespace(
        id=1,
        requirement=requirement,
        category=category,
        importance="REQUIRED",
    )
    return match_resume_to_requirements(resume, [row])[0]


def test_skill_extraction_returns_canonical_skills() -> None:
    assert extract_skills("Developed Python and Flask applications using SQL and Linux.") == [
        "Python",
        "Flask",
        "SQL",
        "Linux",
    ]
    assert "Cyber Security" in extract_skills("Worked in cybersecurity operations.")
    assert "JavaScript" in extract_skills("Built a JS frontend.")
    assert "Node.js" in extract_skills("Worked with NodeJS services.")


def test_exact_skill_match_and_evidence() -> None:
    result = _single_match("Python", "SKILL", "Developed automation tools using Python.")
    assert result["match_status"] == "MATCHED"
    assert "Python" in result["evidence_text"]

    project = _single_match(
        "Python",
        "SKILL",
        "Projects:\nBuilt a Flask web application using Python and SQLite.",
    )
    assert project["match_status"] == "MATCHED"
    assert "Built a Flask web application" in project["evidence_text"]


def test_weak_and_missing_skill_matches_are_distinguished() -> None:
    assert _single_match("Java", "SKILL", "Skills: Java")["match_status"] == "WEAK"
    assert _single_match("Docker", "SKILL", "Developed Python applications.")["match_status"] == "MISSING"
    assert _single_match("Java", "SKILL", "Developed applications using JavaScript.")["match_status"] == "MISSING"
    assert _single_match("C", "SKILL", "Created web applications using HTML and CSS.")["match_status"] == "MISSING"


def test_education_certification_and_responsibility_matching() -> None:
    education = _single_match("B.Tech", "EDUCATION", "Education: B.Tech Computer Engineering.")
    certification = _single_match("Security+", "CERTIFICATION", "Certifications: CompTIA Security+")
    responsibility = _single_match(
        "Monitor SIEM alerts and investigate security incidents",
        "RESPONSIBILITY",
        "Worked in a SOC environment monitoring SIEM alerts and investigating security incidents.",
    )
    assert education["match_status"] == "MATCHED"
    assert certification["match_status"] == "MATCHED"
    assert responsibility["match_status"] == "MATCHED"


def test_full_analysis_returns_skill_gaps_without_score() -> None:
    _clear_phase7_data()
    headers = _register_and_login("analysis@example.com", "Company A")
    job_id = _create_job(headers)
    jd = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Python and SQL are required. Docker is required. Security+ certification is required."},
        headers=headers,
    )
    assert jd.status_code == 200

    uploaded = _upload(
        job_id,
        headers,
        "John Doe\njohn@example.com\nProjects:\nBuilt Python and SQL applications.\nCertifications: CompTIA Security+",
    )
    assert uploaded.status_code == 201
    resume_id = uploaded.json()["id"]

    response = client.get(f"/resumes/{resume_id}/analysis", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_name"] == "John Doe"
    assert "Python" in body["detected_skills"]
    matched = {item["requirement"] for item in body["matched_requirements"]}
    missing = {item["requirement"] for item in body["missing_requirements"]}
    assert {"Python", "SQL", "Security+"} <= matched
    assert "Docker" in missing
    assert "match_score" not in body
    assert body["overall_match_score"] == 75.0
    assert body["required_score"] == 75.0
    assert body["score_status"] == "CALCULATED"
    assert body["counts"] == {"matched": 3, "weak": 0, "missing": 1, "total": 4}
    assert "SKILL" in body["category_breakdown"]
    assert len(body["requirement_analysis"]) == 4
    assert body["skill_gap"]["missing_requirements"][0]["requirement"] == "Docker"


def test_analysis_cross_company_and_unauthenticated_access_are_blocked() -> None:
    _clear_phase7_data()
    company_a_headers = _register_and_login("analysis-a@example.com", "Company A")
    company_b_headers = _register_and_login("analysis-b@example.com", "Company B")
    company_b_job_id = _create_job(company_b_headers)
    client.post(
        f"/jobs/{company_b_job_id}/jd",
        json={"description": "Python is required."},
        headers=company_b_headers,
    )
    uploaded = _upload(company_b_job_id, company_b_headers, "Company B Candidate\nb@example.com\nPython project")
    resume_id = uploaded.json()["id"]

    assert client.get(f"/resumes/{resume_id}/analysis", headers=company_a_headers).status_code == 404
    assert client.get(f"/resumes/{resume_id}/analysis").status_code == 401
