from __future__ import annotations

import re

SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "Java": ("java",),
    "C": ("c",),
    "C++": ("c++",),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript",),
    "React": ("react",),
    "Node.js": ("node.js", "nodejs"),
    "FastAPI": ("fastapi",),
    "Flask": ("flask",),
    "SQL": ("sql",),
    "MySQL": ("mysql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "SQLite": ("sqlite",),
    "MongoDB": ("mongodb",),
    "Linux": ("linux",),
    "Git": ("git",),
    "Docker": ("docker",),
    "AWS": ("aws",),
    "Azure": ("azure",),
    "GCP": ("gcp",),
    "Cyber Security": ("cyber security", "cybersecurity"),
    "Network Security": ("network security",),
    "SIEM": ("siem",),
    "SOC": ("soc",),
    "Penetration Testing": ("penetration testing",),
    "Ethical Hacking": ("ethical hacking",),
    "Incident Response": ("incident response",),
    "Digital Forensics": ("digital forensics",),
    "Cryptography": ("cryptography",),
    "Machine Learning": ("machine learning",),
    "Deep Learning": ("deep learning",),
    "Data Analysis": ("data analysis",),
    "Power BI": ("power bi",),
    "Excel": ("excel",),
    "REST API": ("rest api",),
    "HTML": ("html",),
    "CSS": ("css",),
    "Bootstrap": ("bootstrap",),
    "OpenCV": ("opencv",),
    "FFmpeg": ("ffmpeg",),
    "Blockchain": ("blockchain",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Redis": ("redis",),
}


def _phrase_pattern(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w+#]){re.escape(phrase)}(?![\w+#])", re.IGNORECASE)


def find_skill_alias(text: str, canonical_skill: str) -> str | None:
    for alias in SKILL_ALIASES.get(canonical_skill, (canonical_skill,)):
        if _phrase_pattern(alias).search(text):
            return alias
    return None


def extract_skills(resume_text: str) -> list[str]:
    """Return canonical skills detected with token-aware matching."""
    return [
        canonical
        for canonical in SKILL_ALIASES
        if find_skill_alias(resume_text, canonical) is not None
    ]