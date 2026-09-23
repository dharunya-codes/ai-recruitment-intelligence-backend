import React from 'react';

interface DashboardCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: string;
    isPositive?: boolean;
    neutral?: boolean;
  };
  action?: React.ReactNode;
  className?: string;
}

export const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  action,
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-xl p-5 border border-slate-200/80 shadow-xs hover:shadow-sm transition-all duration-200 ${className}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
            {title}
          </p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              {value}
            </span>
            {trend && (
              <span
                className={`text-xs font-medium px-2 py-0.5 rounded-full inline-flex items-center gap-0.5 ${
                  trend.neutral
                    ? 'bg-slate-100 text-slate-600'
                    : trend.isPositive
                    ? 'bg-emerald-50 text-emerald-700 font-semibold'
                    : 'bg-rose-50 text-rose-700 font-semibold'
                }`}
              >
                {trend.value}
              </span>
            )}
          </div>
          {subtitle && <p className="text-xs text-slate-500 mt-1.5">{subtitle}</p>}
        </div>

        {icon && (
          <div className="p-2.5 rounded-xl bg-slate-50 text-red-600 border border-slate-100 flex items-center justify-center shrink-0">
            {icon}
          </div>
        )}
      </div>

      {action && <div className="mt-4 pt-3 border-t border-slate-100">{action}</div>}
    </div>
  );
};


