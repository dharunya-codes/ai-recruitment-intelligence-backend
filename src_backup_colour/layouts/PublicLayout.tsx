import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Sparkles, ArrowRight, ShieldCheck, Globe, Share2 } from 'lucide-react';

export const PublicLayout: React.FC = () => {
  const location = useLocation();
  const isAuthPage = ['/login', '/signup', '/role-selection'].includes(location.pathname);

  return (
    <div className="min-h-screen bg-slate-50/50 flex flex-col font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900">
      {/* Top Header */}
      <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 text-white flex items-center justify-center shadow-xs group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-slate-900 block leading-none">
                TalentIQ
              </span>
              <span className="text-[10px] font-semibold tracking-wider uppercase text-indigo-600">
                AI Resume Intelligence
              </span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-xs font-semibold text-slate-600">
            <Link to="/candidate/dashboard" className="hover:text-indigo-600 transition-colors">
              Candidate Suite
            </Link>
            <Link to="/recruiter/dashboard" className="hover:text-indigo-600 transition-colors">
              Recruiter Hub
            </Link>
            <Link to="/interview" className="hover:text-indigo-600 transition-colors">
              AI Mock Interview
            </Link>
            <Link to="/candidate/evidence" className="hover:text-indigo-600 transition-colors">
              Evidence Engine
            </Link>
          </nav>

          <div className="flex items-center gap-2.5">
            <Link
              to="/login"
              className="text-xs font-semibold px-3.5 py-2 text-slate-700 hover:text-indigo-600 transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/role-selection"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-xs shadow-indigo-200"
            >
              <span>Get Started</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer (compact for auth pages, full for landing) */}
      {!isAuthPage && (
        <footer className="bg-white border-t border-slate-200/80 py-12 px-4 sm:px-6 text-xs text-slate-500">
          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div className="md:col-span-1">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center">
                  <Sparkles className="w-4 h-4" />
                </div>
                <span className="font-bold text-slate-900 text-sm">TalentIQ AI</span>
              </div>
              <p className="text-slate-500 leading-relaxed text-[11px]">
                Explainable resume intelligence, deep skill gap detection, and personalized AI mock interviews built for modern careers.
              </p>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">
                Candidate Suite
              </h4>
              <ul className="space-y-2 text-[11px]">
                <li><Link to="/candidate/resume" className="hover:text-indigo-600">Resume Upload & ATS Parse</Link></li>
                <li><Link to="/candidate/analysis" className="hover:text-indigo-600">8-Point Quality Inspection</Link></li>
                <li><Link to="/candidate/skill-gap" className="hover:text-indigo-600">Skill Gap Analysis</Link></li>
                <li><Link to="/candidate/evidence" className="hover:text-indigo-600">Evidence Proof Checker</Link></li>
                <li><Link to="/interview" className="hover:text-indigo-600">Personalized Mock Interview</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">
                Recruiter Hub
              </h4>
              <ul className="space-y-2 text-[11px]">
                <li><Link to="/recruiter/dashboard" className="hover:text-indigo-600">Recruiter Dashboard</Link></li>
                <li><Link to="/recruiter/job" className="hover:text-indigo-600">Job Requirement Parser</Link></li>
                <li><Link to="/recruiter/candidates" className="hover:text-indigo-600">Explainable Candidate Matching</Link></li>
                <li><Link to="/reports" className="hover:text-indigo-600">Comprehensive Hiring Reports</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">
                Platform Integrity
              </h4>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 mb-3">
                <div className="flex items-center gap-1.5 text-slate-800 font-semibold text-[11px] mb-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Ethical Guidance Policy</span>
                </div>
                <p className="text-[10px] text-slate-500 leading-normal">
                  We never encourage falsely claiming unpossessed skills. Every recommendation is anchored in genuine verified evidence.
                </p>
              </div>
              <div className="flex items-center gap-3 text-slate-400">
                <span className="p-1.5 rounded-lg hover:bg-slate-100 cursor-pointer flex items-center gap-1 text-[11px]"><Globe className="w-3.5 h-3.5" /> Web</span>
                <span className="p-1.5 rounded-lg hover:bg-slate-100 cursor-pointer flex items-center gap-1 text-[11px]"><Share2 className="w-3.5 h-3.5" /> Share</span>
              </div>
            </div>
          </div>

          <div className="max-w-7xl mx-auto pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-400">
            <span>© {new Date().getFullYear()} TalentIQ AI Platform. Designed for modern recruitment & talent intelligence.</span>
            <div className="flex gap-4">
              <span className="hover:text-slate-600 cursor-pointer">Privacy Policy</span>
              <span>•</span>
              <span className="hover:text-slate-600 cursor-pointer">Terms of Service</span>
              <span>•</span>
              <span className="hover:text-slate-600 cursor-pointer">API Ready (FastAPI)</span>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
};
