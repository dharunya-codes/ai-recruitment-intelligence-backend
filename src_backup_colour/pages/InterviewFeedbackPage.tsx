import React from 'react';
import { Link } from 'react-router-dom';
import { sampleInterviewFeedback } from '../data/mockData';
import { FeedbackCard } from '../components/FeedbackCard';
import { ProgressBar } from '../components/ProgressBar';
import {
  Sparkles,
  Bot,
  Award,
  CheckCircle2,
  FileBarChart2,
  RotateCcw,
} from 'lucide-react';
import { useApp } from '../context/AppContext';

export const InterviewFeedbackPage: React.FC = () => {
  const { resetInterview } = useApp();
  const feedback = sampleInterviewFeedback;

  const categories = [
    { label: 'Technical Knowledge', score: feedback.categories.technicalKnowledge },
    { label: 'Communication', score: feedback.categories.communication },
    { label: 'Relevance', score: feedback.categories.relevance },
    { label: 'Completeness', score: feedback.categories.completeness },
    { label: 'Confidence', score: feedback.categories.confidence },
    { label: 'Problem Solving', score: feedback.categories.problemSolving },
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-indigo-950 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 sm:p-8 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold mb-3 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Interview Evaluation Complete</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Overall Interview Analysis
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl leading-relaxed">
            Candidate performance review for <strong className="text-white">{feedback.candidateName}</strong> targeting{' '}
            <strong className="text-white">{feedback.targetRole}</strong>.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          <Link
            to="/interview"
            onClick={resetInterview}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Retake Interview</span>
          </Link>

          <Link
            to="/reports"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-950/50"
          >
            <FileBarChart2 className="w-4 h-4" />
            <span>View Full Comprehensive Report</span>
          </Link>
        </div>
      </div>

      {/* Overall Score & 6 Category Bars Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-md">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
          {/* Overall Radial / Big Score */}
          <div className="text-center lg:text-left flex flex-col items-center lg:items-start justify-center border-b lg:border-b-0 lg:border-r border-slate-800 pb-6 lg:pb-0 lg:pr-8">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
              Composite Interview Score
            </span>
            <div className="flex items-baseline gap-2 my-2">
              <span className="text-5xl sm:text-6xl font-black text-white">
                {feedback.overallScore}
              </span>
              <span className="text-base text-slate-500 font-bold">/ 100</span>
            </div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold">
              <Award className="w-3.5 h-3.5" />
              <span>Interview Ready: Strong Candidate</span>
            </div>
            <p className="text-xs text-slate-400 mt-3 max-w-xs leading-relaxed">
              Consistently demonstrated clear verbal articulation with deep technical grounding in Python & SQL.
            </p>
          </div>

          {/* 6 Core Categories Grid */}
          <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {categories.map((cat) => (
              <div
                key={cat.label}
                className="p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80"
              >
                <div className="flex justify-between items-center text-xs mb-1.5">
                  <span className="font-semibold text-slate-300">{cat.label}</span>
                  <span className="font-bold text-indigo-400">{cat.score}%</span>
                </div>
                <ProgressBar value={cat.score} size="sm" variant="primary" />
              </div>
            ))}
          </div>
        </div>

        {/* Executive AI Summary Box */}
        <div className="mt-8 pt-6 border-t border-slate-800/90 p-4 rounded-xl bg-indigo-950/40 border border-indigo-900/50 text-xs text-slate-300 leading-relaxed">
          <div className="flex items-center gap-2 font-bold text-indigo-300 mb-1">
            <Bot className="w-4 h-4 text-indigo-400" />
            <span>AI Executive Feedback Summary:</span>
          </div>
          <p className="italic">{feedback.executiveSummary}</p>
        </div>
      </div>

      {/* Answer-by-Answer Detailed Breakdown */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>Answer-by-Answer AI Evaluation ({feedback.evaluations.length} Questions)</span>
          </h2>
          <span className="text-xs text-slate-400">Click question to expand/collapse</span>
        </div>

        <div className="space-y-4">
          {feedback.evaluations.map((item) => (
            <FeedbackCard key={item.questionId} evaluation={item} />
          ))}
        </div>
      </div>
    </div>
  );
};
