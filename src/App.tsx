import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';

// Layouts
import { PublicLayout } from './layouts/PublicLayout';
import { CandidateLayout } from './layouts/CandidateLayout';
import { RecruiterLayout } from './layouts/RecruiterLayout';
import { InterviewLayout } from './layouts/InterviewLayout';

// Public & Auth Pages
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RoleSignInPage } from './pages/RoleSignInPage';
import { SignupPage } from './pages/SignupPage';
import { RoleSelectionPage } from './pages/RoleSelectionPage';
import { ReportsPage } from './pages/ReportsPage';

// Candidate Suite Pages
import { CandidateDashboardPage } from './pages/CandidateDashboardPage';
import { ResumeUploadPage } from './pages/ResumeUploadPage';
import { ResumeAnalysisPage } from './pages/ResumeAnalysisPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { EvidenceCheckerPage } from './pages/EvidenceCheckerPage';
import { JobMatchPage } from './pages/JobMatchPage';
import { CandidateJobDescriptionPage } from './pages/CandidateJobDescriptionPage';

// Recruiter Suite Pages
import { RecruiterDashboardPage } from './pages/RecruiterDashboardPage';
import { JobDescriptionPage } from './pages/JobDescriptionPage';
import { CandidateMatchingPage } from './pages/CandidateMatchingPage';
import { CandidateDetailsPage } from './pages/CandidateDetailsPage';
import { BulkResumeAnalysisPage } from './pages/BulkResumeAnalysisPage';

// Mock Interview Pages
import { MockInterviewPage } from './pages/MockInterviewPage';
import { InterviewFeedbackPage } from './pages/InterviewFeedbackPage';

export const App: React.FC = () => {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          {/* Public & Authentication Routes */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/candidate/signin" element={<RoleSignInPage role="candidate" />} />
            <Route path="/recruiter/signin" element={<RoleSignInPage role="recruiter" />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/role-selection" element={<RoleSelectionPage />} />
            <Route path="/reports" element={<ReportsPage />} />
          </Route>

          {/* Candidate Experience Suite */}
          <Route path="/candidate" element={<CandidateLayout />}>
            <Route index element={<Navigate to="/candidate/dashboard" replace />} />
            <Route path="dashboard" element={<CandidateDashboardPage />} />
            <Route path="resume" element={<ResumeUploadPage />} />
            <Route path="analysis" element={<ResumeAnalysisPage />} />
            <Route path="skill-gap" element={<SkillGapPage />} />
            <Route path="evidence" element={<EvidenceCheckerPage />} />
            <Route path="job-match" element={<JobMatchPage />} />
            <Route path="job-description" element={<CandidateJobDescriptionPage />} />
          </Route>

          {/* Recruiter Experience Suite */}
          <Route path="/recruiter" element={<RecruiterLayout />}>
            <Route index element={<Navigate to="/recruiter/dashboard" replace />} />
            <Route path="dashboard" element={<RecruiterDashboardPage />} />
            <Route path="job" element={<JobDescriptionPage />} />
            <Route path="candidates" element={<CandidateMatchingPage />} />
            <Route path="candidate/:id" element={<CandidateDetailsPage />} />
            <Route path="bulk-resume-analysis" element={<BulkResumeAnalysisPage />} />
          </Route>

          {/* Distraction-Free AI Mock Interview Arena */}
          <Route path="/interview" element={<InterviewLayout />}>
            <Route index element={<MockInterviewPage />} />
            <Route path="feedback" element={<InterviewFeedbackPage />} />
          </Route>

          {/* Fallback Catch-All */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
};

export default App;


