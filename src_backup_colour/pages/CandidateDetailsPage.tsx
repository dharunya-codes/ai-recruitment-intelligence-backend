import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { sampleCandidate, sampleCandidatesPool, sampleEvidenceDetails } from '../data/mockData';
import { StatusBadge } from '../components/StatusBadge';
import { EvidenceCard } from '../components/EvidenceCard';
import {
  ArrowLeft,
  Mail,
  Phone,
  MapPin,
  Bot,
  Briefcase,
  GraduationCap,
  Award,
  FolderGit2,
  FileText,
  Sparkles,
  AlertCircle,
} from 'lucide-react';

export const CandidateDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  // Find candidate in pool or default to Rose Infanta
  const recruiterSummary =
    sampleCandidatesPool.find((c) => c.id === id) || sampleCandidatesPool[0];

  return (
    <div className="space-y-6">
      {/* Back button */}
      <div>
        <Link
          to="/recruiter/candidates"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Candidate Matching</span>
        </Link>
      </div>

      {/* Header Profile Dossier Card */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-slate-100">
          <div className="flex items-start sm:items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-indigo-800 text-white font-extrabold text-2xl flex items-center justify-center shadow-md">
              {recruiterSummary.name
                .split(' ')
                .map((n) => n[0])
                .join('')}
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h1 className="text-2xl font-bold text-slate-900">{recruiterSummary.name}</h1>
                <StatusBadge status={recruiterSummary.status} size="sm" />
                <StatusBadge status={`JD Alignment: ${recruiterSummary.jdAlignment}`} size="sm" />
              </div>

              <p className="text-xs text-slate-500 mt-1 flex flex-wrap items-center gap-3">
                <span className="flex items-center gap-1 font-medium text-slate-700">
                  <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                  Target: {recruiterSummary.targetRole}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <Mail className="w-3.5 h-3.5 text-slate-400" />
                  {recruiterSummary.email}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <Phone className="w-3.5 h-3.5 text-slate-400" />
                  {sampleCandidate.phone}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  {sampleCandidate.location}
                </span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto">
            <div className="p-3 rounded-xl bg-indigo-50 border border-indigo-100 text-center min-w-[100px]">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 block">
                Skill Match
              </span>
              <span className="text-2xl font-black text-indigo-700">
                {recruiterSummary.skillMatchPct}%
              </span>
            </div>
            <div className="p-3 rounded-xl bg-teal-50 border border-teal-100 text-center min-w-[100px]">
              <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 block">
                Evidence
              </span>
              <span className="text-sm font-bold text-teal-800 mt-1 block">
                {recruiterSummary.evidenceStrength}
              </span>
            </div>
          </div>
        </div>

        {/* Explainable Candidate Profile Summary */}
        <div className="mt-6 p-4 rounded-xl bg-indigo-50/50 border border-indigo-100/90 text-xs">
          <div className="flex items-center gap-2 font-bold text-indigo-950 mb-1">
            <Bot className="w-4 h-4 text-indigo-600" />
            <span>Explainable Candidate-Role Analysis:</span>
          </div>
          <p className="text-slate-700 leading-relaxed italic text-xs sm:text-sm">
            "{recruiterSummary.aiProfileSummary}"
          </p>
        </div>

        {/* Missing Requirements Alert */}
        {recruiterSummary.missingRequirements.length > 0 && (
          <div className="mt-4 p-3.5 rounded-xl bg-rose-50/70 border border-rose-200 text-xs text-rose-900 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>
                Missing Requirements for {recruiterSummary.targetRole}:{' '}
                <strong>{recruiterSummary.missingRequirements.join(', ')}</strong>
              </span>
            </div>
            <span className="text-[11px] font-semibold text-rose-700 uppercase tracking-wider">
              Verification Required
            </span>
          </div>
        )}
      </div>

      {/* Grid: Resume Summary & Skills */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Summary, Education & Certs */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-2 flex items-center gap-2">
              <FileText className="w-4 h-4 text-indigo-600" />
              <span>Resume Summary</span>
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {sampleCandidate.summary}
            </p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-indigo-600" />
              <span>Education</span>
            </h3>
            {sampleCandidate.education.map((edu, idx) => (
              <div key={idx} className="text-xs space-y-1">
                <p className="font-bold text-slate-900">{edu.degree}</p>
                <p className="text-slate-600">{edu.institution}</p>
                <div className="flex items-center justify-between text-slate-400 text-[11px]">
                  <span>{edu.year}</span>
                  <span className="text-emerald-700 font-semibold">{edu.grade}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-indigo-600" />
              <span>Certifications</span>
            </h3>
            <div className="space-y-3 text-xs">
              {sampleCandidate.certifications.map((cert, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                  <p className="font-bold text-slate-900">{cert.title}</p>
                  <p className="text-slate-500 text-[11px]">
                    {cert.issuer} • {cert.year}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Center & Right Column: Projects & Evidence Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          {/* Projects with Measurable Outcomes */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
              <FolderGit2 className="w-4 h-4 text-indigo-600" />
              <span>Verified Resume Projects & Technical Depth</span>
            </h3>

            <div className="space-y-4">
              {sampleCandidate.projects.map((proj) => (
                <div
                  key={proj.id}
                  className="p-4 rounded-xl border border-slate-200/80 bg-slate-50/40"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{proj.title}</h4>
                      <span className="text-xs text-slate-500 font-medium">{proj.role}</span>
                    </div>
                    <StatusBadge status={proj.evidenceStrength} size="sm" />
                  </div>

                  <div className="flex flex-wrap gap-1.5 mb-2.5">
                    {proj.technologies.map((tech, i) => (
                      <span
                        key={i}
                        className="px-2 py-0.5 rounded bg-white text-slate-700 text-[11px] font-mono border border-slate-200"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>

                  <p className="text-xs text-slate-600 leading-relaxed mb-3">
                    {proj.description}
                  </p>

                  {proj.measurableOutcome && (
                    <div className="p-2.5 rounded-lg bg-emerald-50 text-emerald-900 text-xs font-medium border border-emerald-100">
                      <strong>Quantified Outcome:</strong> {proj.measurableOutcome}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Deep Evidence Proof for Recruiter */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              <span>Skill Evidence Checklist (Audited by Semantic Engine)</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {sampleEvidenceDetails.slice(0, 4).map((ev) => (
                <EvidenceCard key={ev.skill} evidence={ev} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
