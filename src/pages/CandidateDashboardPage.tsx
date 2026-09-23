import React from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { sampleResumeScore, sampleSkillGap, sampleJobMatch } from '../data/mockData';
import { DashboardCard } from '../components/DashboardCard';
import { ResumeScore } from '../components/ResumeScore';
import { StatusBadge } from '../components/StatusBadge';
import { SkillBadge } from '../components/SkillBadge';
import {
  FileText,
  UploadCloud,
  Mic,
  ArrowRight,
  Sparkles,
  AlertCircle,
  FileSearch,
  CheckCircle2,
  TrendingUp,
} from 'lucide-react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';

export const CandidateDashboardPage: React.FC = () => {
  const { candidate, targetRole } = useApp();

  const radarData = [
    { subject: 'ATS Pass', value: sampleResumeScore.atsScore },
    { subject: 'Formatting', value: sampleResumeScore.sections.formatting.score },
    { subject: 'Grammar', value: sampleResumeScore.sections.grammar.score },
    { subject: 'Projects', value: sampleResumeScore.sections.projectDescription.score },
    { subject: 'Metrics', value: sampleResumeScore.sections.achievementStatements.score },
    { subject: 'Skills Match', value: sampleJobMatch.matchPercentage },
  ];

  const skillMatchBarData = [
    { name: 'Python', score: 95 },
    { name: 'Excel', score: 90 },
    { name: 'SQL', score: 55 },
    { name: 'Pandas', score: 70 },
    { name: 'Statistics', score: 50 },
    { name: 'Power BI', score: 0 },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-red-900 via-red-800 to-slate-900 rounded-2xl p-6 sm:p-8 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-md">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-red-200 text-xs font-semibold mb-3 backdrop-blur-xs">
            <Sparkles className="w-3.5 h-3.5 text-red-300" />
            <span>AI Intelligence Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {candidate.name}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-xl leading-relaxed">
            Your resume is currently evaluated against the{' '}
            <strong className="text-white underline decoration-red-400 underline-offset-2">
              {targetRole}
            </strong>{' '}
            target role standard.
          </p>

          <div className="flex flex-wrap items-center gap-3 mt-4 text-xs">
            <span className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-white/10 text-white font-medium">
              <FileText className="w-3.5 h-3.5 text-red-300" />
              {candidate.uploadedResumeName || 'Rose_Infanta_Data_Analyst.pdf'}
            </span>
            <span className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Resume Parsed & Audited
            </span>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full md:w-auto">
          <Link
            to="/candidate/resume"
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all border border-white/20"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload Resume</span>
          </Link>
          <Link
            to="/interview"
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-red-500 hover:bg-red-400 text-white text-xs font-bold transition-all shadow-md shadow-red-950/50"
          >
            <Mic className="w-4 h-4" />
            <span>Start Mock Interview</span>
          </Link>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <DashboardCard
          title="Resume Score"
          value={`${sampleResumeScore.overallScore}/100`}
          subtitle="ATS Parsed: Grade A-"
          trend={{ value: '+4 pts vs benchmark', isPositive: true }}
          icon={<FileSearch className="w-5 h-5 text-red-600" />}
          action={
            <Link
              to="/candidate/analysis"
              className="text-xs font-semibold text-red-600 hover:text-red-800 flex items-center justify-between"
            >
              <span>View 8-Point Analysis</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Skill Match Pct"
          value={`${sampleJobMatch.matchPercentage}%`}
          subtitle="Matched against Data Analyst JD"
          trend={{ value: '2 Strong / 2 Weak', neutral: true }}
          icon={<Sparkles className="w-5 h-5 text-red-600" />}
          action={
            <Link
              to="/candidate/skill-gap"
              className="text-xs font-semibold text-red-600 hover:text-red-800 flex items-center justify-between"
            >
              <span>Explore Skill Gaps</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Evidence Strength"
          value="Moderate"
          subtitle="Strong in Python & Excel"
          trend={{ value: 'SQL lacks query proof', isPositive: false }}
          icon={<TrendingUp className="w-5 h-5 text-amber-600" />}
          action={
            <Link
              to="/candidate/evidence"
              className="text-xs font-semibold text-red-600 hover:text-red-800 flex items-center justify-between"
            >
              <span>Inspect Proof Snippets</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />

        <DashboardCard
          title="Missing Skills"
          value={sampleSkillGap.missingSkills.length}
          subtitle="Power BI not detected"
          trend={{ value: 'Ethical advice provided', isPositive: true }}
          icon={<AlertCircle className="w-5 h-5 text-rose-600" />}
          action={
            <Link
              to="/candidate/job-match"
              className="text-xs font-semibold text-red-600 hover:text-red-800 flex items-center justify-between"
            >
              <span>Compare Full JD Matrix</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          }
        />
      </div>

      {/* Main Section: Radial Score Gauge & Radar Alignment */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Radial Score Gauge Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900">Resume Quality Breakdown</h3>
              <StatusBadge status="Good" size="sm" />
            </div>

            <ResumeScore
              score={sampleResumeScore.overallScore}
              atsScore={sampleResumeScore.atsScore}
              atsGrade={sampleResumeScore.atsGrade}
              className="my-2"
            />

            <div className="mt-5 space-y-2.5 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600">Contact Information</span>
                <span className="font-bold text-emerald-700">95% (Good)</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600">Project Description</span>
                <span className="font-bold text-amber-700">64% (Needs Improvement)</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600">Achievement Statements</span>
                <span className="font-bold text-amber-700">60% (Needs Improvement)</span>
              </div>
            </div>
          </div>

          <div className="mt-5 pt-4 border-t border-slate-100">
            <Link
              to="/candidate/analysis"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-red-600 hover:text-red-800"
            >
              <span>Inspect all 8 Quality Dimensions</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Competency Radar Chart */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-base font-bold text-slate-900">Competency Radar</h3>
              <span className="text-xs text-slate-400">Target: {targetRole}</span>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Normalized scoring across structural presentation and technical fit.
            </p>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#e2e8f0" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10 }} />
                  <Radar
                    name="Score"
                    dataKey="value"
                    stroke="#4f46e5"
                    fill="#6366f1"
                    fillOpacity={0.4}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-500 flex items-center justify-between">
            <span>Strongest: Contact & Spelling (95%)</span>
            <span className="text-amber-700 font-semibold">Priority: Add Metrics</span>
          </div>
        </div>

        {/* Skill Evidence Verification Distribution */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-base font-bold text-slate-900">Skill Evidence Levels</h3>
              <span className="text-xs font-semibold text-red-600">6 Required</span>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Detected evidence strength across required Data Analyst competencies.
            </p>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={skillMatchBarData} layout="vertical">
                  <XAxis type="number" domain={[0, 100]} hide />
                  <YAxis
                    dataKey="name"
                    type="category"
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#334155', fontSize: 11, fontWeight: 500 }}
                    width={65}
                  />
                  <Tooltip
                    formatter={(val: any) => [`${val}% Evidence Strength`, 'Score']}
                    contentStyle={{ borderRadius: 8, fontSize: 12 }}
                  />
                  <Bar dataKey="score" fill="#4f46e5" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100">
            <Link
              to="/candidate/skill-gap"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-red-600 hover:text-red-800"
            >
              <span>View Skill Gap & Ethical Recommendations</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Bottom Grid: Quick Actions, Missing Skills Alert, Recent Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Missing Skills Warning Card */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-rose-50 text-rose-600 border border-rose-100">
                <AlertCircle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Target Skill Gaps Identified
                </h3>
                <p className="text-xs text-slate-500">
                  Required for <strong>{targetRole}</strong> role alignment
                </p>
              </div>
            </div>

            <Link
              to="/candidate/skill-gap"
              className="text-xs font-semibold text-red-600 hover:underline"
            >
              View Full Gap Matrix
            </Link>
          </div>

          {/* Skill Badges */}
          <div className="flex flex-wrap gap-2 mb-4">
            <SkillBadge name="Python" status="matched" evidenceStrength="Strong" />
            <SkillBadge name="Excel" status="matched" evidenceStrength="Strong" />
            <SkillBadge name="SQL" status="weak_evidence" evidenceStrength="Weak" />
            <SkillBadge name="Statistics" status="weak_evidence" evidenceStrength="Weak" />
            <SkillBadge name="Power BI" status="missing" evidenceStrength="Not Detected" />
            <SkillBadge name="Pandas" status="matched" evidenceStrength="Moderate" />
          </div>

          {/* Ethical Banner */}
          <div className="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-xs text-amber-950 flex items-start gap-2.5">
            <Sparkles className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-amber-900 mb-0.5">Ethical Recommendation:</strong>
              <p className="leading-relaxed text-amber-900/90">
                Never falsely insert skills into your resume. If you genuinely possess Power BI or advanced SQL skills, consider adding a relevant GitHub project, certification, or concrete project description.
              </p>
            </div>
          </div>
        </div>

        {/* Quick Action Hub */}
        <div className="bg-gradient-to-br from-red-50/80 to-red-50/80 rounded-2xl border border-red-100 p-6 flex flex-col justify-between">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-red-600">
              Next Step
            </span>
            <h3 className="text-lg font-bold text-slate-900 mt-1 mb-2">
              Practice AI Mock Interview
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              The AI interviewer has generated 4 dynamic questions referencing your Sales Analysis project and SQL fundamentals.
            </p>

            <div className="p-3 rounded-xl bg-white/90 border border-red-100 text-xs mb-4">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Upcoming Question:</span>
              <p className="text-slate-800 font-medium italic mt-1">
                "You mentioned using Python in your Sales Analysis project. Explain how you used Python for data preprocessing."
              </p>
            </div>
          </div>

          <Link
            to="/interview"
            className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs transition-colors shadow-xs"
          >
            <Mic className="w-4 h-4" />
            <span>Launch Mock Interview Now</span>
          </Link>
        </div>
      </div>
    </div>
  );
};


