import {
  CandidateProfile,
  ResumeScoreBreakdown,
  SkillGapData,
  EvidenceDetail,
  JobMatchComparison,
  RecruiterCandidate,
  JobVacancy,
  InterviewQuestionItem,
  InterviewFeedbackSummary,
  FullReportData,
} from '../types';
import {
  sampleCandidate,
  sampleResumeScore,
  sampleSkillGap,
  sampleEvidenceDetails,
  sampleJobMatch,
  sampleCandidatesPool,
  sampleJobVacancies,
  sampleInterviewQuestions,
  sampleInterviewFeedback,
  sampleFullReport,
} from '../data/mockData';

// API Configuration for future Python FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false';

// Helper for realistic async network simulation
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Service layer for AI Resume Intelligence & Interview Platform.
 * Fully prepared for Python FastAPI REST endpoints.
 */

export interface UploadResumeResponse {
  success: boolean;
  resumeId: string;
  fileName: string;
  message: string;
  detectedRole: string;
}

export const uploadResume = async (
  file: File,
  targetRole: string,
  _jobDescriptionText?: string
): Promise<UploadResumeResponse> => {
  if (!USE_MOCK) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('target_role', targetRole);
      const res = await fetch(`${API_BASE_URL}/resumes/upload`, {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        return await res.json();
      }
    } catch {
      console.warn('Backend unavailable, falling back to local intelligence engine.');
    }
  }

  // Simulated latency
  await delay(600);
  return {
    success: true,
    resumeId: 'res_' + Date.now(),
    fileName: file.name,
    message: 'Resume parsed and categorized successfully with semantic entity extraction.',
    detectedRole: targetRole || 'Data Analyst',
  };
};

export const analyzeResume = async (_resumeId?: string): Promise<ResumeScoreBreakdown> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/resumes/analyze?id=${_resumeId || 'default'}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(450);
  return sampleResumeScore;
};

export const getSkillGap = async (_targetRole?: string): Promise<SkillGapData> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/skills/gap?role=${encodeURIComponent(_targetRole || 'Data Analyst')}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(350);
  return sampleSkillGap;
};

export const getEvidence = async (_resumeId?: string): Promise<EvidenceDetail[]> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/evidence?id=${_resumeId || 'default'}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(400);
  return sampleEvidenceDetails;
};

export const compareJobDescription = async (
  _targetRole: string,
  _jdText?: string
): Promise<JobMatchComparison> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/resumes/compare-jd`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: _targetRole, jd_text: _jdText }),
      });
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(500);
  return sampleJobMatch;
};

export const getCandidates = async (_filterQuery?: string): Promise<RecruiterCandidate[]> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/recruiter/candidates`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(300);
  if (!_filterQuery) return sampleCandidatesPool;
  const q = _filterQuery.toLowerCase();
  return sampleCandidatesPool.filter(
    (c) =>
      c.name.toLowerCase().includes(q) ||
      c.targetRole.toLowerCase().includes(q) ||
      c.aiProfileSummary.toLowerCase().includes(q)
  );
};

export const getCandidateById = async (id: string): Promise<RecruiterCandidate | undefined> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/recruiter/candidates/${id}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(250);
  return sampleCandidatesPool.find((c) => c.id === id) || sampleCandidatesPool[0];
};

export const getCandidateProfile = async (_id?: string): Promise<CandidateProfile> => {
  await delay(200);
  return sampleCandidate;
};

export const getJobVacancies = async (): Promise<JobVacancy[]> => {
  await delay(250);
  return sampleJobVacancies;
};

export const createJobDescription = async (job: Partial<JobVacancy>): Promise<JobVacancy> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/recruiter/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(job),
      });
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, using simulated persistence.');
    }
  }

  await delay(400);
  const newJob: JobVacancy = {
    id: 'job-' + Date.now(),
    title: job.title || 'New Target Role',
    department: job.department || 'Engineering',
    location: job.location || 'Remote',
    type: job.type || 'Full-time',
    description: job.description || '',
    requiredSkills: job.requiredSkills || ['Python', 'SQL'],
    preferredSkills: job.preferredSkills || ['Tableau'],
    minExperienceYears: job.minExperienceYears || 1,
    education: job.education || "Bachelor's degree",
    applicantCount: 1,
    avgMatchScore: 78,
    createdAt: new Date().toISOString().split('T')[0],
  };
  return newJob;
};

export const startInterview = async (
  _role: string,
  _candidateName?: string
): Promise<InterviewQuestionItem[]> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/interview/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: _role, candidate: _candidateName }),
      });
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(350);
  return sampleInterviewQuestions;
};

export const submitInterviewAnswer = async (
  questionId: string,
  answer: string
): Promise<{ success: boolean; evaluation: string; nextQuestionNumber?: number }> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/interview/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: questionId, answer }),
      });
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, simulated evaluation fallback.');
    }
  }

  await delay(500);
  return {
    success: true,
    evaluation: 'Answer evaluated across technical precision and evidence coherence.',
  };
};

export const getInterviewFeedback = async (_sessionId?: string): Promise<InterviewFeedbackSummary> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/interview/feedback?session_id=${_sessionId || 'default'}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(400);
  return sampleInterviewFeedback;
};

export const getReport = async (_candidateId?: string): Promise<FullReportData> => {
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_BASE_URL}/reports?id=${_candidateId || 'cand-001'}`);
      if (res.ok) return await res.json();
    } catch {
      console.warn('Backend unavailable, falling back to mock.');
    }
  }

  await delay(450);
  return sampleFullReport;
};
