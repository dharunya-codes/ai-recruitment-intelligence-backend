from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.report import Report
from tests.test_assessment import _clear_phase10_data, _register_and_login, _setup_job_and_resume
from tests.test_candidate_auth import _pdf_bytes


client = TestClient(app)


def _clear() -> None:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def _candidate(email: str) -> dict[str, str]:
    response = client.post(
        "/candidate/auth/register",
        json={"name": "Candidate", "email": email, "password": "StrongPassword123"},
    )
    assert response.status_code == 200
    token = client.post(
        "/candidate/auth/login",
        json={"email": email, "password": "StrongPassword123"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_invalid_and_missing_tokens_are_rejected() -> None:
    _clear()
    assert client.get("/candidate/resumes").status_code == 401
    assert client.get("/candidate/resumes", headers={"Authorization": "Bearer malformed"}).status_code == 401


def test_candidate_cannot_use_company_endpoints_or_access_other_candidate_data() -> None:
    _clear()
    first = _candidate("hardening-a@example.com")
    second = _candidate("hardening-b@example.com")
    upload = client.post(
        "/candidate/resumes",
        files={"file": ("..\\private.pdf", _pdf_bytes("Python project"), "application/pdf")},
        headers=first,
    )
    assert upload.status_code == 201
    resume_id = upload.json()["id"]
    assert client.get(f"/candidate/resumes/{resume_id}", headers=second).status_code == 404
    assert client.get("/jobs", headers=first).status_code == 404
    assert client.get(f"/reports/{resume_id}", headers=second).status_code == 404


def test_company_registration_rejects_candidate_role_and_companyless_user() -> None:
    _clear()
    assert client.post(
        "/auth/register",
        json={
            "name": "Bad Role",
            "email": "bad-role@example.com",
            "password": "StrongPassword123",
            "role": "CANDIDATE",
            "company_name": "Company",
        },
    ).status_code == 422
    assert client.post(
        "/auth/register",
        json={
            "name": "No Company",
            "email": "no-company@example.com",
            "password": "StrongPassword123",
            "role": "HR",
        },
    ).status_code == 422


def test_company_cross_tenant_job_access_is_not_exposed() -> None:
    _clear()
    company_a = _register_and_login("hardening-company-a@example.com", "Hardening A")
    company_b = _register_and_login("hardening-company-b@example.com", "Hardening B")
    job = client.post("/jobs", json={"title": "Private Role", "description": "Private description"}, headers=company_b)
    assert job.status_code == 201
    job_id = job.json()["id"]
    assert client.get(f"/jobs/{job_id}", headers=company_a).status_code == 404
    assert client.put(f"/jobs/{job_id}", json={"title": "Changed"}, headers=company_a).status_code == 404
    assert client.delete(f"/jobs/{job_id}", headers=company_a).status_code == 404
    assert client.get(f"/jobs/{job_id}/requirements", headers=company_a).status_code == 404