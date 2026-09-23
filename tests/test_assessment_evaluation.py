from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.services.answer_evaluation_service import evaluate_answer
from tests.test_assessment import (
    _clear_phase10_data,
    _register_and_login,
    _setup_job_and_resume,
)


client = TestClient(app)


def _siem_question() -> SimpleNamespace:
    return SimpleNamespace(
        question="What is the purpose of a SIEM?",
        skill="SIEM",
        expected_concepts=None,
    )


def test_evaluator_score_bands_and_no_answer() -> None:
    question = _siem_question()
    strong = evaluate_answer(
        question,
        "SIEM collects security logs and events, correlates them and generates alerts.",
    )
    partial = evaluate_answer(question, "SIEM monitors security logs.")
    incorrect = evaluate_answer(question, "SIEM is a programming language.")
    empty = evaluate_answer(question, " ")

    assert strong.score == 10
    assert strong.evaluation_status == "CORRECT"
    assert partial.evaluation_status == "PARTIAL"
    assert partial.score < strong.score
    assert incorrect.score == 0
    assert incorrect.evaluation_status == "INCORRECT"
    assert empty.score == 0
    assert empty.evaluation_status == "NO_ANSWER"


def test_evaluation_lifecycle_and_result_are_idempotent() -> None:
    _clear_phase10_data()
    headers = _register_and_login("evaluation-lifecycle@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Docker is required.", "Candidate\nDocker")
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    assessment_id = assessment["id"]

    assert client.post(f"/assessment/{assessment_id}/evaluate", headers=headers).status_code == 422
    for question in assessment["questions"]:
        response = client.post(
            f"/assessment/questions/{question['id']}/answer",
            json={"answer": "A Docker image builds and runs an application in a container."},
            headers=headers,
        )
        assert response.status_code == 200
    assert client.post(f"/assessment/{assessment_id}/submit", headers=headers).status_code == 200

    evaluated = client.post(f"/assessment/{assessment_id}/evaluate", headers=headers)
    assert evaluated.status_code == 200
    body = evaluated.json()
    assert body["status"] == "EVALUATED"
    assert body["total_questions"] == len(assessment["questions"])
    assert body["answered"] == body["total_questions"]
    assert {item["question_type"] for item in body["question_results"]} == {
        "TECHNICAL",
        "SCENARIO",
        "PROBLEM_SOLVING",
    }
    assert client.get(f"/assessment/{assessment_id}/result", headers=headers).json() == body
    assert client.post(f"/assessment/{assessment_id}/evaluate", headers=headers).json() == body


def test_evaluation_result_and_evidence_are_separate() -> None:
    _clear_phase10_data()
    headers = _register_and_login("evaluation-evidence@example.com", "Company A")
    _, resume_id = _setup_job_and_resume(headers, "Java is required.", "Candidate\nJava")
    before = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=headers).json()
    for question in assessment["questions"]:
        client.post(
            f"/assessment/questions/{question['id']}/answer",
            json={"answer": "A Java method can be overloaded with different parameters."},
            headers=headers,
        )
    client.post(f"/assessment/{assessment['id']}/submit", headers=headers)
    result = client.post(f"/assessment/{assessment['id']}/evaluate", headers=headers)

    after = client.get(f"/resumes/{resume_id}/analysis", headers=headers).json()
    assert result.status_code == 200
    assert result.json()["score"] >= 0
    assert after["overall_match_score"] == before["overall_match_score"]


def test_evaluation_result_is_company_scoped_and_requires_authentication() -> None:
    _clear_phase10_data()
    company_a = _register_and_login("evaluation-a@example.com", "Company A")
    company_b = _register_and_login("evaluation-b@example.com", "Company B")
    _, resume_id = _setup_job_and_resume(company_b, "Docker is required.", "Candidate B\nDocker")
    assessment = client.post(f"/assessment/{resume_id}/generate", headers=company_b).json()

    assert client.post(f"/assessment/{assessment['id']}/evaluate", headers=company_a).status_code == 404
    assert client.get(f"/assessment/{assessment['id']}/result", headers=company_a).status_code == 404
    assert client.post(f"/assessment/{assessment['id']}/evaluate").status_code == 401