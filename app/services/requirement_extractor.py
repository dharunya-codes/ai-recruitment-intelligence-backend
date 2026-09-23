from __future__ import annotations

import re
from collections.abc import Iterable

REQUIRED_INDICATORS = (
    "required",
    "must have",
    "mandatory",
    "should have",
    "essential",
    "minimum",
    "required skills",
)
PREFERRED_INDICATORS = (
    "preferred",
    "nice to have",
    "desirable",
    "plus",
    "advantage",
    "would be a plus",
)

SKILLS = (
    "Penetration Testing",
    "Digital Forensics",
    "Incident Response",
    "Network Security",
    "Cyber Security",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "REST API",
    "JavaScript",
    "TypeScript",
    "PostgreSQL",
    "MongoDB",
    "Cryptography",
    "Ethical Hacking",
    "Python",
    "Java",
    "React",
    "Node.js",
    "FastAPI",
    "Flask",
    "MySQL",
    "Linux",
    "Docker",
    "AWS",
    "Azure",
    "GCP",
    "SIEM",
    "SOC",
    "Power BI",
    "Excel",
    "HTML",
    "CSS",
    "SQL",
    "Git",
    "C++",
    "C",
)

EDUCATION = (
    "Bachelor of Engineering",
    "Bachelor of Technology",
    "B.Tech",
    "B.E.",
    "B.Sc",
    "M.Tech",
    "M.E.",
    "MCA",
    "Computer Science",
    "Information Technology",
    "Cyber Security",
    "Electronics",
    "related field",
)
EDUCATION_DEGREES = {
    "Bachelor of Engineering",
    "Bachelor of Technology",
    "B.Tech",
    "B.E.",
    "B.Sc",
    "M.Tech",
    "M.E.",
    "MCA",
}

CERTIFICATIONS = (
    "Security+",
    "CISSP",
    "CISA",
    "CCNA",
    "CEH",
    "AWS Certified",
    "Azure Certification",
    "Google Cloud Certification",
)


def _sentences(text: str) -> Iterable[str]:
    separators = r"(?<=[!?;])\s+|(?<=\.)\s+(?=[A-Z0-9])|\n+"
    return (sentence.strip() for sentence in re.split(separators, text) if sentence.strip())


def _importance(context: str, default: str = "REQUIRED") -> str:
    lowered = context.lower()
    if any(indicator in lowered for indicator in PREFERRED_INDICATORS):
        return "PREFERRED"
    if any(indicator in lowered for indicator in REQUIRED_INDICATORS):
        return "REQUIRED"
    return default


def _contains(text: str, phrase: str) -> bool:
    pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _add_requirement(
    requirements: list[dict[str, str]],
    seen: set[str],
    requirement: str,
    category: str,
    importance: str,
) -> None:
    key = requirement.casefold()
    if key in seen:
        return
    seen.add(key)
    requirements.append(
        {
            "requirement": requirement,
            "category": category,
            "importance": importance,
        }
    )


def extract_requirements(jd_text: str) -> list[dict[str, str]]:
    """Extract explainable requirement records from normalized JD text."""
    requirements: list[dict[str, str]] = []
    seen: set[str] = set()

    sentences = list(_sentences(jd_text))

    for sentence in sentences:
        has_education_context = (
            any(_contains(sentence, phrase) for phrase in EDUCATION_DEGREES)
            or "education" in sentence.lower()
            or "degree" in sentence.lower()
        )
        for phrase in EDUCATION:
            if _contains(sentence, phrase) and (
                phrase in EDUCATION_DEGREES or has_education_context
            ):
                _add_requirement(
                    requirements,
                    seen,
                    phrase,
                    "EDUCATION",
                    _importance(sentence),
                )

    for sentence in sentences:
        for phrase in CERTIFICATIONS:
            if _contains(sentence, phrase):
                _add_requirement(
                    requirements,
                    seen,
                    phrase,
                    "CERTIFICATION",
                    _importance(sentence),
                )

    experience_patterns = (
        r"(?<![\d-])\b\d+\s*[-–]\s*\d+\s+years?(?:\s+of)?\s+experience\b",
        r"(?<![\d-])\b\d+\+\s+years?(?:\s+of)?\s+experience\b",
        r"(?<![\d-])\b(?:minimum\s+)?\d+\s+years?(?:\s+of)?\s+experience\b",
        r"\bfreshers?\b",
        r"\bentry[- ]level\b",
    )
    for sentence in sentences:
        for pattern in experience_patterns:
            for match in re.finditer(pattern, sentence, flags=re.IGNORECASE):
                phrase = match.group(0)
                _add_requirement(
                    requirements,
                    seen,
                    phrase,
                    "EXPERIENCE",
                    _importance(sentence),
                )

    for sentence in sentences:
        for phrase in SKILLS:
            if _contains(sentence, phrase):
                _add_requirement(
                    requirements,
                    seen,
                    phrase,
                    "SKILL",
                    _importance(sentence),
                )

    responsibility_pattern = re.compile(
        r"(?:responsible for|responsibilities include|will be responsible for|"
        r"duties include|you will)\s+(.+)",
        flags=re.IGNORECASE,
    )
    for sentence in sentences:
        match = responsibility_pattern.search(sentence)
        if match:
            _add_requirement(
                requirements,
                seen,
                match.group(1).strip(),
                "RESPONSIBILITY",
                "REQUIRED",
            )

    return requirements