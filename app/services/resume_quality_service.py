from __future__ import annotations

from typing import Any


def analyze_resume_quality(resume_text: str) -> list[dict[str, Any]]:
    text = resume_text or ""
    lowered = text.casefold()
    findings: list[dict[str, Any]] = []

    def add(category: str, severity: str, finding: str, evidence: str, recommendation: str) -> None:
        findings.append({"category": category, "severity": severity, "finding": finding, "evidence": evidence, "recommendation": recommendation})

    if "@" not in text:
        add("CONTACT", "MEDIUM", "No email address was detected.", "No email-like text was found.", "Add a professional contact email if appropriate.")
    if not any(marker in lowered for marker in ("summary", "profile", "objective")):
        add("SUMMARY", "LOW", "No summary or profile section was detected.", "No summary heading was found.", "Add a concise role-focused summary supported by your experience.")
    if not any(marker in lowered for marker in ("project", "built", "developed", "implemented")):
        add("PROJECT_EVIDENCE", "HIGH", "No project-level evidence was detected.", "No project or implementation terms were found.", "Add concrete projects and describe your contribution where supported.")
    if not any(marker in lowered for marker in ("experience", "employment", "internship", "worked")):
        add("EXPERIENCE", "MEDIUM", "No experience section was detected.", "No experience-related heading or marker was found.", "Add relevant experience or academic work if available.")
    if "skill" not in lowered and "technology" not in lowered:
        add("SKILLS_SECTION", "MEDIUM", "No skills section was detected.", "No skills or technology heading was found.", "Add a concise skills section supported by the resume evidence.")
    if len(text.strip()) < 120:
        add("LENGTH", "HIGH", "The extracted resume text is very short.", f"Extracted text contains {len(text.strip())} characters.", "Check the uploaded document and add relevant detail if it is genuinely brief.")
    if len(text) > 20000:
        add("LENGTH", "LOW", "The extracted resume text is unusually long.", f"Extracted text contains {len(text)} characters.", "Keep role-relevant evidence clear and concise.")
    if "\x00" in text:
        add("EXTRACTION", "HIGH", "Malformed extraction markers were detected.", "The extracted text contains null characters.", "Re-upload a readable PDF or DOCX file.")
    return findings