from __future__ import annotations

import fitz
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.job import Job
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.models.verification import VerificationQuestion

client = TestClient(app)


def _clear_phase10_data() -> None:
    db = SessionLocal()
    try:
        db.query(CandidateAnswer).delete()
        db.query(AssessmentQuestion).delete()
        db.query(Assessment).delete()
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


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _setup_job_and_resume(headers: dict[str, str], jd: str, resume_text: str) -> tuple[int, int]:
    job = client.post(
        "/jobs",
        json={"title": "Cyber Security Analyst", "description": "Initial"},
        headers=headers,
    )
    assert job.status_code == 201
    job_id = job.json()["id"]
    jd_response = client.post(f"/jobs/{job_id}/jd", json={"description": jd}, headers=headers)
    assert jd_response.status_code == 200
    resume = client.post(
        f"/jobs/{job_id}/resumes",
        files={"file": ("candidate.pdf", _pdf_bytes(resume_text), "application/pdf")},
        headers=headers,
    )
    assert resume.status_code == 201
    return job_id, resume.json()["id"]


def test_cyber_security_assessment_is_role_specific() -> None:
    _clear_phase10_data()
    headers = _register_and_login("assessment-cyber@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "SIEM, Python and Docker are required for a Cyber Security Analyst.",
        "Candidate One\ncandidate@example.com\nSecurity operations experience with SIEM.",
    )

    response = client.post(f"/assessment/{resume_id}/generate", headers=headers)

    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) <= 10
    assert any("SIEM" in question["question"] or "security" in question["question"].lower() for question in questions)
    assert not any("React hooks" in question["question"] for question in questions)


def test_question_distribution_and_missing_skill_priority() -> None:
    _clear_phase10_data()
    headers = _register_and_login("assessment-distribution@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "Docker, Python, SQL, Linux, AWS, Azure, Git and REST API are required.",
        "Candidate Two\ncandidate2@example.com\nBuilt Python and SQL applications.",
    )

    body = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    questions = body["questions"]
    types = [question["question_type"] for question in questions]
    assert len(questions) == 10
    assert types.count("TECHNICAL") == 4
    assert types.count("SCENARIO") == 3
    assert types.count("PROBLEM_SOLVING") == 3
    assert any(question["skill"] == "Docker" for question in questions)


def test_generate_twice_returns_same_active_assessment() -> None:
    _clear_phase10_data()
    headers = _register_and_login("assessment-duplicate@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Python is required.", "Candidate Three\ncandidate3@example.com\nPython project")

    first = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    second = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()

    assert first["id"] == second["id"]
    assert [question["id"] for question in first["questions"]] == [question["id"] for question in second["questions"]]


def test_answer_submission_keeps_assessment_unscored_and_separate() -> None:
    _clear_phase10_data()
    headers = _register_and_login("assessment-answer@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Docker is required.", "Candidate Four\ncandidate4@example.com\nSkills: Docker")
    before = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    question = assessment["questions"][0]

    answer = client.post(
        f"/assessment/questions/{question['id']}/answer",
        json={
            "answer": "I built a Docker project.",
            "typing_duration": 30,
            "paste_attempt_detected": True,
        },
        headers=headers,
    )
    assert answer.status_code == 200
    assert answer.json()["status"] == "IN_PROGRESS"
    assert answer.json()["score"] is None
    assert answer.json()["feedback"] is None
    after = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assert after["overall_match_score"] == before["overall_match_score"]


def test_submit_requires_all_answers_then_marks_submitted() -> None:
    _clear_phase10_data()
    headers = _register_and_login("assessment-submit@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Python and SQL are required.", "Candidate Five\ncandidate5@example.com\nPython and SQL project")
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    assessment_id = assessment["id"]
    questions = assessment["questions"]

    incomplete = client.post(f"/assessment/{assessment_id}/submit", headers=headers)
    assert incomplete.status_code == 422
    assert client.get(f"/assessment/{assessment_id}/status", headers=headers).json()["status"] == "NOT_STARTED"

    for question in questions:
        response = client.post(
            f"/assessment/questions/{question['id']}/answer",
            json={"answer": "Candidate assessment answer."},
            headers=headers,
        )
        assert response.status_code == 200

    submitted = client.post(f"/assessment/{assessment_id}/submit", headers=headers)
    assert submitted.status_code == 200
    assert submitted.json()["status"] == "SUBMITTED"
    assert submitted.json()["score"] is None


def test_assessment_ownership_and_authentication() -> None:
    _clear_phase10_data()
    company_a = _register_and_login("assessment-a@example.com", "Company A")
    company_b = _register_and_login("assessment-b@example.com", "Company B")
    _, resume_id = _setup_job_and_resume(company_b, "Docker is required.", "Candidate B\nb@example.com\nResume")
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=company_b).json()
    assessment_id = assessment["id"]
    question_id = assessment["questions"][0]["id"]

    assert client.post(f"/assessment/{resume_id}/generate", headers=company_a).status_code == 404
    assert client.get(f"/assessment/{assessment_id}", headers=company_a).status_code == 404
    assert client.post(
        f"/assessment/questions/{question_id}/answer",
        json={"answer": "Unauthorized answer"},
        headers=company_a,
    ).status_code == 404
    assert client.post(f"/assessment/{resume_id}/generate").status_code == 401
    assert client.get(f"/assessment/{assessment_id}").status_code == 401
