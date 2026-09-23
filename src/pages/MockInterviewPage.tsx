import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { getRoleInterviewQuestions } from '../data/mockData';
import { InterviewQuestion } from '../components/InterviewQuestion';
import { ProgressBar } from '../components/ProgressBar';
import { Sparkles, Bot, Clock, CheckCircle2, RotateCcw } from 'lucide-react';

export const MockInterviewPage: React.FC = () => {
  const {
    candidate,
    targetRole,
    candidateJobDescription,
    interviewAnswers,
    setInterviewAnswer,
    interviewProgressIndex,
    setInterviewProgressIndex,
    resetInterview,
    showToast,
  } = useApp();

  const navigate = useNavigate();
  const [result, setResult] = useState<{
    correct: number;
    percentage: number;
    answers: Record<string, string>;
  } | null>(null);

  const questions = getRoleInterviewQuestions(
    candidateJobDescription.jobTitle || targetRole,
    candidateJobDescription.description,
  );
  const currentQuestion = questions[interviewProgressIndex] || questions[0];
  const currentAnswer = interviewAnswers[currentQuestion.id] || '';

  const handleAnswerChange = (text: string) => {
    setInterviewAnswer(currentQuestion.id, text);
  };

  const handleNext = () => {
    if (interviewProgressIndex < questions.length - 1) {
      setInterviewProgressIndex(interviewProgressIndex + 1);
    } else {
      const answers = { ...interviewAnswers, [currentQuestion.id]: currentAnswer };
      const correct = questions.reduce(
        (total, question) => total + (answers[question.id] === question.correctAnswer ? 1 : 0),
        0
      );
      setResult({ correct, percentage: Math.round((correct / questions.length) * 100), answers });
      showToast('Skill assessment submitted. Your score is ready.', 'success');
    }
  };

  const handlePrevious = () => {
    if (interviewProgressIndex > 0) {
      setInterviewProgressIndex(interviewProgressIndex - 1);
    }
  };

  const progressPercentage = Math.round(
    ((interviewProgressIndex + 1) / questions.length) * 100
  );

  if (result) {
    return (
      <div className="space-y-6">
        <div className="bg-slate-800/80 border border-slate-700/70 rounded-2xl p-8 text-center shadow-lg">
          <CheckCircle2 className="w-12 h-12 text-red-400 mx-auto mb-3" />
          <p className="text-xs uppercase tracking-wider font-bold text-red-400">Interview Practice Result</p>
          <p className="text-sm text-slate-300 mt-2">Skills assessed: {questions.map((question) => question.skill).filter((skill, index, skills) => skills.indexOf(skill) === index).join(', ')}</p>
          <p className="mt-4 text-xs font-bold uppercase tracking-wider text-slate-400">Total Score</p>
          <h1 className="text-4xl sm:text-5xl font-black text-white mt-2">{result.correct} / {questions.length}</h1>
          <p className="text-2xl font-bold text-red-300 mt-1">{result.percentage}%</p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-8 text-sm">
            <div className="rounded-xl bg-slate-900/70 border border-slate-700 p-4"><strong className="block text-white">{questions.length}</strong><span className="text-slate-400">Total Questions</span></div>
            <div className="rounded-xl bg-slate-900/70 border border-slate-700 p-4"><strong className="block text-white">{result.correct}</strong><span className="text-slate-400">Correct Answers</span></div>
            <div className="rounded-xl bg-slate-900/70 border border-slate-700 p-4"><strong className="block text-white">{questions.length - result.correct}</strong><span className="text-slate-400">Incorrect Answers</span></div>
          </div>
        </div>
        <div className="space-y-3">
          {questions.map((question) => {
            const answer = result.answers[question.id];
            const isCorrect = answer === question.correctAnswer;
            return (
              <div key={question.id} className={`rounded-xl border p-4 ${isCorrect ? 'border-emerald-200 bg-emerald-50' : 'border-red-200 bg-red-50'}`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <strong className="text-sm text-slate-900">Question {question.number}: {question.question}</strong>
                  <span className={`text-xs font-bold ${isCorrect ? 'text-emerald-700' : 'text-red-700'}`}>{isCorrect ? 'Correct' : 'Incorrect'}</span>
                </div>
                {!isCorrect && <p className="mt-2 text-xs text-slate-700">Your answer: <strong>{answer}</strong><br />Correct answer: <strong>{question.correctAnswer}</strong></p>}
                <p className="mt-2 text-xs text-slate-600">{question.explanation}</p>
              </div>
            );
          })}
        </div>
        <div className="flex flex-col sm:flex-row justify-center gap-3">
          <button type="button" onClick={() => { setResult(null); resetInterview(); }} className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 text-slate-200 text-sm font-semibold hover:bg-slate-700">
            <RotateCcw className="w-4 h-4" /> Retake Interview
          </button>
          <button type="button" onClick={() => navigate('/candidate/dashboard')} className="px-5 py-2.5 rounded-xl bg-red-600 text-white text-sm font-semibold hover:bg-red-500">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Session Progress Header */}
      <div className="bg-slate-800/80 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center font-bold">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-white">Role-Based Mock Interview</h2>
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
            <span className="font-bold text-red-400">{progressPercentage}%</span>
          </div>
          <ProgressBar value={progressPercentage} size="sm" variant="primary" />
        </div>
      </div>

      <div className="rounded-xl border border-red-900/50 bg-red-950/40 p-4 text-sm text-red-100">
        Answer 10 multiple-choice questions based on the selected Job Description.
        <span className="block mt-1 text-xs text-red-200/80">Topics: {questions.map((question) => question.skill).filter((skill, index, skills) => skills.indexOf(skill) === index).join(', ')}</span>
      </div>

      {/* Main Question Card Component */}
      <InterviewQuestion
        question={currentQuestion}
        totalQuestions={questions.length}
        currentAnswer={currentAnswer}
        onAnswerChange={handleAnswerChange}
        onPreviousQuestion={handlePrevious}
        onNextQuestion={handleNext}
        isFirstQuestion={interviewProgressIndex === 0}
        isLastQuestion={interviewProgressIndex === questions.length - 1}
      />

      {/* Candidate Guidance Notes */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-400">
        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <Clock className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">Assessment Guidance:</strong>
            <span>Select the answer that best matches your current understanding.</span>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">JD Coverage:</strong>
            <span>Questions target the skills found in the selected Job Description.</span>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 flex items-start gap-2.5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-300 block mb-0.5">Practice Focus:</strong>
            <span>Review explanations after submission to guide your next practice area.</span>
          </div>
        </div>
      </div>
    </div>
  );
};


