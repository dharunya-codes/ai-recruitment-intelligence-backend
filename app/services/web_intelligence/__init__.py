from app.services.web_intelligence.base_source import BaseCandidateSource, BaseJobSource
from app.services.web_intelligence.compliance import (
    ALLOWED_CANDIDATE_SOURCES,
    ALLOWED_JOB_SOURCES,
    is_candidate_source_allowed,
    is_job_source_allowed,
    sanitize_public_candidate_profile,
    sanitize_search_query,
    validate_source_url,
)
from app.services.web_intelligence.normalizer import normalize_external_candidate, normalize_external_job
from app.services.web_intelligence.source_manager import SourceManager, source_manager

__all__ = [
    "BaseJobSource",
    "BaseCandidateSource",
    "SourceManager",
    "source_manager",
    "normalize_external_job",
    "normalize_external_candidate",
    "sanitize_search_query",
    "validate_source_url",
    "is_job_source_allowed",
    "is_candidate_source_allowed",
    "sanitize_public_candidate_profile",
    "ALLOWED_JOB_SOURCES",
    "ALLOWED_CANDIDATE_SOURCES",
]
