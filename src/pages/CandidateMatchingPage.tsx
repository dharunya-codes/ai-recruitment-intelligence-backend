import React, { useState } from 'react';
import { sampleCandidatesPool } from '../data/mockData';
import { CandidateCard } from '../components/CandidateCard';
import { StatusBadge } from '../components/StatusBadge';
import { ProgressBar } from '../components/ProgressBar';
import {
  Search,
  LayoutGrid,
  List,
  Sparkles,
  ArrowRight,
  SlidersHorizontal,
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const CandidateMatchingPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'cards' | 'table'>('cards');

  const filteredCandidates = sampleCandidatesPool.filter((cand) => {
    const matchesSearch =
      cand.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cand.targetRole.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cand.aiProfileSummary.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesRole =
      roleFilter === 'all' ||
      cand.targetRole.toLowerCase().includes(roleFilter.toLowerCase());

    return matchesSearch && matchesRole;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Explainable Talent Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Candidate-Role Matching
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Explainable AI evaluation ranking candidates by verified evidence, project relevance, and genuine alignment.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/recruiter/job"
            className="text-xs font-bold px-3.5 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 transition-colors shadow-2xs"
          >
            Adjust JD Criteria
          </Link>
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-4 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search candidate name, role, or keywords..."
            className="w-full rounded-xl border border-slate-200 pl-10 pr-3.5 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 transition-colors"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
          <div className="flex items-center gap-1.5 text-xs text-slate-600">
            <SlidersHorizontal className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="rounded-lg border border-slate-200 px-2.5 py-1.5 text-xs font-medium bg-white text-slate-700 focus:outline-none focus:border-teal-600"
            >
              <option value="all">All Roles</option>
              <option value="Data Analyst">Data Analyst</option>
              <option value="Frontend Developer">Frontend Developer</option>
              <option value="Machine Learning">Machine Learning</option>
            </select>
          </div>

          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setViewMode('cards')}
              className={`p-1.5 rounded-lg transition-colors ${
                viewMode === 'cards' ? 'bg-white shadow-2xs text-slate-900' : 'text-slate-500'
              }`}
              title="Card View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-lg transition-colors ${
                viewMode === 'table' ? 'bg-white shadow-2xs text-slate-900' : 'text-slate-500'
              }`}
              title="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Candidate List Display */}
      {viewMode === 'cards' ? (
        <div className="space-y-4">
          {filteredCandidates.map((cand) => (
            <CandidateCard key={cand.id} candidate={cand} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50/80 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200/80">
                  <th className="py-3 px-5">Candidate</th>
                  <th className="py-3 px-5">Skill Match</th>
                  <th className="py-3 px-5">Experience Match</th>
                  <th className="py-3 px-5">Project Relevance</th>
                  <th className="py-3 px-5">Evidence Strength</th>
                  <th className="py-3 px-5">JD Alignment</th>
                  <th className="py-3 px-5">Missing Requirements</th>
                  <th className="py-3 px-5">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredCandidates.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3.5 px-5">
                      <div className="font-bold text-slate-900">{c.name}</div>
                      <div className="text-[11px] text-slate-400">{c.targetRole}</div>
                    </td>
                    <td className="py-3.5 px-5">
                      <div className="flex items-center gap-2 w-28">
                        <span className="font-bold text-red-700 w-8">{c.skillMatchPct}%</span>
                        <ProgressBar value={c.skillMatchPct} size="sm" />
                      </div>
                    </td>
                    <td className="py-3.5 px-5 font-medium">{c.experienceMatchPct}%</td>
                    <td className="py-3.5 px-5 font-medium">{c.projectRelevancePct}%</td>
                    <td className="py-3.5 px-5">
                      <StatusBadge status={c.evidenceStrength} size="sm" />
                    </td>
                    <td className="py-3.5 px-5 font-semibold text-slate-800">{c.jdAlignment}</td>
                    <td className="py-3.5 px-5">
                      {c.missingRequirements.length > 0 ? (
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {c.missingRequirements.map((r, i) => (
                            <span
                              key={i}
                              className="px-1.5 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-medium"
                            >
                              {r}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-emerald-700 font-medium">None</span>
                      )}
                    </td>
                    <td className="py-3.5 px-5">
                      <Link
                        to={`/recruiter/candidate/${c.id}`}
                        className="px-2.5 py-1 rounded-lg bg-teal-50 text-teal-800 font-bold border border-teal-200 hover:bg-teal-100 transition-colors inline-flex items-center gap-1"
                      >
                        <span>Audit</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};


