from __future__ import annotations

import json
import re
from collections.abc import Iterable

from app.services.matching_engine import MISSING, MATCHED, WEAK
from app.services.answer_evaluation_service import expected_concepts_for_question

NOT_STARTED = "NOT_STARTED"
IN_PROGRESS = "IN_PROGRESS"
SUBMITTED = "SUBMITTED"
EVALUATED = "EVALUATED"

QUESTION_DISTRIBUTION = (
    ("TECHNICAL", ("MEDIUM", "MEDIUM", "HARD", "HARD")),
    ("SCENARIO", ("MEDIUM", "MEDIUM", "HARD")),
    ("PROBLEM_SOLVING", ("MEDIUM", "MEDIUM", "HARD")),
)

SKILL_TEMPLATES: dict[str, dict[str, tuple[str, ...]]] = {
    "SIEM": {
        "TECHNICAL": ("What is the purpose of a SIEM in a Security Operations Center?",),
        "SCENARIO": ("You observe repeated failed login attempts from one external IP address. How would you investigate the SIEM alerts?",),
        "PROBLEM_SOLVING": ("You detect unusual outbound traffic from an internal workstation. Explain your investigation workflow using SIEM data.",),
    },
    "SQL": {
        "TECHNICAL": ("What is the difference between INNER JOIN and LEFT JOIN in SQL?", "What is the purpose of GROUP BY in SQL?"),
        "SCENARIO": ("A sales dataset contains duplicate customer records. How would you identify and handle them with SQL?",),
        "PROBLEM_SOLVING": ("You receive a slow SQL query over a large table. Describe how you would investigate and improve it.",),
    },
    "Python": {
        "TECHNICAL": ("How would you use Python modules, exceptions, and tests in a maintainable application?",),
        "SCENARIO": ("A Python service starts returning intermittent errors after deployment. How would you investigate it?",),
        "PROBLEM_SOLVING": ("Describe an approach for designing a Python service that validates input and handles failures safely.",),
    },
    "Docker": {
        "TECHNICAL": ("What is the purpose of a Docker image and container?",),
        "SCENARIO": ("A Dockerized application works locally but fails in deployment. What would you check first?",),
        "PROBLEM_SOLVING": ("Explain how you would containerize a Python Flask application using Docker.",),
    },
    "FastAPI": {
        "TECHNICAL": ("How do dependency injection and request validation work in FastAPI?",),
        "SCENARIO": ("A FastAPI endpoint returns unexpected validation errors. How would you diagnose the request and schema?",),
        "PROBLEM_SOLVING": ("Design a basic FastAPI approach for authentication and authorization in a REST API.",),
    },
    "REST API": {
        "TECHNICAL": ("What are the purposes of HTTP methods and status codes in a REST API?",),
        "SCENARIO": ("An API suddenly starts returning 500 errors after deployment. How would you investigate?",),
        "PROBLEM_SOLVING": ("Design a basic approach for handling authentication and authorization in a REST API.",),
    },
    "Java": {
        "TECHNICAL": ("Explain method overloading and method overriding in Java.",),
        "SCENARIO": ("A Java service has slow response times after a release. How would you investigate?",),
        "PROBLEM_SOLVING": ("Describe how you would design the data layer for a Java application.",),
    },
    "Cyber Security": {
        "TECHNICAL": ("What is the difference between authentication and authorization?",),
        "SCENARIO": ("A user reports receiving a suspicious phishing email. Describe your investigation steps.",),
        "PROBLEM_SOLVING": ("A workstation is suspected of being compromised. Describe your investigation workflow.",),
    },
    "Network Security": {
        "TECHNICAL": ("What is the purpose of network segmentation in security?",),
        "SCENARIO": ("You detect an unexpected open service on an internal host. How would you investigate it?",),
        "PROBLEM_SOLVING": ("Design a practical approach for identifying and containing suspicious network traffic.",),
    },
    "Data Analysis": {
        "TECHNICAL": ("How do you validate a dataset before performing data analysis?",),
        "SCENARIO": ("A report shows a sudden unexpected sales trend. How would you investigate the data?",),
        "PROBLEM_SOLVING": ("You receive a dataset with missing values and inconsistent date formats. Describe your preprocessing approach.",),
    },
    "Power BI": {
        "TECHNICAL": ("What is the purpose of a measure and a relationship in Power BI?",),
        "SCENARIO": ("A Power BI dashboard shows numbers that do not match the source data. How would you troubleshoot it?",),
        "PROBLEM_SOLVING": ("Describe how you would design a Power BI dashboard for operational reporting.",),
    },
    "Excel": {
        "TECHNICAL": ("How would you use pivot tables and lookup functions in Excel?",),
        "SCENARIO": ("An Excel report contains duplicate and inconsistent records. How would you clean it?",),
        "PROBLEM_SOLVING": ("Describe a repeatable Excel workflow for transforming raw data into a report.",),
    },
}


def _value(item: object, key: str) -> object:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key)


def _priority(match: object) -> int:
    importance = str(_value(match, "importance") or "REQUIRED").upper()
    status = str(_value(match, "match_status")).upper()
    if importance == "REQUIRED" and status == MISSING:
        return 0
    if importance == "REQUIRED" and status == WEAK:
        return 1
    if importance == "REQUIRED" and status == MATCHED:
        return 2
    if importance == "PREFERRED" and status == WEAK:
        return 3
    return 4


def _canonical_skill(skill: str) -> str:
    return next((name for name in SKILL_TEMPLATES if name.casefold() == skill.casefold()), skill)


def _fallback(skill: str, question_type: str) -> str:
    if question_type == "TECHNICAL":
        return f"What are the main concepts of {skill}, and where would you apply them?"
    if question_type == "SCENARIO":
        return f"You are working on a role that requires {skill}. Describe how you would approach a practical problem involving it."
    return f"A system using {skill} is producing unexpected results. Describe how you would investigate and solve the issue."


def _question_for(skill: str, question_type: str, index: int) -> str:
    canonical = _canonical_skill(skill)
    templates = SKILL_TEMPLATES.get(canonical, {}).get(question_type, ())
    if templates:
        return templates[index % len(templates)]
    return _fallback(skill, question_type)


def _resume_context_question(skill: str, question_type: str, resume_text: str) -> str | None:
    for line in resume_text.splitlines():
        clean_line = line.strip()
        if skill.casefold() in clean_line.casefold() and re.search(
            r"project|built|developed|created|implemented", clean_line, re.IGNORECASE
        ):
            return f"Your resume mentions: '{clean_line}'. Explain the design decisions and challenges in that work involving {skill}."
    return None


def generate_assessment_questions(
    requirement_matches: Iterable[object],
    resume_text: str,
    verification_evidence: Iterable[str] = (),
) -> list[dict[str, str]]:
    matches = sorted(requirement_matches, key=_priority)
    usable = [match for match in matches if str(_value(match, "importance") or "REQUIRED").upper() != "PREFERRED" or str(_value(match, "match_status")).upper() != MISSING]
    if not usable:
        return []

    questions: list[dict[str, str]] = []
    for question_type, difficulties in QUESTION_DISTRIBUTION:
        for index, difficulty in enumerate(difficulties):
            match = usable[len(questions) % len(usable)]
            skill = str(_value(match, "requirement"))
            question = _resume_context_question(skill, question_type, resume_text)
            if question is None:
                question = _question_for(skill, question_type, index)
            questions.append(
                {
                    "question": question,
                    "skill": skill,
                    "question_type": question_type,
                    "difficulty": difficulty,
                    "expected_concepts": json.dumps(
                        expected_concepts_for_question(
                            type("QuestionSpec", (), {"question": question, "skill": skill})()
                        )
                    ),
                }
            )
            if len(questions) == 10:
                return questions
    return questions