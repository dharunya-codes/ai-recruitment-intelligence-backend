from __future__ import annotations

ROLE_KEYWORD_DICTIONARY: dict[str, dict[str, list[str]]] = {
    "backend developer": {
        "titles": [
            "Backend Developer",
            "Python Backend Developer",
            "FastAPI Developer",
            "Django Developer",
            "Junior Backend Developer",
            "Senior Backend Engineer",
            "Node.js Backend Developer",
            "Java Backend Developer",
            "Golang Developer",
            "API Engineer",
        ],
        "core_skills": ["Python", "FastAPI", "REST API", "SQL", "PostgreSQL", "Docker", "Git", "Database Design"],
        "technologies": ["FastAPI", "Flask", "Django", "PostgreSQL", "Redis", "Docker", "SQLAlchemy", "Alembic", "AWS", "Celery"],
    },
    "data analyst": {
        "titles": [
            "Data Analyst",
            "Junior Data Analyst",
            "Business Data Analyst",
            "Data Analytics Specialist",
            "BI Analyst",
            "Product Data Analyst",
            "Quantitative Analyst",
        ],
        "core_skills": ["SQL", "Excel", "Python", "Power BI", "Tableau", "Data Analysis", "Statistics", "Data Visualization"],
        "technologies": ["SQL", "PostgreSQL", "Tableau", "Power BI", "Pandas", "NumPy", "Excel", "Jupyter", "Looker", "BigQuery"],
    },
    "frontend developer": {
        "titles": [
            "Frontend Developer",
            "React Developer",
            "UI Developer",
            "Next.js Developer",
            "Junior Frontend Developer",
            "Web Developer",
            "Vue.js Developer",
            "TypeScript Frontend Developer",
        ],
        "core_skills": ["JavaScript", "TypeScript", "React", "HTML5", "CSS3", "Redux", "Tailwind CSS", "REST API"],
        "technologies": ["React", "TypeScript", "Next.js", "Vite", "Tailwind CSS", "CSS3", "HTML5", "Redux", "Webpack", "Jest"],
    },
    "full stack developer": {
        "titles": [
            "Full Stack Developer",
            "Full Stack Engineer",
            "MERN Stack Developer",
            "Python Full Stack Developer",
            "Junior Full Stack Developer",
            "Web Application Developer",
        ],
        "core_skills": ["JavaScript", "Python", "React", "Node.js", "SQL", "REST API", "Git", "Docker"],
        "technologies": ["React", "Node.js", "Python", "FastAPI", "Express", "MongoDB", "PostgreSQL", "Docker", "TypeScript", "Tailwind CSS"],
    },
    "devops engineer": {
        "titles": [
            "DevOps Engineer",
            "Cloud Engineer",
            "SRE",
            "Site Reliability Engineer",
            "Platform Engineer",
            "Infrastructure Engineer",
            "CI/CD Engineer",
        ],
        "core_skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS", "Terraform", "Git", "Python", "Monitoring"],
        "technologies": ["Docker", "Kubernetes", "Terraform", "GitHub Actions", "AWS", "Prometheus", "Grafana", "Linux", "Ansible", "Helm"],
    },
    "machine learning engineer": {
        "titles": [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist",
            "MLOps Engineer",
            "NLP Engineer",
            "Computer Vision Engineer",
            "Junior ML Engineer",
        ],
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "PyTorch", "TensorFlow", "Scikit-Learn", "Data Preprocessing"],
        "technologies": ["PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Hugging Face", "MLflow", "Docker", "FastAPI", "CUDA"],
    },
    "cyber security analyst": {
        "titles": [
            "Cyber Security Analyst",
            "Security Engineer",
            "Information Security Specialist",
            "SOC Analyst",
            "Penetration Tester",
            "Vulnerability Management Analyst",
        ],
        "core_skills": ["Network Security", "Vulnerability Assessment", "SIEM", "Linux", "Incident Response", "Firewalls", "Python"],
        "technologies": ["Wireshark", "Splunk", "Nmap", "Metasploit", "Burp Suite", "Linux", "Python", "Snort", "Suricata"],
    },
    "qa engineer": {
        "titles": [
            "QA Engineer",
            "Automation Test Engineer",
            "Software Development Engineer in Test (SDET)",
            "Quality Assurance Specialist",
            "Manual & Automation Tester",
        ],
        "core_skills": ["Test Automation", "Selenium", "PyTest", "REST API Testing", "Postman", "CI/CD", "Bug Tracking"],
        "technologies": ["Selenium", "PyTest", "Cypress", "Playwright", "Postman", "Jira", "GitHub Actions", "Python"],
    },
    "mobile developer": {
        "titles": [
            "Mobile App Developer",
            "Flutter Developer",
            "React Native Developer",
            "iOS Developer",
            "Android Developer",
        ],
        "core_skills": ["Flutter", "Dart", "React Native", "JavaScript", "Mobile UI", "REST API", "State Management"],
        "technologies": ["Flutter", "Dart", "React Native", "Swift", "Kotlin", "Firebase", "Redux", "REST API"],
    },
}


def get_role_expansion(target_role: str) -> list[str]:
    """Return expanded search keywords and alternative job titles for the given target role."""
    if not target_role:
        return ["Software Engineer", "Developer"]

    normalized = target_role.strip().lower()

    # Direct match in role dictionary
    for role_key, data in ROLE_KEYWORD_DICTIONARY.items():
        if role_key in normalized or normalized in role_key:
            titles = data["titles"]
            if target_role not in titles:
                return [target_role] + titles
            return titles

    # Word-based overlap matching
    tokens = set(normalized.split())
    best_match = None
    max_overlap = 0

    for role_key, data in ROLE_KEYWORD_DICTIONARY.items():
        key_tokens = set(role_key.split())
        overlap = len(tokens & key_tokens)
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = data["titles"]

    if best_match and max_overlap > 0:
        return [target_role] + [t for t in best_match if t.lower() != normalized]

    # Fallback heuristic expansion
    return [
        target_role,
        f"Junior {target_role}",
        f"Senior {target_role}",
        f"{target_role} Specialist",
    ]


def get_role_core_skills(target_role: str) -> list[str]:
    """Return common core skills associated with a target role."""
    normalized = target_role.strip().lower()
    for role_key, data in ROLE_KEYWORD_DICTIONARY.items():
        if role_key in normalized or normalized in role_key:
            return data["core_skills"]
    return ["Python", "SQL", "Git", "Problem Solving", "Communication"]


def get_role_technologies(target_role: str) -> list[str]:
    """Return common technologies and tools associated with a target role."""
    normalized = target_role.strip().lower()
    for role_key, data in ROLE_KEYWORD_DICTIONARY.items():
        if role_key in normalized or normalized in role_key:
            return data["technologies"]
    return ["Git", "Docker", "Linux", "REST API", "Cloud"]
