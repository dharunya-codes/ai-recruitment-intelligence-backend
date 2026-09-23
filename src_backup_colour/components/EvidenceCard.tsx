import React from 'react';
import { EvidenceDetail } from '../types';
import { StatusBadge } from './StatusBadge';
import { FileText, FolderGit2, AlertCircle, ShieldCheck } from 'lucide-react';

interface EvidenceCardProps {
  evidence: EvidenceDetail;
  className?: string;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({ evidence, className = '' }) => {
  const isFound = evidence.status === 'Found';
  const isStrong = evidence.strength === 'Strong';
  const isWeak = evidence.strength === 'Weak';

  return (
    <div
      className={`bg-white rounded-xl border p-5 shadow-xs hover:shadow-sm transition-all ${
        isStrong
          ? 'border-slate-200 hover:border-indigo-300'
          : isWeak
          ? 'border-amber-200/90 bg-amber-50/10'
          : 'border-slate-200/80 bg-slate-50/40'
      } ${className}`}
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div
            className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm ${
              isStrong
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-100'
                : isWeak
                ? 'bg-amber-50 text-amber-700 border border-amber-100'
                : 'bg-slate-100 text-slate-500'
            }`}
          >
            {evidence.skill.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">{evidence.skill}</h3>
            <p className="text-xs text-slate-500">
              Confidence Score:{' '}
              <strong className="text-slate-700">{evidence.confidence}%</strong>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span
            className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
              isFound ? 'bg-slate-100 text-slate-700' : 'bg-rose-50 text-rose-700'
            }`}
          >
            Status: {evidence.status}
          </span>
          <StatusBadge status={evidence.strength} size="sm" />
        </div>
      </div>

      {/* Evidence Sources */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
          <div className="flex items-center gap-1.5 text-slate-600 font-semibold mb-1.5">
            <FileText className="w-3.5 h-3.5 text-slate-400" />
            <span>Document Occurrences</span>
          </div>
          {evidence.evidenceLocations.length > 0 ? (
            <ul className="space-y-1 text-slate-600">
              {evidence.evidenceLocations.map((loc, i) => (
                <li key={i} className="flex items-center gap-1.5">
                  <span className="w-1 h-1 rounded-full bg-indigo-500" />
                  {loc}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-400 italic">No section markers detected.</p>
          )}
        </div>

        <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
          <div className="flex items-center gap-1.5 text-slate-600 font-semibold mb-1.5">
            <FolderGit2 className="w-3.5 h-3.5 text-slate-400" />
            <span>Associated Projects</span>
          </div>
          {evidence.projectsReferenced.length > 0 ? (
            <div className="flex flex-wrap gap-1.5">
              {evidence.projectsReferenced.map((proj, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded bg-white text-indigo-700 border border-indigo-100 font-medium"
                >
                  {proj}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-slate-400 italic">No project implementation referenced.</p>
          )}
        </div>
      </div>

      {/* Extracted Evidence Snippets */}
      {evidence.snippets.length > 0 && (
        <div className="mt-3 text-xs">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
            Extracted Text Proof
          </p>
          <div className="space-y-1.5">
            {evidence.snippets.map((snip, i) => (
              <div
                key={i}
                className="p-2 rounded bg-slate-50/70 border border-slate-200/60 font-mono text-[11px] text-slate-700"
              >
                {snip}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Strength Explanation Footer */}
      <div className="mt-3.5 pt-3 border-t border-slate-100 flex items-center gap-2 text-xs">
        {isStrong ? (
          <>
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            <span className="text-emerald-800 font-medium">
              Verified in multiple project descriptions with context.
            </span>
          </>
        ) : isWeak ? (
          <>
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
            <span className="text-amber-800 font-medium">
              Keyword only found in skills list without supporting project bullets.
            </span>
          </>
        ) : (
          <>
            <AlertCircle className="w-4 h-4 text-slate-400 shrink-0" />
            <span className="text-slate-500">
              Not detected in either skills block, summary, or project accomplishments.
            </span>
          </>
        )}
      </div>
    </div>
  );
};
