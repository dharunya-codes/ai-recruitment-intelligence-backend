from __future__ import annotations

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
import fitz
from app.models.report import Report
from tests.test_assessment import _clear_phase10_data, _register_and_login, _setup_job_and_resume


client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _register_and_login_candidate(name: str, email: str) -> dict[str, str]:
    reg = client.post(
        "/candidate/auth/register",
        json={"name": name, "email": email, "password": "StrongPassword123"},
    )
    assert reg.status_code == 200, reg.text
    login_resp = client.post(
        "/candidate/auth/login",
        json={"email": email, "password": "StrongPassword123"},
    )
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _clear_report_data() -> None:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def test_candidate_and_company_reports_generation_and_fallback() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-fallback@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "Docker and Python are required. SQL is preferred.",
        "Candidate\nBuilt a Python backend system.",
    )
    before = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()

    generated = client.post(f"/reports/{resume_id}/generate", headers=headers)
    assert generated.status_code == 200
    body = generated.json()
    assert "company" in body["reports"] or "HR" in body["reports"]
    assert "candidate" in body["reports"] or "CANDIDATE" in body["reports"]

    company_rep = body["reports"].get("company") or body["reports"].get("HR")
    candidate_rep = body["reports"].get("candidate") or body["reports"].get("CANDIDATE")

    assert company_rep["generation_status"] in {"GENAI_NOT_CONFIGURED", "completed"}
    assert candidate_rep["generation_status"] in {"GENAI_NOT_CONFIGURED", "completed"}

    # Repeated calls return the same report ID
    repeated = client.post(f"/reports/{resume_id}/generate", headers=headers).json()
    rep_candidate = repeated["reports"].get("candidate") or repeated["reports"].get("CANDIDATE")
    assert rep_candidate["id"] == candidate_rep["id"]

    fetched = client.get(f"/reports/{resume_id}", headers=headers).json()
    assert (fetched["reports"].get("company") or fetched["reports"].get("HR"))["id"] == company_rep["id"]

    after = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assert after["overall_match_score"] == before["overall_match_score"]


def test_company_report_complete_sections_and_breakdown() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-company@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "Docker and Python are required. SQL is preferred.",
        "Candidate One\nemail: one@example.com\nphone: 1234567890\nBuilt a Python microservice with Docker containerization.",
    )

    # Trigger verification question and answer
    v_questions = client.post(f"/verification/{resume_id}/generate", headers=headers).json()
    if v_questions:
        q_id = v_questions[0]["id"]
        client.post(
            f"/verification/questions/{q_id}/answer",
            json={"answer": "I created and tested Docker containers for the backend service."},
            headers=headers,
        )

    # Generate, answer, and evaluate assessment
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    for question in assessment["questions"]:
        client.post(
            f"/assessment/questions/{question['id']}/answer",
            json={
                "answer": "Docker image is a container blueprint with modules and validation.",
                "typing_duration": 45,
                "paste_attempt_detected": True,
            },
            headers=headers,
        )
    client.post(f"/assessment/{assessment['id']}/submit", headers=headers)
    client.post(f"/assessment/{assessment['id']}/evaluate", headers=headers)

    report_resp = client.post(f"/reports/{resume_id}/generate", headers=headers)
    assert report_resp.status_code == 200
    report_data = (report_resp.json()["reports"].get("company") or report_resp.json()["reports"].get("HR"))["report_data"]

    # 1. Candidate Info
    assert report_data["candidate"]["name"] is not None
    assert "email" in report_data["candidate"]
    assert "phone" in report_data["candidate"]

    # 2. Resume Info
    assert report_data["resume"]["id"] == resume_id
    assert report_data["resume"]["file_name"] is not None

    # 3. Job Info
    assert report_data["job"]["title"] is not None

    # 4. Match Analysis & Score Breakdown
    assert report_data["match_analysis"]["overall_score"] is not None
    breakdown = report_data["match_analysis"]["score_breakdown"]
    assert "required_skills" in breakdown
    assert "preferred_skills" in breakdown
    assert "experience" in breakdown
    assert "education" in breakdown
    assert "project_relevance" in breakdown
    assert "evidence_strength" in breakdown

    # 5. Skills (strong, moderate, weak, missing, needs_verification)
    skills = report_data["skills"]
    assert "strong" in skills
    assert "weak" in skills
    assert "missing" in skills
    assert "needs_verification" in skills
    for s in skills["strong"]:
        assert "skill" in s
        assert "resume_mention" in s
        assert "evidence_strength" in s

    # 6. Evidence Analysis
    assert isinstance(report_data["evidence"], list)
    assert len(report_data["evidence"]) > 0

    # 7. Verification
    verification = report_data["verification"]
    assert "status" in verification
    assert "questions" in verification
    assert "answers" in verification
    assert "candidate_reported_evidence" in verification
    if verification["candidate_reported_evidence"]:
        assert all(item["source"] == "candidate-reported; not resume evidence" for item in verification["candidate_reported_evidence"])

    # 8. Assessment with Integrity Metadata
    assessment_data = report_data["assessment"]
    assert assessment_data["status"] == "EVALUATED"
    assert assessment_data["score"] is not None
    assert isinstance(assessment_data["questions"], list)
    assert isinstance(assessment_data["feedback"], list)
    integrity = assessment_data["integrity"]
    assert integrity["paste_attempt_detected"] is True
    assert integrity["typing_duration"] is not None

    # 9. Skill Gaps, Resume Quality, Improvement Areas
    assert isinstance(report_data["skill_gaps"], list)
    assert "findings" in report_data["resume_quality"]
    assert isinstance(report_data["improvement_areas"], list)

    # 10. AI Summary
    ai_summary = report_data["ai_summary"]
    assert "candidate_summary" in ai_summary
    assert "relevant_strengths" in ai_summary
    assert "evidence_summary" in ai_summary
    assert "skill_gaps" in ai_summary
    assert "assessment_summary" in ai_summary

    # 11. Strict No Hire/Reject Decisions
    dumped = str(report_data).lower()
    assert "hire decision" not in dumped
    assert "reject decision" not in dumped
    assert "candidate rejected" not in dumped


def test_candidate_report_complete_sections_and_career_intelligence() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-candidate@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(
        headers,
        "Python and Docker are required. Linux is preferred.",
        "Candidate Two\nBuilt a Python project.",
    )

    report_resp = client.post(f"/reports/{resume_id}/generate", headers=headers)
    assert report_resp.status_code == 200
    report_data = (report_resp.json()["reports"].get("candidate") or report_resp.json()["reports"].get("CANDIDATE"))["report_data"]

    assert report_data["report_type"] in {"candidate", "CANDIDATE"}
    assert "match_analysis" in report_data
    assert "skill_analysis" in report_data
    assert "evidence_analysis" in report_data
    assert "verification_results" in report_data
    assert "assessment_result" in report_data
    assert "resume_quality" in report_data
    assert "skill_gaps" in report_data
    assert "improvement_suggestions" in report_data
    assert "career_intelligence" in report_data
    assert "recommended_projects" in report_data
    assert "roadmap" in report_data
    assert "action_priorities" in report_data
    assert "ai_summary" in report_data

    ai_summary = report_data["ai_summary"]
    assert "strong_skills" in ai_summary
    assert "weak_skills" in ai_summary
    assert "missing_skills" in ai_summary
    assert "resume_improvement_suggestions" in ai_summary
    assert "assessment_feedback" in ai_summary
    assert "career_improvement_guidance" in ai_summary


def test_regenerate_report_updates_existing_record() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-regen@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Python is required.", "Candidate\nPython developer.")

    initial = client.post(f"/reports/{resume_id}/generate", headers=headers).json()
    initial_candidate = initial["reports"].get("candidate") or initial["reports"].get("CANDIDATE")
    initial_company = initial["reports"].get("company") or initial["reports"].get("HR")

    regen = client.post(f"/reports/{resume_id}/regenerate", headers=headers).json()
    regen_candidate = regen["reports"].get("candidate") or regen["reports"].get("CANDIDATE")
    regen_company = regen["reports"].get("company") or regen["reports"].get("HR")

    assert regen_candidate["id"] == initial_candidate["id"]
    assert regen_company["id"] == initial_company["id"]


def test_gemini_grounded_summary_mock_success_and_failure() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-gemini@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Python is required.", "Candidate\nPython developer.")

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"candidate_summary": "Demonstrated strong Python foundation.", "evidence_summary": "Resume contains Python project evidence.", "assessment_summary": "Not yet completed."}'
    mock_client.models.generate_content.return_value = mock_response

    with patch.dict("os.environ", {"GENAI_API_KEY": "fake_key"}), patch("google.genai.Client", return_value=mock_client):
        resp = client.post(f"/reports/{resume_id}/regenerate", headers=headers)
        assert resp.status_code == 200
        rep_data = (resp.json()["reports"].get("company") or resp.json()["reports"].get("HR"))["report_data"]
        assert rep_data["ai_summary"]["candidate_summary"] == "Demonstrated strong Python foundation."

    # In case of Gemini exception, fallback is used gracefully
    mock_client.models.generate_content.side_effect = RuntimeError("API Rate Limit")
    with patch.dict("os.environ", {"GENAI_API_KEY": "fake_key"}), patch("google.genai.Client", return_value=mock_client):
        resp_err = client.post(f"/reports/{resume_id}/regenerate", headers=headers)
        assert resp_err.status_code == 200
        rep_data_err = (resp_err.json()["reports"].get("company") or resp_err.json()["reports"].get("HR"))["report_data"]
        assert "evaluation for" in rep_data_err["ai_summary"]["candidate_summary"]


def test_standalone_candidate_flow_and_authorization() -> None:
    _clear_report_data()
    cand_a_headers = _register_and_login_candidate("Candidate A", "cand-rep-a@example.com")
    cand_b_headers = _register_and_login_candidate("Candidate B", "cand-rep-b@example.com")
    company_headers = _register_and_login("company-rep-auth@example.com", "Company Auth")

    # Upload resume as candidate A
    upload_resp = client.post(
        "/candidate/resumes",
        files={"file": ("resume_a.pdf", _pdf_bytes("Candidate A\nemail: cand-rep-a@example.com\nPython and Docker developer\nBuilt REST API services with Python."), "application/pdf")},
        headers=cand_a_headers,
    )
    assert upload_resp.status_code == 201
    resume_id = upload_resp.json()["id"]

    # Candidate A analyzes resume
    client.post(
        f"/candidate/analysis/{resume_id}",
        json={"target_role": "Python Developer"},
        headers=cand_a_headers,
    )

    # Candidate A generates candidate report
    gen_resp = client.post(f"/candidate/reports/{resume_id}/generate", headers=cand_a_headers)
    assert gen_resp.status_code == 200
    assert "candidate" in gen_resp.json()["reports"] or "CANDIDATE" in gen_resp.json()["reports"]

    # Candidate B cannot access Candidate A's report
    assert client.get(f"/candidate/reports/{resume_id}", headers=cand_b_headers).status_code == 404
    assert client.post(f"/candidate/reports/{resume_id}/generate", headers=cand_b_headers).status_code == 404

    # Company user cannot access Candidate A's standalone report through /reports/
    assert client.get(f"/reports/{resume_id}", headers=company_headers).status_code == 404
    assert client.post(f"/reports/{resume_id}/generate", headers=company_headers).status_code == 404

    # Unauthenticated access is blocked
    assert client.get(f"/candidate/reports/{resume_id}").status_code == 401
    assert client.get(f"/reports/{resume_id}").status_code == 401


def test_query_filtering_by_report_type() -> None:
    _clear_report_data()
    headers = _register_and_login("reports-query@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Python is required.", "Candidate\nPython")

    client.post(f"/reports/{resume_id}/generate", headers=headers)

    # Query with report_type=company
    company_only = client.get(f"/reports/{resume_id}?report_type=company", headers=headers).json()
    assert "company" in company_only["reports"] or "HR" in company_only["reports"]
    assert "candidate" not in company_only["reports"] and "CANDIDATE" not in company_only["reports"]

    # Query with report_type=candidate
    candidate_only = client.get(f"/reports/{resume_id}?report_type=candidate", headers=headers).json()
    assert "candidate" in candidate_only["reports"] or "CANDIDATE" in candidate_only["reports"]
    assert "company" not in candidate_only["reports"] and "HR" not in candidate_only["reports"]