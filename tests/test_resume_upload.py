from __future__ import annotations

from io import BytesIO

import fitz
from docx import Document
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User

client = TestClient(app)


def _clear_phase6_data() -> None:
    db = SessionLocal()
    try:
        db.query(Resume).delete()
        db.query(Candidate).delete()
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
        json={"title": "Security Analyst", "description": "Resume upload job"},
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


def _docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def _upload(job_id: int, headers: dict[str, str], filename: str, content: bytes, content_type: str):
    return client.post(
        f"/jobs/{job_id}/resumes",
        files={"file": (filename, content, content_type)},
        headers=headers,
    )


def test_pdf_upload_extracts_text_and_candidate_information() -> None:
    _clear_phase6_data()
    headers = _register_and_login("resume-pdf@example.com", "Company A")
    job_id = _create_job(headers)

    response = _upload(
        job_id,
        headers,
        "john_resume.pdf",
        _pdf_bytes("John Doe\njohn.doe@gmail.com\n+91 9876543210\nPython Developer"),
        "application/pdf",
    )

    assert response.status_code == 201
    body = response.json()
    assert body["file_name"] == "john_resume.pdf"
    assert body["candidate_name"] == "John Doe"
    assert body["candidate_email"] == "john.doe@gmail.com"
    assert "9876543210" in body["candidate_phone"]

    text_response = client.get(f"/resumes/{body['id']}/text", headers=headers)
    assert text_response.status_code == 200
    assert "Python Developer" in text_response.json()["extracted_text"]


def test_docx_upload_extracts_text() -> None:
    _clear_phase6_data()
    headers = _register_and_login("resume-docx@example.com", "Company A")
    job_id = _create_job(headers)

    response = _upload(
        job_id,
        headers,
        "candidate.docx",
        _docx_bytes("Jane Doe\njane.doe@example.com\nData Analyst"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert response.status_code == 201
    assert response.json()["candidate_name"] == "Jane Doe"
    text_response = client.get(f"/resumes/{response.json()['id']}/text", headers=headers)
    assert "Data Analyst" in text_response.json()["extracted_text"]


def test_same_email_reuses_candidate_for_multiple_resumes() -> None:
    _clear_phase6_data()
    headers = _register_and_login("resume-dedupe@example.com", "Company A")
    job_id = _create_job(headers)
    first = _upload(
        job_id,
        headers,
        "first.pdf",
        _pdf_bytes("John Doe\njohn@example.com\nPython"),
        "application/pdf",
    )
    second = _upload(
        job_id,
        headers,
        "second.docx",
        _docx_bytes("John Doe\njohn@example.com\nJava"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["candidate_id"] == second.json()["candidate_id"]
    assert first.json()["id"] != second.json()["id"]


def test_resume_validation_rejects_unsupported_oversized_and_empty_files() -> None:
    _clear_phase6_data()
    headers = _register_and_login("resume-validation@example.com", "Company A")
    job_id = _create_job(headers)

    unsupported = _upload(job_id, headers, "resume.txt", b"plain text", "text/plain")
    assert unsupported.status_code in {400, 422}

    oversized = _upload(job_id, headers, "large.pdf", b"%PDF" + b"x" * (10 * 1024 * 1024), "application/pdf")
    assert oversized.status_code == 413

    empty_pdf = _upload(job_id, headers, "empty.pdf", _pdf_bytes(""), "application/pdf")
    assert empty_pdf.status_code == 400
    assert "Could not extract" in empty_pdf.json()["detail"]


def test_list_and_get_resume_metadata() -> None:
    _clear_phase6_data()
    headers = _register_and_login("resume-list@example.com", "Company A")
    job_id = _create_job(headers)
    uploaded = _upload(
        job_id,
        headers,
        "candidate.pdf",
        _pdf_bytes("Candidate One\ncandidate@example.com\n+91 9876543210"),
        "application/pdf",
    )
    resume_id = uploaded.json()["id"]

    listed = client.get(f"/jobs/{job_id}/resumes", headers=headers)
    fetched = client.get(f"/resumes/{resume_id}", headers=headers)
    assert listed.status_code == 200
    assert fetched.status_code == 200
    assert listed.json()[0]["id"] == resume_id
    assert "extracted_text" not in fetched.json()


def test_cross_company_resume_access_returns_not_found() -> None:
    _clear_phase6_data()
    company_a_headers = _register_and_login("resume-a@example.com", "Company A")
    company_b_headers = _register_and_login("resume-b@example.com", "Company B")
    company_b_job_id = _create_job(company_b_headers)
    uploaded = _upload(
        company_b_job_id,
        company_b_headers,
        "company-b.pdf",
        _pdf_bytes("Company B Candidate\nb@example.com\nPython"),
        "application/pdf",
    )
    resume_id = uploaded.json()["id"]

    assert _upload(
        company_b_job_id,
        company_a_headers,
        "tampered.pdf",
        _pdf_bytes("Tampered Candidate\ntampered@example.com"),
        "application/pdf",
    ).status_code == 404
    assert client.get(f"/jobs/{company_b_job_id}/resumes", headers=company_a_headers).status_code == 404
    assert client.get(f"/resumes/{resume_id}", headers=company_a_headers).status_code == 404
    assert client.get(f"/resumes/{resume_id}/text", headers=company_a_headers).status_code == 404


def test_resume_upload_requires_authentication() -> None:
    _clear_phase6_data()
    assert _upload(1, {}, "resume.pdf", _pdf_bytes("Candidate One"), "application/pdf").status_code == 401
