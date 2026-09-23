from __future__ import annotations

from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.company import Company
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.user import User
from app.services.jd_parser import parse_jd
from app.services.requirement_extractor import extract_requirements

client = TestClient(app)


def _clear_phase5_data() -> None:
    db = SessionLocal()
    try:
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


def _create_job(headers: dict[str, str], title: str = "Security Analyst") -> int:
    response = client.post(
        "/jobs",
        json={
            "title": title,
            "description": "Initial job description",
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_submit_jd_updates_job_and_creates_requirements() -> None:
    _clear_phase5_data()
    headers = _register_and_login("jd-submit@example.com", "Company A")
    job_id = _create_job(headers)
    description = "Looking for a Cyber Security Analyst with Python, SIEM and Linux knowledge."

    response = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": description},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["job_id"] == job_id
    assert {item["requirement"] for item in response.json()["requirements"]} >= {
        "Python",
        "SIEM",
        "Linux",
    }

    job = client.get(f"/jobs/{job_id}", headers=headers)
    assert job.json()["description"] == description


def test_extractor_covers_skills_experience_education_and_certification() -> None:
    text = parse_jd(
        "Looking for a Cyber Security Analyst with Python, Linux, SIEM and Network Security. "
        "Candidates should have 0-2 years of experience. Security+ certification is preferred. "
        "B.Tech in Computer Science or Cyber Security preferred."
    )

    extracted = extract_requirements(text)
    by_category = {
        category: {item["requirement"] for item in extracted if item["category"] == category}
        for category in {item["category"] for item in extracted}
    }

    assert {"Python", "Linux", "SIEM", "Network Security"} <= by_category["SKILL"]
    assert "0-2 years of experience" in by_category["EXPERIENCE"]
    assert {"B.Tech", "Computer Science", "Cyber Security"} <= by_category["EDUCATION"]
    assert "Security+" in by_category["CERTIFICATION"]
    assert next(
        item for item in extracted if item["requirement"] == "Security+"
    )["importance"] == "PREFERRED"


def test_duplicate_requirements_are_stored_once() -> None:
    _clear_phase5_data()
    headers = _register_and_login("jd-duplicate@example.com", "Company A")
    job_id = _create_job(headers)

    response = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Python is required. Python experience is preferred. Python skills are essential."},
        headers=headers,
    )

    assert response.status_code == 200
    python_requirements = [
        item for item in response.json()["requirements"] if item["requirement"] == "Python"
    ]
    assert len(python_requirements) == 1


def test_submitting_new_jd_replaces_old_requirements() -> None:
    _clear_phase5_data()
    headers = _register_and_login("jd-replace@example.com", "Company A")
    job_id = _create_job(headers)

    first = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Python and Linux are required."},
        headers=headers,
    )
    assert first.status_code == 200

    second = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "AWS and Docker are required."},
        headers=headers,
    )
    assert second.status_code == 200
    requirements = {item["requirement"] for item in second.json()["requirements"]}
    assert "AWS" in requirements
    assert "Docker" in requirements
    assert "Python" not in requirements
    assert "Linux" not in requirements


def test_get_requirements_and_cross_company_protection() -> None:
    _clear_phase5_data()
    company_a_headers = _register_and_login("jd-access-a@example.com", "Company A")
    company_b_headers = _register_and_login("jd-access-b@example.com", "Company B")
    company_a_job_id = _create_job(company_a_headers)
    company_b_job_id = _create_job(company_b_headers)

    submitted = client.post(
        f"/jobs/{company_b_job_id}/jd",
        json={"description": "PostgreSQL and AWS are required."},
        headers=company_b_headers,
    )
    assert submitted.status_code == 200

    own_requirements = client.get(
        f"/jobs/{company_a_job_id}/requirements", headers=company_a_headers
    )
    assert own_requirements.status_code == 200
    assert own_requirements.json() == {"job_id": company_a_job_id, "requirements": []}

    assert client.post(
        f"/jobs/{company_b_job_id}/jd",
        json={"description": "Tampered JD content that is long enough."},
        headers=company_a_headers,
    ).status_code == 404
    assert client.get(
        f"/jobs/{company_b_job_id}/requirements", headers=company_a_headers
    ).status_code == 404


def test_jd_requires_authentication_and_non_empty_description() -> None:
    _clear_phase5_data()
    assert client.post("/jobs/1/jd", json={"description": "A valid enough description"}).status_code == 401

    headers = _register_and_login("jd-validation@example.com", "Company A")
    job_id = _create_job(headers)
    assert client.post(
        f"/jobs/{job_id}/jd",
        json={"description": ""},
        headers=headers,
    ).status_code == 422
