import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { sampleInterviewQuestions } from '../data/mockData';
import { InterviewQuestion } from '../components/InterviewQuestion';
import { ProgressBar } from '../components/ProgressBar';
import { submitInterviewAnswer } from '../services/api';
import { Sparkles, Bot, Clock, CheckCircle2 } from 'lucide-react';

export const MockInterviewPage: React.FC = () => {
  const {
    candidate,
    targetRole,
    interviewAnswers,
    setInterviewAnswer,
    interviewProgressIndex,
    setInterviewProgressIndex,
    showToast,
  } = useApp();

  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCurrentSubmitted, setIsCurrentSubmitted] = useState(false);

  const questions = sampleInterviewQuestions;
  const currentQuestion = questions[interviewProgressIndex] || questions[0];
  const currentAnswer = interviewAnswers[currentQuestion.id] || '';

  const handleAnswerChange = (text: string) => {
    setInterviewAnswer(currentQuestion.id, text);
    setIsCurrentSubmitted(false);
  };

  const handleSubmitCurrentAnswer = async () => {
    if (!currentAnswer.trim()) return;
    setIsSubmitting(true);
    try {
      await submitInterviewAnswer(currentQuestion.id, currentAnswer);
      setIsCurrentSubmitted(true);
      showToast('Answer recorded and evaluated against technical criteria.', 'success');
    } catch {
      showToast('Recorded answer locally.', 'info');
      setIsCurrentSubmitted(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = () => {
    if (interviewProgressIndex < questions.length - 1) {
      setInterviewProgressIndex(interviewProgressIndex + 1);
      setIsCurrentSubmitted(false);
    } else {
      showToast('Interview completed! Generating multi-dimensional feedback...', 'success');
      navigate('/interview/feedback');
    }
  };

  const progressPercentage = Math.round(
    ((interviewProgressIndex + 1) / questions.length) * 100
  );

  return (
    <div className="space-y-6">
      {/* Session Progress Header */}
      <div className="bg-slate-800/80 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-white">Live AI Mock Session</h2>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Active
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Evaluating: <strong className="text-slate-200">{targetRole}</strong> for candidate{' '}
              <strong className="text-slate-200">{candidate.name}</strong>
            </p>
          </div>
        </div>

        <div className="w-full sm:w-60">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
            <span>Progress ({interviewProgressIndex + 1} of {questions.length})</span>
            <span className="font-bold text-indigo-400">{progressPercentage}%</span>
          </div>
          <ProgressBar value={progressPercentage} size="sm" variant="primary" />
        </div>
      </div>

      {/* Main Question Card Component */}
      <InterviewQuestion
        question={currentQuestion}
        totalQuestions={questions.length}
        currentAnswer={currentAnswer}
        onAnswerChange={handleAnswerChange}
        onSubmitAnswer={handleSubmitCurrentAnswer}
        onNextQuestion={handleNext}
        isLastQuestion={interviewProgressIndex === questions.length - 1}
        isSubmitting={isSubmitting}
        isSubmitted={isCurrentSubmitted}
      />

      {/* Candidate Guidance Notes */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-400">
        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <Clock className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">Recommended Duration:</strong>
            <span>Spend 2-3 minutes per response explaining technical methodology.</span>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">Resume Grounding:</strong>
            <span>Questions cite specific projects and libraries from your uploaded file.</span>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">Multi-Dimensional Rubric:</strong>
            <span>Answers will be scored on technical depth, problem solving, and relevance.</span>
          </div>
        </div>
      </div>
    </div>
  );
};
