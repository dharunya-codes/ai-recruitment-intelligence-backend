from __future__ import annotations

from typing import Any

from app.services.web_intelligence.base_source import BaseJobSource

MOCK_PUBLIC_JOBS: list[dict[str, Any]] = [
    {
        "id": "mock_job_101",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Python Developer",
        "company": "Apex Software Labs",
        "location": "Coimbatore, India",
        "employment_type": "Full-time",
        "description": "Seeking a Python Developer to build high-performance backend systems. Required: Python, FastAPI, PostgreSQL, REST API, Git, Docker. Preferred: Redis, Kubernetes.",
        "skills": ["Python", "FastAPI", "PostgreSQL", "REST API", "Git", "Docker", "Redis", "Kubernetes"],
        "url": "https://demo-public-jobs.halo.local/jobs/101",
        "posted_at": "2026-09-18T09:00:00Z",
    },
    {
        "id": "mock_job_102",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Senior Python Backend Engineer",
        "company": "CloudForge Tech",
        "location": "Bengaluru, India",
        "employment_type": "Full-time",
        "description": "Looking for a Senior Python Engineer with expertise in Python, SQL, REST API, Docker, and AWS microservices architectures.",
        "skills": ["Python", "SQL", "REST API", "Docker", "AWS", "Git"],
        "url": "https://demo-public-jobs.halo.local/jobs/102",
        "posted_at": "2026-09-19T11:30:00Z",
    },
    {
        "id": "mock_job_103",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Cyber Security Engineer",
        "company": "Sentinel Defense Systems",
        "location": "Chennai, India",
        "employment_type": "Full-time",
        "description": "Join our security operations team. Required: Linux, Networking, Cyber Security, SIEM, Incident Response, Python. Preferred: Ethical Hacking, Digital Forensics.",
        "skills": ["Linux", "Networking", "Cyber Security", "SIEM", "Incident Response", "Python", "Ethical Hacking", "Digital Forensics"],
        "url": "https://demo-public-jobs.halo.local/jobs/103",
        "posted_at": "2026-09-20T14:15:00Z",
    },
    {
        "id": "mock_job_104",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Cloud Security Engineer",
        "company": "Aegis Cloud Services",
        "location": "Hyderabad, India",
        "employment_type": "Full-time",
        "description": "Seeking Cloud Security Specialist. Must have experience with Cyber Security, AWS, Linux, Network Security, Python, and Docker container security.",
        "skills": ["Cyber Security", "AWS", "Linux", "Network Security", "Python", "Docker"],
        "url": "https://demo-public-jobs.halo.local/jobs/104",
        "posted_at": "2026-09-21T08:45:00Z",
    },
    {
        "id": "mock_job_105",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Backend Developer",
        "company": "Nexus Web Innovations",
        "location": "Remote",
        "employment_type": "Full-time",
        "description": "We are looking for a Backend Developer skilled in Python, SQL, REST API, Docker, and Git to develop scalable API integrations.",
        "skills": ["Python", "SQL", "REST API", "Docker", "Git"],
        "url": "https://demo-public-jobs.halo.local/jobs/105",
        "posted_at": "2026-09-21T16:00:00Z",
    },
    {
        "id": "mock_job_106",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Data Analyst",
        "company": "Insight Metrics Corp",
        "location": "Coimbatore, India",
        "employment_type": "Full-time",
        "description": "Data Analyst position. Required: SQL, Python, Data Analysis, Excel, Power BI. Responsibilities: analyze data trends, build reporting dashboards.",
        "skills": ["SQL", "Python", "Data Analysis", "Excel", "Power BI"],
        "url": "https://demo-public-jobs.halo.local/jobs/106",
        "posted_at": "2026-09-22T10:00:00Z",
    },
    {
        "id": "mock_job_107",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "Frontend Developer",
        "company": "PixelCraft Studio",
        "location": "Bengaluru, India",
        "employment_type": "Full-time",
        "description": "Seeking a Frontend Developer with strong skills in HTML, CSS, JavaScript, React, and Git to construct responsive web applications.",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "url": "https://demo-public-jobs.halo.local/jobs/107",
        "posted_at": "2026-09-22T13:20:00Z",
    },
    {
        "id": "mock_job_108",
        "source": "MOCK_PUBLIC_JOB_SOURCE",
        "title": "DevOps Engineer",
        "company": "Pipeline Automations",
        "location": "Remote",
        "employment_type": "Full-time",
        "description": "DevOps Engineer required to maintain CI/CD pipelines and infrastructure. Required: Linux, Docker, Git, AWS, Python.",
        "skills": ["Linux", "Docker", "Git", "AWS", "Python"],
        "url": "https://demo-public-jobs.halo.local/jobs/108",
        "posted_at": "2026-09-23T07:10:00Z",
    },
]


class MockPublicJobSource(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "MOCK_PUBLIC_JOB_SOURCE"

    def is_enabled(self) -> bool:
        return True

    def search_jobs(
        self,
        query: str,
        location: str | None = None,
        company: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        cleaned_query = query.casefold().strip()
        cleaned_loc = location.casefold().strip() if location else None
        cleaned_comp = company.casefold().strip() if company else None

        results = []
        for job in MOCK_PUBLIC_JOBS:
            # Check query match against title, skills, or description
            title_match = cleaned_query in job["title"].casefold()
            skills_match = any(cleaned_query in s.casefold() for s in job["skills"])
            desc_match = cleaned_query in job["description"].casefold()

            if not (title_match or skills_match or desc_match):
                continue

            if cleaned_loc and cleaned_loc not in job["location"].casefold():
                continue

            if cleaned_comp and cleaned_comp not in job["company"].casefold():
                continue

            results.append(dict(job))
            if len(results) >= limit:
                break

        return results
