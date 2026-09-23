from __future__ import annotations

from typing import Any

from app.services.web_intelligence.base_source import BaseCandidateSource

MOCK_PUBLIC_CANDIDATES: list[dict[str, Any]] = [
    {
        "source_id": "mock_cand_201",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "Demo Security Engineer (Public)",
        "headline": "Information Security Engineer with experience in SIEM, Linux, and Python Security Automation",
        "location": "Chennai, India",
        "public_skills": ["Linux", "Networking", "Cyber Security", "SIEM", "Python", "Incident Response"],
        "experience": ["Worked as Security Analyst at OpenSec (2022-2024)", "Developed Linux security automation at TechNoc (2020-2022)"],
        "projects": [
            "Built SIEM Log Parser project using Python to analyze firewall logs.",
            "Implemented Linux hardening automation project with Python and Shell.",
        ],
        "education": ["B.Tech in Information Technology, 2020"],
        "profile_url": "https://demo-public-profiles.halo.local/u/demo-sec-eng",
    },
    {
        "source_id": "mock_cand_202",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "Alex Rivers (Public Portfolio)",
        "headline": "Python Backend Developer | FastAPI, PostgreSQL, and REST API Architecture",
        "location": "Coimbatore, India",
        "public_skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "REST API", "Docker", "Git"],
        "experience": ["Backend Engineer at DevStudio (2021-Present)"],
        "projects": [
            "E-commerce API: Scalable REST API built with FastAPI and PostgreSQL.",
            "Dockerized Task Queue: Distributed Python background worker with Redis.",
        ],
        "education": ["B.E. in Computer Science, 2021"],
        "profile_url": "https://demo-public-profiles.halo.local/u/alex-rivers",
    },
    {
        "source_id": "mock_cand_203",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "Priya Sharma (Public Contributor)",
        "headline": "Cloud Security Specialist | AWS, Cyber Security, and Infrastructure as Code",
        "location": "Hyderabad, India",
        "public_skills": ["Cyber Security", "AWS", "Linux", "Network Security", "Python", "Docker"],
        "experience": ["Cloud Security Associate at CloudGuard (2022-2024)"],
        "projects": [
            "AWS IAM Auditor: Python utility to identify misconfigured cloud permissions.",
            "Container Security Baseline: Docker security hardening benchmarks.",
        ],
        "education": ["B.Sc in Computer Science, 2022"],
        "profile_url": "https://demo-public-profiles.halo.local/u/priya-sharma",
    },
    {
        "source_id": "mock_cand_204",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "David Chen (Public Open Source)",
        "headline": "Data Analyst & Python Developer | SQL, Power BI, and Analytics",
        "location": "Bengaluru, India",
        "public_skills": ["SQL", "Python", "Data Analysis", "Excel", "Power BI"],
        "experience": ["Data Analyst at MetricFlow (2022-Present)"],
        "projects": [
            "Sales Forecasting Dashboard: Power BI interactive reporting suite.",
            "Customer Retention Analytics: SQL data aggregation and Python modeling.",
        ],
        "education": ["B.Tech in Data Science, 2022"],
        "profile_url": "https://demo-public-profiles.halo.local/u/david-chen",
    },
    {
        "source_id": "mock_cand_205",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "Sara Ali (Public Web Dev)",
        "headline": "Frontend Developer | React, JavaScript, HTML, and CSS",
        "location": "Coimbatore, India",
        "public_skills": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "experience": ["UI Developer at WebCraft (2021-Present)"],
        "projects": [
            "Analytics Dashboard: Responsive React UI with dark mode and data tables.",
            "Design System Component Library: Reusable React and CSS component suite.",
        ],
        "education": ["BCA in Computer Applications, 2021"],
        "profile_url": "https://demo-public-profiles.halo.local/u/sara-ali",
    },
    {
        "source_id": "mock_cand_206",
        "source": "MOCK_PUBLIC_CANDIDATE_SOURCE",
        "name": "Rahul Verma (Public DevOps)",
        "headline": "DevOps & Cloud Engineer | Linux, Docker, AWS, and Git CI/CD",
        "location": "Remote",
        "public_skills": ["Linux", "Docker", "Git", "AWS", "Python"],
        "experience": ["DevOps Engineer at BuildMatrix (2020-Present)"],
        "projects": [
            "Automated CI/CD Pipeline: GitHub Actions pipeline deploying to AWS ECS.",
            "Infrastructure as Code: Terraform scripts for automated cloud provisioning.",
        ],
        "education": ["B.Tech in Computer Engineering, 2020"],
        "profile_url": "https://demo-public-profiles.halo.local/u/rahul-verma",
    },
]


class MockPublicCandidateSource(BaseCandidateSource):
    @property
    def source_name(self) -> str:
        return "MOCK_PUBLIC_CANDIDATE_SOURCE"

    def is_enabled(self) -> bool:
        return True

    def search_candidates(
        self,
        job_title: str,
        requirements: list[str] | None = None,
        location: str | None = None,
        skills_filter: list[str] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        cleaned_title = job_title.casefold().strip()
        cleaned_loc = location.casefold().strip() if location else None
        target_skills = [s.casefold().strip() for s in (skills_filter or requirements or [])]

        results = []
        for candidate in MOCK_PUBLIC_CANDIDATES:
            # Check title / skill affinity
            title_match = any(word in candidate["headline"].casefold() for word in cleaned_title.split() if len(word) > 2)
            candidate_skills = [s.casefold() for s in candidate["public_skills"]]
            skill_overlap = any(s in candidate_skills for s in target_skills) if target_skills else True

            if not (title_match or skill_overlap):
                continue

            if cleaned_loc and cleaned_loc not in candidate["location"].casefold():
                continue

            results.append(dict(candidate))
            if len(results) >= limit:
                break

        return results
