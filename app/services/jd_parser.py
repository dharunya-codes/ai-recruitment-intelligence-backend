from __future__ import annotations

import re


def parse_jd(description: str) -> str:
    """Normalize whitespace while preserving the original JD's wording."""
    return re.sub(r"\s+", " ", description).strip()