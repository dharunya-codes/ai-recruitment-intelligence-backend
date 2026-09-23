import React from 'react';
import { NavLink } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import {
  LayoutDashboard,
  FileSearch,
  Sparkles,
  ShieldCheck,
  Split,
  Mic,
  FileBarChart2,
  Briefcase,
  Users,
  UserCheck,
  UploadCloud,
  X,
} from 'lucide-react';

interface SidebarProps {
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpenMobile = false,
  onCloseMobile,
}) => {
  const { currentRole } = useApp();

  const candidateLinks = [
    { to: '/candidate/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/candidate/resume', label: 'Upload Resume', icon: UploadCloud },
    { to: '/candidate/analysis', label: 'Resume Analysis', icon: FileSearch },
    { to: '/candidate/skill-gap', label: 'Skill Gap', icon: Sparkles },
    { to: '/candidate/evidence', label: 'Evidence Checker', icon: ShieldCheck },
    { to: '/candidate/job-match', label: 'Job Match', icon: Split },
    { to: '/interview', label: 'Mock Interview', icon: Mic },
    { to: '/reports', label: 'Reports', icon: FileBarChart2 },
  ];

  const recruiterLinks = [
    { to: '/recruiter/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/recruiter/job', label: 'Job Description', icon: Briefcase },
    { to: '/recruiter/candidates', label: 'Candidates', icon: Users },
    { to: '/recruiter/candidate/cand-001', label: 'Candidate Analysis', icon: UserCheck },
    { to: '/reports', label: 'Reports', icon: FileBarChart2 },
  ];

  const links = currentRole === 'candidate' ? candidateLinks : recruiterLinks;

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div
          onClick={onCloseMobile}
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-64 bg-white border-r border-slate-200/80 p-5 flex flex-col justify-between transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full'
        } lg:static lg:z-10 shrink-0`}
      >
        <div>
          {/* Top Brand & Close on Mobile */}
          <div className="flex items-center justify-between pb-6 mb-2 border-b border-slate-100 lg:hidden">
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <span>TalentIQ Navigation</span>
            </div>
            <button
              onClick={onCloseMobile}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Mode Pill Indicator */}
          <div className="mb-5 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-500 uppercase tracking-wider text-[10px]">
              Workspace
            </span>
            <span
              className={`font-bold px-2 py-0.5 rounded-md text-[11px] ${
                currentRole === 'candidate'
                  ? 'bg-indigo-100 text-indigo-800'
                  : 'bg-teal-100 text-teal-800'
              }`}
            >
              {currentRole === 'candidate' ? 'Job Seeker Suite' : 'Recruiter AI Hub'}
            </span>
          </div>

          {/* Nav List */}
          <nav className="space-y-1">
            {links.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={onCloseMobile}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                      isActive
                        ? 'bg-indigo-600 text-white shadow-xs shadow-indigo-200'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Sidebar Footer Card */}
        <div className="pt-4 border-t border-slate-100">
          <div className="p-3.5 rounded-xl bg-gradient-to-br from-indigo-50/70 to-violet-50/70 border border-indigo-100/80 text-xs">
            <div className="flex items-center gap-1.5 text-indigo-950 font-bold mb-1">
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              <span>AI Assist Ready</span>
            </div>
            <p className="text-slate-600 text-[11px] leading-relaxed">
              Target role: <strong>Data Analyst</strong>. Resume verified against ATS standards.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
};
