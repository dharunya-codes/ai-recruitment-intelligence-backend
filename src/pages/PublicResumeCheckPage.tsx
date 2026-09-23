import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, ArrowRight, CheckCircle2, FileSearch, RotateCcw } from 'lucide-react';
import { UploadBox } from '../components/UploadBox';
import { publicResumeIssues } from '../data/mockData';

export const PublicResumeCheckPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);

  const handleFileSelected = (file: File) => {
    setSelectedFile(file);
    setHasAnalyzed(false);
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setHasAnalyzed(false);
  };

  return (
    <div className="min-h-[85vh] bg-[#0B0B0F] px-4 py-10 text-[#F5F5F5] sm:py-14">
      <div className="mx-auto max-w-5xl space-y-6">
        {!hasAnalyzed ? (
          <>
            <div className="text-center">
              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-[#E50914] text-white">
                <FileSearch className="h-7 w-7" />
              </div>
              <h1 className="text-2xl font-bold sm:text-3xl">Free Resume Check</h1>
              <p className="mx-auto mt-2 max-w-xl text-sm text-[#A1A1AA]">
                Upload your resume to identify common mistakes and improvement areas.
              </p>
              <span className="mt-3 inline-flex rounded-full border border-[#7F1D1D] bg-[#3B0A0D] px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#FCA5A5]">
                Prototype Analysis
              </span>
            </div>

            <section className="rounded-2xl border border-[#27272A] bg-[#17171D] p-6 shadow-xl sm:p-8">
              <h2 className="mb-1 text-lg font-bold">Upload Your Resume</h2>
              <p className="mb-5 text-xs text-[#A1A1AA]">Accepted formats: PDF, DOCX. No account is required.</p>
              <UploadBox
                selectedFile={selectedFile}
                onFileSelected={handleFileSelected}
                onClearFile={handleClearFile}
              />

              <div className="mt-6 flex flex-col items-center justify-between gap-3 border-t border-[#27272A] pt-5 sm:flex-row">
                <p className="flex items-center gap-2 text-xs text-[#A1A1AA]">
                  <AlertCircle className="h-4 w-4 shrink-0 text-[#E50914]" />
                  This demo provides general suggestions, not automated AI analysis.
                </p>
                <button
                  type="button"
                  disabled={!selectedFile}
                  onClick={() => setHasAnalyzed(true)}
                  className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#E50914] px-5 py-2.5 text-xs font-bold text-white transition-colors hover:bg-[#FF1F2D] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
                >
                  <span>Analyze Resume</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </section>
          </>
        ) : (
          <>
            <div className="flex flex-col gap-4 rounded-2xl border border-[#27272A] bg-[#17171D] p-6 sm:flex-row sm:items-center sm:justify-between sm:p-8">
              <div>
                <span className="inline-flex rounded-full border border-[#7F1D1D] bg-[#3B0A0D] px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#FCA5A5]">
                  Prototype Analysis
                </span>
                <h1 className="mt-3 text-2xl font-bold">Resume Check Results</h1>
                <p className="mt-1 text-xs text-[#A1A1AA]">Suggestions for {selectedFile?.name}. No external service was called.</p>
              </div>
              <div className="rounded-xl border border-amber-700/50 bg-amber-950/30 px-5 py-4 text-center">
                <span className="block text-[10px] font-bold uppercase tracking-wider text-amber-300">Resume Status</span>
                <strong className="mt-1 block text-lg text-amber-200">Needs Improvement</strong>
              </div>
            </div>

            <section className="space-y-4">
              <div>
                <h2 className="text-xl font-bold">Mistakes &amp; Improvement Areas</h2>
                <p className="mt-1 text-xs text-[#A1A1AA]">These are prototype suggestions to guide your next resume revision.</p>
              </div>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                {publicResumeIssues.map((item) => (
                  <article key={item.category} className="rounded-xl border border-[#27272A] bg-[#17171D] p-5">
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="text-sm font-bold text-[#F5F5F5]">{item.category}</h3>
                      <span className={`shrink-0 rounded-full px-2 py-1 text-[10px] font-bold ${item.severity === 'Good' ? 'bg-emerald-950 text-emerald-300' : item.severity === 'Important' ? 'bg-red-950 text-red-300' : 'bg-amber-950 text-amber-300'}`}>
                        {item.severity}
                      </span>
                    </div>
                    <p className="mt-3 text-xs font-semibold text-[#F5F5F5]">Issue:</p>
                    <p className="mt-1 text-xs leading-relaxed text-[#A1A1AA]">{item.issue}</p>
                    <p className="mt-3 text-xs font-semibold text-red-300">Suggestion:</p>
                    <p className="mt-1 text-xs leading-relaxed text-[#A1A1AA]">{item.suggestion}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="rounded-2xl border border-[#27272A] bg-[#111116] p-6 text-center sm:p-8">
              <CheckCircle2 className="mx-auto h-8 w-8 text-[#E50914]" />
              <h2 className="mt-3 text-lg font-bold">Want deeper analysis?</h2>
              <p className="mx-auto mt-1 max-w-lg text-xs text-[#A1A1AA]">Create an account to access the existing candidate resume intelligence tools.</p>
              <div className="mt-5 flex flex-col justify-center gap-3 sm:flex-row">
                <Link to="/candidate/signin" className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#E50914] px-5 py-2.5 text-xs font-bold text-white hover:bg-[#FF1F2D]">
                  Candidate Analysis <ArrowRight className="h-4 w-4" />
                </Link>
                <Link to="/signup" className="inline-flex items-center justify-center gap-2 rounded-xl border border-[#27272A] px-5 py-2.5 text-xs font-bold text-[#F5F5F5] hover:border-[#E50914]">
                  Create Account
                </Link>
              </div>
            </section>

            <button type="button" onClick={() => setHasAnalyzed(false)} className="mx-auto inline-flex items-center gap-2 text-xs font-semibold text-[#A1A1AA] hover:text-[#F5F5F5]">
              <RotateCcw className="h-4 w-4" /> Check another resume
            </button>
          </>
        )}
      </div>
    </div>
  );
};
