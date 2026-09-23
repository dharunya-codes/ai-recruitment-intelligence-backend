import React from 'react';
import { Link } from 'react-router-dom';
import { sampleJobVacancies, sampleCandidatesPool } from '../data/mockData';
import { DashboardCard } from '../components/DashboardCard';
import { JobCard } from '../components/JobCard';
import { StatusBadge } from '../components/StatusBadge';
import { ProgressBar } from '../components/ProgressBar';
import {
  Briefcase,
  Users,
  FileCheck,
  Sparkles,
  ArrowRight,
  PlusCircle,
  TrendingUp,
} from 'lucide-react';

export const RecruiterDashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-indigo-950 rounded-2xl p-6 sm:p-8 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-md">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-teal-200 text-xs font-semibold mb-3 backdrop-blur-xs">
            <Sparkles className="w-3.5 h-3.5 text-teal-300" />
            <span>Recruiter Intelligence Portal</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Talent Acquisition Overview
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-xl leading-relaxed">
            Screen candidates transparently with explainable AI summaries and verified evidence checks rather than opaque keyword filters.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/recruiter/job"
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-all shadow-md shadow-teal-950/40"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Create New Job Vacancy</span>
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <DashboardCard
          title="Active Job Roles"
          value={sampleJobVacancies.length}
          subtitle="Open requisition pipelines"
          trend={{ value: '3 Active pipelines', isPositive: true }}
          icon={<Briefcase className="w-5 h-5 text-teal-700" />}
          action={
            <Link
              to="/recruiter/job"
              className="text-xs font-semibold text-teal-700 hover:underline flex items-center justify-between"
            >
              <span>Manage Job Criteria</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Uploaded Resumes"
          value="48"
          subtitle="Processed in last 30 days"
          trend={{ value: '+12 this week', isPositive: true }}
          icon={<Users className="w-5 h-5 text-indigo-600" />}
          action={
            <Link
              to="/recruiter/candidates"
              className="text-xs font-semibold text-indigo-600 hover:underline flex items-center justify-between"
            >
              <span>View Ingestion Pool</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Candidates Analyzed"
          value="42"
          subtitle="Semantic parsed & scored"
          trend={{ value: '88% completion', isPositive: true }}
          icon={<FileCheck className="w-5 h-5 text-emerald-600" />}
          action={
            <Link
              to="/recruiter/candidates"
              className="text-xs font-semibold text-indigo-600 hover:underline flex items-center justify-between"
            >
              <span>Inspect Rankings</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Average Match Score"
          value="74%"
          subtitle="Across all job roles"
          trend={{ value: '+5% quality gain', isPositive: true }}
          icon={<TrendingUp className="w-5 h-5 text-amber-600" />}
          action={
            <Link
              to="/reports"
              className="text-xs font-semibold text-indigo-600 hover:underline flex items-center justify-between"
            >
              <span>View Executive Reports</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />
      </div>

      {/* Active Job Requisitions Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-slate-900">Active Job Description Requisitions</h2>
            <p className="text-xs text-slate-500">Decomposed skill requirements and applicant volume</p>
          </div>

          <Link
            to="/recruiter/job"
            className="text-xs font-semibold text-teal-700 hover:underline inline-flex items-center gap-1"
          >
            <span>Define New Requirements</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {sampleJobVacancies.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </div>

      {/* Recent Candidates Table */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900">Recent Candidate Evaluations</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Explainable candidate-role fit summaries based on actual resume evidence
            </p>
          </div>

          <Link
            to="/recruiter/candidates"
            className="text-xs font-bold text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
          >
            <span>View All Candidates</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50/80 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200/80">
                <th className="py-3 px-5">Candidate</th>
                <th className="py-3 px-5">Role Applied</th>
                <th className="py-3 px-5">Skill Match</th>
                <th className="py-3 px-5">Evidence Strength</th>
                <th className="py-3 px-5">JD Alignment</th>
                <th className="py-3 px-5">Status</th>
                <th className="py-3 px-5">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {sampleCandidatesPool.map((candidate) => (
                <tr key={candidate.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3.5 px-5">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center shrink-0">
                        {candidate.name[0]}
                      </div>
                      <div>
                        <span className="font-bold text-slate-900 block">{candidate.name}</span>
                        <span className="text-[11px] text-slate-400">{candidate.email}</span>
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-5 font-medium text-slate-800">{candidate.targetRole}</td>
                  <td className="py-3.5 px-5">
                    <div className="flex items-center gap-2 w-28">
                      <span className="font-bold text-indigo-700 w-8">{candidate.skillMatchPct}%</span>
                      <ProgressBar value={candidate.skillMatchPct} size="sm" />
                    </div>
                  </td>
                  <td className="py-3.5 px-5">
                    <StatusBadge status={candidate.evidenceStrength} size="sm" />
                  </td>
                  <td className="py-3.5 px-5 font-semibold text-slate-800">
                    {candidate.jdAlignment}
                  </td>
                  <td className="py-3.5 px-5">
                    <StatusBadge status={candidate.status} size="sm" />
                  </td>
                  <td className="py-3.5 px-5">
                    <Link
                      to={`/recruiter/candidate/${candidate.id}`}
                      className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition-colors inline-block"
                    >
                      Dossier
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
