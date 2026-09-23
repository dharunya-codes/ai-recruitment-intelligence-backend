from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.report import Report
from tests.test_assessment import _clear_phase10_data, _register_and_login, _setup_job_and_resume


client = TestClient(app)


def _clear_report_data() -> None:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def test_candidate_and_hr_reports_use_deterministic_fallback() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-fallback@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "Docker and Python are required.",
        "Candidate\nBuilt a Python project.",
    )
    before = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()

    generated = client.post(f"/reports/{resume_id}/generate", headers=headers)
    assert generated.status_code == 200
    body = generated.json()
    assert set(body["reports"]) == {"CANDIDATE", "HR"}
    candidate = body["reports"]["CANDIDATE"]
    hr = body["reports"]["HR"]
    assert candidate["generation_status"] == "GENAI_NOT_CONFIGURED"
    assert candidate["report_data"]["report_type"] == "CANDIDATE"
    assert "Docker" in candidate["report_data"]["missing_skills"]
    assert hr["report_data"]["report_type"] == "HR"
    assert hr["report_data"]["final_summary"].startswith("This report is decision support")

    repeated = client.post(f"/reports/{resume_id}/generate", headers=headers).json()
    assert repeated["reports"]["CANDIDATE"]["id"] == candidate["id"]
    assert client.get(f"/reports/{resume_id}", headers=headers).json() == repeated
    after = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assert after["overall_match_score"] == before["overall_match_score"]


def test_report_contains_evaluated_assessment_and_preserves_evidence_sources() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-assessment@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Docker is required.", "Candidate\nDocker")
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    for question in assessment["questions"]:
        client.post(
            f"/assessment/questions/{question['id']}/answer",
            json={"answer": "A Docker image runs an application in a container."},
            headers=headers,
        )
    client.post(f"/assessment/{assessment['id']}/submit", headers=headers)
    evaluated = client.post(f"/assessment/{assessment['id']}/evaluate", headers=headers)
    assert evaluated.status_code == 200

    report = client.post(f"/reports/{resume_id}/generate", headers=headers).json()
    candidate_data = report["reports"]["CANDIDATE"]["report_data"]
    assert candidate_data["assessment_summary"]["status"] == "EVALUATED"
    assert candidate_data["assessment_strengths"] == candidate_data["assessment_summary"]["strengths"]
    assert all(item["source"] == "candidate-reported; not resume evidence" for item in candidate_data["verification_summary"])

    regenerated = client.post(f"/reports/{resume_id}/regenerate", headers=headers).json()
    assert regenerated["reports"]["HR"]["id"] == report["reports"]["HR"]["id"]


def test_report_security_and_unauthenticated_access() -> None:
    _clear_report_data()
    company_a = _register_and_login("reports-security-a@example.com", "Company A")
    company_b = _register_and_login("reports-security-b@example.com", "Company B")
    _, resume_id = _setup_job_and_resume(company_b, "Python is required.", "Candidate B\nPython")

    assert client.post(f"/reports/{resume_id}/generate", headers=company_a).status_code == 404
    assert client.get(f"/reports/{resume_id}", headers=company_a).status_code == 404
    assert client.post(f"/reports/{resume_id}/generate").status_code == 401
    assert client.get(f"/reports/{resume_id}").status_code == 401