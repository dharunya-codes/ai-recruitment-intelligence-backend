import {
  CandidateProfile,
  ResumeScoreBreakdown,
  SkillGapData,
  EvidenceDetail,
  JobMatchComparison,
  RecruiterCandidate,
  JobVacancy,
  InterviewQuestionItem,
  InterviewFeedbackSummary,
  FullReportData,
} from '../types';

export const sampleCandidate: CandidateProfile = {
  id: 'cand-001',
  name: 'Rose Infanta',
  email: 'rose.infanta@example.com',
  phone: '+1 (555) 349-2810',
  location: 'San Francisco, CA (Open to Remote)',
  targetRole: 'Data Analyst',
  summary:
    'Aspiring Data Analyst with foundational programming background in Python and C, combined with practical skills in Excel spreadsheet modeling. Proven capability in exploratory data analysis and academic project execution through real-world dataset mining.',
  skills: ['Python', 'C', 'Excel', 'Data Cleaning', 'Jupyter Notebooks', 'Git'],
  projects: [
    {
      id: 'proj-1',
      title: 'Sales Analysis',
      role: 'Lead Analyst & Developer',
      technologies: ['Python', 'Pandas', 'Excel', 'Matplotlib'],
      description:
        'Conducted exploratory sales trend analysis over 50,000 retail transaction records. Cleaned irregular customer records, handled missing value imputations, and built monthly revenue trend visual charts.',
      evidenceStrength: 'Strong',
      measurableOutcome: 'Identified top 12% revenue drivers and reduced seasonal reporting prep time by 40%.',
    },
    {
      id: 'proj-2',
      title: 'Student Productivity Tracker',
      role: 'Software & Data Contributor',
      technologies: ['Python', 'C', 'SQLite', 'CSV Parsing'],
      description:
        'Engineered an automated tracking utility recording daily study hours and task completion milestones. Parsed structured logs to evaluate weekly focus distribution.',
      evidenceStrength: 'Moderate',
      measurableOutcome: 'Analyzed study patterns for 120 students with an automated summary export function.',
    },
  ],
  education: [
    {
      degree: 'B.S. in Computer Science & Information Systems',
      institution: 'State University of Technology',
      year: '2021 - 2025',
      grade: '3.82 / 4.0 GPA',
    },
  ],
  certifications: [
    {
      title: 'Google Data Analytics Professional Certificate (In Progress)',
      issuer: 'Coursera / Google',
      year: '2024',
    },
    {
      title: 'Python for Everybody Specialization',
      issuer: 'University of Michigan',
      year: '2023',
    },
  ],
  uploadedResumeName: 'Rose_Infanta_Data_Analyst_Resume.pdf',
  lastAnalyzedAt: '2025-02-28T10:30:00Z',
};

export const sampleResumeScore: ResumeScoreBreakdown = {
  overallScore: 78,
  atsScore: 82,
  atsGrade: 'Good (A-)',
  sections: {
    contactInfo: {
      title: 'Contact Information',
      status: 'Good',
      score: 95,
      shortExplanation: 'Email, phone number, location, and GitHub profile are clearly identifiable and parsed correctly.',
      recommendation: 'Ensure your LinkedIn URL is hyperlinked and uses clean vanity naming.',
    },
    formatting: {
      title: 'Formatting & Layout',
      status: 'Good',
      score: 88,
      shortExplanation: 'Clean single-column structure with distinct headings and standard margins.',
      recommendation: 'Maintain consistent line spacing (1.15x) throughout bullet lists.',
    },
    grammar: {
      title: 'Grammar',
      status: 'Good',
      score: 90,
      shortExplanation: 'Sentence flow and past-tense verb consistency are well maintained.',
      recommendation: 'Check third-person action verbs across older coursework entries.',
    },
    spelling: {
      title: 'Spelling',
      status: 'Good',
      score: 96,
      shortExplanation: 'No typographical errors found in core technical terms or libraries.',
      recommendation: 'Double check tool capitalizations like "Pandas" and "SQLite".',
    },
    datesConsistency: {
      title: 'Dates Consistency',
      status: 'Good',
      score: 85,
      shortExplanation: 'Standard Month Year (e.g., Aug 2023 - Dec 2023) format is maintained across project timelines.',
      recommendation: 'Ensure both education and projects list dates aligned to the right margin.',
    },
    projectDescription: {
      title: 'Project Description',
      status: 'Needs Improvement',
      score: 64,
      shortExplanation: 'Descriptions focus heavily on task responsibilities rather than quantitative business impact.',
      recommendation: 'Add measurable results and technologies used (e.g., dataset size, compute latency reduction, percentage gains).',
    },
    achievementStatements: {
      title: 'Achievement Statements',
      status: 'Needs Improvement',
      score: 60,
      shortExplanation: 'Only one project features explicit metrics (e.g. 40% reduction). Most bullets remain descriptive.',
      recommendation: 'Adopt the Google X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z].',
    },
    atsCompatibility: {
      title: 'ATS Compatibility',
      status: 'Good',
      score: 82,
      shortExplanation: 'Standard text layers parsed without non-standard glyphs, graphics, or nested text boxes.',
      recommendation: 'Replace icon bullets with standard unicode circle bullets for older enterprise ATS parsers.',
    },
  },
};

export const sampleSkillGap: SkillGapData = {
  targetRole: 'Data Analyst',
  requiredSkills: ['Python', 'SQL', 'Excel', 'Power BI', 'Statistics', 'Pandas'],
  matchedSkills: [
    {
      name: 'Python',
      status: 'matched',
      evidenceStrength: 'Strong',
      detectedIn: ['Skills Section', 'Sales Analysis Project', 'Student Productivity Tracker'],
      recommendation: 'Demonstrated in multiple practical code implementations.',
    },
    {
      name: 'Excel',
      status: 'matched',
      evidenceStrength: 'Strong',
      detectedIn: ['Skills Section', 'Sales Analysis Project'],
      recommendation: 'Solid evidence with formula usage and trend modeling.',
    },
  ],
  weakEvidenceSkills: [
    {
      name: 'SQL',
      status: 'weak_evidence',
      evidenceStrength: 'Weak',
      detectedIn: ['Skills Section'],
      recommendation:
        'If you genuinely possess this skill, consider adding relevant project, certification, education or experience evidence.',
    },
    {
      name: 'Statistics',
      status: 'weak_evidence',
      evidenceStrength: 'Weak',
      detectedIn: ['Coursework mention'],
      recommendation:
        'If you genuinely possess this skill, consider adding relevant project, certification, education or experience evidence.',
    },
  ],
  missingSkills: [
    {
      name: 'Power BI',
      status: 'missing',
      evidenceStrength: 'Not Detected',
      detectedIn: [],
      recommendation:
        'If you genuinely possess this skill, consider adding relevant project, certification, education or experience evidence.',
    },
    {
      name: 'Pandas',
      status: 'missing',
      evidenceStrength: 'Weak',
      detectedIn: ['Sales Analysis body text only'],
      recommendation:
        'Highlight Pandas explicitly in your primary skills matrix and describe DataFrame manipulations performed.',
    },
  ],
  ethicalGuidance:
    'Important: Never fabricate skills or experience on your resume. If you genuinely possess a missing skill, document it with concrete project artifacts, GitHub links, or verified credentials.',
};

export const sampleEvidenceDetails: EvidenceDetail[] = [
  {
    skill: 'Python',
    status: 'Found',
    evidenceLocations: ['Skills Section (Line 14)', 'Sales Analysis Project (Line 22)', 'Student Productivity Tracker (Line 31)'],
    projectsReferenced: ['Sales Analysis', 'Student Productivity Tracker'],
    strength: 'Strong',
    confidence: 96,
    snippets: [
      '"Skills: Python, C, Excel, Data Cleaning, Jupyter Notebooks"',
      '"Conducted exploratory sales trend analysis using Python and Pandas over 50,000 retail transaction records"',
      '"Engineered an automated tracking utility in Python recording daily study hours"',
    ],
  },
  {
    skill: 'SQL',
    status: 'Found',
    evidenceLocations: ['Skills Section only (Line 15)'],
    projectsReferenced: [],
    strength: 'Weak',
    confidence: 58,
    snippets: [
      '"Skills: Python, C, Excel, SQL (basic)"',
      'No queries, joins, schema designs, or database integrations detailed in project bullet points.',
    ],
  },
  {
    skill: 'Excel',
    status: 'Found',
    evidenceLocations: ['Skills Section (Line 15)', 'Sales Analysis Project (Line 24)'],
    projectsReferenced: ['Sales Analysis'],
    strength: 'Strong',
    confidence: 91,
    snippets: [
      '"Skills: ... Excel, Data Cleaning"',
      '"Built spreadsheet models and monthly revenue trend charts in Excel for stakeholder briefing"',
    ],
  },
  {
    skill: 'Power BI',
    status: 'Not Detected',
    evidenceLocations: [],
    projectsReferenced: [],
    strength: 'Not Detected',
    confidence: 0,
    snippets: ['No keyword occurrences or dashboard screenshots detected in resume text.'],
  },
  {
    skill: 'Statistics',
    status: 'Found',
    evidenceLocations: ['Education / Coursework (Line 42)'],
    projectsReferenced: [],
    strength: 'Weak',
    confidence: 52,
    snippets: ['"Relevant Coursework: Probability and Statistical Methods, Discrete Math"'],
  },
  {
    skill: 'Pandas',
    status: 'Found',
    evidenceLocations: ['Sales Analysis Description (Line 23)'],
    projectsReferenced: ['Sales Analysis'],
    strength: 'Moderate',
    confidence: 74,
    snippets: ['"...cleaned customer records and imputed missing values using Pandas DataFrame transforms"'],
  },
];

export const sampleJobMatch: JobMatchComparison = {
  targetRole: 'Data Analyst',
  jobTitle: 'Junior to Mid-Level Data Analyst',
  matchPercentage: 68,
  skillMatrix: [
    { skill: 'Python', status: 'Matched', evidence: 'Strong', notes: 'Demonstrated across multiple projects and scripts.' },
    { skill: 'SQL', status: 'Partial', evidence: 'Weak', notes: 'Listed as skill without project query evidence.' },
    { skill: 'Excel', status: 'Matched', evidence: 'Strong', notes: 'Formulas and monthly reporting charts evidenced.' },
    { skill: 'Power BI', status: 'Missing', evidence: 'None', notes: 'Not detected. Crucial for client dashboarding.' },
    { skill: 'Statistics', status: 'Partial', evidence: 'Moderate', notes: 'Present in coursework but lacking applied A/B test context.' },
    { skill: 'Pandas', status: 'Matched', evidence: 'Moderate', notes: 'Found in Sales Analysis data preprocessing context.' },
  ],
  relevantProjects: [
    {
      title: 'Sales Analysis',
      techUsed: ['Python', 'Pandas', 'Excel'],
      relevanceScore: 92,
      description: 'High relevance: Real business dataset exploring revenue trends and customer behavior.',
      impact: 'Demonstrates data cleaning, exploratory data analysis (EDA), and reporting.',
    },
    {
      title: 'Student Productivity Tracker',
      techUsed: ['Python', 'C', 'SQLite'],
      relevanceScore: 74,
      description: 'Moderate relevance: Demonstrates algorithmic logic, structured data handling, and logging.',
      impact: 'Shows ability to write clean automated processing scripts.',
    },
  ],
  missingRequirements: [
    'Hands-on dashboard development in Power BI or Tableau',
    'Complex multi-table SQL queries (window functions, CTEs, aggregation joins)',
    'Formal business stakeholder presentation experience',
  ],
  weakAreas: [
    'SQL depth: Only listed in technical skills block; no database schemas or queries referenced.',
    'Quantified metrics: Only 1 bullet features a specific quantitative metric.',
  ],
  recommendations: [
    'Build and publish a sample interactive Power BI or Tableau dashboard on GitHub/NovyPro.',
    'If you genuinely have SQL experience, detail a project where you wrote GROUP BY, subqueries, or window functions.',
    'Enhance bullet points with the format: "Achieved [X] by applying [tool/method] resulting in [Y% improvement]."',
  ],
};

export const sampleCandidatesPool: RecruiterCandidate[] = [
  {
    id: 'cand-001',
    name: 'Rose Infanta',
    email: 'rose.infanta@example.com',
    targetRole: 'Data Analyst',
    experienceYears: 1,
    skillMatchPct: 68,
    experienceMatchPct: 70,
    projectRelevancePct: 84,
    evidenceStrength: 'Moderate',
    jdAlignment: 'Medium',
    missingRequirements: ['Power BI', 'Complex SQL Joins'],
    aiProfileSummary:
      'The candidate has experience with Python and Excel and completed two data-related projects. SQL is mentioned but has limited project evidence. Power BI was not detected.',
    status: 'Under Review',
    resumeFileName: 'Rose_Infanta_Data_Analyst.pdf',
    analyzedDate: '2025-02-28',
  },
  {
    id: 'cand-002',
    name: 'Marcus Vance',
    email: 'marcus.vance@example.com',
    targetRole: 'Data Analyst',
    experienceYears: 3,
    skillMatchPct: 92,
    experienceMatchPct: 90,
    projectRelevancePct: 95,
    evidenceStrength: 'Strong',
    jdAlignment: 'High',
    missingRequirements: [],
    aiProfileSummary:
      'Strong candidate with 3 years applied experience in PostgreSQL, Tableau, and automated Python ETL pipelines. All core JD requirements are supported by verified project outcomes.',
    status: 'Shortlisted',
    resumeFileName: 'Marcus_Vance_Senior_Analyst.pdf',
    analyzedDate: '2025-02-27',
  },
  {
    id: 'cand-003',
    name: 'Priya Sharma',
    email: 'priya.sharma@example.com',
    targetRole: 'Data Analyst',
    experienceYears: 2,
    skillMatchPct: 78,
    experienceMatchPct: 75,
    projectRelevancePct: 80,
    evidenceStrength: 'Moderate',
    jdAlignment: 'High',
    missingRequirements: ['Advanced Statistics'],
    aiProfileSummary:
      'Candidate showcases solid SQL database querying and Power BI visual dashboards across financial datasets. Statistical modeling evidence is limited to introductory regression.',
    status: 'Interview Scheduled',
    resumeFileName: 'Priya_Sharma_Analytics.pdf',
    analyzedDate: '2025-02-26',
  },
  {
    id: 'cand-004',
    name: 'Devansh Gupta',
    email: 'devansh.g@example.com',
    targetRole: 'Frontend Developer',
    experienceYears: 2,
    skillMatchPct: 85,
    experienceMatchPct: 80,
    projectRelevancePct: 88,
    evidenceStrength: 'Strong',
    jdAlignment: 'High',
    missingRequirements: ['Next.js App Router'],
    aiProfileSummary:
      'Well-versed in React 19, TypeScript, and Tailwind. Built three production SPAs. Demonstrates deep understanding of state management and web performance.',
    status: 'Under Review',
    resumeFileName: 'Devansh_Gupta_Frontend.pdf',
    analyzedDate: '2025-02-25',
  },
  {
    id: 'cand-005',
    name: 'Elena Rostova',
    email: 'elena.rostova@example.com',
    targetRole: 'Machine Learning Engineer',
    experienceYears: 4,
    skillMatchPct: 89,
    experienceMatchPct: 92,
    projectRelevancePct: 90,
    evidenceStrength: 'Strong',
    jdAlignment: 'High',
    missingRequirements: ['Kubernetes / Kubeflow'],
    aiProfileSummary:
      'Comprehensive PyTorch and Scikit-Learn background with end-to-end model serving in FastAPI and AWS Lambda. Strong mathematical foundations.',
    status: 'Shortlisted',
    resumeFileName: 'Elena_Rostova_ML_Engineer.pdf',
    analyzedDate: '2025-02-24',
  },
];

export const sampleJobVacancies: JobVacancy[] = [
  {
    id: 'job-101',
    title: 'Data Analyst',
    department: 'Business Intelligence',
    location: 'Remote / New York',
    type: 'Full-time',
    description:
      'We are looking for a Data Analyst to transform complex transactional data into actionable commercial insights. You will collaborate with product and growth teams to design dashboards and track key growth indicators.',
    requiredSkills: ['Python', 'SQL', 'Excel', 'Power BI', 'Statistics', 'Pandas'],
    preferredSkills: ['Tableau', 'dbt', 'Snowflake', 'A/B Testing'],
    minExperienceYears: 1,
    education: "Bachelor's in Computer Science, Statistics, Mathematics, or related field",
    applicantCount: 28,
    avgMatchScore: 74,
    createdAt: '2025-02-15',
  },
  {
    id: 'job-102',
    title: 'Senior Data Engineer',
    department: 'Data Infrastructure',
    location: 'San Francisco, CA',
    type: 'Full-time',
    description:
      'Build robust data ingestion pipelines handling real-time clickstream events. Architect lakehouse data pipelines using Apache Spark and Airflow.',
    requiredSkills: ['Python', 'SQL', 'Spark', 'Kafka', 'Airflow', 'AWS'],
    preferredSkills: ['Rust', 'Terraform', 'Databricks'],
    minExperienceYears: 4,
    education: "Bachelor's or Master's in Computer Science",
    applicantCount: 14,
    avgMatchScore: 81,
    createdAt: '2025-02-10',
  },
  {
    id: 'job-103',
    title: 'Product Growth Analyst',
    department: 'Product Growth',
    location: 'Remote',
    type: 'Full-time',
    description:
      'Design product retention cohorts, user onboarding funnel analysis, and experiment attribution models.',
    requiredSkills: ['SQL', 'Mixpanel', 'Python', 'Excel', 'Experimentation'],
    preferredSkills: ['Amplitude', 'Looker', 'R'],
    minExperienceYears: 2,
    education: 'Degree in quantitative field',
    applicantCount: 19,
    avgMatchScore: 69,
    createdAt: '2025-02-20',
  },
];

export const sampleInterviewQuestions: InterviewQuestionItem[] = [
  {
    id: 'iq-1',
    number: 1,
    question:
      'You mentioned using Python in your Sales Analysis project. Explain how you used Python for data preprocessing.',
    context:
      'The interviewer wants to evaluate your understanding of real-world messy data handling, data types, missing records, and transformation routines.',
    expectedDurationSeconds: 180,
    targetRole: 'Data Analyst',
    skillTested: 'Python & Data Preprocessing',
    projectReferenced: 'Sales Analysis Project',
  },
  {
    id: 'iq-2',
    number: 2,
    question:
      'In your resume, SQL is listed in your skills section. Can you describe how you would write a query to find the top 3 highest spending customers per region?',
    context:
      'Assesses practical relational querying ability, specifically window functions like DENSE_RANK() or ROW_NUMBER() vs simple group by.',
    expectedDurationSeconds: 180,
    targetRole: 'Data Analyst',
    skillTested: 'SQL & Window Functions',
  },
  {
    id: 'iq-3',
    number: 3,
    question:
      'When presenting your monthly revenue charts from Excel, how did you handle outliers or anomalous spikes in transaction totals?',
    context:
      'Evaluates analytical rigor, business domain curiosity, and how you communicate edge cases to non-technical stakeholders.',
    expectedDurationSeconds: 180,
    targetRole: 'Data Analyst',
    skillTested: 'Excel & Data Storytelling',
    projectReferenced: 'Sales Analysis Project',
  },
  {
    id: 'iq-4',
    number: 4,
    question:
      'The target job requires Power BI dashboards, which was not explicitly detailed on your resume. How would you quickly ramp up and translate your Excel data models into DAX and Power BI reports?',
    context:
      'Measures learning agility, proactive upskilling, and understanding of core business intelligence architectures.',
    expectedDurationSeconds: 180,
    targetRole: 'Data Analyst',
    skillTested: 'Power BI & Tool Adaptability',
  },
];

export const sampleInterviewFeedback: InterviewFeedbackSummary = {
  overallScore: 81,
  candidateName: 'Rose Infanta',
  targetRole: 'Data Analyst',
  completedAt: '2025-02-28T11:45:00Z',
  categories: {
    technicalKnowledge: 78,
    communication: 86,
    relevance: 84,
    completeness: 75,
    confidence: 82,
    problemSolving: 80,
  },
  evaluations: [
    {
      questionId: 'iq-1',
      questionNumber: 1,
      question:
        'You mentioned using Python in your Sales Analysis project. Explain how you used Python for data preprocessing.',
      candidateAnswer:
        'In the Sales Analysis project, I imported the raw CSV records into Pandas DataFrames. First I checked for null values using isna().sum() and dropped duplicates. Then I converted the date string column into proper datetime objects and filled missing regional sales with median values.',
      technicalUnderstanding: 'Good',
      explanation:
        'The candidate understood the concept but could provide a more specific example regarding why median imputation was chosen over mean or domain-specific logic.',
      expectedConcepts: ['Missing value analysis', 'Imputation strategy', 'Domain context', 'Type conversion'],
      improvementSuggestion:
        'Explain the trade-offs: "I selected median imputation because the transaction amounts had extreme outliers which would skew the mean calculation."',
    },
    {
      questionId: 'iq-2',
      questionNumber: 2,
      question:
        'In your resume, SQL is listed in your skills section. Can you describe how you would write a query to find the top 3 highest spending customers per region?',
      candidateAnswer:
        'I would select customer id, region, sum of amount, then group by region and customer. To get top 3 per region, I would use a window function like DENSE_RANK() OVER (PARTITION BY region ORDER BY sum_spent DESC) in a CTE, and then filter where rank <= 3.',
      technicalUnderstanding: 'Excellent',
      explanation:
        'Strong technical demonstration! The candidate correctly identified the need for a window function and partitioning rather than a naive LIMIT clause.',
      expectedConcepts: ['Window function (ROW_NUMBER / DENSE_RANK)', 'PARTITION BY', 'CTE / Subquery', 'GROUP BY aggregation'],
      improvementSuggestion:
        'Mention potential tie-breaking criteria in business situations (e.g. order by customer tenure if total spending is identical).',
    },
    {
      questionId: 'iq-3',
      questionNumber: 3,
      question:
        'When presenting your monthly revenue charts from Excel, how did you handle outliers or anomalous spikes in transaction totals?',
      candidateAnswer:
        'I investigated the spikes to verify if they were holiday sales promotions like Black Friday or logging errors. When reporting, I separated the promotional spikes into a breakout callout note so the baseline monthly growth wasn’t distorted.',
      technicalUnderstanding: 'Good',
      explanation:
        'Good business sense shown. Distinguishing between genuine business events and data anomalies is essential for stakeholder trust.',
      expectedConcepts: ['Outlier detection criteria', 'Root cause verification', 'Clear communication of anomalies'],
      improvementSuggestion:
        'Reference a specific statistical cutoff (e.g. 1.5x IQR or 3 standard deviations) before qualitative inspection.',
    },
    {
      questionId: 'iq-4',
      questionNumber: 4,
      question:
        'The target job requires Power BI dashboards, which was not explicitly detailed on your resume. How would you quickly ramp up and translate your Excel data models into DAX and Power BI reports?',
      candidateAnswer:
        'Since Power BI shares the Power Query engine and Power Pivot data modeling concepts from Excel, I can transfer my table relationship knowledge immediately. I have already started Microsoft Learn modules covering DAX measures (CALCULATE, RELATED) and Star Schema star modeling.',
      technicalUnderstanding: 'Good',
      explanation:
        'Proactive response addressing the skill gap honestly without false inflation, citing concrete bridge concepts (Power Query & DAX).',
      expectedConcepts: ['Star schema modeling', 'DAX vs Excel formulas', 'Proactive learning path'],
      improvementSuggestion:
        'Publish a small project dashboard on Power BI service or desktop and link the pbix file on your GitHub repository.',
    },
  ],
  executiveSummary:
    'Rose demonstrates solid foundational comprehension in Python and Excel analytics with strong verbal clarity and an honest, growth-oriented mindset. Demonstrating hands-on SQL query patterns and building a tangible Power BI showcase will make her an outstanding hire.',
  keyStrengths: [
    'Clear structured articulation using real project references',
    'Accurate grasp of window functions (PARTITION BY) in SQL',
    'Constructive attitude toward bridging verified skill gaps',
  ],
  actionableNextSteps: [
    'Publish a public Power BI dashboard linking to the Sales Analysis dataset',
    'Quantify outcomes on all resume bullet points with concrete percentages',
    'Incorporate statistical outlier tests (IQR, Z-score) into upcoming mock interviews',
  ],
};

export const sampleFullReport: FullReportData = {
  candidate: sampleCandidate,
  resumeScore: sampleResumeScore,
  skillGap: sampleSkillGap,
  evidence: sampleEvidenceDetails,
  jobMatch: sampleJobMatch,
  interviewFeedback: sampleInterviewFeedback,
  generatedDate: '2025-02-28',
  readinessLevel: 'Moderate',
};
