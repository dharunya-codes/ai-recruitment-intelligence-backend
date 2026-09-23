from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.analysis_snapshot import AnalysisSnapshot
from app.models.report import Report
from app.services.action_priority_service import build_actions
from app.services.career_question_service import answer_career_question
from app.services.evidence_builder_service import build_evidence_recommendations
from app.services.project_recommendation_service import recommend_projects
from app.services.progress_service import compare_snapshots
from tests.test_assessment import _clear_phase10_data, _register_and_login, _setup_job_and_resume
from tests.test_candidate_analysis import _setup


client = TestClient(app)


def _clear() -> None:
    db = SessionLocal()
    try:
        db.query(AnalysisSnapshot).delete()
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def test_career_services_are_structured_and_evidence_based() -> None:
    gaps = [{"skill": "Docker", "status": "MISSING"}, {"skill": "Python", "status": "WEAK_EVIDENCE"}]
    projects = recommend_projects("Backend Developer", gaps)
    assert projects[0]["target_skills"] == ["Docker"]
    assert projects[0]["difficulty"] == "INTERMEDIATE"
    evidence = build_evidence_recommendations(gaps)
    assert evidence[0]["current_status"] == "MISSING"
    actions = build_actions([{"skill": "Docker", "priority": "CRITICAL", "reason": "missing"}], [], ["Python"], ["SQL"])
    assert {item["category"] for item in actions} == {"SKILL", "VERIFICATION", "ASSESSMENT"}
    assert compare_snapshots([])["progress_status"] == "INSUFFICIENT_HISTORY"
    assert compare_snapshots([
        {"requirement_analysis": [{"requirement": "Python", "match_status": "WEAK"}]},
        {"requirement_analysis": [{"requirement": "Python", "match_status": "MATCHED"}]},
    ])[
        "improved"
    ] == ["Python"]
    answer = answer_career_question("UNSUPPORTED", {"priority_gaps": []})
    assert answer["status"] == "INSUFFICIENT_DATA"


def test_candidate_career_endpoints_and_progress() -> None:
    _clear()
    headers, resume_id = _setup("phase16-candidate@example.com")
    first = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Backend Developer"}, headers=headers)
    assert first.status_code == 200
    second = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Backend Developer", "job_description": "Python and Docker are required."}, headers=headers)
    assert second.status_code == 200

    paths = [
        f"/candidate/analysis/{resume_id}/career-intelligence",
        f"/candidate/analysis/{resume_id}/actions",
        f"/candidate/analysis/{resume_id}/projects",
        f"/candidate/analysis/{resume_id}/evidence-builder",
        f"/candidate/analysis/{resume_id}/roadmap",
        f"/candidate/analysis/{resume_id}/progress",
    ]
    responses = [client.get(path, headers=headers) for path in paths]
    assert all(response.status_code == 200 for response in responses)
    assert responses[0].json()["data"]["target_role"] == "Backend Developer"
    assert responses[-1].json()["data"]["progress_status"] in {"CHANGES_DETECTED", "NO_CHANGES_DETECTED"}

    question = client.post(
        f"/candidate/analysis/{resume_id}/career-question",
        json={"question_type": "WHAT_SKILL_IS_MISSING"},
        headers=headers,
    )
    assert question.status_code == 200
    assert question.json()["data"]["status"] == "ANSWERED"


def test_candidate_career_intelligence_isolated_and_hr_route_is_company_scoped() -> None:
    _clear()
    candidate_headers, candidate_resume_id = _setup("phase16-owner@example.com")
    other_registration = client.post("/candidate/auth/register", json={"name": "Other", "email": "phase16-other@example.com", "password": "StrongPassword123"})
    assert other_registration.status_code == 200
    other_token = client.post("/candidate/auth/login", json={"email": "phase16-other@example.com", "password": "StrongPassword123"}).json()["access_token"]
    assert client.get(f"/candidate/analysis/{candidate_resume_id}/career-intelligence", headers={"Authorization": f"Bearer {other_token}"}).status_code == 404
    assert client.get(f"/candidate/analysis/{candidate_resume_id}/career-intelligence").status_code == 401


def test_hr_career_intelligence_returns_no_ranking() -> None:
    _clear()
    headers = _register_and_login("phase16-hr@example.com", "Phase 16 Company")
    _, resume_id = _setup_job_and_resume(headers, "Python and Docker are required.", "Candidate\nPython project")
    # Company resumes use the existing analysis endpoint to establish the deterministic source data.
    analysis = client.get(f"/resumes/{resume_id}/analysis", headers=headers)
    assert analysis.status_code == 200
    from app.database.database import SessionLocal
    from app.models.resume import Resume
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        resume.target_role = "Backend Developer"
        resume.analysis_data = {
            "requirements_source": "COMPANY_JD",
            "counts": analysis.json()["counts"],
            "matched_requirements": analysis.json()["matched_requirements"],
            "requirement_analysis": analysis.json()["requirement_analysis"],
        }
        db.commit()
    finally:
        db.close()
    response = client.get(f"/analysis/{resume_id}/career-intelligence", headers=headers)
    assert response.status_code == 200
    assert "ranking" not in response.json()["data"]
    assert "best_candidate" not in response.json()["data"]