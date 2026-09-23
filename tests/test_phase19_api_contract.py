from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_openapi_contract_has_security_scheme_routes_and_documented_tags() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "bearerAuth" in schema["components"]["securitySchemes"] or "OAuth2PasswordBearer" in schema["components"]["securitySchemes"]
    required_paths = {
        "/auth/login",
        "/candidate/auth/login",
        "/jobs",
        "/jobs/{job_id}/jd",
        "/jobs/{job_id}/requirements",
        "/jobs/{job_id}/resumes",
        "/resumes/{resume_id}/analysis",
        "/verification/{resume_id}/generate",
        "/assessment/{resume_id}/generate",
        "/reports/{resume_id}/generate",
        "/candidate/resumes",
        "/candidate/analysis/{resume_id}",
        "/candidate/analysis/{resume_id}/readiness",
        "/candidate/analysis/{resume_id}/career-intelligence",
        "/candidate/analysis/{resume_id}/roadmap",
        "/candidate/analysis/{resume_id}/progress",
        "/analysis/multi-job",
    }
    assert required_paths.issubset(schema["paths"])
    tags = {tag for path in schema["paths"].values() for operation in path.values() if isinstance(operation, dict) for tag in operation.get("tags", [])}
    assert {"Authentication", "Jobs", "Assessment", "Reports", "Candidate", "Candidate Intelligence", "Career Intelligence"}.issubset(tags)


def test_representative_contract_status_and_error_shapes() -> None:
    assert client.get("/health").json()["status"] == "ok"
    unauthenticated = client.get("/candidate/resumes")
    assert unauthenticated.status_code == 401
    assert set(unauthenticated.json()) == {"detail"}
    invalid_login = client.post("/candidate/auth/login", json={"email": "missing@example.com", "password": "WrongPassword123"})
    assert invalid_login.status_code == 401
    assert set(invalid_login.json()) == {"detail"}
    invalid_payload = client.post("/candidate/auth/register", json={"name": "A", "email": "not-an-email", "password": "short"})
    assert invalid_payload.status_code == 422
    assert "detail" in invalid_payload.json()


def test_openapi_response_models_do_not_expose_sensitive_fields() -> None:
    schema = client.get("/openapi.json").json()
    serialized = str(schema)
    assert "password_hash" not in serialized
    assert "GENAI_API_KEY" not in serialized
    assert "file_path" not in serialized


def test_docs_and_health_are_available() -> None:
    assert client.get("/docs").status_code == 200
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "message": "HALO backend is running"}