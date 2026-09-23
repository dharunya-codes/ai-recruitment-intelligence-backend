import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  FileSearch,
  Mic,
  Users,
  Target,
  ArrowUpRight,
  Star,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-20 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 sm:pt-20">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-red-200/40 via-red-200/30 to-teal-100/30 rounded-full blur-3xl -z-10 pointer-events-none" />

        <div className="max-w-5xl mx-auto px-4 sm:px-6 text-center">
          {/* Top Pill */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 border border-red-200/80 text-red-700 text-xs font-semibold mb-6 shadow-2xs">
            <Sparkles className="w-3.5 h-3.5 text-red-600" />
            <span>AI Resume Intelligence & Interview Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.15]">
            Bridging the gap between{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-600 via-red-600 to-red-800">
              real resume evidence
            </span>{' '}
            and career success.
          </h1>

          <p className="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Analyze resume quality, uncover verified skill gaps against real job descriptions, and practice personalized AI mock interviews grounded in your actual projects.
          </p>

          {/* Dual Action CTAs */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <Link
              to="/role-selection"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-red-600 text-white font-bold text-sm hover:bg-red-700 shadow-md shadow-red-200 transition-all hover:scale-[1.01]"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/candidate/resume"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-50 transition-all shadow-xs"
            >
              <span>Upload & Analyze Resume</span>
            </Link>
          </div>

          {/* Social Proof Stats */}
          <div className="mt-14 pt-8 border-t border-slate-200/60 grid grid-cols-2 sm:grid-cols-4 gap-6 text-center max-w-3xl mx-auto">
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-slate-900">8-Point</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">ATS Quality Audit</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-red-600">100%</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Evidence Grounded</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-slate-900">Adaptive</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">AI Mock Interviews</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-emerald-600">Zero</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">False Skill Inflation</p>
            </div>
          </div>
        </div>
      </section>

      {/* Two Dedicated Modes Section */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-10">
          <h2 className="text-xs font-bold uppercase tracking-wider text-red-600">
            Tailored Experiences
          </h2>
          <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Choose Your Platform Portal
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Candidate Card */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group">
            <div>
              <div className="w-12 h-12 rounded-xl bg-red-50 text-red-600 flex items-center justify-center font-bold text-lg mb-6 border border-red-100">
                <Target className="w-6 h-6" />
              </div>
              <span className="text-xs font-bold uppercase text-red-600 tracking-wider">
                Candidate Mode
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-1 mb-3">
                Job Seeker & Student Intelligence
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-6">
                Analyze your resume, identify skill gaps against your target role (e.g. Data Analyst), inspect proof points, and practice personalized interviews.
              </p>

              <ul className="space-y-2.5 text-xs text-slate-700">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>8-Point quality inspection (Grammar, Formatting, ATS Score)</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Visual skill gap breakdown (Matched vs Weak vs Missing)</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>AI Mock Interview asking questions about your actual projects</span>
                </li>
              </ul>
            </div>

            <div className="mt-8 pt-6 border-t border-slate-100">
              <Link
                to="/candidate/signin"
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition-colors"
              >
                <span>Launch Candidate Dashboard</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>

          {/* Recruiter Card */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group">
            <div>
              <div className="w-12 h-12 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center font-bold text-lg mb-6 border border-teal-100">
                <Users className="w-6 h-6" />
              </div>
              <span className="text-xs font-bold uppercase text-teal-700 tracking-wider">
                Recruiter Mode
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-1 mb-3">
                Explainable Candidate-Role Alignment
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-6">
                Compare candidates against job requirements and understand genuine candidate-role alignment with evidence-backed reasoning, not black-box filters.
              </p>

              <ul className="space-y-2.5 text-xs text-slate-700">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                  <span>Explainable candidate profile summaries</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                  <span>Automated Job Description parser & skill taxonomy</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                  <span>Candidate pool rankings with missing requirement audits</span>
                </li>
              </ul>
            </div>

            <div className="mt-8 pt-6 border-t border-slate-100">
              <Link
                to="/recruiter/signin"
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-teal-800 text-white text-xs font-bold hover:bg-teal-900 transition-colors"
              >
                <span>Launch Recruiter Dashboard</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Core Platform Features Grid */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-red-600">
            Intelligent Features
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Engineered for Explainable Career Readiness
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:border-red-300 transition-all">
            <div className="w-10 h-10 rounded-xl bg-red-50 text-red-600 flex items-center justify-center mb-4">
              <FileSearch className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              Resume Quality Analysis
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Pinpoint formatting glitches, spelling discrepancies, date mismatches, and passive bullet points before ATS scanners discard your application.
            </p>
            <Link
              to="/candidate/analysis"
              className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-red-600 hover:text-red-800"
            >
              <span>Explore Analysis</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:border-red-300 transition-all">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center mb-4">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              Resume Evidence Checker
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Verify if claimed skills are backed by real project bullets or only listed as standalone keywords. Differentiates strong proof from weak claims.
            </p>
            <Link
              to="/candidate/evidence"
              className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-teal-700 hover:text-teal-900"
            >
              <span>View Evidence Engine</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:border-red-300 transition-all">
            <div className="w-10 h-10 rounded-xl bg-red-50 text-red-600 flex items-center justify-center mb-4">
              <Mic className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              Adaptive AI Mock Interview
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Interview questions dynamically probe the projects listed in your resume. Evaluates technical concepts, communication, and depth of knowledge.
            </p>
            <Link
              to="/interview"
              className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-red-600 hover:text-red-800"
            >
              <span>Start Mock Interview</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* How it Works Walkthrough */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="bg-gradient-to-br from-red-900 to-slate-900 rounded-3xl p-8 sm:p-12 text-white relative overflow-hidden">
          <div className="max-w-2xl mb-10">
            <span className="text-xs font-bold uppercase tracking-wider text-red-300">
              Structured Workflow
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold mt-1">
              How TalentIQ Intelligence Works
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
              Three seamless steps to transform raw resumes into transparent, interview-tested career alignment.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xs">
              <span className="text-2xl font-black text-red-400">01</span>
              <h3 className="text-base font-bold mt-2 mb-1.5">Upload & Parse</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Upload your PDF or DOCX resume. Specify your desired role like <strong>Data Analyst</strong> or paste a specific target JD.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xs">
              <span className="text-2xl font-black text-red-400">02</span>
              <h3 className="text-base font-bold mt-2 mb-1.5">Deep Evidence Audit</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Our semantic parser evaluates matched skills, identifies weak evidence, and highlights missing competencies with ethical advice.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xs">
              <span className="text-2xl font-black text-red-400">03</span>
              <h3 className="text-base font-bold mt-2 mb-1.5">Practice & Prove</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Answer AI interview questions addressing your actual project details and receive instant multi-dimensional coaching feedback.
              </p>
            </div>
          </div>

          <div className="mt-10 pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-xs text-red-200">
              <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
              <span>Tested on real candidate resumes across data science, engineering & product.</span>
            </div>
            <Link
              to="/role-selection"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-slate-900 text-xs font-bold hover:bg-slate-100 transition-colors"
            >
              <span>Get Started Now</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};


