import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Sparkles, ArrowRight, UserCheck, Briefcase, Lock, Mail } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const { login, setRole } = useApp();
  const navigate = useNavigate();

  const [email, setEmail] = useState('rose.infanta@example.com');
  const [password, setPassword] = useState('••••••••••••');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      setError('Please provide your email and password.');
      return;
    }
    login(email, 'candidate');
    navigate('/candidate/dashboard');
  };

  const handleContinueAs = (role: 'candidate' | 'recruiter') => {
    setRole(role);
    if (role === 'candidate') {
      login('rose.infanta@example.com', 'candidate');
      navigate('/candidate/dashboard');
    } else {
      login('recruiter.lead@talentintelligence.ai', 'recruiter');
      navigate('/recruiter/dashboard');
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-12">
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-md p-6 sm:p-8 max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-indigo-600 text-white flex items-center justify-center mx-auto mb-3 shadow-xs">
            <Sparkles className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Welcome Back</h2>
          <p className="text-xs text-slate-500 mt-1">
            Access your personalized resume intelligence & interview portal
          </p>
        </div>

        {/* Quick Demo Shortcuts */}
        <div className="mb-6 p-3 rounded-xl bg-slate-50 border border-slate-200/70">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-2 text-center">
            Instant Demo Access
          </span>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleContinueAs('candidate')}
              className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-white border border-indigo-200 text-indigo-700 text-xs font-semibold hover:bg-indigo-50/60 transition-colors shadow-2xs"
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>Candidate</span>
            </button>
            <button
              type="button"
              onClick={() => handleContinueAs('recruiter')}
              className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-white border border-teal-200 text-teal-800 text-xs font-semibold hover:bg-teal-50/60 transition-colors shadow-2xs"
            >
              <Briefcase className="w-3.5 h-3.5" />
              <span>Recruiter</span>
            </button>
          </div>
        </div>

        <div className="relative flex py-2 items-center mb-5">
          <div className="flex-grow border-t border-slate-200" />
          <span className="shrink-0 mx-3 text-[11px] font-medium text-slate-400">or with credentials</span>
          <div className="flex-grow border-t border-slate-200" />
        </div>

        {error && (
          <div className="mb-4 p-2.5 rounded-lg bg-rose-50 text-rose-800 border border-rose-200 text-xs">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
                className="w-full rounded-xl border border-slate-200 pl-10 pr-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-colors"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-bold text-slate-700">Password</label>
              <span className="text-[11px] text-indigo-600 hover:underline cursor-pointer">
                Forgot password?
              </span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full rounded-xl border border-slate-200 pl-10 pr-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full inline-flex items-center justify-center gap-2 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <span>Sign In to Platform</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </form>

        <div className="mt-6 pt-5 border-t border-slate-100 text-center text-xs text-slate-500">
          <span>Don't have an account? </span>
          <Link to="/signup" className="text-indigo-600 font-bold hover:underline">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
};
