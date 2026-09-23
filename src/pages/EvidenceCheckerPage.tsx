import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { sampleEvidenceDetails } from '../data/mockData';
import { useApp } from '../context/AppContext';
import { EvidenceCard } from '../components/EvidenceCard';
import { SkillVerificationQuiz } from '../components/SkillVerificationQuiz';
import {
  Sparkles,
  ShieldCheck,
  ArrowRight,
  FileCheck2,
  AlertTriangle,
} from 'lucide-react';

export const EvidenceCheckerPage: React.FC = () => {
  const { candidateJobDescription } = useApp();
  const [filterStrength, setFilterStrength] = useState<string>('all');

  const filteredEvidence = sampleEvidenceDetails.filter((item) => {
    if (filterStrength === 'all') return true;
    return item.strength === filterStrength;
  });

  const strongCount = sampleEvidenceDetails.filter((e) => e.strength === 'Strong').length;
  const weakCount = sampleEvidenceDetails.filter((e) => e.strength === 'Weak').length;
  const missingCount = sampleEvidenceDetails.filter((e) => e.strength === 'Not Detected').length;
  const missingSkills = sampleEvidenceDetails
    .filter((evidence) => evidence.status === 'Not Detected' || evidence.strength === 'Not Detected')
    .map((evidence) => evidence.skill);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Semantic Proof Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Resume Evidence Checker
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Validates whether listed technical claims have concrete proof in project descriptions or are only superficial keywords.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/candidate/job-match"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <span>View Job Description Match</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      <div className="rounded-xl border border-red-100 bg-red-50/50 p-4 text-xs text-slate-700">
        <strong className="text-red-700">Evidence aligned to:</strong> {candidateJobDescription.jobTitle} at {candidateJobDescription.companyName}
      </div>

      {/* Summary Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl border border-emerald-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700">
              Strong Evidence
            </span>
            <p className="text-2xl font-bold text-slate-900 mt-0.5">{strongCount} Skills</p>
            <p className="text-xs text-slate-500 mt-1">Found in Skills + Project Bullets</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-amber-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-amber-700">
              Weak Evidence
            </span>
            <p className="text-2xl font-bold text-slate-900 mt-0.5">{weakCount} Skills</p>
            <p className="text-xs text-slate-500 mt-1">Skills section only, no project proof</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
            <AlertTriangle className="w-5 h-5" />
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-rose-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-rose-700">
              Not Detected
            </span>
            <p className="text-2xl font-bold text-slate-900 mt-0.5">{missingCount} Skill</p>
            <p className="text-xs text-slate-500 mt-1">Absent from entire document</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center font-bold">
            <FileCheck2 className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <h2 className="text-base font-bold text-slate-900">
          Evaluated Skill Evidence Cards ({filteredEvidence.length})
        </h2>

        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 border border-slate-200/80 text-xs font-semibold self-start sm:self-auto">
          <button
            onClick={() => setFilterStrength('all')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStrength === 'all'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All ({sampleEvidenceDetails.length})
          </button>
          <button
            onClick={() => setFilterStrength('Strong')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStrength === 'Strong'
                ? 'bg-white text-emerald-800 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Strong ({strongCount})
          </button>
          <button
            onClick={() => setFilterStrength('Weak')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStrength === 'Weak'
                ? 'bg-white text-amber-800 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Weak ({weakCount})
          </button>
          <button
            onClick={() => setFilterStrength('Not Detected')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStrength === 'Not Detected'
                ? 'bg-white text-rose-800 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Missing ({missingCount})
          </button>
        </div>
      </div>

      {/* Evidence Cards Stack */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredEvidence.map((evidence) => (
          <EvidenceCard key={evidence.skill} evidence={evidence} />
        ))}
      </div>

      <SkillVerificationQuiz missingSkills={missingSkills} />
    </div>
  );
};


