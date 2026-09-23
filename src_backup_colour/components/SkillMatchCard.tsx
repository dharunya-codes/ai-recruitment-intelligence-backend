import React from 'react';
import { SkillItem } from '../types';
import { StatusBadge } from './StatusBadge';
import { CheckCircle2, AlertTriangle, XCircle, Info } from 'lucide-react';

interface SkillMatchCardProps {
  skill: SkillItem;
  className?: string;
}

export const SkillMatchCard: React.FC<SkillMatchCardProps> = ({ skill, className = '' }) => {
  const isMatched = skill.status === 'matched';
  const isWeak = skill.status === 'weak_evidence';
  const isMissing = skill.status === 'missing';

  return (
    <div
      className={`rounded-xl border p-4.5 transition-all ${
        isMatched
          ? 'bg-white border-emerald-100 hover:border-emerald-200'
          : isWeak
          ? 'bg-amber-50/20 border-amber-200/80 hover:border-amber-300'
          : 'bg-rose-50/20 border-rose-200/80 hover:border-rose-300'
      } ${className}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div
            className={`p-2 rounded-lg shrink-0 ${
              isMatched
                ? 'bg-emerald-100/70 text-emerald-700'
                : isWeak
                ? 'bg-amber-100/70 text-amber-700'
                : 'bg-rose-100/70 text-rose-700'
            }`}
          >
            {isMatched && <CheckCircle2 className="w-4 h-4" />}
            {isWeak && <AlertTriangle className="w-4 h-4" />}
            {isMissing && <XCircle className="w-4 h-4" />}
          </div>

          <div>
            <h4 className="text-sm font-bold text-slate-900">{skill.name}</h4>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-[11px] font-medium text-slate-500">
                Evidence: <strong className="text-slate-700">{skill.evidenceStrength}</strong>
              </span>
            </div>
          </div>
        </div>

        <StatusBadge
          status={
            isMatched
              ? 'Matched'
              : isWeak
              ? 'Weak Evidence'
              : 'Missing'
          }
          size="sm"
        />
      </div>

      {/* Detected In */}
      {skill.detectedIn.length > 0 && (
        <div className="mt-3 pt-2.5 border-t border-slate-100/90 text-xs">
          <span className="text-slate-400 font-medium">Found in:</span>
          <div className="flex flex-wrap gap-1.5 mt-1">
            {skill.detectedIn.map((loc, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-[11px] font-mono"
              >
                {loc}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Ethical Guidance Recommendation */}
      {skill.recommendation && (
        <div
          className={`mt-3 p-2.5 rounded-lg text-xs flex items-start gap-2 ${
            isMatched
              ? 'bg-emerald-50/60 text-emerald-800'
              : isWeak
              ? 'bg-amber-50 text-amber-900 border border-amber-200/60'
              : 'bg-rose-50 text-rose-900 border border-rose-200/60'
          }`}
        >
          <Info className="w-3.5 h-3.5 mt-0.5 shrink-0 opacity-80" />
          <p className="leading-relaxed">{skill.recommendation}</p>
        </div>
      )}
    </div>
  );
};
