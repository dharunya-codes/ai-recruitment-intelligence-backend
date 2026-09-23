import React from 'react';

interface ProgressBarProps {
  value: number; // 0 - 100
  max?: number;
  label?: string;
  showValue?: boolean;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'success' | 'warning' | 'auto';
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  label,
  showValue = false,
  size = 'md',
  variant = 'auto',
  className = '',
}) => {
  const percentage = Math.min(Math.max(Math.round((value / max) * 100), 0), 100);

  let barColor = 'bg-indigo-600';
  if (variant === 'success') {
    barColor = 'bg-emerald-500';
  } else if (variant === 'warning') {
    barColor = 'bg-amber-500';
  } else if (variant === 'auto') {
    if (percentage >= 80) barColor = 'bg-emerald-500';
    else if (percentage >= 60) barColor = 'bg-indigo-600';
    else if (percentage >= 40) barColor = 'bg-amber-500';
    else barColor = 'bg-rose-500';
  }

  const heightClass = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  }[size];

  return (
    <div className={`w-full ${className}`}>
      {(label || showValue) && (
        <div className="flex justify-between items-center text-xs text-slate-600 mb-1.5 font-medium">
          {label && <span>{label}</span>}
          {showValue && <span className="font-semibold text-slate-900">{percentage}%</span>}
        </div>
      )}
      <div className={`w-full bg-slate-100 rounded-full overflow-hidden ${heightClass}`}>
        <div
          className={`${heightClass} rounded-full transition-all duration-500 ease-out ${barColor}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
