import React from 'react';
import { EvidenceStrength } from '../types';

interface SkillBadgeProps {
  name: string;
  status?: 'matched' | 'weak_evidence' | 'missing' | 'detected' | string;
  evidenceStrength?: EvidenceStrength;
  showEvidenceDot?: boolean;
  className?: string;
  onClick?: () => void;
}

export const SkillBadge: React.FC<SkillBadgeProps> = ({
  name,
  status = 'matched',
  evidenceStrength,
  showEvidenceDot = true,
  className = '',
  onClick,
}) => {
  let badgeStyle = 'bg-slate-100 text-slate-800 border-slate-200';
  let dotColor = 'bg-slate-400';

  if (status === 'matched' || evidenceStrength === 'Strong') {
    badgeStyle = 'bg-emerald-50/80 text-emerald-800 border-emerald-200/80 hover:bg-emerald-100/70';
    dotColor = 'bg-emerald-500';
  } else if (status === 'weak_evidence' || evidenceStrength === 'Weak' || evidenceStrength === 'Moderate') {
    badgeStyle = 'bg-amber-50/80 text-amber-800 border-amber-200/80 hover:bg-amber-100/70';
    dotColor = 'bg-amber-500';
  } else if (status === 'missing' || evidenceStrength === 'Not Detected' || evidenceStrength === 'None') {
    badgeStyle = 'bg-rose-50/80 text-rose-800 border-rose-200/80 hover:bg-rose-100/70';
    dotColor = 'bg-rose-500';
  }

  return (
    <span
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium border transition-colors ${badgeStyle} ${
        onClick ? 'cursor-pointer' : ''
      } ${className}`}
    >
      {showEvidenceDot && <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`} />}
      <span>{name}</span>
      {evidenceStrength && (
        <span className="text-[10px] opacity-75 ml-0.5 font-normal">({evidenceStrength})</span>
      )}
    </span>
  );
};
