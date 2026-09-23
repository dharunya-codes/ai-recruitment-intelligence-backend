import React from 'react';
import { Award, CheckCircle2 } from 'lucide-react';

interface ResumeScoreProps {
  score: number;
  atsScore?: number;
  atsGrade?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const ResumeScore: React.FC<ResumeScoreProps> = ({
  score,
  atsScore = 82,
  atsGrade = 'A-',
  size = 'md',
  className = '',
}) => {
  const normalizedScore = Math.min(Math.max(score, 0), 100);
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  let scoreColor = '#4f46e5'; // Indigo
  let scoreBadgeBg = 'bg-indigo-50 text-indigo-700 border-indigo-200';
  if (normalizedScore >= 80) {
    scoreColor = '#10b981'; // Emerald
    scoreBadgeBg = 'bg-emerald-50 text-emerald-700 border-emerald-200';
  } else if (normalizedScore >= 60) {
    scoreColor = '#6366f1'; // Violet/Indigo
    scoreBadgeBg = 'bg-indigo-50 text-indigo-700 border-indigo-200';
  } else {
    scoreColor = '#f59e0b'; // Amber
    scoreBadgeBg = 'bg-amber-50 text-amber-700 border-amber-200';
  }

  const dim = size === 'sm' ? 'w-24 h-24' : size === 'lg' ? 'w-36 h-36' : 'w-28 h-28';
  const textScoreSize = size === 'sm' ? 'text-2xl' : size === 'lg' ? 'text-4xl' : 'text-3xl';

  return (
    <div className={`flex flex-col sm:flex-row items-center gap-5 ${className}`}>
      {/* Radial Gauge */}
      <div className={`relative ${dim} flex items-center justify-center shrink-0`}>
        <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke="#f1f5f9"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke={scoreColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className={`font-black tracking-tight text-slate-900 ${textScoreSize}`}>
            {normalizedScore}
          </span>
          <span className="text-[10px] uppercase font-bold text-slate-400 -mt-1">/ 100</span>
        </div>
      </div>

      {/* Metric Breakdown */}
      <div className="flex flex-col gap-1.5 text-center sm:text-left">
        <div className="flex items-center justify-center sm:justify-start gap-2">
          <h4 className="text-base font-bold text-slate-900">Resume Quality Score</h4>
          <span className={`text-xs px-2 py-0.5 rounded-md font-semibold border ${scoreBadgeBg}`}>
            {normalizedScore >= 75 ? 'Strong Resume' : 'Moderate'}
          </span>
        </div>

        <p className="text-xs text-slate-500 max-w-xs">
          Multi-dimensional evaluation across ATS parseability, syntax, and quantifiable impact.
        </p>

        <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3 mt-1 pt-1.5 border-t border-slate-100 text-xs">
          <div className="flex items-center gap-1 text-slate-600 font-medium">
            <Award className="w-3.5 h-3.5 text-indigo-600" />
            <span>ATS Pass: <strong className="text-slate-900">{atsScore}%</strong></span>
          </div>
          <div className="flex items-center gap-1 text-slate-600 font-medium">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>Grade: <strong className="text-slate-900">{atsGrade}</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};
