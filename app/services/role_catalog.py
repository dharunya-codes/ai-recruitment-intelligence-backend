from __future__ import annotations

ROLE_EXPECTATIONS: dict[str, dict[str, list[str]]] = {
    "cyber security analyst": {"skills": ["Linux", "Networking", "Cyber Security", "SIEM", "Python"], "responsibilities": ["Monitor security events", "Investigate alerts", "Analyze incidents"]},
    "soc analyst": {"skills": ["Linux", "Networking", "SIEM", "SOC", "Incident Response"], "responsibilities": ["Monitor security events", "Investigate alerts", "Analyze incidents"]},
    "software developer": {"skills": ["Python", "Java", "SQL", "Git", "REST API"], "responsibilities": ["Design applications", "Implement features", "Test software"]},
    "data analyst": {"skills": ["SQL", "Python", "Data Analysis", "Excel", "Power BI"], "responsibilities": ["Prepare data", "Analyze trends", "Create reports"]},
    "web developer": {"skills": ["HTML", "CSS", "JavaScript", "Git", "REST API"], "responsibilities": ["Build web interfaces", "Implement features", "Test applications"]},
    "backend developer": {"skills": ["Python", "SQL", "REST API", "Docker", "Git"], "responsibilities": ["Design APIs", "Implement services", "Handle data"]},
    "frontend developer": {"skills": ["HTML", "CSS", "JavaScript", "React", "Git"], "responsibilities": ["Build user interfaces", "Implement components", "Test web applications"]},
}


def role_expectations(role: str) -> dict[str, list[str]] | None:
    return ROLE_EXPECTATIONS.get(role.casefold().strip())