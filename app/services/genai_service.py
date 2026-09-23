from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any


class GenAIService:
    """Report explanation layer. Deterministic data remains the source of truth."""

    def generate_reports(self, context: dict[str, Any]) -> dict[str, Any]:
        provider = os.getenv("GENAI_PROVIDER", "").strip()
        if not provider or not os.getenv("GENAI_API_KEY", "").strip():
            status = "GENAI_NOT_CONFIGURED"
        else:
            status = "GENAI_NOT_CONFIGURED"
        context["generation_status"] = status
        generated_at = datetime.now(timezone.utc).isoformat()
        return {
            "generation_status": status,
            "candidate": self._candidate_report(context, generated_at),
            "hr": self._hr_report(context, generated_at),
        }

    def _candidate_report(self, context: dict[str, Any], generated_at: str) -> dict[str, Any]:
        analysis = context["resume_analysis"]
        assessment = context["assessment"]
        missing = analysis["missing_requirements"]
        weak = analysis["weak_requirements"]
        strong = analysis["matched_requirements"]
        gaps = [item["requirement"] for item in missing + weak]
        return {
            "report_type": "CANDIDATE",
            "generation_status": context["generation_status"],
            "executive_summary": self._candidate_summary(context),
            "role_target": context["job"]["title"],
            "match_summary": (
                f"{'Role Compatibility Score' if analysis.get('score_type') == 'ROLE_COMPATIBILITY' else 'Job Match Score'}: "
                f"{analysis['overall_match_score']}."
            ),
            "strong_skills": [item["requirement"] for item in strong],
            "weak_skills": [item["requirement"] for item in weak],
            "missing_skills": [item["requirement"] for item in missing],
            "evidence_gaps": [
                f"{item['requirement']}: {item.get('reason') or 'Not demonstrated in the available resume evidence.'}"
                for item in missing + weak
            ],
            "verification_summary": self._verification_summary(context["verification"]),
            "assessment_summary": assessment,
            "assessment_strengths": assessment.get("strengths", []),
            "assessment_improvement_areas": assessment.get("areas_for_improvement", []),
            "resume_improvements": self._resume_improvements(context),
            "project_improvements": self._project_improvements(context),
            "skill_roadmap": [self._roadmap_item(item) for item in gaps],
            "interview_preparation": [
                f"Prepare an evidence-based example for {item['requirement']}." for item in weak + missing
            ],
            "next_steps": [
                "Strengthen the highest-priority gaps listed in the roadmap.",
                "Add concrete project contributions and outcomes to the resume where available.",
            ],
            "generated_at": generated_at,
        }

    def _hr_report(self, context: dict[str, Any], generated_at: str) -> dict[str, Any]:
        analysis = context["resume_analysis"]
        assessment = context["assessment"]
        return {
            "report_type": "HR",
            "generation_status": context["generation_status"],
            "candidate_summary": context["candidate"]["name"],
            "role": context["job"]["title"],
            "match_score": analysis["overall_match_score"],
            "requirement_summary": analysis["counts"],
            "matched_requirements": analysis["matched_requirements"],
            "weak_requirements": analysis["weak_requirements"],
            "missing_requirements": analysis["missing_requirements"],
            "evidence_summary": self._evidence_summary(context["evidence"]),
            "verification_summary": self._verification_summary(context["verification"]),
            "assessment_summary": assessment,
            "assessment_score": assessment.get("score"),
            "category_scores": assessment.get("category_scores", {}),
            "assessment_strengths": assessment.get("strengths", []),
            "assessment_improvement_areas": assessment.get("areas_for_improvement", []),
            "evidence_limitations": self._evidence_limitations(context),
            "final_summary": (
                "This report is decision support based on the submitted resume, verification responses, "
                "and assessment responses. HR remains the final decision-maker."
            ),
            "generated_at": generated_at,
        }

    @staticmethod
    def _candidate_summary(context: dict[str, Any]) -> str:
        analysis = context["resume_analysis"]
        return (
            f"For {context['job']['title']}, the available resume evidence demonstrates "
            f"{analysis['counts']['matched']} of {analysis['counts']['total']} requirements. "
            "Use the gaps below to guide your next improvements."
        )

    @staticmethod
    def _verification_summary(verification: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "skill": item["skill"],
                "status": item["status"],
                "candidate_reported_evidence": item["candidate_reported_evidence"],
                "source": "candidate-reported; not resume evidence",
            }
            for item in verification
        ]

    @staticmethod
    def _evidence_summary(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "skill": item["skill"],
                "evidence_strength": item["evidence_strength"],
                "evidence_text": item["evidence_text"],
                "source": "resume",
            }
            for item in evidence
        ]

    @staticmethod
    def _evidence_limitations(context: dict[str, Any]) -> list[str]:
        limitations = [
            "Assessment and verification responses are separate from resume evidence.",
            "Absence of evidence does not establish absence of the underlying skill.",
        ]
        if not context["verification"]:
            limitations.append("No verification responses were available.")
        if context["assessment"].get("status") != "EVALUATED":
            limitations.append("No evaluated assessment result was available.")
        return limitations

    @staticmethod
    def _resume_improvements(context: dict[str, Any]) -> list[str]:
        suggestions = []
        if context["resume_analysis"]["weak_requirements"] or context["resume_analysis"]["missing_requirements"]:
            suggestions.append("Describe the technologies, contribution, and outcome for relevant projects where available.")
            suggestions.append("Consider adding measurable outcomes if they are available; no metrics were inferred here.")
        return suggestions or ["Keep role-relevant project evidence specific and outcome-focused."]

    @staticmethod
    def _project_improvements(context: dict[str, Any]) -> list[str]:
        text = context.get("resume_text", "").lower()
        suggestions = []
        for label, marker in (("problem", "problem"), ("contribution", "built"), ("outcome", "result")):
            if marker not in text:
                suggestions.append(f"Add the project {label} if it is supported by your experience.")
        return suggestions

    @staticmethod
    def _roadmap_item(requirement: str) -> dict[str, str]:
        return {
            "skill": requirement,
            "priority": "Review required role concepts and practice them in a small evidence-based project.",
            "basis": "Derived from a weak or missing requirement; no unrelated skill was added.",
        }