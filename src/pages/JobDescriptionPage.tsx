import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { createJobDescription } from '../services/api';
import {
  Briefcase,
  Sparkles,
  Plus,
  X,
  Upload,
  ArrowRight,
  FileText,
} from 'lucide-react';

export const JobDescriptionPage: React.FC = () => {
  const { showToast, setRecruiterJobDescription } = useApp();
  const navigate = useNavigate();

  const [jobTitle, setJobTitle] = useState('Data Analyst');
  const [companyName, setCompanyName] = useState('TalentIQ Client');
  const [department, setDepartment] = useState('Business Intelligence');
  const [minExperience, setMinExperience] = useState('1');
  const [education, setEducation] = useState("Bachelor's in Computer Science, Statistics, Mathematics or related quantitative field");
  const [jdText, setJdText] = useState(
    `We are seeking a Data Analyst to translate complex business metrics into clean reports and interactive dashboards.
Responsibilities:
- Build and maintain reporting pipelines using SQL and Python.
- Create automated visual dashboards in Power BI or Tableau.
- Perform exploratory data analysis over large transactional customer datasets.
- Communicate actionable trends to business stakeholders.`
  );

  const [requiredSkills, setRequiredSkills] = useState<string[]>([
    'Python',
    'SQL',
    'Excel',
    'Power BI',
    'Statistics',
    'Pandas',
  ]);
  const [newReqSkill, setNewReqSkill] = useState('');

  const [preferredSkills, setPreferredSkills] = useState<string[]>([
    'Tableau',
    'Snowflake',
    'dbt',
    'A/B Testing',
  ]);
  const [newPrefSkill, setNewPrefSkill] = useState('');

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const addRequiredSkill = () => {
    if (newReqSkill.trim() && !requiredSkills.includes(newReqSkill.trim())) {
      setRequiredSkills([...requiredSkills, newReqSkill.trim()]);
      setNewReqSkill('');
    }
  };

  const removeRequiredSkill = (skill: string) => {
    setRequiredSkills(requiredSkills.filter((s) => s !== skill));
  };

  const addPreferredSkill = () => {
    if (newPrefSkill.trim() && !preferredSkills.includes(newPrefSkill.trim())) {
      setPreferredSkills([...preferredSkills, newPrefSkill.trim()]);
      setNewPrefSkill('');
    }
  };

  const removePreferredSkill = (skill: string) => {
    setPreferredSkills(preferredSkills.filter((s) => s !== skill));
  };

  const handleAnalyzeJobRequirements = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);

    try {
      setRecruiterJobDescription({ jobTitle, companyName, description: jdText, requiredSkills, minExperience: minExperience, education });
      await createJobDescription({
        title: jobTitle,
        department,
        description: jdText,
        requiredSkills,
        preferredSkills,
        minExperienceYears: Number(minExperience) || 1,
        education,
      });

      showToast('Job requirements structured and parsed successfully!', 'success');
      navigate('/recruiter/candidates');
    } catch {
      showToast('Created job profile. Redirecting to candidate matching...', 'info');
      navigate('/recruiter/candidates');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Job Architecture & Skill Taxonomy</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Job Description & Criteria Definition
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Define core competencies, preferred tools, and minimum requirements to calibrate the explainable AI candidate ranking engine.
        </p>
      </div>

      <form onSubmit={handleAnalyzeJobRequirements} className="space-y-6">
        {/* Core Metadata */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-teal-700" />
            <span>Position Details</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Job Title</label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Data Analyst"
                required
                className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Company Name</label>
              <input type="text" value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="e.g. ABC Technologies" required className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Department</label>
              <input
                type="text"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                placeholder="e.g. Business Intelligence"
                className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Minimum Experience (Years)
              </label>
              <input
                type="number"
                min="0"
                max="20"
                value={minExperience}
                onChange={(e) => setMinExperience(e.target.value)}
                className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Education Requirements
              </label>
              <input
                type="text"
                value={education}
                onChange={(e) => setEducation(e.target.value)}
                placeholder="Degree or certification prerequisites"
                className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
            </div>
          </div>
        </div>

        {/* Job Description Text or File */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <FileText className="w-4 h-4 text-teal-700" />
              <span>Full Job Description Content</span>
            </h3>
            <span className="text-xs text-slate-400">Paste text or upload JD document</span>
          </div>

          <textarea
            rows={6}
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste your raw job description, role objectives, day-to-day responsibilities, and qualifications..."
            className="w-full rounded-xl border border-slate-200 p-4 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600 font-mono leading-relaxed"
          />

          <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-dashed border-slate-300 text-xs">
            <div className="flex items-center gap-2 text-slate-600">
              <Upload className="w-4 h-4 text-slate-400" />
              <span>Have a PDF/Word JD specification?</span>
            </div>
            <button
              type="button"
              onClick={() => showToast('Simulated JD document parser loaded.', 'info')}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 transition-colors"
            >
              Upload JD File
            </button>
          </div>
        </div>

        {/* Required Skills Taxonomy */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                Required Core Skills (Mandatory for High Alignment)
              </label>
              <span className="text-xs text-slate-400">{requiredSkills.length} defined</span>
            </div>
            <div className="flex flex-wrap gap-2 mb-3">
              {requiredSkills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-teal-50 text-teal-900 text-xs font-semibold border border-teal-200"
                >
                  <span>{skill}</span>
                  <button
                    type="button"
                    onClick={() => removeRequiredSkill(skill)}
                    className="hover:text-rose-600"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={newReqSkill}
                onChange={(e) => setNewReqSkill(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addRequiredSkill())}
                placeholder="Add required skill (e.g. SQL, Tableau, Pandas)"
                className="flex-1 rounded-xl border border-slate-200 px-3.5 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
              <button
                type="button"
                onClick={addRequiredSkill}
                className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Preferred Skills */}
          <div className="pt-4 border-t border-slate-100">
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                Preferred Nice-to-Have Skills (Bonus Match)
              </label>
              <span className="text-xs text-slate-400">{preferredSkills.length} defined</span>
            </div>
            <div className="flex flex-wrap gap-2 mb-3">
              {preferredSkills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-100 text-slate-800 text-xs font-semibold border border-slate-200"
                >
                  <span>{skill}</span>
                  <button
                    type="button"
                    onClick={() => removePreferredSkill(skill)}
                    className="hover:text-rose-600"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={newPrefSkill}
                onChange={(e) => setNewPrefSkill(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addPreferredSkill())}
                placeholder="Add bonus skill (e.g. Snowflake, Docker)"
                className="flex-1 rounded-xl border border-slate-200 px-3.5 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              />
              <button
                type="button"
                onClick={addPreferredSkill}
                className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex items-center justify-end">
          <button
            type="submit"
            disabled={isAnalyzing}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-teal-800 hover:bg-teal-900 text-white font-bold text-xs transition-all shadow-md shadow-teal-950/30"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isAnalyzing ? 'Extracting Criteria...' : 'Analyze Job Requirements'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};


