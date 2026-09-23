import React, { useState } from 'react';
import { CheckCircle2, CircleAlert, ArrowRight, ShieldCheck } from 'lucide-react';
import { generateSkillQuiz } from '../data/mockData';

interface SkillVerificationQuizProps {
  missingSkills: string[];
}

interface QuizResult {
  correct: number;
  answers: Record<string, number>;
}

const getRecommendation = (correct: number) => {
  if (correct === 4) return 'Strong understanding demonstrated. Consider adding this skill to your resume only if you genuinely have practical experience with it.';
  if (correct === 3) return 'Good understanding, but some revision is recommended before highlighting the skill.';
  if (correct === 2) return 'Basic understanding detected. More practice is recommended before listing the skill prominently.';
  return 'The skill was not demonstrated strongly. Consider learning and practicing it before listing it prominently.';
};

export const SkillVerificationQuiz: React.FC<SkillVerificationQuizProps> = ({ missingSkills }) => {
  const questions = generateSkillQuiz(missingSkills);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});

  if (questions.length === 0) {
    return (
      <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs sm:p-8">
        <div className="flex items-center gap-3">
          <ShieldCheck className="h-6 w-6 text-red-600" />
          <div>
            <h2 className="text-lg font-bold text-slate-900">Missing Skill Verification</h2>
            <p className="mt-1 text-xs text-slate-500">Skill-specific questions are not available yet for this skill.</p>
          </div>
        </div>
      </section>
    );
  }

  const currentQuestion = questions[questionIndex];
  const skillsTested = questions
    .map((question) => question.skill)
    .filter((skill, index, skills) => skills.indexOf(skill) === index);

  const submitAnswer = () => {
    if (selectedAnswer === null) return;
    setAnswers((current) => ({ ...current, [currentQuestion.id]: selectedAnswer }));
    setSubmitted(true);
  };

  const nextQuestion = () => {
    if (questionIndex === questions.length - 1) {
      const completedAnswers = { ...answers, [currentQuestion.id]: selectedAnswer as number };
      const correct = questions.filter(
        (question) => completedAnswers[question.id] === question.correctAnswer
      ).length;
      setResult({ correct, answers: completedAnswers });
      return;
    }

    setQuestionIndex((current) => current + 1);
    setSelectedAnswer(null);
    setSubmitted(false);
  };

  if (result) {
    return (
      <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs sm:p-8">
        <div className="text-center">
          <CheckCircle2 className="mx-auto h-10 w-10 text-red-600" />
          <h2 className="mt-3 text-xl font-bold text-slate-900">Skill Verification Result</h2>
          <p className="mt-2 text-3xl font-black text-red-600">Score: {result.correct} / {questions.length}</p>
          <p className="mt-1 text-sm font-semibold text-slate-600">Percentage: {Math.round((result.correct / questions.length) * 100)}%</p>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-3 text-center sm:grid-cols-3">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-3"><strong className="block text-lg text-slate-900">{result.correct}</strong><span className="text-xs text-slate-500">Correct Answers</span></div>
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-3"><strong className="block text-lg text-slate-900">{questions.length - result.correct}</strong><span className="text-xs text-slate-500">Incorrect Answers</span></div>
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-3"><strong className="block text-lg text-slate-900">{skillsTested.join(', ')}</strong><span className="text-xs text-slate-500">Skills Tested</span></div>
        </div>

        <div className="mt-5 rounded-xl border border-red-100 bg-red-50/60 p-4 text-xs leading-relaxed text-red-900">
          <strong>Recommendation: </strong>{getRecommendation(result.correct)}
        </div>

        <div className="mt-5 space-y-3">
          {questions.map((question) => {
            const answer = result.answers[question.id];
            const correct = answer === question.correctAnswer;
            return (
              <div key={question.id} className={`rounded-xl border p-4 ${correct ? 'border-emerald-200 bg-emerald-50/60' : 'border-rose-200 bg-rose-50/60'}`}>
                <div className="flex items-start justify-between gap-3">
                  <p className="text-sm font-bold text-slate-900">Question {questions.indexOf(question) + 1}: {question.question}</p>
                  <span className={`shrink-0 text-xs font-bold ${correct ? 'text-emerald-700' : 'text-rose-700'}`}>{correct ? 'Correct' : 'Incorrect'}</span>
                </div>
                {!correct && (
                  <p className="mt-2 text-xs text-slate-700">Your answer: <strong>{question.options[answer]}</strong><br />Correct answer: <strong>{question.options[question.correctAnswer]}</strong></p>
                )}
                <p className="mt-2 text-xs text-slate-600">{question.explanation}</p>
              </div>
            );
          })}
        </div>
      </section>
    );
  }

  const isCorrect = submitted && selectedAnswer === currentQuestion.correctAnswer;

  return (
    <section className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs sm:p-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>4 Questions</span>
          </div>
          <h2 className="mt-3 text-xl font-bold text-slate-900">Missing Skill Verification</h2>
          <p className="mt-1 text-xs text-slate-500">Test your understanding of skills that were not clearly demonstrated in your resume.</p>
        </div>
        <span className="text-xs font-bold text-slate-500">Question {questionIndex + 1} of {questions.length}</span>
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 bg-slate-50/70 p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <span className="text-xs font-bold uppercase tracking-wider text-red-700">Skill: {currentQuestion.skill}</span>
          <span className="text-xs text-slate-500">{selectedAnswer === null ? 'Choose one answer' : submitted ? isCorrect ? 'Correct' : 'Incorrect' : 'Answer selected'}</span>
        </div>
        <h3 className="text-base font-bold leading-relaxed text-slate-900">{currentQuestion.question}</h3>

        <div className="mt-4 grid gap-2.5">
          {currentQuestion.options.map((option, index) => (
            <label key={option} className={`flex items-center gap-3 rounded-xl border p-3 text-sm transition-colors ${selectedAnswer === index ? 'border-red-600 bg-red-50 text-red-900' : 'border-slate-200 bg-white text-slate-700 hover:border-red-300'} ${submitted ? 'cursor-default' : 'cursor-pointer'}`}>
              <input type="radio" name={currentQuestion.id} checked={selectedAnswer === index} onChange={() => setSelectedAnswer(index)} disabled={submitted} className="h-4 w-4 accent-red-600" />
              <span className="font-semibold">{option}</span>
            </label>
          ))}
        </div>

        {submitted && (
          <div className={`mt-4 flex items-start gap-2 rounded-lg border p-3 text-xs ${isCorrect ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-rose-200 bg-rose-50 text-rose-800'}`}>
            {isCorrect ? <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" /> : <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />}
            <span>{isCorrect ? 'Correct answer. ' : `Incorrect. Correct answer: ${currentQuestion.options[currentQuestion.correctAnswer]}. `}{currentQuestion.explanation}</span>
          </div>
        )}

        <div className="mt-5 flex justify-end">
          {!submitted ? (
            <button type="button" onClick={submitAnswer} disabled={selectedAnswer === null} className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-xs font-bold text-white transition-colors hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50">Submit Answer <ArrowRight className="h-4 w-4" /></button>
          ) : (
            <button type="button" onClick={nextQuestion} className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-xs font-bold text-white transition-colors hover:bg-red-700">{questionIndex === questions.length - 1 ? 'View Result' : 'Next Question'} <ArrowRight className="h-4 w-4" /></button>
          )}
        </div>
      </div>
    </section>
  );
};
