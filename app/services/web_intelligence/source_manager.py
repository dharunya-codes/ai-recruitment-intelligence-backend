from __future__ import annotations

import logging
from typing import Any

from app.schemas.web_intelligence import ExternalCandidate, ExternalJob
from app.services.web_intelligence.base_source import BaseCandidateSource, BaseJobSource
from app.services.web_intelligence.candidate_sources.mock_public_candidate_source import MockPublicCandidateSource
from app.services.web_intelligence.candidate_sources.open_public_profile_source import OpenPublicProfileSource
from app.services.web_intelligence.compliance import enforce_bounds, is_candidate_source_allowed, is_job_source_allowed, sanitize_search_query
from app.services.web_intelligence.job_sources.mock_public_job_source import MockPublicJobSource
from app.services.web_intelligence.job_sources.open_public_job_feed import OpenPublicJobFeedSource
from app.services.web_intelligence.normalizer import normalize_external_candidate, normalize_external_job

logger = logging.getLogger(__name__)


class SourceManager:
    def __init__(self) -> None:
        self._job_sources: dict[str, BaseJobSource] = {}
        self._candidate_sources: dict[str, BaseCandidateSource] = {}
        self._register_default_sources()

    def _register_default_sources(self) -> None:
        # Register default compliant job sources
        self.register_job_source(MockPublicJobSource())
        self.register_job_source(OpenPublicJobFeedSource())

        # Register default compliant candidate sources
        self.register_candidate_source(MockPublicCandidateSource())
        self.register_candidate_source(OpenPublicProfileSource())

    def register_job_source(self, source: BaseJobSource) -> None:
        if is_job_source_allowed(source.source_name):
            self._job_sources[source.source_name] = source
        else:
            logger.warning("Job source %s not in allowlist; registration skipped", source.source_name)

    def register_candidate_source(self, source: BaseCandidateSource) -> None:
        if is_candidate_source_allowed(source.source_name):
            self._candidate_sources[source.source_name] = source
        else:
            logger.warning("Candidate source %s not in allowlist; registration skipped", source.source_name)

    def search_jobs(
        self,
        query: str,
        location: str | None = None,
        company: str | None = None,
        source_filter: str | None = None,
        limit: int = 10,
    ) -> list[ExternalJob]:
        sanitized_query = sanitize_search_query(query)
        if not sanitized_query:
            return []

        bounded_limit = enforce_bounds(limit, min_val=1, max_val=50, default=10)
        results: list[ExternalJob] = []
        seen_keys: set[tuple[str, str]] = set()

        for source_name, source in self._job_sources.items():
            if source_filter and source_name.casefold() != source_filter.casefold():
                continue
            if not source.is_enabled():
                continue

            try:
                raw_jobs = source.search_jobs(
                    query=sanitized_query,
                    location=location,
                    company=company,
                    limit=bounded_limit,
                )
                for raw_job in raw_jobs:
                    normalized = normalize_external_job(raw_job, default_source=source_name)
                    dedup_key = (normalized.title.casefold(), normalized.company.casefold())
                    if dedup_key not in seen_keys:
                        seen_keys.add(dedup_key)
                        results.append(normalized)
                        if len(results) >= bounded_limit:
                            return results
            except Exception as exc:
                # Source failure isolation: one failing source does not crash the entire search
                logger.error("Job source %s failed during search: %s", source_name, exc)
                continue

        return results[:bounded_limit]

    def search_candidates(
        self,
        job_title: str,
        requirements: list[str] | None = None,
        location: str | None = None,
        skills_filter: list[str] | None = None,
        source_filter: str | None = None,
        limit: int = 10,
    ) -> list[ExternalCandidate]:
        sanitized_title = sanitize_search_query(job_title)
        if not sanitized_title:
            return []

        bounded_limit = enforce_bounds(limit, min_val=1, max_val=50, default=10)
        results: list[ExternalCandidate] = []
        seen_ids: set[str] = set()

        for source_name, source in self._candidate_sources.items():
            if source_filter and source_name.casefold() != source_filter.casefold():
                continue
            if not source.is_enabled():
                continue

            try:
                raw_candidates = source.search_candidates(
                    job_title=sanitized_title,
                    requirements=requirements,
                    location=location,
                    skills_filter=skills_filter,
                    limit=bounded_limit,
                )
                for raw_cand in raw_candidates:
                    normalized = normalize_external_candidate(raw_cand, default_source=source_name)
                    if normalized.source_id not in seen_ids:
                        seen_ids.add(normalized.source_id)
                        results.append(normalized)
                        if len(results) >= bounded_limit:
                            return results
            except Exception as exc:
                logger.error("Candidate source %s failed during search: %s", source_name, exc)
                continue

        return results[:bounded_limit]


# Global singleton source manager
source_manager = SourceManager()
