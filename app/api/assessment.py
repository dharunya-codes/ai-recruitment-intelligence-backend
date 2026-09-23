from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.resumes import _get_company_resume
from app.database.database import get_db
from app.models.assessment import Assessment, AssessmentQuestion, CandidateAnswer
from app.models.requirement import JobRequirement
from app.models.user import User
from app.models.verification import VerificationQuestion
from app.schemas.assessment import (
    AssessmentAnswerRequest,
    AssessmentAnswerResponse,
    AssessmentQuestionResponse,
    AssessmentResponse,
    AssessmentResultResponse,
    AssessmentQuestionResult,
    CategoryScore,
    AssessmentStatusResponse,
)
from app.services.assessment_service import (
    EVALUATED,
    IN_PROGRESS,
    NOT_STARTED,
    SUBMITTED,
    generate_assessment_questions,
)
from app.services.answer_evaluation_service import evaluate_answer
from app.services.matching_engine import match_resume_to_requirements
from app.utils.security import get_company_user

router = APIRouter(prefix="/assessment", tags=["Assessment"])


def _assessment_response(assessment: Assessment) -> AssessmentResponse:
    questions = [
        AssessmentQuestionResponse(
            id=question.id,
            question=question.question,
            skill=question.skill,
            question_type=question.question_type,
            difficulty=question.difficulty,
        )
        for question in assessment.assessment_questions
    ]
    return AssessmentResponse(
        id=assessment.id,
        candidate_id=assessment.candidate_id,
        job_id=assessment.job_id,
        resume_id=assessment.resume_id,
        score=assessment.score,
        status=assessment.status or NOT_STARTED,
        created_at=assessment.created_at,
        question_count=len(questions),
        questions=questions,
    )


def _get_company_assessment(assessment_id: int, company_id: int, db: Session) -> Assessment:
    assessment = (
        db.query(Assessment)
        .join(Assessment.resume)
        .join(Assessment.job)
        .filter(Assessment.id == assessment_id, Assessment.job.has(company_id=company_id))
        .first()
    )
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


def _assessment_context(resume, db: Session) -> tuple[list[dict[str, object]], list[str]]:
    requirements = (
        db.query(JobRequirement)
        .filter(JobRequirement.job_id == resume.job_id)
        .order_by(JobRequirement.id)
        .all()
    )
    matches = match_resume_to_requirements(resume.extracted_text or "", requirements)
    verification_evidence = [
        question.candidate_reported_evidence
        for question in db.query(VerificationQuestion)
        .filter(VerificationQuestion.resume_id == resume.id)
        .all()
        if question.candidate_reported_evidence
    ]
    return matches, verification_evidence


@router.post("/{resume_id}/generate", response_model=AssessmentResponse)
def generate_assessment(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    existing = (
        db.query(Assessment)
        .filter(
            Assessment.resume_id == resume.id,
            Assessment.job_id == resume.job_id,
            Assessment.status.in_([NOT_STARTED, IN_PROGRESS]),
        )
        .order_by(Assessment.id.desc())
        .first()
    )
    if existing is not None:
        return _assessment_response(existing)

    matches, verification_evidence = _assessment_context(resume, db)
    generated_questions = generate_assessment_questions(
        matches,
        resume.extracted_text or "",
        verification_evidence,
    )
    assessment = Assessment(
        candidate_id=resume.candidate_id,
        job_id=resume.job_id,
        resume_id=resume.id,
        score=None,
        status=NOT_STARTED,
    )
    db.add(assessment)
    db.flush()
    for item in generated_questions:
        db.add(
            AssessmentQuestion(
                assessment_id=assessment.id,
                question=item["question"],
                skill=item["skill"],
                question_type=item["question_type"],
                difficulty=item["difficulty"],
                expected_concepts=item["expected_concepts"],
            )
        )
    db.commit()
    db.refresh(assessment)
    return _assessment_response(assessment)


def _stored_result(assessment: Assessment) -> AssessmentResultResponse:
    category_scores = json.loads(assessment.category_scores or "{}")
    question_results = []
    for question in assessment.assessment_questions:
        answer = max(question.candidate_answers, key=lambda item: item.id, default=None)
        if answer is None:
            continue
        question_results.append(
            AssessmentQuestionResult(
                question_id=question.id,
                question=question.question,
                skill=question.skill,
                question_type=question.question_type,
                score=answer.score or 0,
                max_score=10,
                evaluation_status=answer.evaluation_status or "NO_ANSWER",
                feedback=answer.feedback or "No answer was submitted.",
                strengths=json.loads(answer.strengths or "[]"),
                missing_points=json.loads(answer.missing_points or "[]"),
            )
        )
    return AssessmentResultResponse(
        assessment_id=assessment.id,
        status=assessment.status or NOT_STARTED,
        score=assessment.score or 0,
        total_questions=assessment.total_questions or len(assessment.assessment_questions),
        answered=assessment.answered or 0,
        unanswered=assessment.unanswered or 0,
        category_scores={key: CategoryScore(**value) for key, value in category_scores.items()},
        question_results=question_results,
        strengths=json.loads(assessment.strengths or "[]"),
        areas_for_improvement=json.loads(assessment.areas_for_improvement or "[]"),
    )


@router.post("/{assessment_id}/evaluate", response_model=AssessmentResultResponse)
def evaluate_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentResultResponse:
    assessment = _get_company_assessment(assessment_id, current_user.company_id, db)
    if assessment.status == EVALUATED:
        return _stored_result(assessment)
    if assessment.status != SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only submitted assessments can be evaluated",
        )

    question_results = []
    category_totals: dict[str, dict[str, float]] = {}
    strengths: list[str] = []
    areas_for_improvement: list[str] = []
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
        if result.evaluation_status != "NO_ANSWER":
            answered += 1
        question_type = question.question_type or "OTHER"
        totals = category_totals.setdefault(question_type, {"obtained": 0, "total": 0, "answered": 0})
        totals["obtained"] += result.score
        totals["total"] += result.max_score
        if result.evaluation_status != "NO_ANSWER":
            totals["answered"] += 1
        question_results.append(
            AssessmentQuestionResult(
                question_id=question.id,
                question=question.question,
                skill=question.skill,
                question_type=question.question_type,
                score=result.score,
                max_score=result.max_score,
                evaluation_status=result.evaluation_status,
                feedback=result.feedback,
                strengths=result.strengths,
                missing_points=result.missing_points,
            )
        )
        if result.score >= 8:
            strengths.append(f"Strong understanding of {question.skill or 'the assessed topic'}.")
        if result.score <= 6:
            areas_for_improvement.append(f"Review {question.skill or 'the assessed topic'} concepts.")

    total_possible = sum(item["total"] for item in category_totals.values())
    total_obtained = sum(item["obtained"] for item in category_totals.values())
    category_scores = {
        category: {
            "score": round((values["obtained"] / values["total"]) * 100, 2) if values["total"] else 0.0,
            "answered": int(values["answered"]),
            "total": int(values["total"] / 10),
        }
        for category, values in category_totals.items()
    }
    assessment.score = round((total_obtained / total_possible) * 100, 2) if total_possible else 0.0
    assessment.total_questions = len(assessment.assessment_questions)
    assessment.answered = answered
    assessment.unanswered = assessment.total_questions - answered
    assessment.category_scores = json.dumps(category_scores)
    assessment.strengths = json.dumps(list(dict.fromkeys(strengths)))
    assessment.areas_for_improvement = json.dumps(list(dict.fromkeys(areas_for_improvement)))
    assessment.status = EVALUATED
    db.commit()
    db.refresh(assessment)
    return _stored_result(assessment)


@router.get("/{assessment_id}/result", response_model=AssessmentResultResponse)
def get_assessment_result(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentResultResponse:
    assessment = _get_company_assessment(assessment_id, current_user.company_id, db)
    if assessment.status != EVALUATED:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Assessment has not been evaluated")
    return _stored_result(assessment)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentResponse:
    return _assessment_response(_get_company_assessment(assessment_id, current_user.company_id, db))


@router.post("/questions/{question_id}/answer", response_model=AssessmentAnswerResponse)
def submit_assessment_answer(
    question_id: int,
    payload: AssessmentAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentAnswerResponse:
    question = (
        db.query(AssessmentQuestion)
        .join(Assessment)
        .filter(AssessmentQuestion.id == question_id)
        .first()
    )
    if question is None:
        raise HTTPException(status_code=404, detail="Assessment question not found")
    assessment = _get_company_assessment(question.assessment_id, current_user.company_id, db)
    if assessment.status in {SUBMITTED, EVALUATED}:
        raise HTTPException(status_code=422, detail="Assessment is no longer accepting answers")
    answer = (
        db.query(CandidateAnswer)
        .filter(CandidateAnswer.question_id == question.id)
        .order_by(CandidateAnswer.id.desc())
        .first()
    )
    if answer is None:
        answer = CandidateAnswer(question_id=question.id)
        db.add(answer)
    answer.answer = payload.answer.strip() if payload.answer else None
    answer.score = None
    answer.feedback = None
    answer.started_at = payload.started_at
    answer.submitted_at = payload.submitted_at
    answer.typing_duration = payload.typing_duration
    answer.paste_attempt_detected = bool(payload.paste_attempt_detected)
    if assessment.status == NOT_STARTED:
        assessment.status = IN_PROGRESS
    db.commit()
    db.refresh(answer)
    return AssessmentAnswerResponse(
        id=answer.id,
        question_id=question.id,
        assessment_id=assessment.id,
        status=assessment.status or IN_PROGRESS,
        score=answer.score,
        feedback=answer.feedback,
    )


@router.post("/{assessment_id}/submit", response_model=AssessmentResponse)
def submit_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentResponse:
    assessment = _get_company_assessment(assessment_id, current_user.company_id, db)
    if assessment.status in {SUBMITTED, EVALUATED}:
        raise HTTPException(status_code=422, detail="Assessment is no longer accepting submissions")
    questions = assessment.assessment_questions
    answered_ids = {
        answer.question_id
        for answer in db.query(CandidateAnswer)
        .filter(CandidateAnswer.question_id.in_([question.id for question in questions]))
        .all()
        if answer.answer and answer.answer.strip()
    }
    if len(answered_ids) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All assessment questions must be answered before submission",
        )
    assessment.status = SUBMITTED
    assessment.score = None
    db.commit()
    db.refresh(assessment)
    return _assessment_response(assessment)


@router.get("/{assessment_id}/status", response_model=AssessmentStatusResponse)
def assessment_status(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> AssessmentStatusResponse:
    assessment = _get_company_assessment(assessment_id, current_user.company_id, db)
    questions = assessment.assessment_questions
    answered = sum(
        db.query(CandidateAnswer)
        .filter(CandidateAnswer.question_id == question.id, CandidateAnswer.answer.isnot(None))
        .first()
        is not None
        for question in questions
    )
    return AssessmentStatusResponse(
        assessment_id=assessment.id,
        status=assessment.status or NOT_STARTED,
        total_questions=len(questions),
        answered=answered,
        unanswered=len(questions) - answered,
    )