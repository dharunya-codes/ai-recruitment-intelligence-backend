import React from 'react';
import { Link } from 'react-router-dom';
import { sampleJobMatch } from '../data/mockData';
import { useApp } from '../context/AppContext';
import { StatusBadge } from '../components/StatusBadge';
import { ProgressBar } from '../components/ProgressBar';
import {
  Sparkles,
  FolderGit2,
  AlertCircle,
  Lightbulb,
  Mic,
  TrendingUp,
} from 'lucide-react';

export const JobMatchPage: React.FC = () => {
  const { candidateJobDescription } = useApp();
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Target JD Intelligence</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Resume vs Job Description
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Algorithmic alignment of Rose Infanta's resume against standard{' '}
            <strong className="text-slate-800">{sampleJobMatch.targetRole}</strong> job description.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/interview"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <Mic className="w-3.5 h-3.5" />
            <span>Practice Mock Interview</span>
          </Link>
        </div>
      </div>

      <div className="rounded-xl border border-red-100 bg-red-50/50 p-4 text-xs text-slate-700">
        <strong className="text-red-700">Comparing against:</strong> {candidateJobDescription.jobTitle} at {candidateJobDescription.companyName}
      </div>

      {/* Top Alignment Banner */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Target Job Spec
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-0.5">
            {sampleJobMatch.jobTitle}
          </h2>
          <p className="text-xs text-slate-500 mt-1 max-w-lg">
            Evaluation measures required vs preferred skills, relevance of candidate's past academic & personal projects, and overall JD alignment.
          </p>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-100 min-w-[240px]">
          <div className="text-center">
            <span className="text-3xl font-black text-red-600">
              {sampleJobMatch.matchPercentage}%
            </span>
            <span className="block text-[10px] uppercase font-bold text-slate-400 mt-0.5">
              Overall Fit
            </span>
          </div>
          <div className="flex-1">
            <ProgressBar value={sampleJobMatch.matchPercentage} size="md" />
            <span className="text-[11px] text-slate-500 font-medium block mt-1">
              Solid baseline with project relevance
            </span>
          </div>
        </div>
      </div>

      {/* Required Skills Table */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900">Required Skills Matrix</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Direct mapping of JD requirements to resume proof
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-lg bg-red-50 text-red-700 font-bold border border-red-100">
            6 Skills Evaluated
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50/80 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200/80">
                <th className="py-3 px-5">Skill</th>
                <th className="py-3 px-5">Status</th>
                <th className="py-3 px-5">Evidence Strength</th>
                <th className="py-3 px-5">AI Verification Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {sampleJobMatch.skillMatrix.map((row) => (
                <tr key={row.skill} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-3.5 px-5 font-bold text-slate-900">{row.skill}</td>
                  <td className="py-3.5 px-5">
                    <StatusBadge status={row.status} size="sm" />
                  </td>
                  <td className="py-3.5 px-5">
                    <span
                      className={`inline-flex items-center gap-1 font-semibold ${
                        row.evidence === 'Strong'
                          ? 'text-emerald-700'
                          : row.evidence === 'Weak' || row.evidence === 'Moderate'
                          ? 'text-amber-700'
                          : 'text-rose-700'
                      }`}
                    >
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          row.evidence === 'Strong'
                            ? 'bg-emerald-500'
                            : row.evidence === 'Weak' || row.evidence === 'Moderate'
                            ? 'bg-amber-500'
                            : 'bg-rose-500'
                        }`}
                      />
                      {row.evidence}
                    </span>
                  </td>
                  <td className="py-3.5 px-5 text-slate-600">{row.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Relevant Projects Section */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
        <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
          <FolderGit2 className="w-4 h-4 text-red-600" />
          <span>Relevant Resume Projects</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sampleJobMatch.relevantProjects.map((proj) => (
            <div
              key={proj.title}
              className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-bold text-slate-900">{proj.title}</h4>
                  <span className="text-xs px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                    {proj.relevanceScore}% Match
                  </span>
                </div>

                <div className="flex flex-wrap gap-1.5 mb-2.5">
                  {proj.techUsed.map((t, i) => (
                    <span
                      key={i}
                      className="px-2 py-0.5 rounded bg-white text-slate-700 text-[11px] font-medium border border-slate-200/70"
                    >
                      {t}
                    </span>
                  ))}
                </div>

                <p className="text-xs text-slate-600 mb-2">{proj.description}</p>
              </div>

              <div className="pt-2 border-t border-slate-200/60 text-[11px] text-red-700 font-medium">
                {proj.impact}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Weak Areas & Missing Requirements Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Missing Requirements */}
        <div className="bg-white rounded-2xl border border-rose-200/80 p-6 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-rose-900">
            <AlertCircle className="w-4 h-4 text-rose-600" />
            <h3 className="text-sm font-bold">Missing Job Requirements</h3>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            {sampleJobMatch.missingRequirements.map((req, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 shrink-0" />
                <span>{req}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weak Areas */}
        <div className="bg-white rounded-2xl border border-amber-200/80 p-6 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-amber-900">
            <TrendingUp className="w-4 h-4 text-amber-600" />
            <h3 className="text-sm font-bold">Identified Weak Areas</h3>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            {sampleJobMatch.weakAreas.map((area, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                <span>{area}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommendations Card */}
      <div className="bg-red-50/60 rounded-2xl border border-red-200 p-6">
        <div className="flex items-center gap-2 mb-3 text-red-950 font-bold">
          <Lightbulb className="w-4 h-4 text-red-600" />
          <span>Tailored AI Action Recommendations</span>
        </div>
        <div className="space-y-2.5 text-xs text-slate-700">
          {sampleJobMatch.recommendations.map((rec, idx) => (
            <div key={idx} className="flex items-start gap-2.5 bg-white p-3 rounded-xl border border-red-100">
              <span className="w-5 h-5 rounded-full bg-red-100 text-red-700 flex items-center justify-center font-bold text-[11px] shrink-0">
                {idx + 1}
              </span>
              <p className="leading-relaxed">{rec}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};


