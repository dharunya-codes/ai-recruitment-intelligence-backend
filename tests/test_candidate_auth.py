import fitz
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.report import Report
from tests.test_assessment import _clear_phase10_data


client = TestClient(app)


def _clear() -> None:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _register(email: str) -> dict[str, str]:
    response = client.post("/candidate/auth/register", json={"name": "Candidate User", "email": email, "password": "StrongPassword123"})
    assert response.status_code == 200
    token = client.post("/candidate/auth/login", json={"email": email, "password": "StrongPassword123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_candidate_registration_login_profile_and_duplicate_email() -> None:
    _clear()
    headers = _register("candidate-auth@example.com")
    duplicate = client.post("/candidate/auth/register", json={"name": "Another Candidate", "email": "candidate-auth@example.com", "password": "StrongPassword123"})
    assert duplicate.status_code == 400
    profile = client.get("/candidate/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["role"] == "CANDIDATE"
    assert profile.json()["email"] == "candidate-auth@example.com"
    assert client.get("/auth/me", headers=headers).json()["company_id"] is None
    assert client.post("/candidate/auth/login", json={"email": "candidate-auth@example.com", "password": "WrongPassword123"}).status_code == 401


def test_candidate_resume_ownership_and_upload_validation() -> None:
    _clear()
    own = _register("candidate-own@example.com")
    other = _register("candidate-other@example.com")
    upload = client.post("/candidate/resumes", files={"file": ("resume.pdf", _pdf_bytes("Candidate Python project"), "application/pdf")}, headers=own)
    assert upload.status_code == 201
    resume_id = upload.json()["id"]
    assert client.get(f"/candidate/resumes/{resume_id}", headers=own).status_code == 200
    assert client.get(f"/candidate/resumes/{resume_id}", headers=other).status_code == 404
    assert client.get("/candidate/resumes").status_code == 401
    assert client.post("/candidate/resumes", files={"file": ("resume.txt", b"invalid", "text/plain")}, headers=own).status_code == 400