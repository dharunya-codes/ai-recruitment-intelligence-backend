from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

ALLOWED_JOB_SOURCES: set[str] = {
    "MOCK_PUBLIC_JOB_SOURCE",
    "OPEN_PUBLIC_JOB_FEED",
    "PUBLIC_TECH_CAREERS",
    "PUBLIC_GITHUB_JOBS_ARCHIVE",
}

ALLOWED_CANDIDATE_SOURCES: set[str] = {
    "MOCK_PUBLIC_CANDIDATE_SOURCE",
    "OPEN_PUBLIC_DEVELOPER_FEED",
    "PUBLIC_OPEN_SOURCE_CONTRIBUTORS",
}

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_PATTERN = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")


def sanitize_search_query(query: str) -> str:
    """Sanitize user input query and strip unsafe characters while preserving valid technical keywords."""
    if not query:
        return ""
    cleaned = query.strip()
    # Strip dangerous injection characters while preserving letters, numbers, spaces, and standard punctuation
    cleaned = re.sub(r"[^\w\s\+\#\.\,\-\_]", "", cleaned)
    return cleaned[:100].strip()


def validate_source_url(url: str | None) -> bool:
    """Validate that a supplied URL uses http/https scheme and is well-formed."""
    if not url:
        return True
    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def is_job_source_allowed(source_name: str) -> bool:
    """Check if the job source is in the permitted allowlist."""
    return source_name.upper() in ALLOWED_JOB_SOURCES


def is_candidate_source_allowed(source_name: str) -> bool:
    """Check if the candidate profile source is in the permitted allowlist."""
    return source_name.upper() in ALLOWED_CANDIDATE_SOURCES


def sanitize_public_candidate_profile(raw_profile: dict[str, Any]) -> dict[str, Any]:
    """
    Enforces privacy and legal data minimization by stripping any accidentally
    scraped personal contact information (email addresses, phone numbers, direct messages).
    """
    cleaned = dict(raw_profile)
    for field in ("headline", "experience", "projects", "education", "name"):
        val = cleaned.get(field)
        if isinstance(val, str):
            val = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", val)
            val = PHONE_PATTERN.sub("[REDACTED_PHONE]", val)
            cleaned[field] = val
        elif isinstance(val, list):
            cleaned[field] = [
                PHONE_PATTERN.sub("[REDACTED_PHONE]", EMAIL_PATTERN.sub("[REDACTED_EMAIL]", str(item)))
                for item in val
            ]
    # Explicitly remove any private contact keys if present
    for private_key in ("email", "phone", "phone_number", "address", "ssn", "dob"):
        cleaned.pop(private_key, None)
    return cleaned


def enforce_bounds(limit: int, min_val: int = 1, max_val: int = 50, default: int = 10) -> int:
    """Enforces bounds on pagination and result limits."""
    try:
        val = int(limit)
        return max(min_val, min(max_val, val))
    except (TypeError, ValueError):
        return default
