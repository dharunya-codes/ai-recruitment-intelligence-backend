from __future__ import annotations

import re
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}
DISALLOWED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

SOURCE_GITHUB = "GitHub"
SOURCE_ARBEITNOW = "Arbeitnow Public API"
SOURCE_REMOTEOK = "RemoteOK Public Feed"
SOURCE_JOBICY = "Jobicy Public Feed"
SOURCE_PUBLIC_FEED = "Public Tech Job Directory"
SOURCE_LINKEDIN_NOTICE = "LinkedIn Authorized Integration (Notice)"

SOURCE_TYPE_API = "github_api"
SOURCE_TYPE_PUBLIC_FEED = "public_feed"
SOURCE_TYPE_PUBLIC_WEB = "permitted_public_web"
SOURCE_TYPE_AUTHORIZED = "authorized_source"

LINKEDIN_POLICY_NOTICE = (
    "LinkedIn integration requires an authorized source or partner API. "
    "Direct automated scraping of private profiles or bypassing access controls is not performed."
)


def validate_source_url(url: str | None) -> bool:
    """Validate that a URL is a syntactically valid public HTTP/HTTPS URL."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme.lower() not in ALLOWED_SCHEMES:
            return False
        host = parsed.netloc.split(":")[0].lower()
        if not host or host in DISALLOWED_HOSTS:
            return False
        return True
    except Exception:
        return False


def sanitize_public_profile_text(text: str) -> str:
    """Sanitize raw profile text to ensure no sensitive PII is returned."""
    if not text:
        return ""
    # Strip raw email addresses
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    cleaned = re.sub(email_pattern, "[Contact via Public Profile]", text)
    # Strip phone numbers
    phone_pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b"
    cleaned = re.sub(phone_pattern, "[Phone Redacted]", cleaned)
    return cleaned.strip()
