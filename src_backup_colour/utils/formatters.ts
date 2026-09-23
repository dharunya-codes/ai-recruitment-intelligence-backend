/**
 * Formatting utilities for AI Resume Intelligence & Interview Platform
 */

export const formatScore = (score: number, max: number = 100): string => {
  return `${Math.round(score)}/${max}`;
};

export const formatPercentage = (val: number): string => {
  return `${Math.min(Math.max(Math.round(val), 0), 100)}%`;
};

export const getEvidenceBadgeClass = (strength: string): string => {
  switch (strength.toLowerCase()) {
    case 'strong':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    case 'moderate':
    case 'weak':
      return 'bg-amber-50 text-amber-800 border-amber-200';
    case 'not detected':
    case 'none':
    default:
      return 'bg-rose-50 text-rose-700 border-rose-200';
  }
};

export const truncateText = (text: string, maxLength: number = 120): string => {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
};
