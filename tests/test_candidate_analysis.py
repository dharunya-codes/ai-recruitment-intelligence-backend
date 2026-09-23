import fitz
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.report import Report
from tests.test_assessment import _clear_phase10_data


client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _setup(email: str = "candidate-analysis@example.com") -> tuple[dict[str, str], int]:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()
    registered = client.post("/candidate/auth/register", json={"name": "Analysis Candidate", "email": email, "password": "StrongPassword123"})
    assert registered.status_code == 200
    token = client.post("/candidate/auth/login", json={"email": email, "password": "StrongPassword123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resume = client.post("/candidate/resumes", files={"file": ("resume.pdf", _pdf_bytes("Candidate built Python automation and used Linux."), "application/pdf")}, headers=headers)
    assert resume.status_code == 201
    return headers, resume.json()["id"]


def test_role_and_jd_analysis_have_distinct_score_semantics() -> None:
    headers, resume_id = _setup()
    role = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Cyber Security Analyst"}, headers=headers)
    assert role.status_code == 200
    assert role.json()["score_type"] == "ROLE_COMPATIBILITY"
    assert role.json()["requirements_source"] == "ROLE_BASED_EXPECTATIONS"
    jd = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Automation Developer", "job_description": "Python and Linux are required."}, headers=headers)
    assert jd.status_code == 200
    assert jd.json()["score_type"] == "JOB_MATCH"
    assert jd.json()["requirements_source"] == "COMPANY_JD"
    history = client.get("/candidate/analyses", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 1


def test_candidate_verification_assessment_and_candidate_only_report() -> None:
    headers, resume_id = _setup("candidate-workflow@example.com")
    analysis = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Backend Developer"}, headers=headers)
    assert analysis.status_code == 200
    questions = client.post(f"/candidate/verification/{resume_id}/generate", headers=headers)
    assert questions.status_code == 200
    if questions.json():
        answer = client.post(f"/candidate/verification/questions/{questions.json()[0]['id']}/answer", json={"answer": "I built a Python project."}, headers=headers)
        assert answer.status_code == 200
        assert answer.json()["evidence_status"] == "CANDIDATE_VERIFIED"

    assessment = client.post(f"/candidate/assessment/{resume_id}/generate", headers=headers)
    assert assessment.status_code == 200
    for question in assessment.json()["questions"]:
        assert client.post(f"/candidate/assessment/questions/{question['id']}/answer", json={"answer": "I built a Python service and tested it."}, headers=headers).status_code == 200
    assessment_id = assessment.json()["id"]
    assert client.post(f"/candidate/assessment/{assessment_id}/submit", headers=headers).status_code == 200
    assert client.post(f"/candidate/assessment/{assessment_id}/evaluate", headers=headers).status_code == 200

    report = client.post(f"/reports/{resume_id}/generate", headers=headers)
    assert report.status_code == 200
    assert set(report.json()["reports"]) == {"CANDIDATE"}
    assert client.get(f"/reports/{resume_id}?report_type=HR", headers=headers).status_code == 404
    assert client.get(f"/reports/{resume_id}", headers=headers).json()["reports"]["CANDIDATE"]["report_data"]["assessment_summary"]["status"] == "EVALUATED"