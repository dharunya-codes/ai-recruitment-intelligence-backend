import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, UserCheck, Briefcase, Lock, Mail } from 'lucide-react';
import { isValidEmail } from '../utils/validators';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState('rose.infanta@example.com');
  const [password, setPassword] = useState('••••••••••••');
  const [selectedRole, setSelectedRole] = useState<'candidate' | 'recruiter'>('candidate');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      setError('Please provide your email and password.');
      return;
    }
    if (!isValidEmail(email)) {
      setError('Please enter a valid email address.');
      return;
    }
    navigate(selectedRole === 'candidate' ? '/candidate/signin' : '/recruiter/signin');
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-12 bg-[#0B0B0F]">
      <div className="bg-[#17171D] rounded-2xl border border-[#27272A] shadow-md p-6 sm:p-8 max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-red-600 text-white flex items-center justify-center mx-auto mb-3 shadow-xs">
            <Sparkles className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-[#F5F5F5]">Welcome Back</h2>
          <p className="text-xs text-[#A1A1AA] mt-1">
            Access your personalized resume intelligence & interview portal
          </p>
        </div>

        {/* Role Selection */}
        <div className="mb-6 p-3 rounded-xl bg-[#111116] border border-[#27272A]">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#A1A1AA] block mb-2 text-center">
            Select Your Role
          </span>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => setSelectedRole('candidate')}
              className={`inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg border text-xs font-semibold transition-colors shadow-2xs ${selectedRole === 'candidate' ? 'bg-[#E50914] border-[#E50914] text-white' : 'bg-[#17171D] border-[#27272A] text-[#A1A1AA] hover:border-[#E50914] hover:text-[#F5F5F5]'}`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>Candidate</span>
            </button>
            <button
              type="button"
              onClick={() => setSelectedRole('recruiter')}
              className={`inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg border text-xs font-semibold transition-colors shadow-2xs ${selectedRole === 'recruiter' ? 'bg-[#E50914] border-[#E50914] text-white' : 'bg-[#17171D] border-[#27272A] text-[#A1A1AA] hover:border-[#E50914] hover:text-[#F5F5F5]'}`}
            >
              <Briefcase className="w-3.5 h-3.5" />
              <span>Recruiter</span>
            </button>
          </div>
        </div>

        <div className="relative flex py-2 items-center mb-5">
          <div className="flex-grow border-t border-[#27272A]" />
          <span className="shrink-0 mx-3 text-[11px] font-medium text-[#A1A1AA]">Sign in with credentials</span>
          <div className="flex-grow border-t border-[#27272A]" />
        </div>

        {error && (
          <div className="mb-4 p-2.5 rounded-lg bg-[#3B0A0D] text-[#FCA5A5] border border-[#7F1D1D] text-xs">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-[#F5F5F5] mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#A1A1AA] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
                className="w-full rounded-xl border border-[#27272A] bg-[#111116] pl-10 pr-3.5 py-2.5 text-xs text-[#F5F5F5] placeholder:text-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-red-500/20 focus:border-[#E50914] transition-colors"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-bold text-[#F5F5F5]">Password</label>
              <span className="text-[11px] text-[#E50914] hover:underline cursor-pointer">
                Forgot password?
              </span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#A1A1AA] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full rounded-xl border border-[#27272A] bg-[#111116] pl-10 pr-3.5 py-2.5 text-xs text-[#F5F5F5] placeholder:text-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-red-500/20 focus:border-[#E50914] transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full inline-flex items-center justify-center gap-2 py-2.5 rounded-xl bg-[#E50914] hover:bg-[#FF1F2D] text-white text-xs font-bold transition-all shadow-xs"
          >
            <span>Sign In to Platform</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </form>

        <div className="mt-6 pt-5 border-t border-[#27272A] text-center text-xs text-[#A1A1AA]">
          <span>Don't have an account? </span>
          <Link to="/signup" className="text-red-600 font-bold hover:underline">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
};


