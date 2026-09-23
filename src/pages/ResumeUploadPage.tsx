import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { UploadBox } from '../components/UploadBox';
import { uploadResume } from '../services/api';
import {
  Sparkles,
  FileText,
  CheckCircle2,
  ArrowRight,
  Loader2,
  AlertCircle,
} from 'lucide-react';

export const ResumeUploadPage: React.FC = () => {
  const { uploadedFile, setUploadedFile, targetRole, setTargetRole, candidateJobDescription, setCandidateJobDescription, showToast } = useApp();
  const navigate = useNavigate();

  const [jobDescription, setJobDescription] = useState(candidateJobDescription.description);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState<string>('');

  const targetRoles = [
    'Data Analyst',
    'Senior Data Engineer',
    'Frontend Developer',
    'Machine Learning Engineer',
    'Product Growth Analyst',
  ];

  const handleFileSelected = (file: File) => {
    setUploadedFile(file);
    showToast(`Loaded ${file.name}`, 'info');
  };

  const handleClearFile = () => {
    setUploadedFile(null);
  };

  const handleStartAnalysis = async () => {
    setIsAnalyzing(true);
    setCandidateJobDescription((current) => ({ ...current, jobTitle: targetRole, description: jobDescription }));
    setTargetRole(targetRole);
    setAnalysisStep('Uploading and extracting semantic text layers...');
    try {
      const mockFile = uploadedFile || new File(['mock content'], 'Rose_Infanta_Data_Analyst.pdf', { type: 'application/pdf' });
      await uploadResume(mockFile, targetRole, jobDescription);

      setAnalysisStep('Auditing 8-point ATS formatting and achievement metrics...');
      await new Promise((r) => setTimeout(r, 600));

      setAnalysisStep('Checking project evidence for Python, SQL, and Power BI...');
      await new Promise((r) => setTimeout(r, 500));

      showToast('Resume analysis complete! Redirecting to intelligence report...', 'success');
      navigate('/candidate/analysis');
    } catch {
      showToast('Error parsing resume. Falling back to local intelligence.', 'warning');
      navigate('/candidate/analysis');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Resume Ingestion Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Upload Your Resume
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Upload your latest resume document (.pdf or .docx) and select your target job role for comprehensive ATS analysis.
        </p>
      </div>

      {/* Target Role & JD Selection */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
            Select Target Job Role
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {targetRoles.map((role) => (
              <button
                key={role}
                type="button"
                onClick={() => setTargetRole(role)}
                className={`px-3.5 py-2.5 rounded-xl border text-xs font-semibold text-left flex items-center justify-between transition-all ${
                  targetRole === role
                    ? 'border-red-600 bg-red-50/70 text-red-700 ring-2 ring-red-500/20'
                    : 'border-slate-200 hover:bg-slate-50 text-slate-600'
                }`}
              >
                <span>{role}</span>
                {targetRole === role && <CheckCircle2 className="w-3.5 h-3.5 text-red-600" />}
              </button>
            ))}
          </div>
        </div>

        {/* Upload Box */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
            Resume Document (.PDF or .DOCX)
          </label>
          <UploadBox
            selectedFile={uploadedFile}
            onFileSelected={handleFileSelected}
            onClearFile={handleClearFile}
          />
        </div>

        {/* Job Description Paste Area */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
              Target Job Description (JD)
            </label>
            <span className="text-[11px] text-slate-400">Optional for custom alignment</span>
          </div>
          <textarea
            rows={4}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste target job description or skill criteria here..."
            className="w-full rounded-xl border border-slate-200 p-3.5 text-xs text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-600 font-mono transition-all"
          />
        </div>
      </div>

      {/* Resume Preview & Metadata Card */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
        <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
          <FileText className="w-4 h-4 text-red-600" />
          <span>Resume Document Snapshot Preview</span>
        </h3>

        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 text-xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-slate-500">Document Identifier:</span>
            <span className="font-semibold text-slate-800">
              {uploadedFile ? uploadedFile.name : 'Rose_Infanta_Data_Analyst.pdf (Pre-loaded Sample)'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-500">Parsed Candidate:</span>
            <span className="font-semibold text-slate-800">Rose Infanta</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-500">Detected Skill Entities:</span>
            <span className="font-semibold text-red-700">
              Python, C, Excel, Pandas, Jupyter, Git (6 entities)
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-500">Detected Projects:</span>
            <span className="font-semibold text-slate-800">
              Sales Analysis, Student Productivity Tracker
            </span>
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <AlertCircle className="w-4 h-4 text-red-500 shrink-0" />
            <span>Files are parsed client-side with mock analysis readiness for FastAPI.</span>
          </div>

          <button
            type="button"
            disabled={isAnalyzing}
            onClick={handleStartAnalysis}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs transition-all shadow-md shadow-red-200 disabled:opacity-60"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>{analysisStep || 'Analyzing Resume...'}</span>
              </>
            ) : (
              <>
                <span>Analyze Resume Now</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};


