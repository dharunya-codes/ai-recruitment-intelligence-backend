import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Sparkles, ArrowRightLeft, Bell, User, LogOut, Menu } from 'lucide-react';

interface NavbarProps {
  onToggleMobileSidebar?: () => void;
  showSidebarToggle?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onToggleMobileSidebar,
  showSidebarToggle = false,
}) => {
  const { currentRole, setRole, candidate, isLoggedIn, logout } = useApp();
  const navigate = useNavigate();

  const handleRoleToggle = () => {
    const nextRole = currentRole === 'candidate' ? 'recruiter' : 'candidate';
    setRole(nextRole);
    navigate(nextRole === 'candidate' ? '/candidate/signin' : '/recruiter/signin');
  };

  const handleLogout = () => {
    navigate('/role-selection', { replace: true });
    logout(currentRole);
  };

  return (
    <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-6 py-3">
      <div className="flex items-center justify-between gap-4 max-w-7xl mx-auto">
        {/* Left Section: Logo & Toggle */}
        <div className="flex items-center gap-3">
          {showSidebarToggle && (
            <button
              onClick={onToggleMobileSidebar}
              className="lg:hidden p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition-colors"
              title="Toggle Menu"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}

          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-red-600 to-red-600 text-white flex items-center justify-center shadow-xs shadow-red-200 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-slate-900 block leading-none">
                TalentIQ
              </span>
              <span className="text-[10px] font-semibold tracking-wider uppercase text-red-600">
                Resume Intelligence
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Global Navigation or Feature Pills */}
        <div className="hidden md:flex items-center gap-1.5 text-xs font-medium text-slate-600">
          <Link
            to="/candidate/signin"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              currentRole === 'candidate'
                ? 'bg-slate-100 text-slate-900 font-semibold'
                : 'hover:bg-slate-50 text-slate-600'
            }`}
          >
            Candidate Portal
          </Link>
          <Link
            to="/recruiter/signin"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              currentRole === 'recruiter'
                ? 'bg-slate-100 text-slate-900 font-semibold'
                : 'hover:bg-slate-50 text-slate-600'
            }`}
          >
            Recruiter Portal
          </Link>
          <Link
            to="/interview"
            className="px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors"
          >
            AI Mock Interview
          </Link>
          <Link
            to="/reports"
            className="px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors"
          >
            Reports
          </Link>
        </div>

        {/* Right Section: Role Switcher & User Profile */}
        <div className="flex items-center gap-2.5">
          {/* Quick Switch Role CTA */}
          <button
            onClick={handleRoleToggle}
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 bg-white text-slate-700 text-xs font-semibold hover:border-red-300 hover:bg-red-50/40 transition-all shadow-2xs"
            title={`Switch to ${currentRole === 'candidate' ? 'Recruiter' : 'Candidate'} Mode`}
          >
            <ArrowRightLeft className="w-3.5 h-3.5 text-red-600" />
            <span>Switch to {currentRole === 'candidate' ? 'Recruiter' : 'Candidate'}</span>
          </button>

          {/* Current Role Badge */}
          <span
            className={`text-xs px-2.5 py-1 rounded-full font-bold uppercase tracking-wider border ${
              currentRole === 'candidate'
                ? 'bg-red-50 text-red-700 border-red-200'
                : 'bg-teal-50 text-teal-800 border-teal-200'
            }`}
          >
            {currentRole}
          </span>

          {/* Notification Button */}
          <button
            type="button"
            className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors relative"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-600" />
          </button>

          {/* Profile Badge */}
          {isLoggedIn ? (
            <div className="flex items-center gap-2 pl-1 border-l border-slate-200">
              <div className="w-8 h-8 rounded-full bg-red-100 text-red-700 border border-red-200 flex items-center justify-center font-bold text-xs">
                {currentRole === 'candidate' ? candidate.name[0] : 'R'}
              </div>
              <div className="hidden xl:block text-left text-xs">
                <span className="font-semibold text-slate-900 block truncate max-w-[120px]">
                  {currentRole === 'candidate' ? candidate.name : 'Recruiter Team'}
                </span>
                <span className="text-[11px] text-slate-400 block truncate max-w-[120px]">
                  {currentRole === 'candidate' ? candidate.targetRole : 'Talent Acquisition'}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-slate-100"
                title="Logout"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <Link
              to="/login"
              className="inline-flex items-center gap-1 text-xs font-semibold px-3 py-1.5 rounded-xl bg-red-600 text-white hover:bg-red-700 transition-colors"
            >
              <User className="w-3.5 h-3.5" />
              <span>Login</span>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};


