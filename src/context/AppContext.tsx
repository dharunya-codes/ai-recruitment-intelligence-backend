import React, { createContext, useCallback, useEffect, useState } from 'react';
import { CandidateProfile, RecruiterProfile, RoleType } from '../types';
import { sampleCandidate } from '../data/mockData';

interface ToastInfo {
  id: string;
  message: string;
  type: 'success' | 'info' | 'warning' | 'error';
}

interface AppContextType {
  currentRole: RoleType;
  setRole: (role: RoleType) => void;
  candidate: CandidateProfile;
  setCandidate: React.Dispatch<React.SetStateAction<CandidateProfile>>;
  recruiter: RecruiterProfile;
  setRecruiter: React.Dispatch<React.SetStateAction<RecruiterProfile>>;
  uploadedFile: File | null;
  setUploadedFile: (file: File | null) => void;
  targetRole: string;
  setTargetRole: (role: string) => void;
  interviewAnswers: Record<string, string>;
  setInterviewAnswer: (questionId: string, answer: string) => void;
  interviewProgressIndex: number;
  setInterviewProgressIndex: (index: number) => void;
  resetInterview: () => void;
  toasts: ToastInfo[];
  showToast: (message: string, type?: 'success' | 'info' | 'warning' | 'error') => void;
  removeToast: (id: string) => void;
  isLoggedIn: boolean;
  candidateAuthenticated: boolean;
  recruiterAuthenticated: boolean;
  userEmail: string;
  login: (email: string, role: RoleType) => void;
  logout: (role?: RoleType) => void;
}

export const AppContext = createContext<AppContextType | undefined>(undefined);

let toastCounter = 0;
const generateToastId = () => `toast-${++toastCounter}-${Date.now()}`;
const candidateAuthKey = 'talentiq_candidate_authenticated';
const recruiterAuthKey = 'talentiq_recruiter_authenticated';
const candidateProfileKey = 'talentiq_candidate_profile';
const recruiterProfileKey = 'talentiq_recruiter_profile';

const readStoredBoolean = (key: string) =>
  typeof window !== 'undefined' && window.localStorage.getItem(key) === 'true';

const readStoredValue = <T,>(key: string, fallback: T): T => {
  if (typeof window === 'undefined') return fallback;
  const stored = window.localStorage.getItem(key);
  if (!stored) return fallback;
  try {
    return JSON.parse(stored) as T;
  } catch {
    return fallback;
  }
};

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentRole, setCurrentRole] = useState<RoleType>('candidate');
  const [candidate, setCandidate] = useState<CandidateProfile>(() =>
    readStoredValue(candidateProfileKey, sampleCandidate)
  );
  const [recruiter, setRecruiter] = useState<RecruiterProfile>(() => readStoredValue(recruiterProfileKey, {
    fullName: '',
    workEmail: '',
    companyName: '',
    companyEmail: '',
    jobTitle: '',
    companyLocation: '',
    industry: '',
    yearsOfExperience: '',
  }));
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [targetRole, setTargetRole] = useState<string>('Data Analyst');
  const [interviewAnswers, setInterviewAnswers] = useState<Record<string, string>>({
    'iq-1':
      'In the Sales Analysis project, I imported the raw CSV records into Pandas DataFrames. First I checked for null values using isna().sum() and dropped duplicates. Then I converted the date string column into proper datetime objects and filled missing regional sales with median values.',
  });
  const [interviewProgressIndex, setInterviewProgressIndex] = useState<number>(0);
  const [toasts, setToasts] = useState<ToastInfo[]>([]);
  const [candidateAuthenticated, setCandidateAuthenticated] = useState(() =>
    readStoredBoolean(candidateAuthKey)
  );
  const [recruiterAuthenticated, setRecruiterAuthenticated] = useState(() =>
    readStoredBoolean(recruiterAuthKey)
  );
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(() =>
    readStoredBoolean(candidateAuthKey) || readStoredBoolean(recruiterAuthKey)
  );
  const [userEmail, setUserEmail] = useState<string>(() =>
    readStoredValue('talentiq_user_email', 'rose.infanta@example.com')
  );

  useEffect(() => {
    window.localStorage.setItem(candidateProfileKey, JSON.stringify(candidate));
  }, [candidate]);

  useEffect(() => {
    window.localStorage.setItem(recruiterProfileKey, JSON.stringify(recruiter));
  }, [recruiter]);

  const setRole = useCallback((role: RoleType) => {
    setCurrentRole(role);
    if (role === 'recruiter') {
      setUserEmail('recruiter.lead@hiretalent.ai');
    } else {
      setUserEmail('rose.infanta@example.com');
    }
  }, []);

  const setInterviewAnswer = (questionId: string, answer: string) => {
    setInterviewAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const resetInterview = () => {
    setInterviewProgressIndex(0);
    setInterviewAnswers({});
  };

  const showToast = (message: string, type: 'success' | 'info' | 'warning' | 'error' = 'success') => {
    const id = generateToastId();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      removeToast(id);
    }, 4000);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const login = (email: string, role: RoleType) => {
    setIsLoggedIn(true);
    setUserEmail(email);
    setCurrentRole(role);
    window.localStorage.setItem('talentiq_user_email', email);
    if (role === 'candidate') {
      setCandidateAuthenticated(true);
      window.localStorage.setItem(candidateAuthKey, 'true');
    } else {
      setRecruiterAuthenticated(true);
      window.localStorage.setItem(recruiterAuthKey, 'true');
    }
    showToast(`Logged in as ${role === 'recruiter' ? 'Recruiter' : 'Candidate'}`, 'success');
  };

  const logout = (role = currentRole) => {
    if (role === 'candidate') {
      setCandidateAuthenticated(false);
      window.localStorage.removeItem(candidateAuthKey);
      window.localStorage.removeItem(candidateProfileKey);
    } else {
      setRecruiterAuthenticated(false);
      window.localStorage.removeItem(recruiterAuthKey);
      window.localStorage.removeItem(recruiterProfileKey);
    }
    setIsLoggedIn(role === 'candidate' ? recruiterAuthenticated : candidateAuthenticated);
    showToast('Logged out successfully', 'info');
  };

  return (
    <AppContext.Provider
      value={{
        currentRole,
        setRole,
        candidate,
        setCandidate,
        recruiter,
        setRecruiter,
        uploadedFile,
        setUploadedFile,
        targetRole,
        setTargetRole,
        interviewAnswers,
        setInterviewAnswer,
        interviewProgressIndex,
        setInterviewProgressIndex,
        resetInterview,
        toasts,
        showToast,
        removeToast,
        isLoggedIn,
        candidateAuthenticated,
        recruiterAuthenticated,
        userEmail,
        login,
        logout,
      }}
    >
      {children}

      {/* Global Toast Notification Container */}
      <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto px-4 py-3 rounded-lg shadow-lg border text-sm font-medium transition-all flex items-center justify-between gap-3 animate-in fade-in slide-in-from-bottom-2 duration-200 ${
              toast.type === 'success'
                ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
                : toast.type === 'error'
                ? 'bg-rose-50 text-rose-900 border-rose-200'
                : toast.type === 'warning'
                ? 'bg-amber-50 text-amber-900 border-amber-200'
                : 'bg-red-50 text-blue-900 border-blue-200'
            }`}
          >
            <span>{toast.message}</span>
            <button
              onClick={() => removeToast(toast.id)}
              className="text-slate-400 hover:text-slate-700 text-xs font-bold px-1"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </AppContext.Provider>
  );
};

export { useApp } from '../hooks/useApp';


