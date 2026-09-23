from __future__ import annotations

import os
from typing import Any

from app.services.web_intelligence.base_source import BaseJobSource


class OpenPublicJobFeedSource(BaseJobSource):
    """
    Adapter for permitted open public structured job feeds (JSON / RSS).
    Disabled by default until a verified permitted live feed URL is configured.
    """

    def __init__(self, feed_url: str | None = None) -> None:
        self._feed_url = feed_url or os.getenv("OPEN_PUBLIC_JOB_FEED_URL")

    @property
    def source_name(self) -> str:
        return "OPEN_PUBLIC_JOB_FEED"

    def is_enabled(self) -> bool:
        # Only active if explicit permitted feed URL is configured in environment
        return bool(self._feed_url and os.getenv("ENABLE_LIVE_PUBLIC_JOB_FEED", "false").lower() == "true")

    def search_jobs(
        self,
        query: str,
        location: str | None = None,
        company: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        if not self.is_enabled():
            return []
        # When live feed integration is enabled, query the endpoint safely with timeout
        # Fallback cleanly on network isolation / unavailability
        return []
