import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { UserCheck, Briefcase, FileSearch, ArrowRight, CheckCircle2, ShieldCheck, Sparkles } from 'lucide-react';

export const RoleSelectionPage: React.FC = () => {
  const { setRole } = useApp();
  const navigate = useNavigate();

  const handleSelect = (role: 'candidate' | 'recruiter') => {
    setRole(role);
    if (role === 'candidate') {
      navigate('/candidate/signin');
    } else {
      navigate('/recruiter/signin');
    }
  };

  return (
    <div className="min-h-[85vh] flex flex-col items-center justify-center px-4 py-12">
      <div className="text-center max-w-xl mx-auto mb-10">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-semibold mb-3">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Interactive Onboarding</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          How would you like to use TalentIQ?
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-2">
          Select your primary mode. You can seamlessly switch between workspaces at any time.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl w-full">
        {/* Candidate Card */}
        <div
          onClick={() => handleSelect('candidate')}
          className="bg-white rounded-2xl border-2 border-slate-200/80 hover:border-red-600 p-8 cursor-pointer transition-all duration-200 shadow-xs hover:shadow-lg flex flex-col justify-between group"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center font-bold text-xl mb-6 border border-red-100 group-hover:bg-red-600 group-hover:text-white transition-colors">
              <UserCheck className="w-7 h-7" />
            </div>

            <div className="flex items-center justify-between mb-1">
              <h3 className="text-2xl font-bold text-slate-900">Candidate</h3>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-red-50 text-red-700 border border-red-200">
                Job Seeker
              </span>
            </div>

            <p className="text-sm font-medium text-red-900/80 mt-1 mb-4 italic">
              "Analyze your resume, identify skill gaps and practice personalized interviews."
            </p>

            <p className="text-xs text-slate-600 leading-relaxed mb-6">
              Ideal for students, new graduates, and professionals looking to optimize their resumes for ATS, find true skill gaps, and practice project-based interviews.
            </p>

            <ul className="space-y-2 text-xs text-slate-600">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>8-point resume quality and error detection</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Role-specific skill gap visual analysis</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Resume evidence checking & proof extraction</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>AI Mock Interview grounded in your resume projects</span>
              </li>
            </ul>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-100">
            <button
              type="button"
              className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-red-600 text-white font-bold text-xs group-hover:bg-red-700 transition-colors shadow-xs"
            >
              <span>Continue as Candidate</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Recruiter Card */}
        <div
          onClick={() => handleSelect('recruiter')}
          className="bg-white rounded-2xl border-2 border-slate-200/80 hover:border-teal-600 p-8 cursor-pointer transition-all duration-200 shadow-xs hover:shadow-lg flex flex-col justify-between group"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-teal-50 text-teal-700 flex items-center justify-center font-bold text-xl mb-6 border border-teal-100 group-hover:bg-teal-700 group-hover:text-white transition-colors">
              <Briefcase className="w-7 h-7" />
            </div>

            <div className="flex items-center justify-between mb-1">
              <h3 className="text-2xl font-bold text-slate-900">Recruiter</h3>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-teal-50 text-teal-800 border border-teal-200">
                Talent Team
              </span>
            </div>

            <p className="text-sm font-medium text-teal-950/80 mt-1 mb-4 italic">
              "Compare candidates against job requirements and understand candidate-role alignment."
            </p>

            <p className="text-xs text-slate-600 leading-relaxed mb-6">
              Designed for hiring managers and recruiters looking for explainable intelligence, verified evidence checks, and transparent talent-JD matching.
            </p>

            <ul className="space-y-2 text-xs text-slate-600">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                <span>Automated JD requirement decomposition</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                <span>Explainable candidate profile summaries</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                <span>Multi-candidate pool comparison & filtering</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                <span>Evidence verification audits before screening calls</span>
              </li>
            </ul>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-100">
            <button
              type="button"
              className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-teal-800 text-white font-bold text-xs group-hover:bg-teal-900 transition-colors shadow-xs"
            >
              <span>Continue as Recruiter</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Public Resume Check Card */}
        <div
          onClick={() => navigate('/public-resume-check')}
          className="bg-white rounded-2xl border-2 border-slate-200/80 hover:border-red-600 p-8 cursor-pointer transition-all duration-200 shadow-xs hover:shadow-lg flex flex-col justify-between group"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center font-bold text-xl mb-6 border border-red-100 group-hover:bg-red-600 group-hover:text-white transition-colors">
              <FileSearch className="w-7 h-7" />
            </div>

            <div className="flex items-center justify-between mb-1">
              <h3 className="text-2xl font-bold text-slate-900">Public Resume Check</h3>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-red-50 text-red-700 border border-red-200">
                No Account
              </span>
            </div>

            <p className="text-sm font-medium text-red-900/80 mt-1 mb-4 italic">
              "Quickly check your resume before creating an account."
            </p>

            <p className="text-xs text-slate-600 leading-relaxed mb-6">
              Quickly check your resume for common mistakes and improvement areas without creating an account.
            </p>

            <ul className="space-y-2 text-xs text-slate-600">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-red-600 shrink-0" />
                <span>PDF and DOCX upload support</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-red-600 shrink-0" />
                <span>Common resume quality checks</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-red-600 shrink-0" />
                <span>Suggestions without private account features</span>
              </li>
            </ul>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-100">
            <button
              type="button"
              onClick={() => navigate('/public-resume-check')}
              className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-red-600 text-white font-bold text-xs group-hover:bg-red-700 transition-colors shadow-xs"
            >
              <span>Check My Resume</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8 text-center text-xs text-slate-400 flex items-center gap-2">
        <ShieldCheck className="w-4 h-4 text-slate-400" />
        <span>You can switch between Candidate and Recruiter mode anytime via the top bar.</span>
      </div>
    </div>
  );
};


