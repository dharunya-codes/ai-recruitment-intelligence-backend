from __future__ import annotations

from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.company import Company
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User

client = TestClient(app)


def _clear_phase4_data() -> None:
    db = SessionLocal()
    try:
        db.query(CandidateAnswer).delete()
        db.query(AssessmentQuestion).delete()
        db.query(Assessment).delete()
        db.query(JobRequirement).delete()
        db.query(Resume).delete()
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


def _job_payload(title: str = "Cyber Security Analyst") -> dict[str, str]:
    return {
        "title": title,
        "department": "Cyber Security",
        "location": "Chennai",
        "employment_type": "Full-time",
        "description": "Looking for a Cyber Security Analyst.",
        "minimum_experience": "0-2 years",
        "education": "B.Tech / B.E.",
        "certifications": "Security+ preferred",
    }


def test_create_job_assigns_authenticated_company() -> None:
    _clear_phase4_data()
    headers = _register_and_login("phase4-create@example.com", "Company A")

    response = client.post("/jobs", json=_job_payload(), headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Cyber Security Analyst"
    assert body["company_id"] == 1


def test_list_jobs_returns_only_authenticated_company_jobs() -> None:
    _clear_phase4_data()
    company_a_headers = _register_and_login("phase4-list-a@example.com", "Company A")
    company_b_headers = _register_and_login("phase4-list-b@example.com", "Company B")

    client.post("/jobs", json=_job_payload("Company A Job"), headers=company_a_headers)
    client.post("/jobs", json=_job_payload("Company B Job"), headers=company_b_headers)

    response = client.get("/jobs", headers=company_a_headers)

    assert response.status_code == 200
    assert [job["title"] for job in response.json()] == ["Company A Job"]


def test_get_update_and_delete_own_job() -> None:
    _clear_phase4_data()
    headers = _register_and_login("phase4-crud@example.com", "Company A")
    created = client.post("/jobs", json=_job_payload(), headers=headers)
    job_id = created.json()["id"]

    fetched = client.get(f"/jobs/{job_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == job_id

    updated = client.put(
        f"/jobs/{job_id}",
        json={"title": "Senior Cyber Security Analyst"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Senior Cyber Security Analyst"

    deleted = client.delete(f"/jobs/{job_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json() == {"message": "Job deleted successfully"}
    assert client.get(f"/jobs/{job_id}", headers=headers).status_code == 404


def test_cross_company_job_access_returns_not_found() -> None:
    _clear_phase4_data()
    company_a_headers = _register_and_login("phase4-cross-a@example.com", "Company A")
    company_b_headers = _register_and_login("phase4-cross-b@example.com", "Company B")
    company_b_job = client.post(
        "/jobs", json=_job_payload("Company B Job"), headers=company_b_headers
    )
    job_id = company_b_job.json()["id"]

    assert client.get(f"/jobs/{job_id}", headers=company_a_headers).status_code == 404
    assert (
        client.put(
            f"/jobs/{job_id}",
            json={"title": "Tampered Job"},
            headers=company_a_headers,
        ).status_code
        == 404
    )
    assert client.delete(f"/jobs/{job_id}", headers=company_a_headers).status_code == 404


def test_jobs_require_authentication_and_validate_required_fields() -> None:
    _clear_phase4_data()

    unauthenticated = client.get("/jobs")
    assert unauthenticated.status_code == 401

    headers = _register_and_login("phase4-validation@example.com", "Company A")
    invalid = client.post(
        "/jobs",
        json={"title": "", "description": ""},
        headers=headers,
    )
    assert invalid.status_code == 422


def test_get_my_company_returns_authenticated_company() -> None:
    _clear_phase4_data()
    headers = _register_and_login("phase4-company@example.com", "Example Technologies")

    response = client.get("/companies/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Example Technologies"
    assert response.json()["email"] == "phase4-company@example.com"
