import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { RoleType } from '../types';
import { ArrowRight, Briefcase, Lock, Mail, UserCheck } from 'lucide-react';
import { isValidEmail, isValidIndianPhone, isValidName, isValidNumber, isValidYear } from '../utils/validators';

interface RoleSignInPageProps {
  role: RoleType;
}

type FormValues = Record<string, string>;
type FormField = { key: string; label: string; type: string };

const candidateFields: FormField[] = [
  { key: 'fullName', label: 'Full Name', type: 'text' },
  { key: 'email', label: 'Email Address', type: 'email' },
  { key: 'password', label: 'Password', type: 'password' },
  { key: 'confirmPassword', label: 'Confirm Password', type: 'password' },
  { key: 'phone', label: 'Phone Number', type: 'tel' },
  { key: 'collegeUniversity', label: 'College / University', type: 'text' },
  { key: 'degree', label: 'Degree', type: 'text' },
  { key: 'department', label: 'Department / Specialization', type: 'text' },
  { key: 'graduationYear', label: 'Graduation Year', type: 'text' },
  { key: 'targetRole', label: 'Target Job Role', type: 'text' },
  { key: 'yearsOfExperience', label: 'Years of Experience', type: 'text' },
  { key: 'skills', label: 'Key Skills', type: 'text' },
];

const recruiterFields: FormField[] = [
  { key: 'fullName', label: 'Full Name', type: 'text' },
  { key: 'workEmail', label: 'Work Email', type: 'email' },
  { key: 'password', label: 'Password', type: 'password' },
  { key: 'confirmPassword', label: 'Confirm Password', type: 'password' },
  { key: 'companyName', label: 'Company Name', type: 'text' },
  { key: 'companyEmail', label: 'Company Email', type: 'email' },
  { key: 'jobTitle', label: 'Job Title / Recruiter Role', type: 'text' },
  { key: 'companyLocation', label: 'Company Location', type: 'text' },
  { key: 'industry', label: 'Industry', type: 'text' },
  { key: 'yearsOfExperience', label: 'Years of Recruiting Experience', type: 'text' },
];

const initialValues = (fields: FormField[]): FormValues =>
  Object.fromEntries(fields.map(({ key }) => [key, '']));

export const RoleSignInPage: React.FC<RoleSignInPageProps> = ({ role }) => {
  const { setCandidate, setRecruiter, login, showToast } = useApp();
  const navigate = useNavigate();
  const fields = role === 'candidate' ? candidateFields : recruiterFields;
  const signInFields = fields.slice(0, 4);
  const profileFields = fields.slice(4);
  const [values, setValues] = useState<FormValues>(() => initialValues(fields));
  const [step, setStep] = useState<'signin' | 'profile'>('signin');
  const [error, setError] = useState<string | null>(null);

  const isCandidate = role === 'candidate';
  const title = isCandidate ? 'Candidate Sign In' : 'Recruiter Sign In';
  const subtitle = isCandidate
    ? 'Sign in to access your personalized career intelligence dashboard.'
    : 'Sign in to access your talent acquisition dashboard.';

  const handleChange = (key: string, value: string) => {
    setValues((current) => ({ ...current, [key]: value }));
    setError(null);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const currentFields = step === 'signin' ? signInFields : profileFields;
    const missingField = currentFields.find(({ key }) =>
      key !== 'phone' && !values[key].trim()
    );
    if (missingField) {
      setError(`Please enter your ${missingField.label.toLowerCase()}.`);
      return;
    }

    if (step === 'signin') {
      const email = isCandidate ? values.email : values.workEmail;
      if (!isValidEmail(email)) {
        setError('Please enter a valid email address.');
        return;
      }

      if (values.password.length < 8) {
        setError('Password must be at least 8 characters long.');
        return;
      }

      if (values.password !== values.confirmPassword) {
        setError('Passwords do not match.');
        return;
      }

      setStep('profile');
      setError(null);
      return;
    }

    if (!isValidName(values.fullName)) {
      setError('Please enter a valid name.');
      return;
    }
    if (isCandidate && values.phone.trim() && !isValidIndianPhone(values.phone)) {
      setError('Please enter a valid 10-digit phone number.');
      return;
    }
    if (isCandidate && !isValidYear(values.graduationYear)) {
      setError('Please enter a valid graduation year.');
      return;
    }
    if (!isCandidate && !isValidEmail(values.companyEmail)) {
      setError('Please enter a valid email address.');
      return;
    }
    if (!isValidNumber(values.yearsOfExperience)) {
      setError('Please enter a valid number.');
      return;
    }

    if (isCandidate) {
      setCandidate((current) => ({
        ...current,
        name: values.fullName,
        email: values.email,
        phone: values.phone,
        collegeUniversity: values.collegeUniversity,
        degree: values.degree,
        department: values.department,
        graduationYear: values.graduationYear,
        targetRole: values.targetRole,
        yearsOfExperience: values.yearsOfExperience,
        skills: values.skills.split(',').map((skill) => skill.trim()).filter(Boolean),
      }));
      login(values.email, 'candidate');
      showToast('Candidate profile saved.', 'success');
      navigate('/candidate/dashboard');
      return;
    }

    setRecruiter({
      fullName: values.fullName,
      workEmail: values.workEmail,
      companyName: values.companyName,
      companyEmail: values.companyEmail,
      jobTitle: values.jobTitle,
      companyLocation: values.companyLocation,
      industry: values.industry,
      yearsOfExperience: values.yearsOfExperience,
    });
    login(values.workEmail, 'recruiter');
    showToast('Recruiter profile saved.', 'success');
    navigate('/recruiter/dashboard');
  };

  return (
    <div className="min-h-[85vh] bg-[#0B0B0F] px-4 py-10 sm:py-14">
      <div className="mx-auto max-w-2xl rounded-2xl border border-[#27272A] bg-[#17171D] p-6 shadow-md sm:p-8">
        <div className="mb-7 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-[#E50914] text-white">
            {isCandidate ? <UserCheck className="h-6 w-6" /> : <Briefcase className="h-6 w-6" />}
          </div>
          <h1 className="text-2xl font-bold text-[#F5F5F5]">{title}</h1>
          <p className="mx-auto mt-2 max-w-lg text-xs leading-relaxed text-[#A1A1AA]">{subtitle}</p>
          <span className="mt-3 inline-flex rounded-full border border-[#7F1D1D] bg-[#3B0A0D] px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#FCA5A5]">
            {step === 'signin' ? title : isCandidate ? 'Candidate Details / Profile' : 'Recruiter Details / Profile'}
          </span>
        </div>

        {error && (
          <div className="mb-5 rounded-lg border border-[#7F1D1D] bg-[#3B0A0D] p-3 text-xs text-[#FCA5A5]" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {(step === 'signin' ? signInFields : profileFields).map(({ key, label, type }) => (
            <div key={key} className={key === 'skills' || key === 'department' ? 'sm:col-span-2' : ''}>
              <label htmlFor={key} className="mb-1 block text-xs font-bold text-[#F5F5F5]">
                {label}
              </label>
              <div className="relative">
                {type === 'email' && <Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#A1A1AA]" />}
                {type === 'password' && <Lock className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#A1A1AA]" />}
                <input
                  id={key}
                  type={type}
                  value={values[key]}
                  onChange={(event) => handleChange(key, event.target.value)}
                  placeholder={key === 'skills' ? 'Python, SQL, Excel' : label}
                  className={`w-full rounded-xl border border-[#27272A] bg-[#111116] py-2.5 pr-3.5 text-xs text-[#F5F5F5] placeholder:text-[#71717A] focus:border-[#E50914] focus:outline-none focus:ring-2 focus:ring-red-500/20 ${type === 'email' || type === 'password' ? 'pl-10' : 'pl-3.5'}`}
                />
              </div>
            </div>
          ))}

          <button type="submit" className="mt-2 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#E50914] px-5 py-3 text-xs font-bold text-white transition-colors hover:bg-[#FF1F2D] sm:col-span-2">
            <span>
              {step === 'signin'
                ? isCandidate ? 'Continue as Candidate' : 'Continue as Recruiter'
                : isCandidate ? 'Continue to Candidate Dashboard' : 'Continue to Recruiter Dashboard'}
            </span>
            <ArrowRight className="h-4 w-4" />
          </button>

          {step === 'profile' && (
            <button
              type="button"
              onClick={() => { setStep('signin'); setError(null); }}
              className="text-xs font-semibold text-[#A1A1AA] hover:text-[#F5F5F5] sm:col-span-2"
            >
              Back to Sign In
            </button>
          )}
        </form>
      </div>
    </div>
  );
};
