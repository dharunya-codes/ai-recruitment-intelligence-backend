from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_GENAI_MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """You are HALO, an AI-powered Recruitment and Career Intelligence platform assistant.
Your task is to provide objective, grounded, natural-language explanations, executive summaries, and career guidance based solely on structured resume evaluation and assessment results.

STRICT GROUNDING & HALLUCINATION PREVENTION RULES:
1. Ground every statement strictly on the provided input data.
2. NEVER invent, assume, or fabricate candidate skills, work experience, companies, job titles, internships, certifications, projects, or assessment achievements.
3. If information or evidence is not present in the input, clearly state that it is unavailable rather than guessing.
4. Distinguish RESUME EVIDENCE from CANDIDATE-REPORTED VERIFICATION. Candidate verification answers are self-reported and must NEVER be described as verified resume evidence.
5. Distinguish ASSESSMENT PERFORMANCE from PROFESSIONAL EXPERIENCE. Assessment scores demonstrate tested conceptual/scenario understanding, not professional work history.
6. Do NOT make automatic Hire or Reject decisions. Frame all insights as explainable decision-support for human review.
"""


class GenAIService:
    """
    Google Gemini 2.5 Flash service layer for HALO reports, explanations, and guidance.
    Deterministic backend analysis remains the primary source of truth.
    """

    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        self._api_key = api_key
        self._model_name = model_name

    def get_api_key(self) -> str:
        if self._api_key is not None:
            return self._api_key.strip()
        return os.getenv("GENAI_API_KEY", "").strip()

    def get_model_name(self) -> str:
        if self._model_name is not None:
            return self._model_name.strip()
        return os.getenv("GENAI_MODEL", DEFAULT_GENAI_MODEL).strip() or DEFAULT_GENAI_MODEL

    def is_configured(self) -> bool:
        return bool(self.get_api_key())

    def _get_client(self) -> Any | None:
        api_key = self.get_api_key()
        if not api_key:
            return None
        try:
            from google import genai

            return genai.Client(api_key=api_key)
        except Exception as exc:
            logger.error("Failed to initialize Google GenAI Client: %s", exc)
            return None

    def _call_gemini(self, prompt: str, system_instruction: str = SYSTEM_INSTRUCTION) -> tuple[str | None, str]:
        """
        Calls Gemini 2.5 Flash with error handling and status tracking.
        Returns: (response_text, generation_status)
        """
        if not self.is_configured():
            return None, "GENAI_NOT_CONFIGURED"

        client = self._get_client()
        if client is None:
            return None, "GENAI_NOT_CONFIGURED"

        model = self.get_model_name()
        try:
            from google.genai import types

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                top_p=0.9,
            )
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            text = response.text
            if text and text.strip():
                return text.strip(), "GENAI_SUCCESS"
            return None, "GENAI_EMPTY_RESPONSE"
        except Exception as exc:
            # Never log or expose API keys
            logger.error("Gemini API call failed for model %s: %s", model, exc)
            return None, "GENAI_ERROR"

    def generate_candidate_summary(self, context: dict[str, Any]) -> tuple[str, str]:
        """Generate a personalized, grounded executive summary for the candidate report."""
        if not self.is_configured():
            return self._candidate_summary(context), "GENAI_NOT_CONFIGURED"

        analysis = context.get("resume_analysis", {})
        job = context.get("job", {})
        prompt = f"""Generate a concise, constructive 2-3 sentence executive summary for a candidate evaluating their resume for the role: '{job.get('title')}'.

Structured Input Data:
- Overall Compatibility Score: {analysis.get('overall_match_score')}
- Matched Skills: {[item.get('requirement') for item in analysis.get('matched_requirements', [])]}
- Weak Skills: {[item.get('requirement') for item in analysis.get('weak_requirements', [])]}
- Missing Skills: {[item.get('requirement') for item in analysis.get('missing_requirements', [])]}
- Verification Status: {context.get('verification')}
- Assessment Status: {context.get('assessment', {}).get('status')} (Score: {context.get('assessment', {}).get('score')})

Explain what the resume currently demonstrates and what key skill areas the candidate should focus on next."""

        text, status = self._call_gemini(prompt)
        if status == "GENAI_SUCCESS" and text:
            return text, status
        return self._candidate_summary(context), status

    def generate_hr_summary(self, context: dict[str, Any]) -> tuple[str, str]:
        """Generate an objective, decision-support candidate overview for the HR report."""
        if not self.is_configured():
            return f"Candidate {context.get('candidate', {}).get('name', 'Profile')} evaluation for {context.get('job', {}).get('title', 'Target Role')}.", "GENAI_NOT_CONFIGURED"

        analysis = context.get("resume_analysis", {})
        job = context.get("job", {})
        candidate = context.get("candidate", {})

        prompt = f"""Generate an objective, concise 2-3 sentence decision-support overview of candidate '{candidate.get('name')}' for the HR report for role '{job.get('title')}'.

Structured Input Data:
- Candidate Name: {candidate.get('name')}
- Role: {job.get('title')}
- Match Score: {analysis.get('overall_match_score')} / 100
- Demonstrated Skills in Resume: {[item.get('requirement') for item in analysis.get('matched_requirements', [])]}
- Skills with Limited Evidence: {[item.get('requirement') for item in analysis.get('weak_requirements', [])]}
- Missing Requirements: {[item.get('requirement') for item in analysis.get('missing_requirements', [])]}
- Assessment Evaluated: {context.get('assessment', {}).get('status') == 'EVALUATED'} (Score: {context.get('assessment', {}).get('score')})
- Verification Responses Provided: {len(context.get('verification', []))}

Provide an objective summary of demonstrated qualifications versus skill gaps for recruiter review."""

        text, status = self._call_gemini(prompt)
        if status == "GENAI_SUCCESS" and text:
            return text, status
        return f"Candidate {candidate.get('name', 'Profile')} evaluation for {job.get('title', 'Target Role')}.", status

    def generate_improvement_suggestions(self, context: dict[str, Any]) -> list[str]:
        """Generate targeted resume improvement suggestions based on weak/missing skills."""
        deterministic_suggestions = self._resume_improvements(context)
        if not self.is_configured():
            return deterministic_suggestions

        analysis = context.get("resume_analysis", {})
        weak = [item.get("requirement") for item in analysis.get("weak_requirements", [])]
        missing = [item.get("requirement") for item in analysis.get("missing_requirements", [])]

        prompt = f"""Based on the following gaps, provide 2 to 4 actionable, professional resume improvement tips.
Weak Evidence Skills: {weak}
Missing Skills: {missing}
Format as a JSON array of strings: ["Tip 1", "Tip 2"]"""

        text, status = self._call_gemini(prompt)
        if status == "GENAI_SUCCESS" and text:
            try:
                cleaned = text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()
                elif cleaned.startswith("```"):
                    cleaned = cleaned.removeprefix("```").removesuffix("```").strip()
                parsed = json.loads(cleaned)
                if isinstance(parsed, list) and all(isinstance(i, str) for i in parsed):
                    return parsed
            except Exception:
                pass
        return deterministic_suggestions

    def generate_reports(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Generate explainable candidate and HR reports using Gemini 2.5 Flash
        when configured, or deterministic grounding fallback otherwise.
        """
        if not self.is_configured():
            status = "GENAI_NOT_CONFIGURED"
        else:
            # Check generation status via candidate summary call
            _, status = self.generate_candidate_summary(context)
            if status != "GENAI_SUCCESS":
                status = "GENAI_ERROR"

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

        executive_summary = (
            self.generate_candidate_summary(context)[0]
            if context.get("generation_status") == "GENAI_SUCCESS"
            else self._candidate_summary(context)
        )

        return {
            "report_type": "CANDIDATE",
            "generation_status": context["generation_status"],
            "executive_summary": executive_summary,
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
        candidate_summary = (
            self.generate_hr_summary(context)[0]
            if context.get("generation_status") == "GENAI_SUCCESS"
            else context["candidate"]["name"]
        )

        return {
            "report_type": "HR",
            "generation_status": context["generation_status"],
            "candidate_summary": candidate_summary,
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