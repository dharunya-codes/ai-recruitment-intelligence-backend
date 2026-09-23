from __future__ import annotations

from io import BytesIO

import fitz
from docx import Document
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.analysis_snapshot import AnalysisSnapshot
from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.candidate import Candidate
from app.models.evidence import SkillEvidence
from app.models.report import Report
from app.models.resume import Resume
from app.models.user import User
from app.models.verification import VerificationQuestion

client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def _docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def _clear_test_db() -> None:
    db = SessionLocal()
    try:
        db.query(CandidateAnswer).delete()
        db.query(AssessmentQuestion).delete()
        db.query(Assessment).delete()
        db.query(VerificationQuestion).delete()
        db.query(SkillEvidence).delete()
        db.query(AnalysisSnapshot).delete()
        db.query(Report).delete()
        db.query(Resume).delete()
        db.query(Candidate).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def _register_and_login_candidate(name: str, email: str, password: str = "StrongPassword123") -> tuple[dict[str, str], int]:
    reg = client.post("/candidate/auth/register", json={"name": name, "email": email, "password": password})
    assert reg.status_code == 200, reg.text
    user_id = reg.json()["user"]["id"]
    login = client.post("/candidate/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_public_candidate_full_evaluation_flow() -> None:
    _clear_test_db()

    # 1. Candidate Registration
    headers, user_id = _register_and_login_candidate("Alice Developer", "alice.dev@example.com")

    # 2. Candidate Profile / Me
    me_resp = client.get("/candidate/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "alice.dev@example.com"
    assert me_resp.json()["role"] == "CANDIDATE"

    # 3. Resume Upload (PDF)
    resume_text = """
    Alice Developer
    Email: alice.dev@example.com
    Phone: +1 555-0199
    Summary: Experienced Software Developer with strong background in Python, SQL, REST API, Git, and Docker.
    Experience:
    Software Engineer at Tech Corp (2021-2024)
    - Built REST API services using Python and FastAPI.
    - Designed relational databases and optimized queries using SQL.
    - Used Docker for containerization and Git for source control.
    Projects:
    - Microservices API: Built backend service with Python, SQL, and Docker.
    Education:
    Bachelor of Science in Computer Science
    """
    upload_resp = client.post(
        "/candidate/resumes",
        files={"file": ("alice_resume.pdf", _pdf_bytes(resume_text), "application/pdf")},
        headers=headers,
    )
    assert upload_resp.status_code == 201
    resume_id = upload_resp.json()["id"]
    assert upload_resp.json()["file_name"] == "alice_resume.pdf"
    assert upload_resp.json()["job_id"] is None

    # 4. Role-Catalog Analysis (Option A: Target Role only)
    role_analysis_resp = client.post(
        f"/candidate/analysis/{resume_id}",
        json={"target_role": "Python Developer"},
        headers=headers,
    )
    assert role_analysis_resp.status_code == 200
    role_data = role_analysis_resp.json()
    assert role_data["target_role"] == "Python Developer"
    assert role_data["score_type"] == "ROLE_COMPATIBILITY"
    assert role_data["analysis_type"] == "ROLE_COMPATIBILITY"
    assert role_data["role_source"] == "ROLE_CATALOG"
    assert role_data["requirements_source"] == "ROLE_BASED_EXPECTATIONS"
    assert role_data["match_score"] is not None
    assert "score_breakdown" in role_data
    assert "strong_skills" in role_data
    assert "weak_skills" in role_data
    assert "missing_skills" in role_data
    assert "needs_verification" in role_data
    assert "evidence" in role_data
    assert "skill_gaps" in role_data
    assert "resume_quality" in role_data
    assert "improvement_suggestions" in role_data
    assert "Python" in role_data["strong_skills"]

    # Verify no automated hire/reject decision in payload
    assert "hire" not in role_data
    assert "reject" not in role_data
    assert "decision" not in role_data

    # 5. Single Analysis Retrieval (GET /candidate/analysis/{resume_id})
    get_analysis_resp = client.get(f"/candidate/analysis/{resume_id}", headers=headers)
    assert get_analysis_resp.status_code == 200
    retrieved_data = get_analysis_resp.json()
    assert retrieved_data["resume_id"] == resume_id
    assert retrieved_data["target_role"] == "Python Developer"
    assert retrieved_data["match_score"] == role_data["match_score"]

    # 6. Candidate Intelligence Sub-endpoints
    rq_resp = client.get(f"/candidate/analysis/{resume_id}/resume-quality", headers=headers)
    assert rq_resp.status_code == 200
    assert "findings" in rq_resp.json()["data"]

    sp_resp = client.get(f"/candidate/analysis/{resume_id}/skill-priorities", headers=headers)
    assert sp_resp.status_code == 200
    assert "priorities" in sp_resp.json()["data"]

    # 7. Candidate Verification Flow
    gen_v_resp = client.post(f"/candidate/verification/{resume_id}/generate", headers=headers)
    assert gen_v_resp.status_code == 200
    v_questions = gen_v_resp.json()
    if v_questions:
        q_id = v_questions[0]["id"]
        ans_v_resp = client.post(
            f"/candidate/verification/questions/{q_id}/answer",
            json={"answer": "I built production APIs and services using this technology in my capstone project."},
            headers=headers,
        )
        assert ans_v_resp.status_code == 200
        assert ans_v_resp.json()["evidence_status"] == "CANDIDATE_VERIFIED"

    # 8. Candidate Assessment Flow
    gen_a_resp = client.post(f"/candidate/assessment/{resume_id}/generate", headers=headers)
    assert gen_a_resp.status_code == 200
    assessment_id = gen_a_resp.json()["id"]
    for q in gen_a_resp.json()["questions"]:
        ans_a_resp = client.post(
            f"/candidate/assessment/questions/{q['id']}/answer",
            json={"answer": "Detailed technical implementation and concept explanation for " + str(q.get("skill"))},
            headers=headers,
        )
        assert ans_a_resp.status_code == 200

    sub_a_resp = client.post(f"/candidate/assessment/{assessment_id}/submit", headers=headers)
    assert sub_a_resp.status_code == 200
    eval_a_resp = client.post(f"/candidate/assessment/{assessment_id}/evaluate", headers=headers)
    assert eval_a_resp.status_code == 200
    assert eval_a_resp.json()["score"] is not None

    # 9. Candidate Personal Report Generation and Retrieval
    gen_rep_resp = client.post(f"/candidate/reports/{resume_id}/generate", headers=headers)
    assert gen_rep_resp.status_code == 200
    assert "CANDIDATE" in gen_rep_resp.json()["reports"]
    assert "HR" not in gen_rep_resp.json()["reports"]

    get_rep_resp = client.get(f"/candidate/reports/{resume_id}", headers=headers)
    assert get_rep_resp.status_code == 200
    assert "CANDIDATE" in get_rep_resp.json()["reports"]


def test_custom_target_role_fallback_without_jd() -> None:
    _clear_test_db()
    headers, _ = _register_and_login_candidate("Bob Custom", "bob.custom@example.com")

    resume_text = """
    Bob Custom
    Email: bob.custom@example.com
    Summary: Security engineer skilled in Linux, Cyber Security, Cryptography, and Blockchain.
    Projects: Built decentralized protocol and secure smart contracts using Blockchain and Cryptography.
    """
    upload_resp = client.post(
        "/candidate/resumes",
        files={"file": ("bob_resume.docx", _docx_bytes(resume_text), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        headers=headers,
    )
    assert upload_resp.status_code == 201
    resume_id = upload_resp.json()["id"]

    # Custom role not present in hardcoded role catalog
    custom_role_resp = client.post(
        f"/candidate/analysis/{resume_id}",
        json={"target_role": "AI Security Systems Architect"},
        headers=headers,
    )
    assert custom_role_resp.status_code == 200
    data = custom_role_resp.json()
    assert data["target_role"] == "AI Security Systems Architect"
    assert data["role_source"] == "CUSTOM_ROLE"
    assert data["analysis_type"] == "ROLE_COMPATIBILITY"
    assert data["score_type"] == "ROLE_COMPATIBILITY"
    assert data["match_score"] is not None
    assert len(data["detected_skills"]) > 0


def test_jd_based_standalone_analysis() -> None:
    _clear_test_db()
    headers, _ = _register_and_login_candidate("Carol JD", "carol.jd@example.com")

    resume_text = "Carol Developer\nEmail: carol@example.com\nPython, Docker, Kubernetes, Git, SQL"
    upload_resp = client.post(
        "/candidate/resumes",
        files={"file": ("carol_resume.pdf", _pdf_bytes(resume_text), "application/pdf")},
        headers=headers,
    )
    resume_id = upload_resp.json()["id"]

    jd_resp = client.post(
        f"/candidate/analysis/{resume_id}",
        json={
            "target_role": "DevOps Specialist",
            "job_description": "We are seeking a DevOps Specialist. Required: Python, Docker, Git. Preferred: Kubernetes.",
        },
        headers=headers,
    )
    assert jd_resp.status_code == 200
    data = jd_resp.json()
    assert data["score_type"] == "JOB_MATCH"
    assert data["analysis_type"] == "JOB_MATCH"
    assert data["role_source"] == "JOB_DESCRIPTION"
    assert data["requirements_source"] == "COMPANY_JD"


def test_candidate_data_isolation_and_unauthorized_access() -> None:
    _clear_test_db()

    # Candidate A
    headers_a, _ = _register_and_login_candidate("Candidate A", "cand_a@example.com")
    upload_a = client.post(
        "/candidate/resumes",
        files={"file": ("cand_a.pdf", _pdf_bytes("Candidate A with Python"), "application/pdf")},
        headers=headers_a,
    )
    resume_id_a = upload_a.json()["id"]
    client.post(f"/candidate/analysis/{resume_id_a}", json={"target_role": "Python Developer"}, headers=headers_a)
    client.post(f"/candidate/reports/{resume_id_a}/generate", headers=headers_a)

    # Candidate B
    headers_b, _ = _register_and_login_candidate("Candidate B", "cand_b@example.com")

    # Candidate B tries to access Candidate A's resume
    assert client.get(f"/candidate/resumes/{resume_id_a}", headers=headers_b).status_code == 404

    # Candidate B tries to access Candidate A's analysis
    assert client.get(f"/candidate/analysis/{resume_id_a}", headers=headers_b).status_code == 404

    # Candidate B tries to analyze Candidate A's resume
    assert client.post(f"/candidate/analysis/{resume_id_a}", json={"target_role": "Python Developer"}, headers=headers_b).status_code == 404

    # Candidate B tries to access Candidate A's report
    assert client.get(f"/candidate/reports/{resume_id_a}", headers=headers_b).status_code == 404

    # Candidate B tries to generate report for Candidate A's resume
    assert client.post(f"/candidate/reports/{resume_id_a}/generate", headers=headers_b).status_code == 404

    # Unauthenticated requests are rejected
    assert client.get(f"/candidate/resumes/{resume_id_a}").status_code == 401
    assert client.get(f"/candidate/analysis/{resume_id_a}").status_code == 401
    assert client.get(f"/candidate/reports/{resume_id_a}").status_code == 401
