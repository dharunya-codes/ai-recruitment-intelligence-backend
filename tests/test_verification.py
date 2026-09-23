from __future__ import annotations

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
from app.models.verification import VerificationQuestion
from app.services.skill_verification_service import generate_verification_questions

client = TestClient(app)


def _clear_phase9_data() -> None:
    db = SessionLocal()
    try:
        db.query(VerificationQuestion).delete()
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


def _create_job(headers: dict[str, str], title: str = "Security Analyst") -> int:
    response = client.post(
        "/jobs",
        json={"title": title, "description": "Initial description"},
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


def _match(skill: str, importance: str, status: str) -> dict[str, object]:
    return {
        "requirement_id": 1,
        "requirement": skill,
        "category": "SKILL",
        "importance": importance,
        "match_status": status,
        "evidence_text": "Skills: " + skill if status != "MISSING" else None,
    }


def test_question_generation_rules_and_priorities() -> None:
    matches = [
        _match("Docker", "REQUIRED", "MISSING"),
        _match("Java", "REQUIRED", "WEAK"),
        _match("AWS", "PREFERRED", "WEAK"),
        _match("Azure", "PREFERRED", "MISSING"),
        _match("Python", "REQUIRED", "MATCHED"),
    ]
    questions = generate_verification_questions(matches, "Skills: Java and Python")

    assert [item["skill"] for item in questions] == ["Docker", "Java", "AWS"]
    assert [item["priority"] for item in questions] == ["HIGH", "MEDIUM", "LOW"]
    assert all("Azure" not in str(item) for item in questions)
    assert all("Python" not in str(item) for item in questions)


def test_question_generation_is_limited_to_five() -> None:
    matches = [_match(f"Skill {index}", "REQUIRED", "MISSING") for index in range(7)]
    assert len(generate_verification_questions(matches, "")) == 5


def test_generate_answer_status_and_resume_evidence_separation() -> None:
    _clear_phase9_data()
    headers = _register_and_login("verify@example.com", "Company A")
    job_id = _create_job(headers)
    jd = client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Java is required. Docker is required. AWS is preferred."},
        headers=headers,
    )
    assert jd.status_code == 200
    uploaded = _upload(job_id, headers, "John Doe\njohn@example.com\nSkills: Java")
    assert uploaded.status_code == 201
    resume_id = uploaded.json()["id"]

    before = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    generated = client.post(f"/verification/{resume_id}/generate", headers=headers)
    assert generated.status_code == 200
    questions = generated.json()
    assert {item["skill"] for item in questions} == {"Java", "Docker"}

    duplicate = client.post(f"/verification/{resume_id}/generate", headers=headers)
    assert duplicate.status_code == 200
    assert [item["id"] for item in duplicate.json()] == [item["id"] for item in questions]

    java_question = next(item for item in questions if item["skill"] == "Java")
    answer = client.post(
        f"/verification/questions/{java_question['id']}/answer",
        json={"answer": "I built a Java Student Management System."},
        headers=headers,
    )
    assert answer.status_code == 200
    answer_body = answer.json()
    assert answer_body["status"] == "ANSWERED"
    assert answer_body["evidence_status"] == "CANDIDATE_VERIFIED"
    assert "Java Student Management System" in answer_body["candidate_reported_evidence"]
    assert answer_body["resume_evidence_unchanged"] is True
    assert answer_body["resume_project_evidence"] is False

    after = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assert after["overall_match_score"] == before["overall_match_score"]
    assert after["required_score"] == before["required_score"]
    assert next(item for item in after["weak_requirements"] if item["requirement"] == "Java")["match_status"] == "WEAK"

    verification_status = client.get(f"/verification/{resume_id}/status", headers=headers)
    assert verification_status.status_code == 200
    assert verification_status.json()["answered"] == 1
    assert verification_status.json()["pending"] == 1


def test_empty_answer_has_no_supporting_evidence() -> None:
    _clear_phase9_data()
    headers = _register_and_login("empty-answer@example.com", "Company A")
    job_id = _create_job(headers)
    client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Docker is required."},
        headers=headers,
    )
    resume = _upload(job_id, headers, "Candidate\ncandidate@example.com\nResume text")
    question = client.post(f"/verification/{resume.json()['id']}/generate", headers=headers).json()[0]

    response = client.post(
        f"/verification/questions/{question['id']}/answer",
        json={"answer": "I have some familiarity."},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ANSWERED"
    assert response.json()["evidence_status"] == "NO_SUPPORTING_EVIDENCE"
    assert response.json()["candidate_reported_evidence"] is None


def test_verification_ownership_and_authentication() -> None:
    _clear_phase9_data()
    company_a_headers = _register_and_login("verify-a@example.com", "Company A")
    company_b_headers = _register_and_login("verify-b@example.com", "Company B")
    job_id = _create_job(company_b_headers)
    client.post(
        f"/jobs/{job_id}/jd",
        json={"description": "Docker is required."},
        headers=company_b_headers,
    )
    resume = _upload(job_id, company_b_headers, "Company B\nb@example.com\nResume")
    resume_id = resume.json()["id"]
    generated = client.post(f"/verification/{resume_id}/generate", headers=company_b_headers)
    question_id = generated.json()[0]["id"]

    assert client.post(f"/verification/{resume_id}/generate", headers=company_a_headers).status_code == 404
    assert client.get(f"/verification/{resume_id}/questions", headers=company_a_headers).status_code == 404
    assert client.get(f"/verification/{resume_id}/status", headers=company_a_headers).status_code == 404
    assert client.post(
        f"/verification/questions/{question_id}/answer",
        json={"answer": "I built a Docker application."},
        headers=company_a_headers,
    ).status_code == 404
    assert client.post(f"/verification/{resume_id}/generate").status_code == 401
    assert client.get(f"/verification/{resume_id}/questions").status_code == 401
    assert client.post(
        f"/verification/questions/{question_id}/answer",
        json={"answer": "I built a Docker application."},
    ).status_code == 401
