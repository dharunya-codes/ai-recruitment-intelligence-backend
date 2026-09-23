import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { sampleResumeScore } from '../data/mockData';
import { ResumeScore } from '../components/ResumeScore';
import { StatusBadge } from '../components/StatusBadge';
import { ProgressBar } from '../components/ProgressBar';
import {
  Sparkles,
  FileSearch,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  ArrowRight,
} from 'lucide-react';

export const ResumeAnalysisPage: React.FC = () => {
  const [filterStatus, setFilterStatus] = useState<'all' | 'Good' | 'Needs Improvement'>('all');

  const sectionsList = Object.entries(sampleResumeScore.sections).map(([key, section]) => ({
    key,
    ...section,
  }));

  const filteredSections = sectionsList.filter((s) => {
    if (filterStatus === 'all') return true;
    return s.status === filterStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>8-Point Quality Inspection</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Resume Quality Analysis
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Comprehensive audit covering structural formatting, grammar, dates consistency, and ATS readability.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/candidate/skill-gap"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <span>Proceed to Skill Gap</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Top Overview Score Card */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs">
        <ResumeScore
          score={sampleResumeScore.overallScore}
          atsScore={sampleResumeScore.atsScore}
          atsGrade={sampleResumeScore.atsGrade}
          size="lg"
        />

        <div className="mt-6 pt-5 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Total Dimensions</span>
            <p className="text-xl font-bold text-slate-900 mt-0.5">8 Areas</p>
          </div>
          <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-100">
            <span className="text-[11px] font-semibold uppercase text-emerald-700">Good Status</span>
            <p className="text-xl font-bold text-emerald-800 mt-0.5">6 Areas</p>
          </div>
          <div className="p-3 rounded-xl bg-amber-50/60 border border-amber-100">
            <span className="text-[11px] font-semibold uppercase text-amber-700">Needs Attention</span>
            <p className="text-xl font-bold text-amber-800 mt-0.5">2 Areas</p>
          </div>
          <div className="p-3 rounded-xl bg-indigo-50/60 border border-indigo-100">
            <span className="text-[11px] font-semibold uppercase text-indigo-700">ATS Pass Rating</span>
            <p className="text-xl font-bold text-indigo-900 mt-0.5">A- (82%)</p>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <FileSearch className="w-4 h-4 text-indigo-600" />
          <span>Detailed Section Reports</span>
        </h2>

        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 border border-slate-200/80 text-xs font-semibold">
          <button
            onClick={() => setFilterStatus('all')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStatus === 'all' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All (8)
          </button>
          <button
            onClick={() => setFilterStatus('Needs Improvement')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStatus === 'Needs Improvement' ? 'bg-white text-amber-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Needs Improvement (2)
          </button>
          <button
            onClick={() => setFilterStatus('Good')}
            className={`px-3 py-1 rounded-lg transition-colors ${
              filterStatus === 'Good' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Good (6)
          </button>
        </div>
      </div>

      {/* Sections Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredSections.map((sec) => {
          const isGood = sec.status === 'Good';
          return (
            <div
              key={sec.key}
              className={`bg-white rounded-2xl border p-5 shadow-xs transition-all ${
                isGood
                  ? 'border-slate-200 hover:border-slate-300'
                  : 'border-amber-300 bg-amber-50/15 hover:border-amber-400'
              }`}
            >
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`p-2 rounded-xl shrink-0 ${
                      isGood ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'
                    }`}
                  >
                    {isGood ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{sec.title}</h3>
                    <span className="text-[11px] text-slate-400">Score: {sec.score}/100</span>
                  </div>
                </div>

                <StatusBadge status={sec.status} size="sm" />
              </div>

              <ProgressBar value={sec.score} size="sm" className="mb-3" />

              <p className="text-xs text-slate-600 leading-relaxed mb-3">
                {sec.shortExplanation}
              </p>

              {/* Recommendation Box */}
              <div
                className={`p-3 rounded-xl text-xs flex items-start gap-2.5 ${
                  isGood
                    ? 'bg-slate-50 text-slate-700 border border-slate-100'
                    : 'bg-amber-50 text-amber-900 border border-amber-200/80 font-medium'
                }`}
              >
                <Lightbulb
                  className={`w-3.5 h-3.5 shrink-0 mt-0.5 ${
                    isGood ? 'text-slate-400' : 'text-amber-600'
                  }`}
                />
                <div>
                  <span className="font-bold block mb-0.5">Recommendation:</span>
                  <span>{sec.recommendation}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
