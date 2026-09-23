from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.report import Report
from app.services.candidate_readiness_service import build_readiness_profile
from app.services.evidence_consistency_service import analyze_evidence_consistency
from app.services.improvement_plan_service import build_improvement_plan
from app.services.resume_quality_service import analyze_resume_quality
from app.services.skill_priority_engine import build_advanced_gaps, build_skill_priorities, transferable_skills
from tests.test_assessment import _clear_phase10_data, _register_and_login, _setup_job_and_resume
from tests.test_candidate_analysis import _setup


client = TestClient(app)


def _clear() -> None:
    db = SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()
    _clear_phase10_data()


def test_skill_priorities_and_advanced_gap_states() -> None:
    requirements = [
        {"requirement": "Docker", "importance": "REQUIRED", "match_status": "MISSING"},
        {"requirement": "Python", "importance": "REQUIRED", "match_status": "WEAK"},
        {"requirement": "SQL", "importance": "PREFERRED", "match_status": "MATCHED"},
    ]
    priorities = build_skill_priorities(requirements)
    assert priorities[0]["skill"] == "Docker"
    assert priorities[0]["priority"] == "CRITICAL"
    assert next(item for item in priorities if item["skill"] == "Python")["priority"] == "HIGH"
    gaps = build_advanced_gaps(requirements, {"Python": "CANDIDATE_VERIFIED"})
    assert next(item for item in gaps if item["skill"] == "Docker")["status"] == "MISSING"
    assert next(item for item in gaps if item["skill"] == "Python")["status"] == "CANDIDATE_VERIFIED"
    assert transferable_skills(["Python", "Unknown"])[0]["transferable_to"] == ["Security Automation"]


def test_readiness_quality_consistency_and_plan_are_explainable() -> None:
    analysis = {"counts": {"matched": 2, "weak": 1, "missing": 1, "total": 4}}
    quality = analyze_resume_quality("Candidate Python skills")
    readiness = build_readiness_profile(analysis, [{"status": "ANSWERED"}], {"status": "IN_PROGRESS"}, quality)
    assert readiness["role_alignment"]["status"] == "MODERATE"
    assert readiness["verification"]["status"] == "FULLY_VERIFIED"
    plan = build_improvement_plan([{"skill": "Docker", "priority": "CRITICAL"}], ["Review joins"], quality)
    assert plan["IMMEDIATE"]
    assert plan["MEDIUM_TERM"] == [{"skill": "Assessment focus", "action": "Review joins"}]
    consistency = analyze_evidence_consistency(
        [{"requirement": "Docker", "match_status": "MISSING"}],
        [{"skill": "Docker", "evidence_status": "NO_SUPPORTING_EVIDENCE"}],
        [{"skill": "Docker", "score": 2}],
    )
    assert "insufficient" in consistency[0]["conclusion"].lower() or "differ" in consistency[0]["conclusion"].lower()


def test_candidate_intelligence_endpoints_are_owned_and_return_structured_data() -> None:
    _clear()
    headers, resume_id = _setup("phase15-candidate@example.com")
    analysis = client.post(f"/candidate/analysis/{resume_id}", json={"target_role": "Backend Developer"}, headers=headers)
    assert analysis.status_code == 200
    readiness = client.get(f"/candidate/analysis/{resume_id}/readiness", headers=headers)
    priorities = client.get(f"/candidate/analysis/{resume_id}/skill-priorities", headers=headers)
    quality = client.get(f"/candidate/analysis/{resume_id}/resume-quality", headers=headers)
    plan = client.get(f"/candidate/analysis/{resume_id}/improvement-plan", headers=headers)
    consistency = client.get(f"/analysis/{resume_id}/evidence-consistency", headers=headers)
    assert readiness.status_code == priorities.status_code == quality.status_code == plan.status_code == consistency.status_code == 200
    assert "dimensions" in readiness.json()["data"]
    assert "priorities" in priorities.json()["data"]
    assert "findings" in quality.json()["data"]
    assert "IMMEDIATE" in plan.json()["data"]
    assert "items" in consistency.json()["data"]


def test_candidate_intelligence_does_not_cross_candidate_ownership() -> None:
    _clear()
    headers, resume_id = _setup("phase15-owner@example.com")
    registration = client.post("/candidate/auth/register", json={"name": "Other", "email": "phase15-other@example.com", "password": "StrongPassword123"})
    assert registration.status_code == 200
    token = client.post("/candidate/auth/login", json={"email": "phase15-other@example.com", "password": "StrongPassword123"}).json()["access_token"]
    other = {"Authorization": f"Bearer {token}"}
    assert client.get(f"/candidate/analysis/{resume_id}/readiness", headers=other).status_code == 404


def test_hr_multi_job_analysis_is_independent_and_company_scoped() -> None:
    _clear()
    headers = _register_and_login("phase15-hr@example.com", "Phase 15 Company")
    first_job, resume_id = _setup_job_and_resume(headers, "Python and SQL are required.", "Candidate\nPython project")
    second = client.post("/jobs", json={"title": "Second Role", "description": "Docker is required."}, headers=headers)
    assert second.status_code == 201
    result = client.post("/analysis/multi-job", json={"resume_id": resume_id, "job_ids": [first_job, second.json()["id"]]}, headers=headers)
    assert result.status_code == 200
    assert len(result.json()["analyses"]) == 2
    assert all("best" not in item and "ranking" not in item for item in result.json()["analyses"])