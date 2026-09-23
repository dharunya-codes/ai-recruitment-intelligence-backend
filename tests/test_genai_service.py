from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.services.genai_service import GenAIService


def _sample_context() -> dict:
    return {
        "candidate": {"name": "Test Candidate"},
        "job": {"title": "Python Developer", "description": "Python, SQL, REST API"},
        "resume_text": "Experienced Python Developer who built REST APIs with FastAPI and SQL.",
        "resume_analysis": {
            "overall_match_score": 85.0,
            "required_score": 90.0,
            "preferred_score": 75.0,
            "score_status": "CALCULATED",
            "counts": {"matched": 3, "weak": 1, "missing": 0, "total": 4},
            "matched_requirements": [{"requirement": "Python"}, {"requirement": "SQL"}, {"requirement": "REST API"}],
            "weak_requirements": [{"requirement": "Docker"}],
            "missing_requirements": [],
        },
        "evidence": [
            {"skill": "Python", "evidence_strength": "STRONG", "evidence_text": "Built REST APIs with Python"},
        ],
        "verification": [
            {"skill": "Docker", "status": "ANSWERED", "candidate_reported_evidence": "Built Docker container in personal project"},
        ],
        "assessment": {
            "status": "EVALUATED",
            "score": 88.0,
            "strengths": ["Strong understanding of Python"],
            "areas_for_improvement": ["Review Docker containerization"],
        },
    }


def test_genai_not_configured_returns_deterministic_fallback(monkeypatch) -> None:
    monkeypatch.delenv("GENAI_API_KEY", raising=False)
    monkeypatch.setenv("GENAI_MODEL", "gemini-2.5-flash")

    service = GenAIService()
    assert not service.is_configured()
    assert service.get_model_name() == "gemini-2.5-flash"

    context = _sample_context()
    reports = service.generate_reports(context)
    assert reports["generation_status"] == "GENAI_NOT_CONFIGURED"
    assert reports["candidate"]["report_type"] == "CANDIDATE"
    assert "Python" in reports["candidate"]["strong_skills"]
    assert "Docker" in reports["candidate"]["weak_skills"]
    assert reports["hr"]["report_type"] == "HR"


def test_genai_successful_generation(monkeypatch) -> None:
    monkeypatch.setenv("GENAI_API_KEY", "fake-test-key")
    monkeypatch.setenv("GENAI_MODEL", "gemini-2.5-flash")

    service = GenAIService()
    assert service.is_configured()

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Candidate demonstrates strong Python and SQL backend fundamentals with minor Docker gaps."
    mock_client.models.generate_content.return_value = mock_response

    with patch.object(service, "_get_client", return_value=mock_client):
        context = _sample_context()
        summary, status = service.generate_candidate_summary(context)
        assert status == "GENAI_SUCCESS"
        assert "strong Python" in summary

        reports = service.generate_reports(context)
        assert reports["generation_status"] == "GENAI_SUCCESS"
        assert "strong Python" in reports["candidate"]["executive_summary"]


def test_genai_api_failure_handled_gracefully(monkeypatch) -> None:
    monkeypatch.setenv("GENAI_API_KEY", "fake-test-key")
    monkeypatch.setenv("GENAI_MODEL", "gemini-2.5-flash")

    service = GenAIService()

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = ConnectionError("Remote API connection timeout")

    with patch.object(service, "_get_client", return_value=mock_client):
        context = _sample_context()
        reports = service.generate_reports(context)
        assert reports["generation_status"] == "GENAI_ERROR"
        # Verify fallback reports are still intact and valid
        assert reports["candidate"]["report_type"] == "CANDIDATE"
        assert reports["candidate"]["strong_skills"] == ["Python", "SQL", "REST API"]
        assert reports["hr"]["report_type"] == "HR"


def test_evidence_grounding_and_source_segregation(monkeypatch) -> None:
    monkeypatch.delenv("GENAI_API_KEY", raising=False)
    service = GenAIService()
    context = _sample_context()
    reports = service.generate_reports(context)

    candidate_report = reports["candidate"]
    # Verify candidate verification is explicitly tagged as candidate-reported, not resume evidence
    for v in candidate_report["verification_summary"]:
        assert v["source"] == "candidate-reported; not resume evidence"

    # Verify resume evidence is tagged as resume source
    for e in reports["hr"]["evidence_summary"]:
        assert e["source"] == "resume"
