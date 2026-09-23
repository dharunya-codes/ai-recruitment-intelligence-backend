import React, { useState } from 'react';
import { InterviewQuestionItem } from '../types';
import { Mic, MicOff, Send, ArrowRight, Sparkles, HelpCircle, CheckCircle } from 'lucide-react';

interface InterviewQuestionProps {
  question: InterviewQuestionItem;
  totalQuestions: number;
  currentAnswer: string;
  onAnswerChange: (answer: string) => void;
  onSubmitAnswer: () => void;
  onNextQuestion: () => void;
  isLastQuestion: boolean;
  isSubmitting?: boolean;
  isSubmitted?: boolean;
}

export const InterviewQuestion: React.FC<InterviewQuestionProps> = ({
  question,
  totalQuestions,
  currentAnswer,
  onAnswerChange,
  onSubmitAnswer,
  onNextQuestion,
  isLastQuestion,
  isSubmitting = false,
  isSubmitted = false,
}) => {
  const [isRecording, setIsRecording] = useState(false);

  const toggleMic = () => {
    setIsRecording(!isRecording);
    if (!isRecording && !currentAnswer) {
      // Simulate speech-to-text dictation sample if empty
      onAnswerChange(
        'In the Sales Analysis project, I utilized Pandas to clean dirty transaction logs, applied median imputation for missing values, and parsed date strings for seasonal trend aggregation.'
      );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8">
      {/* Question Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 font-bold text-xs border border-indigo-100">
            Question {question.number} of {totalQuestions}
          </span>
          <span className="text-xs font-semibold text-slate-500">
            Testing: <strong className="text-slate-800">{question.skillTested}</strong>
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
          <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center shrink-0 mt-0.5 shadow-xs font-bold text-sm">
            AI
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
              {question.question}
            </h2>
            <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-2">
              <HelpCircle className="w-3.5 h-3.5 text-indigo-500" />
              <span>{question.context}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Answer Input Area */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Your Response
          </label>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={toggleMic}
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                isRecording
                  ? 'bg-rose-50 text-rose-700 border border-rose-200 animate-pulse'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
              title="Toggle Simulated Voice Input"
            >
              {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
              <span>{isRecording ? 'Listening (Simulated)...' : 'Use Voice Input'}</span>
            </button>
            <span className="text-xs text-slate-400 font-mono">
              {currentAnswer.trim() ? currentAnswer.trim().split(/\s+/).length : 0} words
            </span>
          </div>
        </div>

        <div className="relative">
          <textarea
            rows={6}
            value={currentAnswer}
            onChange={(e) => onAnswerChange(e.target.value)}
            placeholder="Type your response clearly here. Explain your methodology, specific technologies, trade-offs, and quantifiable impact from your resume..."
            className="w-full rounded-xl border border-slate-200 p-4 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-all leading-relaxed"
          />

          {isSubmitted && (
            <div className="absolute top-3 right-3 flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Answer Saved</span>
            </div>
          )}
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-6 pt-5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="text-xs text-slate-500 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
          <span>Responses are analyzed against actual resume evidence & target JD requirements.</span>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button
            type="button"
            disabled={!currentAnswer.trim() || isSubmitting}
            onClick={onSubmitAnswer}
            className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl border border-indigo-200 text-indigo-700 font-semibold text-sm hover:bg-indigo-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            <span>{isSubmitting ? 'Evaluating...' : 'Submit Answer'}</span>
          </button>

          <button
            type="button"
            onClick={onNextQuestion}
            className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-sm hover:bg-indigo-700 transition-colors shadow-xs"
          >
            <span>{isLastQuestion ? 'Complete & View Feedback' : 'Next Question'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
