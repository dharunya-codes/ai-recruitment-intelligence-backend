from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.resumes import _get_company_resume
from app.database.database import get_db
from app.models.requirement import JobRequirement
from app.models.resume import Resume
from app.models.user import User
from app.models.verification import VerificationQuestion
from app.schemas.analysis import RequirementMatch
from app.schemas.verification import (
    VerificationAnswerRequest,
    VerificationAnswerResponse,
    VerificationQuestionResponse,
    VerificationStatusItem,
    VerificationStatusResponse,
)
from app.services.matching_engine import match_resume_to_requirements
from app.services.skill_verification_service import (
    ANSWERED,
    CANDIDATE_VERIFIED,
    NO_SUPPORTING_EVIDENCE,
    NOT_VERIFIED,
    PENDING,
    extract_candidate_reported_evidence,
    generate_verification_questions,
)
from app.utils.security import get_company_user

router = APIRouter(prefix="/verification", tags=["Verification"])


def _question_response(question: VerificationQuestion, priority: str, question_type: str) -> VerificationQuestionResponse:
    return VerificationQuestionResponse(
        id=question.id,
        resume_id=question.resume_id,
        skill=question.skill,
        question=question.question,
        priority=priority,
        question_type=question_type,
        status=question.status or PENDING,
        evidence_status=question.evidence_status or NOT_VERIFIED,
    )


def _question_context(resume: Resume, db: Session) -> list[dict[str, object]]:
    requirements = (
        db.query(JobRequirement)
        .filter(JobRequirement.job_id == resume.job_id)
        .order_by(JobRequirement.id)
        .all()
    )
    matches = match_resume_to_requirements(resume.extracted_text or "", requirements)
    return generate_verification_questions(matches, resume.extracted_text or "")


def _existing_question_response(question: VerificationQuestion, context: list[dict[str, object]]) -> VerificationQuestionResponse:
    match = next((item for item in context if item["skill"] == question.skill), None)
    if match is None:
        return _question_response(question, "LOW", "SKILL_USAGE")
    return _question_response(question, str(match["priority"]), str(match["question_type"]))


@router.post("/{resume_id}/generate", response_model=list[VerificationQuestionResponse])
def generate_questions(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> list[VerificationQuestionResponse]:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    existing = (
        db.query(VerificationQuestion)
        .filter(VerificationQuestion.resume_id == resume.id)
        .order_by(VerificationQuestion.id)
        .all()
    )
    context = _question_context(resume, db)
    if existing:
        return [_existing_question_response(question, context) for question in existing]

    questions = []
    for item in context:
        question = VerificationQuestion(
            resume_id=resume.id,
            candidate_id=resume.candidate_id,
            skill=str(item["skill"]),
            question=str(item["question"]),
            status=PENDING,
            evidence_status=NOT_VERIFIED,
        )
        db.add(question)
        questions.append((question, item))
    db.commit()
    return [
        _question_response(question, str(item["priority"]), str(item["question_type"]))
        for question, item in questions
    ]


@router.get("/{resume_id}/questions", response_model=list[VerificationQuestionResponse])
def get_questions(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> list[VerificationQuestionResponse]:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    context = _question_context(resume, db)
    questions = (
        db.query(VerificationQuestion)
        .filter(VerificationQuestion.resume_id == resume.id)
        .order_by(VerificationQuestion.id)
        .all()
    )
    return [_existing_question_response(question, context) for question in questions]


@router.post("/questions/{question_id}/answer", response_model=VerificationAnswerResponse)
def submit_answer(
    question_id: int,
    payload: VerificationAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> VerificationAnswerResponse:
    question = db.query(VerificationQuestion).filter(VerificationQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Verification question not found")
    _get_company_resume(question.resume_id, current_user.company_id, db)

    answer = payload.answer.strip()
    reported_evidence = extract_candidate_reported_evidence(answer)
    question.answer = answer
    question.status = ANSWERED
    question.evidence_status = CANDIDATE_VERIFIED if reported_evidence else NO_SUPPORTING_EVIDENCE
    question.candidate_reported_evidence = reported_evidence
    db.commit()
    db.refresh(question)
    return VerificationAnswerResponse(
        id=question.id,
        skill=question.skill,
        status=question.status,
        evidence_status=question.evidence_status,
        candidate_reported_evidence=question.candidate_reported_evidence,
    )


@router.get("/{resume_id}/status", response_model=VerificationStatusResponse)
def get_verification_status(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_company_user),
) -> VerificationStatusResponse:
    resume = _get_company_resume(resume_id, current_user.company_id, db)
    questions = (
        db.query(VerificationQuestion)
        .filter(VerificationQuestion.resume_id == resume.id)
        .order_by(VerificationQuestion.id)
        .all()
    )
    answered = sum(question.status == ANSWERED for question in questions)
    return VerificationStatusResponse(
        resume_id=resume.id,
        total_questions=len(questions),
        answered=answered,
        pending=len(questions) - answered,
        verification_items=[
            VerificationStatusItem(
                skill=question.skill,
                question=question.question,
                status=question.status or PENDING,
                evidence_status=question.evidence_status or NOT_VERIFIED,
                candidate_reported_evidence=question.candidate_reported_evidence,
            )
            for question in questions
        ],
    )