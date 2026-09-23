import React, { useMemo, useRef, useState } from 'react';
import { AlertCircle, BarChart3, CheckCircle2, FileSearch, Trash2, UploadCloud, X } from 'lucide-react';
import { sampleBulkResumeCandidates } from '../data/mockData';

const MAX_RESUMES = 50;
const acceptedExtensions = ['.pdf', '.docx'];

interface UploadedResume {
  id: string;
  file: File;
  candidateName: string;
  status: 'Ready' | 'Analyzed';
}

const candidateNameFromFile = (fileName: string, index: number) => {
  const baseName = fileName.replace(/\.(pdf|docx)$/i, '').replace(/[_-]+/g, ' ').trim();
  const cleanedName = baseName.replace(/resume|cv/gi, '').trim();
  return cleanedName || sampleBulkResumeCandidates[index % sampleBulkResumeCandidates.length].name;
};

const isSupportedResume = (file: File) =>
  acceptedExtensions.some((extension) => file.name.toLowerCase().endsWith(extension));

export const BulkResumeAnalysisPage: React.FC = () => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploads, setUploads] = useState<UploadedResume[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasAnalyzed, setHasAnalyzed] = useState(false);

  const addFiles = (files: FileList | File[]) => {
    const incoming = Array.from(files);
    const invalidFile = incoming.find((file) => !isSupportedResume(file));
    if (invalidFile) {
      setError(`${invalidFile.name} is not supported. Upload PDF or DOCX files only.`);
    }

    const validFiles = incoming.filter(isSupportedResume);
    const remainingSlots = MAX_RESUMES - uploads.length;
    if (validFiles.length > remainingSlots) {
      setError('Maximum 50 resumes can be analyzed in one batch.');
    }

    const filesToAdd = validFiles.slice(0, Math.max(0, remainingSlots));
    if (filesToAdd.length === 0) return;

    setUploads((current) => [
      ...current,
      ...filesToAdd.map((file, index) => ({
        id: `${file.name}-${file.lastModified}-${current.length + index}`,
        file,
        candidateName: candidateNameFromFile(file.name, current.length + index),
        status: 'Ready' as const,
      })),
    ]);
    setHasAnalyzed(false);
    if (!invalidFile && filesToAdd.length === validFiles.length) setError(null);
  };

  const handleFileInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) addFiles(event.target.files);
    event.target.value = '';
  };

  const removeUpload = (id: string) => {
    setUploads((current) => current.filter((upload) => upload.id !== id));
    setHasAnalyzed(false);
    setError(null);
  };

  const clearAll = () => {
    setUploads([]);
    setHasAnalyzed(false);
    setError(null);
  };

  const analyzedCandidates = useMemo(() => uploads.map((upload, index) => ({
    ...sampleBulkResumeCandidates[index % sampleBulkResumeCandidates.length],
    id: upload.id,
    name: upload.candidateName,
    resumeFile: upload.file.name,
    status: 'Analyzed' as const,
  })), [uploads]);

  const handleAnalyze = () => {
    if (uploads.length > 0) setHasAnalyzed(true);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
            <BarChart3 className="h-3.5 w-3.5" />
            Bulk Recruiter Workflow
          </div>
          <h1 className="mt-3 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Bulk Resume Analysis</h1>
          <p className="mt-1 text-xs text-slate-500 sm:text-sm">Upload and analyze multiple candidate resumes in one batch.</p>
        </div>
        <span className="inline-flex w-fit items-center rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-bold text-red-700">Maximum 50 Candidates</span>
      </div>

      <section
        onDragOver={(event) => { event.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={(event) => { event.preventDefault(); setIsDragOver(false); addFiles(event.dataTransfer.files); }}
        className={`rounded-2xl border-2 border-dashed p-8 text-center transition-colors sm:p-12 ${isDragOver ? 'border-red-600 bg-red-50/60' : 'border-slate-300 bg-white hover:border-red-400'}`}
      >
        <input ref={inputRef} type="file" multiple accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" onChange={handleFileInput} className="hidden" />
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-red-100 bg-red-50 text-red-600">
          <UploadCloud className="h-7 w-7" />
        </div>
        <h2 className="mt-4 text-base font-bold text-slate-900">Drop resumes here or click to upload</h2>
        <p className="mt-1 text-xs text-slate-500">PDF and DOCX files • Maximum 50 resumes</p>
        <button type="button" onClick={() => inputRef.current?.click()} className="mt-5 inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-red-700">
          <UploadCloud className="h-4 w-4" /> Add Resumes
        </button>
      </section>

      {error && <div className="flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800"><AlertCircle className="h-4 w-4 shrink-0 text-rose-600" />{error}<button type="button" onClick={() => setError(null)} className="ml-auto" title="Dismiss error"><X className="h-4 w-4" /></button></div>}

      {uploads.length > 0 && (
        <section className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-xs">
          <div className="flex flex-col gap-3 border-b border-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Candidate Uploads ({uploads.length}/{MAX_RESUMES})</h2>
              <p className="mt-1 text-xs text-slate-500">Review the batch before starting the prototype analysis.</p>
            </div>
            <div className="flex gap-2">
              <button type="button" onClick={() => inputRef.current?.click()} className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 hover:border-red-300">Add More Resumes</button>
              <button type="button" onClick={clearAll} className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 hover:border-red-300">Clear All</button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-left text-xs">
              <thead className="bg-slate-50 text-[10px] uppercase tracking-wider text-slate-500"><tr><th className="px-5 py-3">#</th><th className="px-5 py-3">Candidate</th><th className="px-5 py-3">File Name</th><th className="px-5 py-3">File Type</th><th className="px-5 py-3">File Size</th><th className="px-5 py-3">Status</th><th className="px-5 py-3">Action</th></tr></thead>
              <tbody className="divide-y divide-slate-100">
                {uploads.map((upload, index) => <tr key={upload.id}><td className="px-5 py-3 font-semibold text-slate-500">{index + 1}</td><td className="px-5 py-3 font-semibold text-slate-900">{upload.candidateName}</td><td className="max-w-[220px] truncate px-5 py-3 text-slate-600">{upload.file.name}</td><td className="px-5 py-3 text-slate-600">{upload.file.name.toLowerCase().endsWith('.pdf') ? 'PDF' : 'DOCX'}</td><td className="px-5 py-3 text-slate-600">{(upload.file.size / 1024).toFixed(1)} KB</td><td className="px-5 py-3"><span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-1 font-semibold text-emerald-700"><CheckCircle2 className="h-3 w-3" />{hasAnalyzed ? 'Analyzed' : upload.status}</span></td><td className="px-5 py-3"><button type="button" onClick={() => removeUpload(upload.id)} className="inline-flex items-center gap-1 text-rose-600 hover:text-rose-800" title={`Remove ${upload.file.name}`}><Trash2 className="h-4 w-4" />Remove</button></td></tr>)}
              </tbody>
            </table>
          </div>
          <div className="flex flex-col items-center justify-between gap-3 border-t border-slate-100 p-5 sm:flex-row"><p className="text-xs text-slate-500">Mock analysis uses deterministic recruiter candidate data. No backend request is made.</p><button type="button" onClick={handleAnalyze} className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-red-700"><FileSearch className="h-4 w-4" />Analyze Resumes</button></div>
        </section>
      )}

      {hasAnalyzed && <section className="space-y-4"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold text-slate-900">Batch Analysis Results</h2><p className="mt-1 text-xs text-slate-500">{analyzedCandidates.length} candidate summaries generated from deterministic mock data.</p></div></div><div className="grid grid-cols-1 gap-4 xl:grid-cols-2">{analyzedCandidates.map((candidate) => <article key={candidate.id} className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs"><div className="flex items-start justify-between gap-3"><div><h3 className="font-bold text-slate-900">{candidate.name}</h3><p className="mt-1 text-xs text-slate-500">{candidate.targetRole} • {candidate.experience} years experience</p></div><span className={`rounded-full px-2 py-1 text-[10px] font-bold ${candidate.evidenceStrength === 'Strong' ? 'bg-emerald-50 text-emerald-700' : candidate.evidenceStrength === 'Medium' ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'}`}>{candidate.evidenceStrength} Evidence</span></div><div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs"><div className="rounded-lg bg-slate-50 p-2"><strong className="block text-slate-900">{candidate.resumeScore}</strong><span className="text-slate-500">Resume</span></div><div className="rounded-lg bg-slate-50 p-2"><strong className="block text-slate-900">{candidate.skillMatch}%</strong><span className="text-slate-500">Skills</span></div><div className="rounded-lg bg-slate-50 p-2"><strong className="block text-slate-900">{candidate.atsScore}</strong><span className="text-slate-500">ATS</span></div></div><div className="mt-4 flex flex-wrap gap-1.5">{candidate.matchedSkills.map((skill) => <span key={skill} className="rounded-md bg-red-50 px-2 py-1 text-[10px] font-semibold text-red-700">{skill}</span>)}</div></article>)}</div></section>}
    </div>
  );
};
