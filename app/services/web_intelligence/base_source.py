from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseJobSource(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this job source."""
        raise NotImplementedError

    @abstractmethod
    def is_enabled(self) -> bool:
        """Returns True if the source is configured and active."""
        raise NotImplementedError

    @abstractmethod
    def search_jobs(
        self,
        query: str,
        location: str | None = None,
        company: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for public job postings and return raw or semi-structured dictionaries."""
        raise NotImplementedError


class BaseCandidateSource(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this candidate profile source."""
        raise NotImplementedError

    @abstractmethod
    def is_enabled(self) -> bool:
        """Returns True if the source is configured and active."""
        raise NotImplementedError

    @abstractmethod
    def search_candidates(
        self,
        job_title: str,
        requirements: list[str] | None = None,
        location: str | None = None,
        skills_filter: list[str] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for permitted public candidate profiles and return raw dictionaries."""
        raise NotImplementedError
