from __future__ import annotations

import os
from typing import Any

from app.services.web_intelligence.base_source import BaseCandidateSource


class OpenPublicProfileSource(BaseCandidateSource):
    """
    Adapter for permitted public developer/open profile sources.
    Disabled by default until a verified permitted source is configured.
    """

    def __init__(self, api_url: str | None = None) -> None:
        self._api_url = api_url or os.getenv("OPEN_PUBLIC_PROFILE_API_URL")

    @property
    def source_name(self) -> str:
        return "OPEN_PUBLIC_DEVELOPER_FEED"

    def is_enabled(self) -> bool:
        return bool(self._api_url and os.getenv("ENABLE_LIVE_PUBLIC_PROFILE_SOURCE", "false").lower() == "true")

    def search_candidates(
        self,
        job_title: str,
        requirements: list[str] | None = None,
        location: str | None = None,
        skills_filter: list[str] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        if not self.is_enabled():
            return []
        # Safe isolation: if live provider is enabled in future, execute query with strict timeouts
        return []
