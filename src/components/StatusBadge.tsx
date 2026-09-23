import React from 'react';
import { SectionStatus, EvidenceStrength, MatchStatus } from '../types';

interface StatusBadgeProps {
  status?: SectionStatus | EvidenceStrength | MatchStatus | string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status = 'Good',
  size = 'md',
  className = '',
}) => {
  const normalized = String(status).toLowerCase();

  let colorClasses = 'bg-slate-100 text-slate-700 border-slate-200';

  if (
    normalized === 'good' ||
    normalized === 'strong' ||
    normalized === 'matched' ||
    normalized === 'excellent' ||
    normalized === 'shortlisted' ||
    normalized === 'high'
  ) {
    colorClasses = 'bg-emerald-50 text-emerald-700 border-emerald-200/70';
  } else if (
    normalized === 'needs improvement' ||
    normalized === 'moderate' ||
    normalized === 'partial' ||
    normalized === 'weak' ||
    normalized === 'medium' ||
    normalized === 'under review'
  ) {
    colorClasses = 'bg-amber-50 text-amber-800 border-amber-200/70';
  } else if (
    normalized === 'critical' ||
    normalized === 'missing' ||
    normalized === 'not detected' ||
    normalized === 'none' ||
    normalized === 'low'
  ) {
    colorClasses = 'bg-rose-50 text-rose-700 border-rose-200/70';
  }

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs font-medium px-2.5 py-1',
    lg: 'text-sm font-semibold px-3 py-1.5',
  }[size];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border transition-colors ${sizeClasses} ${colorClasses} ${className}`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          normalized.includes('good') ||
          normalized.includes('strong') ||
          normalized.includes('matched') ||
          normalized.includes('high')
            ? 'bg-emerald-500'
            : normalized.includes('needs') ||
              normalized.includes('moderate') ||
              normalized.includes('partial') ||
              normalized.includes('weak')
            ? 'bg-amber-500'
            : 'bg-rose-500'
        }`}
      />
      {status}
    </span>
  );
};


