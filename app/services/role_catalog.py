from __future__ import annotations

ROLE_EXPECTATIONS: dict[str, dict[str, list[str]]] = {
    "cyber security analyst": {"skills": ["Linux", "Networking", "Cyber Security", "SIEM", "Python"], "responsibilities": ["Monitor security events", "Investigate alerts", "Analyze incidents"]},
    "soc analyst": {"skills": ["Linux", "Networking", "SIEM", "SOC", "Incident Response"], "responsibilities": ["Monitor security events", "Investigate alerts", "Analyze incidents"]},
    "software developer": {"skills": ["Python", "Java", "SQL", "Git", "REST API"], "responsibilities": ["Design applications", "Implement features", "Test software"]},
    "data analyst": {"skills": ["SQL", "Python", "Data Analysis", "Excel", "Power BI"], "responsibilities": ["Prepare data", "Analyze trends", "Create reports"]},
    "web developer": {"skills": ["HTML", "CSS", "JavaScript", "Git", "REST API"], "responsibilities": ["Build web interfaces", "Implement features", "Test applications"]},
    "backend developer": {"skills": ["Python", "SQL", "REST API", "Docker", "Git"], "responsibilities": ["Design APIs", "Implement services", "Handle data"]},
    "frontend developer": {"skills": ["HTML", "CSS", "JavaScript", "React", "Git"], "responsibilities": ["Build user interfaces", "Implement components", "Test web applications"]},
    "python developer": {"skills": ["Python", "SQL", "REST API", "Git", "Docker"], "responsibilities": ["Build backend services", "Implement business logic", "Maintain APIs"]},
    "devops engineer": {"skills": ["Linux", "Docker", "Git", "AWS", "Python"], "responsibilities": ["Maintain CI/CD pipelines", "Manage infrastructure", "Monitor services"]},
    "cloud security engineer": {"skills": ["Cyber Security", "AWS", "Linux", "Network Security", "Python"], "responsibilities": ["Secure cloud infrastructure", "Enforce compliance", "Monitor cloud events"]},
    "ai security engineer": {"skills": ["Python", "Machine Learning", "Cyber Security", "Linux", "REST API"], "responsibilities": ["Secure AI systems", "Evaluate model robustness", "Implement security controls"]},
    "blockchain developer": {"skills": ["Blockchain", "Cryptography", "Python", "JavaScript", "Git"], "responsibilities": ["Develop smart contracts", "Build decentralized protocols", "Test blockchain logic"]},
    "product security engineer": {"skills": ["Cyber Security", "Python", "Linux", "REST API", "Penetration Testing"], "responsibilities": ["Review architecture security", "Conduct security assessments", "Guide secure development"]},
    "security operations analyst": {"skills": ["SIEM", "SOC", "Incident Response", "Linux", "Networking"], "responsibilities": ["Monitor security alerts", "Triage incidents", "Execute incident response"]},
}


def role_expectations(role: str) -> dict[str, list[str]] | None:
    return ROLE_EXPECTATIONS.get(role.casefold().strip())


def extract_custom_role_expectations(role: str) -> dict[str, list[str]]:
    """Synthesize a safe, deterministic generic role expectation set for uncataloged target roles."""
    cleaned_role = role.strip()
    lowered = cleaned_role.casefold()

    from app.services.skill_extractor import SKILL_ALIASES, find_skill_alias

    extracted_skills: list[str] = []
    # 1. Match canonical skills and aliases mentioned in the role title
    for canonical in SKILL_ALIASES:
        if find_skill_alias(cleaned_role, canonical):
            if canonical not in extracted_skills:
                extracted_skills.append(canonical)

    # 2. Check domain keywords to provide relevant foundation skills
    domain_mappings = [
        (("security", "cyber", "infosec", "soc", "penetration", "threat", "vulnerability"), ["Cyber Security", "Linux", "Networking", "Python"]),
        (("cloud", "aws", "azure", "gcp", "devops", "sre", "infrastructure"), ["Linux", "Docker", "Git", "AWS", "Python"]),
        (("data", "analytics", "bi", "scientist"), ["Python", "SQL", "Data Analysis", "Excel"]),
        (("ai", "machine learning", "ml", "deep learning", "nlp", "vision"), ["Python", "Machine Learning", "Deep Learning", "SQL", "Git"]),
        (("frontend", "ui", "ux", "web"), ["HTML", "CSS", "JavaScript", "React", "Git"]),
        (("backend", "api", "microservice"), ["Python", "SQL", "REST API", "Docker", "Git"]),
        (("full stack", "fullstack"), ["JavaScript", "Python", "React", "SQL", "Git", "REST API"]),
        (("blockchain", "crypto", "smart contract"), ["Blockchain", "Cryptography", "Python", "JavaScript", "Git"]),
        (("mobile", "android", "ios"), ["JavaScript", "React", "REST API", "Git"]),
        (("qa", "test", "automation"), ["Python", "Git", "REST API", "SQL"]),
    ]

    for keywords, skills in domain_mappings:
        if any(kw in lowered for kw in keywords):
            for skill in skills:
                if skill not in extracted_skills:
                    extracted_skills.append(skill)

    # Fallback to general software engineering foundation if nothing matched
    if not extracted_skills:
        extracted_skills = ["Python", "SQL", "Git", "REST API"]

    responsibilities = [
        f"Design, build, and maintain {cleaned_role} deliverables",
        f"Collaborate with team members on {cleaned_role} requirements",
        f"Follow best practices and quality standards for {cleaned_role} workflows",
    ]

    return {
        "skills": extracted_skills[:6],
        "responsibilities": responsibilities,
    }