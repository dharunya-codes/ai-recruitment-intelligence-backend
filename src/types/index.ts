// Type definitions for AI Resume Intelligence & Interview Platform

export type RoleType = 'candidate' | 'recruiter';

export type EvidenceStrength = 'Strong' | 'Moderate' | 'Weak' | 'None' | 'Not Detected';
export type MatchStatus = 'Matched' | 'Partial' | 'Missing';
export type SectionStatus = 'Good' | 'Needs Improvement' | 'Critical';

export interface ProjectItem {
  id: string;
  title: string;
  role: string;
  technologies: string[];
  description: string;
  evidenceStrength: EvidenceStrength;
  measurableOutcome?: string;
}

export interface EducationItem {
  degree: string;
  institution: string;
  year: string;
  grade?: string;
}

export interface CertificationItem {
  title: string;
  issuer: string;
  year: string;
  verificationUrl?: string;
}

export interface CandidateProfile {
  id: string;
  name: string;
  email: string;
  phone: string;
  location: string;
  targetRole: string;
  summary: string;
  skills: string[];
  projects: ProjectItem[];
  education: EducationItem[];
  certifications: CertificationItem[];
  uploadedResumeName?: string;
  lastAnalyzedAt?: string;
  collegeUniversity?: string;
  degree?: string;
  department?: string;
  graduationYear?: string;
  yearsOfExperience?: string;
}

export interface RecruiterProfile {
  fullName: string;
  workEmail: string;
  companyName: string;
  companyEmail: string;
  jobTitle: string;
  companyLocation: string;
  industry: string;
  yearsOfExperience: string;
}

export interface CandidateJobDescription {
  jobTitle: string;
  companyName: string;
  description: string;
}

export interface RecruiterJobDescription {
  jobTitle: string;
  companyName: string;
  description: string;
  requiredSkills: string[];
  minExperience: string;
  education: string;
}

export interface QualitySection {
  title: string;
  status: SectionStatus;
  score: number; // 0 - 100
  shortExplanation: string;
  recommendation: string;
}

export interface ResumeScoreBreakdown {
  overallScore: number;
  atsScore: number;
  atsGrade: string;
  sections: {
    contactInfo: QualitySection;
    formatting: QualitySection;
    grammar: QualitySection;
    spelling: QualitySection;
    datesConsistency: QualitySection;
    projectDescription: QualitySection;
    achievementStatements: QualitySection;
    atsCompatibility: QualitySection;
  };
}

export interface SkillItem {
  name: string;
  status: 'matched' | 'weak_evidence' | 'missing';
  evidenceStrength: EvidenceStrength;
  detectedIn: string[];
  recommendation?: string;
}

export interface SkillGapData {
  targetRole: string;
  requiredSkills: string[];
  matchedSkills: SkillItem[];
  weakEvidenceSkills: SkillItem[];
  missingSkills: SkillItem[];
  ethicalGuidance: string;
}

export interface EvidenceDetail {
  skill: string;
  status: 'Found' | 'Not Detected';
  evidenceLocations: string[];
  projectsReferenced: string[];
  strength: EvidenceStrength;
  snippets: string[];
  confidence: number;
}

export interface SkillQuizQuestion {
  id: string;
  skill: string;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

export interface SkillMatrixRow {
  skill: string;
  status: MatchStatus;
  evidence: EvidenceStrength;
  notes: string;
}

export interface JobMatchComparison {
  targetRole: string;
  jobTitle: string;
  matchPercentage: number;
  skillMatrix: SkillMatrixRow[];
  relevantProjects: {
    title: string;
    techUsed: string[];
    relevanceScore: number;
    description: string;
    impact: string;
  }[];
  missingRequirements: string[];
  weakAreas: string[];
  recommendations: string[];
}

export interface RecruiterCandidate {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  targetRole: string;
  experienceYears: number;
  skillMatchPct: number;
  experienceMatchPct: number;
  projectRelevancePct: number;
  evidenceStrength: EvidenceStrength;
  jdAlignment: 'High' | 'Medium' | 'Low';
  missingRequirements: string[];
  aiProfileSummary: string;
  status: 'Under Review' | 'Interview Scheduled' | 'Shortlisted' | 'Archived';
  resumeFileName: string;
  analyzedDate: string;
}

export interface BulkResumeCandidate {
  id: string;
  name: string;
  email: string;
  phone: string;
  location: string;
  resumeFile: string;
  targetRole: string;
  experience: number;
  education: string;
  skills: string[];
  matchedSkills: string[];
  missingSkills: string[];
  resumeScore: number;
  skillMatch: number;
  atsScore: number;
  experienceMatch: number;
  educationMatch: number;
  evidenceStrength: 'Strong' | 'Medium' | 'Weak';
  status: 'Analyzed' | 'Processing' | 'Needs Review';
}

export interface JobVacancy {
  id: string;
  title: string;
  department: string;
  location: string;
  type: string;
  description: string;
  requiredSkills: string[];
  preferredSkills: string[];
  minExperienceYears: number;
  education: string;
  applicantCount: number;
  avgMatchScore: number;
  createdAt: string;
}

export interface InterviewQuestionItem {
  id: string;
  number: number;
  skill: string;
  question: string;
  options: string[];
  correctAnswer: string;
  explanation: string;
  context: string;
  expectedDurationSeconds: number;
  targetRole: string;
  skillTested: string;
  projectReferenced?: string;
}

export interface InterviewEvaluation {
  questionId: string;
  questionNumber: number;
  question: string;
  candidateAnswer: string;
  technicalUnderstanding: 'Excellent' | 'Good' | 'Needs Improvement';
  explanation: string;
  expectedConcepts: string[];
  improvementSuggestion: string;
}

export interface InterviewCategoryScores {
  technicalKnowledge: number;
  communication: number;
  relevance: number;
  completeness: number;
  confidence: number;
  problemSolving: number;
}

export interface InterviewFeedbackSummary {
  overallScore: number;
  candidateName: string;
  targetRole: string;
  completedAt: string;
  categories: InterviewCategoryScores;
  evaluations: InterviewEvaluation[];
  executiveSummary: string;
  keyStrengths: string[];
  actionableNextSteps: string[];
}

export interface FullReportData {
  candidate: CandidateProfile;
  resumeScore: ResumeScoreBreakdown;
  skillGap: SkillGapData;
  evidence: EvidenceDetail[];
  jobMatch: JobMatchComparison;
  interviewFeedback: InterviewFeedbackSummary;
  generatedDate: string;
  readinessLevel: 'High' | 'Moderate' | 'Needs Development';
}


