import React from 'react';
import { Loader2, Sparkles } from 'lucide-react';

interface LoadingStateProps {
  title?: string;
  message?: string;
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  title = 'Processing Intelligence...',
  message = 'Extracting resume syntax, cross-referencing industry skill taxonomy, and evaluating evidence strength.',
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-2xl border border-slate-200/80 p-10 text-center max-w-md mx-auto shadow-xs ${className}`}
    >
      <div className="relative w-14 h-14 mx-auto mb-4 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-4 border-red-100 animate-ping opacity-25" />
        <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center border border-red-100 shadow-xs">
          <Loader2 className="w-6 h-6 animate-spin" />
        </div>
      </div>

      <h3 className="text-base font-bold text-slate-900 mb-1 flex items-center justify-center gap-1.5">
        <Sparkles className="w-4 h-4 text-red-600" />
        <span>{title}</span>
      </h3>
      <p className="text-xs text-slate-500 leading-relaxed">{message}</p>
    </div>
  );
};


