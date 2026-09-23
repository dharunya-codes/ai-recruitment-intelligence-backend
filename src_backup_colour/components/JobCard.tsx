import React from 'react';
import { JobVacancy } from '../types';
import { Briefcase, Users, MapPin, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

interface JobCardProps {
  job: JobVacancy;
  className?: string;
  onSelect?: (job: JobVacancy) => void;
}

export const JobCard: React.FC<JobCardProps> = ({ job, className = '', onSelect }) => {
  return (
    <div
      className={`bg-white rounded-xl border border-slate-200/90 p-5 shadow-xs hover:border-indigo-200 hover:shadow-sm transition-all duration-200 ${className}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <span className="text-[11px] font-semibold uppercase text-indigo-600 tracking-wider">
            {job.department}
          </span>
          <h3 className="text-lg font-bold text-slate-900 mt-0.5">{job.title}</h3>
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1">
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              {job.location}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Briefcase className="w-3.5 h-3.5 text-slate-400" />
              {job.type}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Users className="w-3.5 h-3.5 text-slate-400" />
              {job.applicantCount} candidates
            </span>
          </div>
        </div>

        <div className="text-right shrink-0">
          <div className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-bold">
            <Sparkles className="w-3 h-3 text-indigo-600" />
            <span>Avg Match: {job.avgMatchScore}%</span>
          </div>
        </div>
      </div>

      <p className="text-xs text-slate-600 mt-3 line-clamp-2 leading-relaxed">
        {job.description}
      </p>

      {/* Required Skills */}
      <div className="mt-3.5">
        <span className="text-[11px] font-semibold text-slate-400 uppercase">Required Skills:</span>
        <div className="flex flex-wrap gap-1.5 mt-1">
          {job.requiredSkills.map((skill, idx) => (
            <span
              key={idx}
              className="text-xs px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium border border-slate-200/60"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Footer / Actions */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
        <span className="text-slate-400">Created {job.createdAt}</span>
        <div className="flex items-center gap-2">
          {onSelect && (
            <button
              onClick={() => onSelect(job)}
              className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 transition-colors"
            >
              Select Role
            </button>
          )}
          <Link
            to={`/recruiter/candidates?jobId=${job.id}`}
            className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-colors shadow-xs"
          >
            Review Candidates
          </Link>
        </div>
      </div>
    </div>
  );
};
