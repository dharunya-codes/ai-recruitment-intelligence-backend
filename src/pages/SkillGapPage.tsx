import React from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { sampleSkillGap } from '../data/mockData';
import { SkillMatchCard } from '../components/SkillMatchCard';
import {
  Sparkles,
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  BookOpen,
} from 'lucide-react';

export const SkillGapPage: React.FC = () => {
  const { targetRole } = useApp();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Target Role Intelligence</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Skill Gap Analysis
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Visual comparison of your verified resume evidence against target{' '}
            <strong className="text-slate-800">{targetRole}</strong> core competencies.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/candidate/evidence"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <span>Inspect Evidence Proof</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Target Role & Required Skills Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Evaluated Position
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-0.5">{targetRole}</h2>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs px-3 py-1 rounded-lg bg-red-50 text-red-700 font-bold border border-red-100">
              6 Core Requirements
            </span>
          </div>
        </div>

        <div className="mt-4">
          <span className="text-xs font-semibold text-slate-600 block mb-2">
            Standard Industry Requirements for this Role:
          </span>
          <div className="flex flex-wrap gap-2">
            {sampleSkillGap.requiredSkills.map((req, idx) => (
              <span
                key={idx}
                className="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 text-xs font-semibold border border-slate-200"
              >
                {req}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Crucial Ethical Recommendation Banner */}
      <div className="bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent rounded-2xl border-2 border-amber-300/80 p-5 sm:p-6 text-amber-950 flex items-start gap-4">
        <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center shrink-0 border border-amber-300">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-amber-900 mb-1">
            Ethical Skill Representation Principle
          </h3>
          <p className="text-xs text-amber-900 leading-relaxed">
            <strong>Never falsely add skills you do not have to trick an ATS.</strong> If you genuinely possess a missing or weakly evidenced skill (e.g. Power BI or SQL), consider adding relevant project, certification, education or experience evidence to prove your proficiency transparently.
          </p>
        </div>
      </div>

      {/* 3-Column Visual Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Column 1: Matched Skills */}
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-xl bg-emerald-50 border border-emerald-200/80">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <h3 className="text-xs font-bold text-emerald-900 uppercase tracking-wider">
                Matched Skills ({sampleSkillGap.matchedSkills.length})
              </h3>
            </div>
            <span className="text-[11px] font-bold text-emerald-700 bg-white px-2 py-0.5 rounded-full border border-emerald-200">
              Verified
            </span>
          </div>

          <p className="text-[11px] text-slate-500 px-1">
            Skills supported by multiple project descriptions and syntax instances.
          </p>

          <div className="space-y-3">
            {sampleSkillGap.matchedSkills.map((skill) => (
              <SkillMatchCard key={skill.name} skill={skill} />
            ))}
          </div>
        </div>

        {/* Column 2: Weak Evidence */}
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-xl bg-amber-50 border border-amber-200/80">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <h3 className="text-xs font-bold text-amber-900 uppercase tracking-wider">
                Weak Evidence ({sampleSkillGap.weakEvidenceSkills.length})
              </h3>
            </div>
            <span className="text-[11px] font-bold text-amber-800 bg-white px-2 py-0.5 rounded-full border border-amber-200">
              Keyword Only
            </span>
          </div>

          <p className="text-[11px] text-slate-500 px-1">
            Listed in skills or coursework but missing descriptive query or methodology proof.
          </p>

          <div className="space-y-3">
            {sampleSkillGap.weakEvidenceSkills.map((skill) => (
              <SkillMatchCard key={skill.name} skill={skill} />
            ))}
          </div>
        </div>

        {/* Column 3: Missing Skills */}
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-xl bg-rose-50 border border-rose-200/80">
            <div className="flex items-center gap-2">
              <XCircle className="w-4 h-4 text-rose-600" />
              <h3 className="text-xs font-bold text-rose-900 uppercase tracking-wider">
                Missing Skills ({sampleSkillGap.missingSkills.length})
              </h3>
            </div>
            <span className="text-[11px] font-bold text-rose-700 bg-white px-2 py-0.5 rounded-full border border-rose-200">
              Not Found
            </span>
          </div>

          <p className="text-[11px] text-slate-500 px-1">
            Expected by recruiters for this role but not detected anywhere in the document.
          </p>

          <div className="space-y-3">
            {sampleSkillGap.missingSkills.map((skill) => (
              <SkillMatchCard key={skill.name} skill={skill} />
            ))}
          </div>
        </div>
      </div>

      {/* Suggested Upskilling Roadmap */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
        <div className="flex items-center gap-2 mb-3">
          <BookOpen className="w-4 h-4 text-red-600" />
          <h3 className="text-sm font-bold text-slate-900">
            Genuine Evidence Building Roadmap for Rose Infanta
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <h4 className="font-bold text-slate-900 mb-1">Bridge the Power BI Gap</h4>
            <p className="text-slate-600 leading-relaxed mb-2">
              Create an interactive Power BI dashboard using a public Kaggle dataset (e.g. Retail Sales). Publish the report on NovyPro or GitHub with screenshots.
            </p>
            <span className="text-[11px] text-red-600 font-semibold">
              Est. time: 4-6 hours of portfolio work
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <h4 className="font-bold text-slate-900 mb-1">Strengthen SQL Evidence</h4>
            <p className="text-slate-600 leading-relaxed mb-2">
              Update your Sales Analysis bullet point to state: "Authored PostgreSQL queries using CTEs and window functions (ROW_NUMBER) to partition customer cohorts."
            </p>
            <span className="text-[11px] text-emerald-600 font-semibold">
              Zero additional software needed — update existing project bullet
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};


