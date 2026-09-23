import React, { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Sparkles, X, AlertCircle } from 'lucide-react';

export const InterviewLayout: React.FC = () => {
  const { candidate, targetRole } = useApp();
  const [showExitConfirm, setShowExitConfirm] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const isFeedbackPage = location.pathname.includes('/feedback');

  const handleExit = () => {
    setShowExitConfirm(false);
    navigate('/candidate/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans selection:bg-red-500 selection:text-white">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md px-4 sm:px-6 py-3.5 sticky top-0 z-30">
        <div className="max-w-5xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-red-600 text-white flex items-center justify-center">
                <Sparkles className="w-4 h-4" />
              </div>
              <span className="font-bold text-sm tracking-tight text-white hidden sm:inline">
                TalentIQ Mock Room
              </span>
            </Link>

            <span className="text-slate-700 hidden sm:inline">•</span>

            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-400">Candidate:</span>
              <strong className="text-white font-medium">{candidate.name}</strong>
              <span className="text-slate-600">|</span>
              <span className="text-slate-400">Role:</span>
              <span className="px-2 py-0.5 rounded bg-red-900/60 text-red-300 font-semibold border border-red-700/50">
                {targetRole}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {isFeedbackPage ? (
              <Link
                to="/candidate/dashboard"
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-200 text-xs font-semibold hover:bg-slate-700 transition-colors"
              >
                Back to Dashboard
              </Link>
            ) : (
              <button
                type="button"
                onClick={() => setShowExitConfirm(true)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-700/60 transition-colors"
              >
                <X className="w-4 h-4 text-slate-400" />
                <span>Exit Session</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Interview Arena */}
      <main className="flex-1 flex flex-col justify-center px-4 py-8 sm:px-6">
        <div className="max-w-4xl w-full mx-auto">
          <Outlet />
        </div>
      </main>

      {/* Exit Confirmation Modal */}
      {showExitConfirm && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-sm w-full shadow-2xl">
            <div className="flex items-center gap-3 text-amber-400 mb-3">
              <AlertCircle className="w-6 h-6 shrink-0" />
              <h3 className="font-bold text-base text-white">Leave Interview?</h3>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed mb-5">
              Your answered questions have been recorded, but leaving now will exit your active interview session.
            </p>
            <div className="flex items-center justify-end gap-2.5">
              <button
                onClick={() => setShowExitConfirm(false)}
                className="px-3.5 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
              >
                Continue Interview
              </button>
              <button
                onClick={handleExit}
                className="px-3.5 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-700"
              >
                Exit Now
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};


