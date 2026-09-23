import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { sampleFullReport } from '../data/mockData';
import { StatusBadge } from '../components/StatusBadge';
import { ProgressBar } from '../components/ProgressBar';
import {
  Download,
  Sparkles,
  CheckCircle2,
  ShieldCheck,
  Briefcase,
  Calendar,
} from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const { candidate, targetRole, showToast } = useApp();
  const report = sampleFullReport;
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = () => {
    setIsDownloading(true);
    showToast('Compiling executive intelligence PDF dossier...', 'info');
    setTimeout(() => {
      setIsDownloading(false);
      window.print();
    }, 800);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12 print:p-0 print:space-y-4">
      {/* Header with Download Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 no-print">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Unified Executive Audit</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Comprehensive Candidate Intelligence Report
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Complete multi-pillar audit combining resume formatting, verified skill proof, and AI interview performance.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={handleDownload}
            disabled={isDownloading}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-xs disabled:opacity-50"
          >
            <Download className="w-4 h-4" />
            <span>{isDownloading ? 'Preparing PDF...' : 'Download Report'}</span>
          </button>
        </div>
      </div>

      {/* Printable Report Dossier Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-10 space-y-8 print:shadow-none print:border-0">
        {/* Document Header & Candidate Meta */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-xs">
                IQ
              </span>
              <span className="font-extrabold text-base tracking-tight text-slate-900">
                TalentIQ Intelligence Dossier
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
              {candidate.name}
            </h2>
            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1">
              <span className="flex items-center gap-1 font-medium text-slate-700">
                <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                Target Role: {targetRole}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-slate-400" />
                Report Date: {report.generatedDate}
              </span>
              <span>•</span>
              <span>ID: {candidate.id}</span>
            </div>
          </div>

          <div className="flex flex-col items-start sm:items-end">
            <span className="text-xs text-slate-400 uppercase font-bold">Readiness Verdict</span>
            <div className="mt-1">
              <StatusBadge status={`Readiness: ${report.readinessLevel}`} size="lg" />
            </div>
          </div>
        </div>

        {/* Executive 4-Pillar Score Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
              Resume Quality
            </span>
            <span className="text-2xl sm:text-3xl font-black text-slate-900 mt-1 block">
              {report.resumeScore.overallScore}/100
            </span>
            <span className="text-[11px] font-semibold text-emerald-700">
              Grade {report.resumeScore.atsGrade}
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
              JD Skill Match
            </span>
            <span className="text-2xl sm:text-3xl font-black text-indigo-700 mt-1 block">
              {report.jobMatch.matchPercentage}%
            </span>
            <span className="text-[11px] font-semibold text-slate-500">
              Against Data Analyst JD
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
              Evidence Strength
            </span>
            <span className="text-xl sm:text-2xl font-black text-slate-900 mt-1 block">
              Moderate
            </span>
            <span className="text-[11px] font-semibold text-amber-700">
              2 Strong / 2 Weak / 1 Missing
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
              Interview Score
            </span>
            <span className="text-2xl sm:text-3xl font-black text-emerald-700 mt-1 block">
              {report.interviewFeedback.overallScore}/100
            </span>
            <span className="text-[11px] font-semibold text-emerald-700">
              4 Questions Evaluated
            </span>
          </div>
        </div>

        {/* Section 1: Resume Score & Quality Details */}
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900">
              1. Resume Quality & Structural Inspection
            </h3>
            <span className="text-xs font-semibold text-slate-500">
              ATS Compatibility: {report.resumeScore.atsScore}%
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            {Object.entries(report.resumeScore.sections).map(([key, sec]) => (
              <div
                key={key}
                className="p-3 rounded-xl bg-slate-50/70 border border-slate-200/70 flex items-start justify-between gap-3"
              >
                <div>
                  <span className="font-bold text-slate-900">{sec.title}</span>
                  <p className="text-slate-500 text-[11px] mt-0.5">{sec.shortExplanation}</p>
                </div>
                <StatusBadge status={sec.status} size="sm" />
              </div>
            ))}
          </div>
        </div>

        {/* Section 2: Skill Match & Evidence Table */}
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900">
              2. Skill Gap & Evidence Verification
            </h3>
            <span className="text-xs font-semibold text-slate-500">
              Role Standard: {targetRole}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-200 rounded-xl overflow-hidden">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold">
                <tr>
                  <th className="py-2.5 px-4">Required Skill</th>
                  <th className="py-2.5 px-4">Status</th>
                  <th className="py-2.5 px-4">Evidence Level</th>
                  <th className="py-2.5 px-4">Detected Locations</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {report.jobMatch.skillMatrix.map((row) => (
                  <tr key={row.skill}>
                    <td className="py-2.5 px-4 font-bold text-slate-900">{row.skill}</td>
                    <td className="py-2.5 px-4">
                      <StatusBadge status={row.status} size="sm" />
                    </td>
                    <td className="py-2.5 px-4 font-semibold">{row.evidence}</td>
                    <td className="py-2.5 px-4 text-slate-500">{row.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Section 3: AI Mock Interview Performance */}
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900">
              3. AI Mock Interview Performance Breakdown
            </h3>
            <span className="text-xs font-bold text-emerald-700">
              Composite: {report.interviewFeedback.overallScore}/100
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {Object.entries(report.interviewFeedback.categories).map(([k, score]) => (
              <div key={k} className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                <div className="flex justify-between items-center mb-1">
                  <span className="capitalize font-semibold text-slate-700">
                    {k.replace(/([A-Z])/g, ' $1')}
                  </span>
                  <span className="font-bold text-indigo-700">{score}%</span>
                </div>
                <ProgressBar value={score} size="sm" />
              </div>
            ))}
          </div>

          <div className="p-4 rounded-xl bg-indigo-50/60 border border-indigo-100 text-xs text-slate-700">
            <strong className="block text-indigo-950 font-bold mb-1">Interviewer Summary:</strong>
            <p className="leading-relaxed italic">{report.interviewFeedback.executiveSummary}</p>
          </div>
        </div>

        {/* Section 4: Actionable Recommendations & Ethical Principle */}
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900">
              4. Key Recommendations & Career Roadmap
            </h3>
          </div>

          <div className="space-y-2.5 text-xs">
            {report.jobMatch.recommendations.map((rec, i) => (
              <div key={i} className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-50 border border-slate-200/70">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <p className="text-slate-800 leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>

          {/* Ethical Policy Card */}
          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/90 text-xs text-amber-950 flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <strong className="font-bold block text-amber-900 mb-0.5">
                Ethical Evidence Principle:
              </strong>
              <p className="leading-relaxed text-amber-900/90">
                Never falsely claim missing skills to bypass ATS filters. True career advancement relies on documenting real code, portfolio demonstrations, and verified skills.
              </p>
            </div>
          </div>
        </div>

        {/* Footer Signature Block */}
        <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <span>Report Generated by TalentIQ AI Ingestion Engine • Ready for FastAPI Python REST Service</span>
          <span className="font-mono text-[11px]">Verification Hash: SHA256-7a8e2b9c</span>
        </div>
      </div>
    </div>
  );
};
