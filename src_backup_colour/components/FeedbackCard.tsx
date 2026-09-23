import React, { useState } from 'react';
import { InterviewEvaluation } from '../types';
import { StatusBadge } from './StatusBadge';
import { ChevronDown, ChevronUp, Lightbulb, CheckCircle2, MessageSquare, Bot } from 'lucide-react';

interface FeedbackCardProps {
  evaluation: InterviewEvaluation;
  className?: string;
}

export const FeedbackCard: React.FC<FeedbackCardProps> = ({ evaluation, className = '' }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div
      className={`bg-white rounded-xl border border-slate-200/90 shadow-xs hover:shadow-sm transition-all overflow-hidden ${className}`}
    >
      {/* Accordion Bar */}
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-5 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-50/50 transition-colors"
      >
        <div className="flex items-start gap-3">
          <span className="w-7 h-7 rounded-lg bg-indigo-50 text-indigo-700 font-bold text-xs flex items-center justify-center shrink-0 border border-indigo-100 mt-0.5">
            Q{evaluation.questionNumber}
          </span>
          <div>
            <h3 className="text-base font-bold text-slate-900 leading-snug">
              {evaluation.question}
            </h3>
            <div className="flex items-center gap-3 mt-1.5">
              <span className="text-xs text-slate-500">
                Technical Understanding:
              </span>
              <StatusBadge status={evaluation.technicalUnderstanding} size="sm" />
            </div>
          </div>
        </div>

        <button
          type="button"
          className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 shrink-0"
        >
          {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {/* Expanded Details */}
      {isExpanded && (
        <div className="px-5 pb-5 pt-1 border-t border-slate-100 space-y-4 text-xs">
          {/* Candidate Answer */}
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
            <div className="flex items-center gap-1.5 font-bold text-slate-700 mb-1.5">
              <MessageSquare className="w-3.5 h-3.5 text-slate-500" />
              <span>Your Candidate Answer</span>
            </div>
            <p className="text-slate-800 leading-relaxed italic bg-white p-3 rounded-lg border border-slate-100">
              "{evaluation.candidateAnswer}"
            </p>
          </div>

          {/* AI Analysis */}
          <div className="p-3.5 rounded-xl bg-indigo-50/50 border border-indigo-100">
            <div className="flex items-center gap-1.5 font-bold text-indigo-950 mb-1">
              <Bot className="w-4 h-4 text-indigo-600" />
              <span>AI Evaluation Critique</span>
            </div>
            <p className="text-slate-700 leading-relaxed">{evaluation.explanation}</p>
          </div>

          {/* Expected Concepts */}
          <div>
            <div className="flex items-center gap-1.5 font-bold text-slate-700 mb-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>Expected Technical Concepts Evaluated:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {evaluation.expectedConcepts.map((concept, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 font-medium border border-emerald-200/70"
                >
                  {concept}
                </span>
              ))}
            </div>
          </div>

          {/* Improvement Suggestion */}
          <div className="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200 text-amber-950 flex items-start gap-2.5">
            <Lightbulb className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-amber-900 block mb-0.5">
                Recommended Actionable Improvement:
              </span>
              <p className="text-amber-900/90 leading-relaxed">
                {evaluation.improvementSuggestion}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
