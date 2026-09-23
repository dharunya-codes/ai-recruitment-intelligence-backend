import React from 'react';
import { InterviewQuestionItem } from '../types';
import { ArrowLeft, ArrowRight, Sparkles, HelpCircle } from 'lucide-react';

interface InterviewQuestionProps {
  question: InterviewQuestionItem;
  totalQuestions: number;
  currentAnswer: string;
  onAnswerChange: (answer: string) => void;
  onPreviousQuestion: () => void;
  onNextQuestion: () => void;
  isFirstQuestion: boolean;
  isLastQuestion: boolean;
}

export const InterviewQuestion: React.FC<InterviewQuestionProps> = ({
  question,
  totalQuestions,
  currentAnswer,
  onAnswerChange,
  onPreviousQuestion,
  onNextQuestion,
  isFirstQuestion,
  isLastQuestion,
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8">
      {/* Question Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-red-50 text-red-700 font-bold text-xs border border-red-100">
            Question {question.number} of {totalQuestions}
          </span>
          <span className="text-xs font-semibold text-slate-500">
            Testing: <strong className="text-slate-800">{question.skill}</strong>
          </span>
        </div>

        {question.projectReferenced && (
          <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 border border-amber-200/80">
            Referencing: {question.projectReferenced}
          </span>
        )}
      </div>

      {/* Question Prompt */}
      <div className="my-6">
        <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-red-600 text-white flex items-center justify-center shrink-0 mt-0.5 shadow-xs font-bold text-sm">
            Q
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
              {question.question}
            </h2>
            <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-2">
              <HelpCircle className="w-3.5 h-3.5 text-red-500" />
              <span>{question.context}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Multiple Choice Answer Area */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Select one answer
          </label>
        </div>

        <div className="grid gap-3">
          {question.options.map((option) => {
            const isSelected = currentAnswer === option;
            return (
              <label
                key={option}
                className={`flex items-center gap-3 rounded-xl border p-4 cursor-pointer transition-colors ${
                  isSelected
                    ? 'border-red-600 bg-red-50 text-red-900 ring-2 ring-red-500/20'
                    : 'border-slate-200 text-slate-700 hover:border-red-300 hover:bg-red-50/40'
                }`}
              >
                <input
                  type="radio"
                  name={question.id}
                  value={option}
                  checked={isSelected}
                  onChange={() => onAnswerChange(option)}
                  className="h-4 w-4 accent-red-600"
                />
                <span className="text-sm font-semibold">{option}</span>
              </label>
            );
          })}
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-6 pt-5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="text-xs text-slate-500 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-red-500" />
          <span>Your selection is saved for this interview session.</span>
        </div>

        <div className="flex w-full gap-3 sm:w-auto">
          <button
            type="button"
            disabled={isFirstQuestion}
            onClick={onPreviousQuestion}
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40 sm:flex-initial"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Previous</span>
          </button>
          <button
            type="button"
            disabled={!currentAnswer}
            onClick={onNextQuestion}
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-initial"
          >
            <span>{isLastQuestion ? 'Submit Interview' : 'Next'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};


