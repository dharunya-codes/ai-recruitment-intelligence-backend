from __future__ import annotations

import json
import uuid
from pathlib import Path
from types import SimpleNamespace

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.resumes import MAX_EXTRACTED_TEXT_SIZE, MAX_RESUME_SIZE, UPLOAD_DIRECTORY, _validate_upload
from app.database.database import get_db
from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.analysis_snapshot import AnalysisSnapshot
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User
from app.models.verification import VerificationQuestion
from app.schemas.assessment import AssessmentAnswerRequest, AssessmentAnswerResponse, AssessmentResponse
from app.schemas.assessment import AssessmentResultResponse, CategoryScore, AssessmentQuestionResult
from app.schemas.candidate import (
    CandidateAnalysisRequest,
    CandidateAnalysisResponse,
    CandidateResumeResponse,
)
from app.schemas.verification import VerificationAnswerRequest, VerificationAnswerResponse, VerificationQuestionResponse
from app.services.answer_evaluation_service import evaluate_answer
from app.services.analysis_cache_service import analysis_cache, make_analysis_cache_key
from app.services.audit_service import record_audit_event
from app.services.assessment_service import EVALUATED, IN_PROGRESS, NOT_STARTED, SUBMITTED, generate_assessment_questions
from app.services.gap_engine import generate_skill_gap_summary
from app.services.matching_engine import MISSING, MATCHED, WEAK, match_resume_to_requirements
from app.services.requirement_extractor import extract_requirements
from app.services.resume_parser import extract_text_from_docx, extract_text_from_pdf
from app.services.scoring_engine import calculate_candidate_score
from app.services.skill_extractor import extract_skills
from app.services.skill_verification_service import (
    ANSWERED,
    CANDIDATE_VERIFIED,
    NO_SUPPORTING_EVIDENCE,
    NOT_VERIFIED,
    PENDING,
    extract_candidate_reported_evidence,
    generate_verification_questions,
)
from app.services.role_catalog import role_expectations
from app.utils.security import get_candidate_user

router = APIRouter(prefix="/candidate", tags=["Candidate"])


def _candidate_record(user: User, db: Session) -> Candidate:
    candidate = db.query(Candidate).filter(Candidate.user_id == user.id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    return candidate


def _get_candidate_resume(resume_id: int, user: User, db: Session) -> Resume:
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.candidate_user_id == user.id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


def _resume_response(resume: Resume) -> CandidateResumeResponse:
    return CandidateResumeResponse(
        id=resume.id,
        candidate_id=resume.candidate_id,
        job_id=resume.job_id,
        file_name=resume.file_name,
        target_role=resume.target_role,
        score_type=resume.score_type,
        created_at=resume.created_at,
    )


def _requirements_for_analysis(payload: CandidateAnalysisRequest) -> tuple[list[object], str, str]:
    if payload.job_description:
        extracted = extract_requirements(payload.job_description)
        requirements = [SimpleNamespace(id=index + 1, **item) for index, item in enumerate(extracted)]
        return requirements, "COMPANY_JD", "JOB_MATCH"
    expectations = role_expectations(payload.target_role)
    if expectations is None:
        raise HTTPException(status_code=422, detail="This role is not in the role expectation catalog; provide a job_description")
    records = [
        SimpleNamespace(id=index + 1, requirement=skill, category="SKILL", importance="REQUIRED")
        for index, skill in enumerate(expectations["skills"])
    ]
    records.extend(
        SimpleNamespace(id=len(records) + index + 1, requirement=item, category="RESPONSIBILITY", importance="PREFERRED")
        for index, item in enumerate(expectations["responsibilities"])
    )
    return records, "ROLE_BASED_EXPECTATIONS", "ROLE_COMPATIBILITY"


def _analysis_payload(resume: Resume) -> dict:
    data = resume.analysis_data or {}
    return data


@router.post("/resumes", response_model=CandidateResumeResponse, status_code=201)
def upload_candidate_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_candidate_user),
) -> CandidateResumeResponse:
    candidate = _candidate_record(current_user, db)
    original_name = Path(file.filename or "resume").name
    content = file.file.read(MAX_RESUME_SIZE + 1)
    if len(content) > MAX_RESUME_SIZE:
        raise HTTPException(status_code=413, detail="Resume file exceeds the 10 MB limit")
    extension = _validate_upload(original_name, file.content_type, content)
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    stored_path = UPLOAD_DIRECTORY / f"{uuid.uuid4().hex}{extension}"
    stored_path.write_bytes(content)
    try:
        extracted_text = extract_text_from_pdf(stored_path) if extension == ".pdf" else extract_text_from_docx(stored_path)
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract readable text from resume")
        if len(extracted_text) > MAX_EXTRACTED_TEXT_SIZE:
            raise HTTPException(status_code=400, detail="Extracted resume content is too large")
        resume = Resume(
            candidate_id=candidate.id,
            candidate_user_id=current_user.id,
            job_id=None,
            file_name=original_name,
            file_path=stored_path.as_posix(),
            extracted_text=extracted_text,
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        record_audit_event(db, "RESUME_UPLOAD", user_id=current_user.id, role=current_user.role, resource_type="resume", resource_id=resume.id, success=True)
        return _resume_response(resume)
    except HTTPException:
        stored_path.unlink(missing_ok=True)
        db.rollback()
        raise
    except Exception as exc:
        stored_path.unlink(missing_ok=True)
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not process resume") from exc


@router.get("/resumes", response_model=list[CandidateResumeResponse])
def list_candidate_resumes(db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> list[CandidateResumeResponse]:
    resumes = db.query(Resume).filter(Resume.candidate_user_id == current_user.id).order_by(Resume.id).all()
    return [_resume_response(resume) for resume in resumes]


@router.get("/resumes/{resume_id}", response_model=CandidateResumeResponse)
def get_candidate_resume(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> CandidateResumeResponse:
    return _resume_response(_get_candidate_resume(resume_id, current_user, db))


@router.get("/me")
def candidate_me(current_user: User = Depends(get_candidate_user)) -> dict:
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role, "created_at": current_user.created_at}


@router.post("/analysis/{resume_id}", response_model=CandidateAnalysisResponse)
def analyze_candidate_resume(
    resume_id: int,
    payload: CandidateAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_candidate_user),
) -> CandidateAnalysisResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    requirements, source, score_type = _requirements_for_analysis(payload)
    if not requirements:
        raise HTTPException(status_code=422, detail="No analyzable requirements were found")
    requirement_context = [
        {"id": item.id, "requirement": item.requirement, "category": item.category, "importance": item.importance}
        for item in requirements
    ]
    cache_key = make_analysis_cache_key(
        owner_scope=current_user.id,
        resume_text=resume.extracted_text or "",
        job_context={"source": source, "description": payload.job_description, "requirements": requirement_context},
        target_role=payload.target_role,
    )

    def compute_analysis() -> dict:
        matches = match_resume_to_requirements(resume.extracted_text or "", requirements)
        score = calculate_candidate_score(matches)
        return {
            "target_role": payload.target_role,
            "requirements_source": source,
            "score_type": score_type,
            "overall_match_score": score.get("overall_match_score"),
            "required_score": score.get("required_score"),
            "preferred_score": score.get("preferred_score"),
            "score_status": score.get("score_status"),
            "detected_skills": extract_skills(resume.extracted_text or ""),
            "matched_requirements": [item for item in matches if item["match_status"] == MATCHED],
            "weak_requirements": [item for item in matches if item["match_status"] == WEAK],
            "missing_requirements": [item for item in matches if item["match_status"] == MISSING],
            "requirement_analysis": score.get("requirement_analysis", []),
            "category_breakdown": score.get("category_breakdown", {}),
            "counts": score.get("counts", {}),
            "skill_gap": generate_skill_gap_summary(matches),
        }

    data = analysis_cache.get_or_compute(cache_key, compute_analysis)
    score = {"overall_match_score": data["overall_match_score"]}
    resume.target_role = payload.target_role
    resume.target_job_description = payload.job_description
    resume.score_type = score_type
    resume.analysis_data = data
    db.commit()
    db.add(
        AnalysisSnapshot(
            candidate_user_id=current_user.id,
            resume_id=resume.id,
            target_role=payload.target_role,
            overall_score=score.get("overall_match_score"),
            analysis_data=data,
        )
    )
    db.commit()
    return CandidateAnalysisResponse(resume_id=resume.id, **data)


@router.get("/analyses", response_model=list[CandidateAnalysisResponse])
def list_candidate_analyses(db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> list[CandidateAnalysisResponse]:
    resumes = db.query(Resume).filter(Resume.candidate_user_id == current_user.id, Resume.analysis_data.isnot(None)).order_by(Resume.id).all()
    return [CandidateAnalysisResponse(resume_id=resume.id, **_analysis_payload(resume)) for resume in resumes]


def _candidate_matches(resume: Resume) -> list[dict]:
    data = _analysis_payload(resume)
    return data.get("requirement_analysis", [])


@router.post("/verification/{resume_id}/generate", response_model=list[VerificationQuestionResponse])
def generate_candidate_verification(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> list[VerificationQuestionResponse]:
    resume = _get_candidate_resume(resume_id, current_user, db)
    matches = _candidate_matches(resume)
    if not matches:
        raise HTTPException(status_code=422, detail="Analyze the resume before starting verification")
    existing = db.query(VerificationQuestion).filter(VerificationQuestion.resume_id == resume.id).order_by(VerificationQuestion.id).all()
    if not existing:
        generated = generate_verification_questions(matches, resume.extracted_text or "")
        for item in generated:
            db.add(VerificationQuestion(resume_id=resume.id, candidate_id=resume.candidate_id, skill=str(item["skill"]), question=str(item["question"]), status=PENDING, evidence_status=NOT_VERIFIED))
        db.commit()
        existing = db.query(VerificationQuestion).filter(VerificationQuestion.resume_id == resume.id).order_by(VerificationQuestion.id).all()
    context = {str(item["skill"]): item for item in generate_verification_questions(matches, resume.extracted_text or "")}
    return [VerificationQuestionResponse(id=item.id, resume_id=item.resume_id, skill=item.skill, question=item.question, priority=str(context.get(item.skill, {}).get("priority", "LOW")), question_type=str(context.get(item.skill, {}).get("question_type", "SKILL_USAGE")), status=item.status or PENDING, evidence_status=item.evidence_status or NOT_VERIFIED) for item in existing]


@router.post("/verification/questions/{question_id}/answer", response_model=VerificationAnswerResponse)
def answer_candidate_verification(question_id: int, payload: VerificationAnswerRequest, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> VerificationAnswerResponse:
    question = db.query(VerificationQuestion).filter(VerificationQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Verification question not found")
    _get_candidate_resume(question.resume_id, current_user, db)
    answer = payload.answer.strip()
    reported = extract_candidate_reported_evidence(answer)
    question.answer = answer
    question.status = ANSWERED
    question.evidence_status = CANDIDATE_VERIFIED if reported else NO_SUPPORTING_EVIDENCE
    question.candidate_reported_evidence = reported
    db.commit()
    return VerificationAnswerResponse(id=question.id, skill=question.skill, status=question.status, evidence_status=question.evidence_status, candidate_reported_evidence=reported)


@router.post("/assessment/{resume_id}/generate", response_model=AssessmentResponse)
def generate_candidate_assessment(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> AssessmentResponse:
    resume = _get_candidate_resume(resume_id, current_user, db)
    if not _candidate_matches(resume):
        raise HTTPException(status_code=422, detail="Analyze the resume before starting an assessment")
    existing = db.query(Assessment).filter(Assessment.resume_id == resume.id, Assessment.status.in_([NOT_STARTED, IN_PROGRESS])).order_by(Assessment.id.desc()).first()
    if existing:
        from app.api.assessment import _assessment_response
        return _assessment_response(existing)
    assessment = Assessment(candidate_id=resume.candidate_id, job_id=None, resume_id=resume.id, status=NOT_STARTED)
    db.add(assessment)
    db.flush()
    for item in generate_assessment_questions(_candidate_matches(resume), resume.extracted_text or ""):
        db.add(AssessmentQuestion(assessment_id=assessment.id, question=item["question"], skill=item["skill"], question_type=item["question_type"], difficulty=item["difficulty"], expected_concepts=item.get("expected_concepts")))
    db.commit()
    db.refresh(assessment)
    from app.api.assessment import _assessment_response
    return _assessment_response(assessment)


@router.post("/assessment/questions/{question_id}/answer", response_model=AssessmentAnswerResponse)
def answer_candidate_assessment(question_id: int, payload: AssessmentAnswerRequest, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> AssessmentAnswerResponse:
    question = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Assessment question not found")
    assessment = db.query(Assessment).filter(Assessment.id == question.assessment_id).first()
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    _get_candidate_resume(assessment.resume_id, current_user, db)
    if assessment.status in {SUBMITTED, EVALUATED}:
        raise HTTPException(status_code=422, detail="Assessment is no longer accepting answers")
    answer = db.query(CandidateAnswer).filter(CandidateAnswer.question_id == question.id).order_by(CandidateAnswer.id.desc()).first()
    if answer is None:
        answer = CandidateAnswer(question_id=question.id)
        db.add(answer)
    answer.answer = payload.answer.strip() if payload.answer else None
    answer.started_at = payload.started_at
    answer.submitted_at = payload.submitted_at
    answer.typing_duration = payload.typing_duration
    answer.paste_attempt_detected = bool(payload.paste_attempt_detected)
    if assessment.status == NOT_STARTED:
        assessment.status = IN_PROGRESS
    db.commit()
    db.refresh(answer)
    return AssessmentAnswerResponse(id=answer.id, question_id=question.id, assessment_id=assessment.id, status=assessment.status or IN_PROGRESS, score=answer.score, feedback=answer.feedback)


@router.post("/assessment/{assessment_id}/submit", response_model=AssessmentResponse)
def submit_candidate_assessment(assessment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> AssessmentResponse:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    _get_candidate_resume(assessment.resume_id, current_user, db)
    if assessment.status in {SUBMITTED, EVALUATED}:
        raise HTTPException(status_code=422, detail="Assessment is no longer accepting submissions")
    questions = assessment.assessment_questions
    answers = {item.question_id for item in db.query(CandidateAnswer).filter(CandidateAnswer.question_id.in_([item.id for item in questions])).all() if item.answer and item.answer.strip()}
    if len(answers) != len(questions):
        raise HTTPException(status_code=422, detail="All assessment questions must be answered before submission")
    assessment.status = SUBMITTED
    db.commit()
    record_audit_event(db, "ASSESSMENT_SUBMITTED", user_id=current_user.id, role=current_user.role, resource_type="assessment", resource_id=assessment.id, success=True)
    from app.api.assessment import _assessment_response
    return _assessment_response(assessment)


@router.post("/assessment/{assessment_id}/evaluate", response_model=AssessmentResultResponse)
def evaluate_candidate_assessment(assessment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_candidate_user)) -> AssessmentResultResponse:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    _get_candidate_resume(assessment.resume_id, current_user, db)
    if assessment.status == EVALUATED:
        from app.api.assessment import _stored_result
        return _stored_result(assessment)
    if assessment.status != SUBMITTED:
        raise HTTPException(status_code=422, detail="Only submitted assessments can be evaluated")
    category_totals: dict[str, dict[str, float]] = {}
    strengths: list[str] = []
    improvements: list[str] = []
    question_results: list[AssessmentQuestionResult] = []
    answered = 0
    for question in assessment.assessment_questions:
        answer = max(question.candidate_answers, key=lambda item: item.id, default=None)
        result = evaluate_answer(question, answer.answer if answer else None)
        if answer is None:
            answer = CandidateAnswer(question_id=question.id)
            db.add(answer)
        answer.score = result.score
        answer.feedback = result.feedback
        answer.evaluation_status = result.evaluation_status
        answer.strengths = json.dumps(result.strengths)
        answer.missing_points = json.dumps(result.missing_points)
        answered += result.evaluation_status != "NO_ANSWER"
        category = question.question_type or "OTHER"
        totals = category_totals.setdefault(category, {"obtained": 0, "total": 0, "answered": 0})
        totals["obtained"] += result.score
        totals["total"] += result.max_score
        totals["answered"] += result.evaluation_status != "NO_ANSWER"
        question_results.append(AssessmentQuestionResult(question_id=question.id, question=question.question, skill=question.skill, question_type=question.question_type, score=result.score, max_score=result.max_score, evaluation_status=result.evaluation_status, feedback=result.feedback, strengths=result.strengths, missing_points=result.missing_points))
        if result.score >= 8:
            strengths.append(f"Strong understanding of {question.skill or 'the assessed topic'}.")
        if result.score <= 6:
            improvements.append(f"Review {question.skill or 'the assessed topic'} concepts.")
    possible = sum(item["total"] for item in category_totals.values())
    obtained = sum(item["obtained"] for item in category_totals.values())
    categories = {key: {"score": round(value["obtained"] / value["total"] * 100, 2) if value["total"] else 0.0, "answered": int(value["answered"]), "total": int(value["total"] / 10)} for key, value in category_totals.items()}
    assessment.score = round(obtained / possible * 100, 2) if possible else 0.0
    assessment.total_questions = len(assessment.assessment_questions)
    assessment.answered = answered
    assessment.unanswered = assessment.total_questions - answered
    assessment.category_scores = json.dumps(categories)
    assessment.strengths = json.dumps(list(dict.fromkeys(strengths)))
    assessment.areas_for_improvement = json.dumps(list(dict.fromkeys(improvements)))
    assessment.status = EVALUATED
    db.commit()
    db.refresh(assessment)
    from app.api.assessment import _stored_result
    return _stored_result(assessment)