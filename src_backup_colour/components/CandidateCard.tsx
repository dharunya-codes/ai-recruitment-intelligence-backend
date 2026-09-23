import React from 'react';
import { RecruiterCandidate } from '../types';
import { StatusBadge } from './StatusBadge';
import { ProgressBar } from './ProgressBar';
import { ArrowRight, Bot, Briefcase, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';

interface CandidateCardProps {
  candidate: RecruiterCandidate;
  className?: string;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({ candidate, className = '' }) => {
  return (
    <div
      className={`bg-white rounded-xl border border-slate-200/90 p-5 shadow-xs hover:shadow-md transition-all duration-200 ${className}`}
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-800 text-white font-bold text-lg flex items-center justify-center shadow-xs">
            {candidate.name
              .split(' ')
              .map((n) => n[0])
              .join('')}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-slate-900">{candidate.name}</h3>
              <span className="text-xs px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-medium">
                {candidate.experienceYears}y exp
              </span>
            </div>
            <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
              <Briefcase className="w-3.5 h-3.5 text-slate-400" />
              <span>Target: {candidate.targetRole}</span>
              <span>•</span>
              <FileText className="w-3.5 h-3.5 text-slate-400" />
              <span>{candidate.resumeFileName}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <StatusBadge status={candidate.status} size="sm" />
          <StatusBadge status={`JD Alignment: ${candidate.jdAlignment}`} size="sm" />
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4 p-3 bg-slate-50/80 rounded-xl border border-slate-100 text-center">
        <div>
          <span className="text-[11px] font-semibold uppercase text-slate-400">Skill Match</span>
          <p className="text-lg font-bold text-indigo-700">{candidate.skillMatchPct}%</p>
          <ProgressBar value={candidate.skillMatchPct} size="sm" className="mt-1" />
        </div>

        <div>
          <span className="text-[11px] font-semibold uppercase text-slate-400">Exp Match</span>
          <p className="text-lg font-bold text-slate-800">{candidate.experienceMatchPct}%</p>
          <ProgressBar value={candidate.experienceMatchPct} size="sm" className="mt-1" />
        </div>

        <div>
          <span className="text-[11px] font-semibold uppercase text-slate-400">Project Rel.</span>
          <p className="text-lg font-bold text-slate-800">{candidate.projectRelevancePct}%</p>
          <ProgressBar value={candidate.projectRelevancePct} size="sm" className="mt-1" />
        </div>

        <div>
          <span className="text-[11px] font-semibold uppercase text-slate-400">Evidence</span>
          <p className="text-sm font-bold text-slate-800 mt-1">
            <StatusBadge status={candidate.evidenceStrength} size="sm" />
          </p>
        </div>
      </div>

      {/* Explainable Candidate-Role Analysis */}
      <div className="p-3.5 rounded-lg bg-indigo-50/40 border border-indigo-100 text-xs">
        <div className="flex items-center gap-1.5 font-bold text-indigo-950 mb-1">
          <Bot className="w-4 h-4 text-indigo-600" />
          <span>Explainable Candidate-Role Intelligence</span>
        </div>
        <p className="text-slate-700 leading-relaxed italic">
          "{candidate.aiProfileSummary}"
        </p>
      </div>

      {/* Missing Requirements Tag List */}
      {candidate.missingRequirements.length > 0 && (
        <div className="mt-3 text-xs flex items-center gap-2 flex-wrap">
          <span className="text-slate-400 font-medium">Missing Requirements:</span>
          {candidate.missingRequirements.map((req, i) => (
            <span
              key={i}
              className="px-2 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 text-[11px] font-medium"
            >
              {req}
            </span>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
        <span className="text-slate-400">Analyzed {candidate.analyzedDate}</span>
        <Link
          to={`/recruiter/candidate/${candidate.id}`}
          className="inline-flex items-center gap-1.5 font-semibold text-indigo-600 hover:text-indigo-800 hover:underline"
        >
          <span>View Deep Audit Dossier</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
