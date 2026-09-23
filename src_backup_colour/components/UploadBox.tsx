import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, X } from 'lucide-react';

interface UploadBoxProps {
  onFileSelected: (file: File) => void;
  selectedFile: File | null;
  onClearFile?: () => void;
  accept?: string;
  maxSizeBytes?: number;
  className?: string;
}

export const UploadBox: React.FC<UploadBoxProps> = ({
  onFileSelected,
  selectedFile,
  onClearFile,
  accept = '.pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  maxSizeBytes = 10 * 1024 * 1024, // 10MB
  className = '',
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndHandle = (file: File) => {
    setErrorMsg(null);
    const validExtensions = ['.pdf', '.docx'];
    const hasValidExt = validExtensions.some((ext) =>
      file.name.toLowerCase().endsWith(ext)
    );

    if (!hasValidExt) {
      setErrorMsg('Invalid file format. Please upload a PDF or DOCX resume document.');
      return;
    }

    if (file.size > maxSizeBytes) {
      setErrorMsg(`File exceeds maximum allowed size (${(maxSizeBytes / (1024 * 1024)).toFixed(0)}MB).`);
      return;
    }

    onFileSelected(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndHandle(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndHandle(e.target.files[0]);
    }
  };

  return (
    <div className={`w-full ${className}`}>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleFileInput}
        className="hidden"
      />

      {selectedFile ? (
        <div className="p-6 rounded-2xl border-2 border-indigo-200 bg-indigo-50/30 flex items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-xs">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <p className="text-sm font-bold text-slate-900 truncate max-w-xs sm:max-w-md">
                  {selectedFile.name}
                </p>
                <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-full">
                  <CheckCircle2 className="w-3 h-3" /> Ready
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                {(selectedFile.size / 1024).toFixed(1)} KB •{' '}
                {selectedFile.type || (selectedFile.name.endsWith('.pdf') ? 'PDF Document' : 'DOCX Document')}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 transition-colors"
            >
              Replace
            </button>
            {onClearFile && (
              <button
                type="button"
                onClick={onClearFile}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
                title="Remove file"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      ) : (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 sm:p-10 text-center cursor-pointer transition-all ${
            isDragOver
              ? 'border-indigo-600 bg-indigo-50/50 scale-[0.99]'
              : 'border-slate-300 hover:border-indigo-400 bg-white hover:bg-slate-50/50'
          }`}
        >
          <div className="w-14 h-14 mx-auto rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4 border border-indigo-100/80 shadow-xs">
            <UploadCloud className="w-7 h-7" />
          </div>

          <h3 className="text-base font-bold text-slate-900 mb-1">
            Drag & drop your resume file here
          </h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mb-4">
            Supports official ATS documents in <strong>.PDF</strong> or <strong>.DOCX</strong> format (up to 10MB).
          </p>

          <button
            type="button"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100 text-slate-700 text-xs font-bold hover:bg-slate-200 transition-colors"
          >
            <span>Browse from computer</span>
          </button>
        </div>
      )}

      {errorMsg && (
        <div className="mt-2.5 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
          <span>{errorMsg}</span>
        </div>
      )}
    </div>
  );
};
