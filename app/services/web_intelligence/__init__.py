from __future__ import annotations

from app.services.web_intelligence.github_client import GitHubClient, github_client
from app.services.web_intelligence.jd_web_requirements import extract_web_requirements
from app.services.web_intelligence.job_matcher import (
    match_candidate_to_discovered_jobs,
    match_resume_to_discovered_job,
)
from app.services.web_intelligence.job_normalizer import normalize_job_posting
from app.services.web_intelligence.linkedin_adapter import (
    LinkedInAdapter,
    SOURCE_LINKEDIN,
    SOURCE_TYPE_LINKEDIN_API,
    linkedin_adapter,
)
from app.services.web_intelligence.profile_matcher import (
    match_profile_to_requirements,
    match_profiles_for_recruiter,
)
from app.services.web_intelligence.profile_normalizer import normalize_public_profile
from app.services.web_intelligence.public_job_search import (
    PublicJobSearchService,
    public_job_search,
)
from app.services.web_intelligence.public_profile_search import (
    PublicProfileSearchService,
    public_profile_search,
)
from app.services.web_intelligence.role_keywords import (
    ROLE_KEYWORD_DICTIONARY,
    get_role_core_skills,
    get_role_expansion,
    get_role_technologies,
)
from app.services.web_intelligence.skill_demand import aggregate_skill_demand
from app.services.web_intelligence.source_policy import (
    LINKEDIN_POLICY_NOTICE,
    SOURCE_ARBEITNOW,
    SOURCE_GITHUB,
    SOURCE_LINKEDIN_NOTICE,
    SOURCE_PUBLIC_FEED,
    SOURCE_REMOTEOK,
    SOURCE_TYPE_API,
    SOURCE_TYPE_AUTHORIZED,
    SOURCE_TYPE_PUBLIC_FEED,
    SOURCE_TYPE_PUBLIC_WEB,
    sanitize_public_profile_text,
    validate_source_url,
)

__all__ = [
    "GitHubClient",
    "github_client",
    "extract_web_requirements",
    "match_candidate_to_discovered_jobs",
    "match_resume_to_discovered_job",
    "normalize_job_posting",
    "match_profile_to_requirements",
    "match_profiles_for_recruiter",
    "normalize_public_profile",
    "PublicJobSearchService",
    "public_job_search",
    "PublicProfileSearchService",
    "public_profile_search",
    "ROLE_KEYWORD_DICTIONARY",
    "get_role_core_skills",
    "get_role_expansion",
    "get_role_technologies",
    "aggregate_skill_demand",
    "LINKEDIN_POLICY_NOTICE",
    "SOURCE_ARBEITNOW",
    "SOURCE_GITHUB",
    "SOURCE_LINKEDIN_NOTICE",
    "SOURCE_PUBLIC_FEED",
    "SOURCE_REMOTEOK",
    "SOURCE_TYPE_API",
    "SOURCE_TYPE_AUTHORIZED",
    "SOURCE_TYPE_PUBLIC_FEED",
    "SOURCE_TYPE_PUBLIC_WEB",
    "sanitize_public_profile_text",
    "validate_source_url",
]
