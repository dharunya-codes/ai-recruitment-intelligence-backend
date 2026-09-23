import React, { useState } from 'react';
import { Briefcase, CheckCircle2, Save, X } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const CandidateJobDescriptionPage: React.FC = () => {
  const { candidateJobDescription, setCandidateJobDescription, setTargetRole, showToast } = useApp();
  const [form, setForm] = useState(candidateJobDescription);
  const [error, setError] = useState<string | null>(null);

  const update = (key: keyof typeof form, value: string) => {
    setForm((current) => ({ ...current, [key]: value }));
    setError(null);
  };

  const save = (event: React.FormEvent) => {
    event.preventDefault();
    if (!form.jobTitle.trim() || !form.companyName.trim() || !form.description.trim()) {
      setError('Please enter a job title, company name, and job description.');
      return;
    }
    setCandidateJobDescription({
      jobTitle: form.jobTitle.trim(),
      companyName: form.companyName.trim(),
      description: form.description.trim(),
    });
    setTargetRole(form.jobTitle.trim());
    showToast('Candidate Job Description saved for analysis and interview practice.', 'success');
  };

  const clear = () => {
    const empty = { jobTitle: '', companyName: '', description: '' };
    setForm(empty);
    setCandidateJobDescription(empty);
    setError(null);
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <div className="mb-2 inline-flex items-center gap-1.5 rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700"><Briefcase className="h-3.5 w-3.5" /> Candidate Targeting</div>
        <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Job Description</h1>
        <p className="mt-1 text-xs text-slate-500 sm:text-sm">Save one target Job Description to guide your resume, skills, evidence, matching, and interview views.</p>
      </div>

      <form onSubmit={save} className="space-y-5 rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs sm:p-8">
        {error && <div className="rounded-lg border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">{error}</div>}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div><label htmlFor="candidate-job-title" className="mb-1 block text-xs font-bold text-slate-700">Job Title</label><input id="candidate-job-title" value={form.jobTitle} onChange={(e) => update('jobTitle', e.target.value)} placeholder="Data Analyst" className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:border-red-600 focus:outline-none" /></div>
          <div><label htmlFor="candidate-company" className="mb-1 block text-xs font-bold text-slate-700">Company Name</label><input id="candidate-company" value={form.companyName} onChange={(e) => update('companyName', e.target.value)} placeholder="ABC Technologies" className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:border-red-600 focus:outline-none" /></div>
        </div>
        <div><label htmlFor="candidate-jd" className="mb-1 block text-xs font-bold text-slate-700">Job Description</label><textarea id="candidate-jd" rows={9} value={form.description} onChange={(e) => update('description', e.target.value)} placeholder="Paste responsibilities, requirements, tools, and qualifications..." className="w-full rounded-xl border border-slate-200 p-4 text-xs leading-relaxed text-slate-900 focus:border-red-600 focus:outline-none" /></div>
        <div className="flex flex-col justify-end gap-2 sm:flex-row"><button type="button" onClick={clear} className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-5 py-2.5 text-xs font-bold text-slate-700 hover:border-red-300"><X className="h-4 w-4" /> Clear</button><button type="submit" className="inline-flex items-center justify-center gap-2 rounded-xl bg-red-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-red-700"><Save className="h-4 w-4" /> Save Job Description</button></div>
      </form>

      <section className="rounded-2xl border border-red-100 bg-red-50/50 p-6 shadow-xs"><div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-red-700"><CheckCircle2 className="h-4 w-4" /> Currently Selected Job Description</div><h2 className="mt-3 text-lg font-bold text-slate-900">{candidateJobDescription.jobTitle || 'No job title saved'}</h2><p className="mt-1 text-xs font-semibold text-slate-600">{candidateJobDescription.companyName || 'No company saved'}</p><p className="mt-4 whitespace-pre-wrap text-xs leading-relaxed text-slate-700">{candidateJobDescription.description || 'Save a Job Description to connect it to the candidate workflow.'}</p></section>
    </div>
  );
};
