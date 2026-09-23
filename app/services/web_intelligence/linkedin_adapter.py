from __future__ import annotations

import json
import os
from typing import Any
import urllib.parse
import urllib.request

from app.services.web_intelligence.source_policy import (
    LINKEDIN_POLICY_NOTICE,
    SOURCE_TYPE_AUTHORIZED,
    sanitize_public_profile_text,
    validate_source_url,
)

SOURCE_LINKEDIN = "LinkedIn"
SOURCE_TYPE_LINKEDIN_API = "linkedin_authorized_api"


class LinkedInAdapter:
    """Official Authorized LinkedIn API Adapter.
    
    Strictly uses official authorized LinkedIn API credentials.
    Does NOT perform unauthorized scraping, browser automation, or login bypass.
    """

    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self) -> None:
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()

    def is_configured(self) -> bool:
        """Check if authorized LinkedIn API credentials/tokens are configured."""
        return bool(self.access_token or (self.client_id and self.client_secret))

    def get_status(self) -> dict[str, Any]:
        """Return clear status and transparency notice regarding LinkedIn integration."""
        if not self.is_configured():
            return {
                "source": SOURCE_LINKEDIN,
                "status": "not_configured",
                "message": "Authorized LinkedIn access is not configured.",
                "is_configured": False,
                "compliance_notice": LINKEDIN_POLICY_NOTICE,
            }
        return {
            "source": SOURCE_LINKEDIN,
            "status": "available",
            "message": "Authorized LinkedIn API configured.",
            "is_configured": True,
            "compliance_notice": LINKEDIN_POLICY_NOTICE,
        }

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": "HALO-Recruitment-Intelligence/1.0",
            "Accept": "application/json",
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def search_profiles(
        self,
        role: str,
        skills: list[str],
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search profiles via official LinkedIn API if authorized.
        
        If not configured, returns an empty list without fabricating profiles.
        """
        if not self.is_configured():
            return []

        # If authorized credentials exist, call LinkedIn People API / Partner endpoint
        try:
            query = f"{role} {' '.join(skills[:2])}".strip()
            encoded_q = urllib.parse.quote(query)
            url = f"{self.BASE_URL}/peopleSearch?keywords={encoded_q}&count={min(limit, 20)}"
            req = urllib.request.Request(url, headers=self._get_headers())

            with urllib.request.urlopen(req, timeout=3.5) as response:
                if response.status == 200:
                    payload = json.loads(response.read().decode("utf-8"))
                    elements = payload.get("elements", [])
                    return [self.normalize_profile(elem) for elem in elements[:limit]]
                elif response.status == 429:
                    return []
        except Exception:
            return []

        return []

    def get_profile(self, profile_url_or_id: str) -> dict[str, Any] | None:
        """Fetch an authorized profile record by ID or URL."""
        if not self.is_configured() or not profile_url_or_id:
            return None

        try:
            encoded_id = urllib.parse.quote(profile_url_or_id.strip())
            url = f"{self.BASE_URL}/people/{encoded_id}"
            req = urllib.request.Request(url, headers=self._get_headers())
            with urllib.request.urlopen(req, timeout=3.5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return self.normalize_profile(data)
        except Exception:
            return None
        return None

    def normalize_profile(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Normalize an authorized LinkedIn profile payload into the standard HALO format."""
        first_name = raw_data.get("firstName", {}).get("localized", {}).get("en_US") or raw_data.get("firstName", "")
        last_name = raw_data.get("lastName", {}).get("localized", {}).get("en_US") or raw_data.get("lastName", "")
        full_name = f"{first_name} {last_name}".strip() or raw_data.get("name", "Authorized LinkedIn Professional")

        headline = raw_data.get("headline", {}).get("localized", {}).get("en_US") or raw_data.get("headline", "Software Professional")
        headline = sanitize_public_profile_text(headline)

        location = raw_data.get("locationName") or raw_data.get("location", "Global / Remote")
        profile_url = raw_data.get("publicProfileUrl") or raw_data.get("profile_url") or "https://www.linkedin.com"
        if not validate_source_url(profile_url):
            profile_url = "https://www.linkedin.com"

        skills = raw_data.get("skills") or []
        cleaned_skills = [s.strip() for s in skills if isinstance(s, str) and s.strip()]

        return {
            "name": full_name,
            "headline": headline,
            "location": location,
            "public_skills": cleaned_skills,
            "profile_url": profile_url,
            "source": SOURCE_LINKEDIN,
            "source_type": SOURCE_TYPE_LINKEDIN_API,
            "public_evidence": [
                {
                    "skill": s,
                    "source": SOURCE_LINKEDIN,
                    "evidence": f"Authorized LinkedIn profile lists skill in {s}.",
                    "url": profile_url,
                }
                for s in cleaned_skills[:3]
            ],
        }


linkedin_adapter = LinkedInAdapter()
