import {
  CandidateProfile,
  ResumeScoreBreakdown,
  SkillGapData,
  EvidenceDetail,
  JobMatchComparison,
  RecruiterCandidate,
  JobVacancy,
  InterviewQuestionItem,
  SkillQuizQuestion,
  InterviewFeedbackSummary,
  FullReportData,
  BulkResumeCandidate,
} from '../types';

export interface PublicResumeIssue {
  category: string;
  severity: 'Good' | 'Needs Review' | 'Important';
  issue: string;
  suggestion: string;
}

export const publicResumeIssues: PublicResumeIssue[] = [
  {
    category: 'Contact Information',
    severity: 'Needs Review',
    issue: 'Phone number or email format needs improvement.',
    suggestion: 'Use a professional email address and include a complete phone number with a consistent format.',
  },
  {
    category: 'Resume Formatting',
    severity: 'Needs Review',
    issue: 'Some sections use inconsistent spacing and formatting.',
    suggestion: 'Use consistent heading styles, margins, spacing, and date formats throughout the document.',
  },
  {
    category: 'Grammar & Spelling',
    severity: 'Needs Review',
    issue: 'Some sentences contain grammar or spelling issues.',
    suggestion: 'Proofread bullet points and keep action verbs and verb tense consistent.',
  },
  {
    category: 'Skills Section',
    severity: 'Important',
    issue: 'Skills are listed without enough supporting project or experience evidence.',
    suggestion: 'Connect each important skill to a genuine project, experience, certification, or measurable outcome.',
  },
  {
    category: 'Project Description',
    severity: 'Important',
    issue: 'Project descriptions are too general.',
    suggestion: 'Add your contribution, tools used, dataset or project scale, and measurable outcomes.',
  },
  {
    category: 'Achievements',
    severity: 'Needs Review',
    issue: 'Achievements are not clearly quantified.',
    suggestion: 'Use numbers, percentages, time saved, volume handled, or other truthful measurable results.',
  },
  {
    category: 'ATS Compatibility',
    severity: 'Needs Review',
    issue: 'Some formatting elements may reduce ATS readability.',
    suggestion: 'Prefer standard headings, readable fonts, simple layouts, and text-based contact details.',
  },
  {
    category: 'Resume Length',
    severity: 'Good',
    issue: 'The resume length is within a reasonable range for an early-career candidate.',
    suggestion: 'Keep the strongest and most relevant evidence while removing repetitive content.',
  },
];

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

const powerBiQuestions: InterviewQuestionItem[] = [
  {
    id: 'iq-1', number: 1, skill: 'Power BI',
    question: 'Which feature in Power BI is primarily used to transform and clean data?',
    options: ['A. Power Query', 'B. PowerPoint', 'C. Task Manager', 'D. Notepad'],
    correctAnswer: 'A. Power Query', explanation: 'Power Query provides the data transformation and cleaning tools used before analysis.',
    context: 'Assesses a core Power BI data-preparation concept.', expectedDurationSeconds: 120, targetRole: 'Data Analyst', skillTested: 'Power BI',
  },
  {
    id: 'iq-2', number: 2, skill: 'Power BI',
    question: 'Which language is commonly used in Power BI for creating measures?',
    options: ['A. HTML', 'B. DAX', 'C. CSS', 'D. Java'],
    correctAnswer: 'B. DAX', explanation: 'DAX is used to create measures and calculated columns in Power BI models.',
    context: 'Assesses Power BI model and measure fundamentals.', expectedDurationSeconds: 120, targetRole: 'Data Analyst', skillTested: 'Power BI',
  },
  {
    id: 'iq-3', number: 3, skill: 'Power BI',
    question: 'Which visual is most suitable for showing sales trends over time?',
    options: ['A. Line chart', 'B. Pie chart only', 'C. Text box', 'D. Card only'],
    correctAnswer: 'A. Line chart', explanation: 'A line chart clearly shows movement and patterns across an ordered time axis.',
    context: 'Assesses practical Power BI visualization choices.', expectedDurationSeconds: 120, targetRole: 'Data Analyst', skillTested: 'Power BI',
  },
  {
    id: 'iq-4', number: 4, skill: 'Power BI',
    question: 'What is the main purpose of a Power BI dashboard?',
    options: ['A. To write operating system code', 'B. To visualize and monitor important data insights', 'C. To edit videos', 'D. To manage computer files'],
    correctAnswer: 'B. To visualize and monitor important data insights', explanation: 'Dashboards bring important metrics and visual insights together for monitoring and decisions.',
    context: 'Assesses the purpose of business intelligence dashboards.', expectedDurationSeconds: 120, targetRole: 'Data Analyst', skillTested: 'Power BI',
  },
];

const makeSkillQuestion = (
  skill: string,
  question: string,
  options: string[],
  correctAnswer: string,
  explanation: string
): Omit<InterviewQuestionItem, 'id' | 'number'> => ({
  skill,
  question,
  options,
  correctAnswer,
  explanation,
  context: `Assesses foundational ${skill} knowledge identified in the candidate's skill-gap analysis.`,
  expectedDurationSeconds: 120,
  targetRole: 'Data Analyst',
  skillTested: skill,
});

const skillQuestionBank: Record<string, Omit<InterviewQuestionItem, 'id' | 'number'>[]> = {
  'Power BI': powerBiQuestions,
  SQL: [
    makeSkillQuestion('SQL', 'Which SQL clause filters grouped results after aggregation?', ['A. WHERE', 'B. HAVING', 'C. ORDER BY', 'D. DISTINCT'], 'B. HAVING', 'HAVING filters groups after aggregate functions have been applied.'),
    makeSkillQuestion('SQL', 'Which SQL operation combines rows from related tables?', ['A. JOIN', 'B. LOOP', 'C. RENDER', 'D. STYLE'], 'A. JOIN', 'A JOIN combines related rows from two or more tables.'),
    makeSkillQuestion('SQL', 'Which function counts rows in a SQL result?', ['A. COUNT', 'B. TOTAL_ROWS', 'C. NUMBER', 'D. SIZE_ROWS'], 'A. COUNT', 'COUNT returns the number of rows or non-null values, depending on its expression.'),
    makeSkillQuestion('SQL', 'Which keyword sorts SQL query results?', ['A. GROUP', 'B. SORT', 'C. ORDER BY', 'D. ARRANGE'], 'C. ORDER BY', 'ORDER BY sorts the returned rows by one or more columns.'),
  ],
  Statistics: [
    makeSkillQuestion('Statistics', 'Which statistic represents the middle value in an ordered dataset?', ['A. Mean', 'B. Mode', 'C. Median', 'D. Range'], 'C. Median', 'The median is the central value after observations are sorted.'),
    makeSkillQuestion('Statistics', 'What does standard deviation describe?', ['A. Data spread', 'B. Column name length', 'C. Number of tables', 'D. File size'], 'A. Data spread', 'Standard deviation describes how far observations tend to vary from the mean.'),
    makeSkillQuestion('Statistics', 'What is the mean of 2, 4, and 6?', ['A. 2', 'B. 3', 'C. 4', 'D. 6'], 'C. 4', 'The mean is the sum of the values divided by their count: (2 + 4 + 6) / 3 = 4.'),
    makeSkillQuestion('Statistics', 'What is an outlier?', ['A. A typical value', 'B. An unusually distant observation', 'C. A missing column', 'D. A duplicate chart'], 'B. An unusually distant observation', 'An outlier is an observation that differs substantially from the rest of the data.'),
  ],
  Pandas: [
    makeSkillQuestion('Pandas', 'Which Pandas structure stores tabular data?', ['A. DataFrame', 'B. TensorBoard', 'C. Canvas', 'D. Component'], 'A. DataFrame', 'A DataFrame is Pandas’ two-dimensional tabular data structure.'),
    makeSkillQuestion('Pandas', 'Which Pandas method previews the first rows of a DataFrame?', ['A. head()', 'B. first_rows()', 'C. preview()', 'D. start()'], 'A. head()', 'head() returns the first rows of a DataFrame for quick inspection.'),
    makeSkillQuestion('Pandas', 'Which Pandas method removes missing values?', ['A. dropna()', 'B. removeNulls()', 'C. clearNA()', 'D. deleteEmpty()'], 'A. dropna()', 'dropna() removes rows or columns containing missing values.'),
    makeSkillQuestion('Pandas', 'Which Pandas method combines tables using matching keys?', ['A. merge()', 'B. attach()', 'C. connect()', 'D. unionRows()'], 'A. merge()', 'merge() combines DataFrames using columns or indexes as matching keys.'),
  ],
  Python: [
    makeSkillQuestion('Python', 'Which Python structure stores key-value pairs?', ['A. Dictionary', 'B. Tuple', 'C. Set only', 'D. Comment'], 'A. Dictionary', 'A dictionary stores values using unique keys.'),
    makeSkillQuestion('Python', 'Which keyword starts a conditional branch?', ['A. if', 'B. loop', 'C. check', 'D. when'], 'A. if', 'The if keyword evaluates a condition and runs code when it is true.'),
    makeSkillQuestion('Python', 'Which library is commonly used for numerical arrays?', ['A. NumPy', 'B. Flask', 'C. React', 'D. Django'], 'A. NumPy', 'NumPy provides efficient array structures and numerical operations.'),
    makeSkillQuestion('Python', 'What does a function help you do?', ['A. Reuse a block of logic', 'B. Delete the operating system', 'C. Format a monitor', 'D. Replace all data'], 'A. Reuse a block of logic', 'Functions package reusable logic with inputs and outputs.'),
  ],
  Excel: [
    makeSkillQuestion('Excel', 'Which Excel function calculates an average based on a condition?', ['A. AVERAGEIF', 'B. COUNTALL', 'C. TEXTJOIN', 'D. FORMAT'], 'A. AVERAGEIF', 'AVERAGEIF calculates an average for cells that meet a criterion.'),
    makeSkillQuestion('Excel', 'What is a PivotTable mainly used for?', ['A. Summarizing and exploring data', 'B. Writing application code', 'C. Editing photos', 'D. Encrypting files'], 'A. Summarizing and exploring data', 'PivotTables summarize and reorganize data for analysis.'),
    makeSkillQuestion('Excel', 'Which chart is best for a trend over time?', ['A. Line chart', 'B. Text box', 'C. Icon set only', 'D. Comment'], 'A. Line chart', 'Line charts make changes across an ordered time axis easy to see.'),
    makeSkillQuestion('Excel', 'What does a cell reference identify?', ['A. A cell location', 'B. A workbook password', 'C. A printer', 'D. A chart color'], 'A. A cell location', 'A reference such as B4 identifies a cell by column and row.'),
  ],
  'Data Visualization': [
    makeSkillQuestion('Data Visualization', 'Which chart is usually best for comparing categories?', ['A. Bar chart', 'B. Line chart only', 'C. Text paragraph', 'D. Audio clip'], 'A. Bar chart', 'Bar charts make category-to-category comparisons clear.'),
    makeSkillQuestion('Data Visualization', 'What should a chart title communicate?', ['A. What the visual shows', 'B. The author password', 'C. The file size', 'D. The screen resolution'], 'A. What the visual shows', 'A clear title gives viewers immediate context for the visual.'),
    makeSkillQuestion('Data Visualization', 'Why should a visual avoid unnecessary decoration?', ['A. It keeps attention on the data', 'B. It increases file size', 'C. It hides labels', 'D. It changes the dataset'], 'A. It keeps attention on the data', 'Reducing clutter improves comprehension and highlights the underlying pattern.'),
    makeSkillQuestion('Data Visualization', 'Which visual can show the relationship between two numeric variables?', ['A. Scatter plot', 'B. Logo', 'C. Checklist', 'D. Text box'], 'A. Scatter plot', 'A scatter plot shows how two numeric variables relate to each other.'),
  ],
  'Machine Learning': [
    makeSkillQuestion('Machine Learning', 'What is a feature in a machine-learning dataset?', ['A. An input variable', 'B. A chart color', 'C. A password', 'D. A file extension'], 'A. An input variable', 'A feature is an input variable used to make a prediction or classification.'),
    makeSkillQuestion('Machine Learning', 'Why split data into training and test sets?', ['A. To evaluate generalization', 'B. To duplicate every row', 'C. To change file formats', 'D. To remove all labels'], 'A. To evaluate generalization', 'A separate test set estimates how the model performs on unseen data.'),
    makeSkillQuestion('Machine Learning', 'What is classification used for?', ['A. Predicting categories', 'B. Sorting files by size', 'C. Drawing charts', 'D. Compressing images'], 'A. Predicting categories', 'Classification assigns observations to categories such as approved or declined.'),
    makeSkillQuestion('Machine Learning', 'What does overfitting mean?', ['A. Memorizing training data too closely', 'B. Having no input data', 'C. Using a small chart', 'D. Renaming a model'], 'A. Memorizing training data too closely', 'An overfit model performs well on training data but poorly on new data.'),
  ],
  Communication: [
    makeSkillQuestion('Communication', 'What makes an analytical finding easier for stakeholders to act on?', ['A. A clear insight with context and next step', 'B. More unexplained jargon', 'C. A longer spreadsheet only', 'D. Removing the evidence'], 'A. A clear insight with context and next step', 'Actionable communication connects the finding to its business meaning and next action.'),
    makeSkillQuestion('Communication', 'What should you do when a stakeholder asks an ambiguous question?', ['A. Clarify the goal and success measure', 'B. Guess silently', 'C. Ignore the question', 'D. Change the dataset'], 'A. Clarify the goal and success measure', 'Clarifying the intended decision prevents analysis from solving the wrong problem.'),
    makeSkillQuestion('Communication', 'Which structure helps explain a project result?', ['A. Situation, action, result', 'B. Tools only', 'C. Code without context', 'D. A list of unrelated claims'], 'A. Situation, action, result', 'A structured explanation shows the problem, contribution, and outcome.'),
    makeSkillQuestion('Communication', 'How should uncertainty in a result be presented?', ['A. State assumptions and limitations clearly', 'B. Hide all limitations', 'C. Claim certainty without evidence', 'D. Remove the result'], 'A. State assumptions and limitations clearly', 'Transparent limitations help stakeholders interpret a result responsibly.'),
  ],
  Tableau: [
    makeSkillQuestion('Tableau', 'Which Tableau feature is commonly used to combine views interactively?', ['A. Dashboard', 'B. Terminal', 'C. Compiler', 'D. File Explorer'], 'A. Dashboard', 'A Tableau dashboard combines worksheets and interactive controls in one view.'),
    makeSkillQuestion('Tableau', 'What is a Tableau filter used for?', ['A. Restricting the data shown', 'B. Encrypting the workbook', 'C. Installing a driver', 'D. Writing Python code'], 'A. Restricting the data shown', 'Filters limit the records or values displayed in a view.'),
    makeSkillQuestion('Tableau', 'Which chart is useful for comparing categories in Tableau?', ['A. Bar chart', 'B. Paragraph', 'C. Audio track', 'D. Folder tree'], 'A. Bar chart', 'Bar charts make category comparisons straightforward.'),
    makeSkillQuestion('Tableau', 'What does a calculated field provide?', ['A. A derived value based on an expression', 'B. A new monitor', 'C. A password reset', 'D. A file backup'], 'A. A derived value based on an expression', 'Calculated fields derive analytical values from existing data.'),
  ],
};

export const generateSkillQuiz = (missingSkills: string[]): SkillQuizQuestion[] => {
  const availableSkills = missingSkills.filter(
    (skill, index, skills) => skillQuestionBank[skill] && skills.indexOf(skill) === index
  );

  if (availableSkills.length === 0) return [];

  return Array.from({ length: 4 }, (_, index) => {
    const skill = availableSkills[index % availableSkills.length];
    const bank = skillQuestionBank[skill];
    const source = bank[index % bank.length];
    return {
      id: `skill-quiz-${index + 1}`,
      skill: source.skill,
      question: source.question,
      options: source.options,
      correctAnswer: source.options.indexOf(source.correctAnswer),
      explanation: source.explanation,
    };
  });
};

const fallbackQuestions = (skill: string) => [
  makeSkillQuestion(skill, `Which activity is most closely associated with ${skill}?`, [`A. Applying ${skill} concepts to data`, 'B. Editing video files', 'C. Managing computer hardware', 'D. Designing a logo'], 'A. Applying ' + skill + ' concepts to data', `${skill} should be assessed through practical, role-relevant data work.`),
  makeSkillQuestion(skill, `Why is ${skill} relevant to a data analyst?`, [`A. It supports data-related work`, 'B. It replaces every database', 'C. It is only used for gaming', 'D. It formats a computer'], 'A. It supports data-related work', `${skill} is relevant when it supports a real analysis task or workflow.`),
  makeSkillQuestion(skill, `What is a good way to practice ${skill}?`, [`A. Use it in a small verified project`, 'B. Claim it without evidence', 'C. Avoid documenting results', 'D. Remove it from every tool'], 'A. Use it in a small verified project', `A small documented project provides meaningful practice and evidence for ${skill}.`),
  makeSkillQuestion(skill, `What should you check when using ${skill} on a dataset?`, ['A. Inputs and outputs are valid', 'B. The screen brightness', 'C. The keyboard layout', 'D. The file icon color'], 'A. Inputs and outputs are valid', `Validating inputs and outputs helps ensure ${skill} is being applied correctly.`),
];

export const getSkillAssessmentQuestions = (): InterviewQuestionItem[] => {
  const skills = [...sampleSkillGap.missingSkills, ...sampleSkillGap.weakEvidenceSkills]
    .map((item) => item.name)
    .filter((skill, index, allSkills) => allSkills.indexOf(skill) === index);
  const assessmentSkills = skills.length ? skills : ['Data Analysis'];

  return Array.from({ length: 4 }, (_, index) => {
    const skill = assessmentSkills[index % assessmentSkills.length];
    const bank = skillQuestionBank[skill] || fallbackQuestions(skill);
    const template = bank[index % bank.length];
    return { ...template, id: `gap-iq-${index + 1}`, number: index + 1 };
  });
};

export const getRoleInterviewQuestions = (
  jobTitle: string,
  description: string,
  requiredSkills: string[] = []
): InterviewQuestionItem[] => {
  const source = `${jobTitle} ${description} ${requiredSkills.join(' ')}`.toLowerCase();
  const supportedSkills = Object.keys(skillQuestionBank);
  const detectedSkills = supportedSkills.filter((skill) => source.includes(skill.toLowerCase()));
  const skills = detectedSkills.length ? detectedSkills : [jobTitle || 'Data Analysis'];

  return Array.from({ length: 10 }, (_, index) => {
    const skill = skills[index % skills.length];
    const bank = skillQuestionBank[skill] || fallbackQuestions(skill);
    const template = bank[index % bank.length];
    return {
      ...template,
      id: `role-iq-${index + 1}`,
      number: index + 1,
      context: `Role-based practice question for the selected ${jobTitle || 'target'} Job Description.`,
      targetRole: jobTitle || 'Target Role',
    };
  });
};

export const sampleInterviewQuestions: InterviewQuestionItem[] = getSkillAssessmentQuestions();

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

const bulkCandidateNames = [
  'Aarav Mehta', 'Maya Chen', 'Liam Carter', 'Sofia Patel', 'Noah Williams',
  'Anika Rao', 'Ethan Brooks', 'Zoya Khan', 'Lucas Martin', 'Isha Nair',
  'Daniel Kim', 'Leah Johnson', 'Arjun Shah', 'Grace Wilson', 'Mateo Garcia',
  'Nora Adams', 'Kabir Menon', 'Olivia Davis', 'Rohan Iyer', 'Emma Taylor',
  'Vikram Singh', 'Chloe Brown', 'Aditya Das', 'Mia Anderson', 'Neil Thomas',
  'Sara Joseph', 'Henry Moore', 'Diya Kapoor', 'James Lee', 'Aanya Verma',
  'Benjamin Clark', 'Meera Pillai', 'Oliver Hall', 'Tara Sen', 'William Scott',
  'Nisha George', 'Alexander Young', 'Riya Bhat', 'Michael Green', 'Pooja Shah',
  'Samuel Baker', 'Kavya Roy', 'David Nelson', 'Aditi Suresh', 'Joseph Hill',
  'Ira Bose', 'Matthew Wright', 'Tanvi Desai', 'Christopher King', 'Sana Ali',
];

const bulkRoles = ['Data Analyst', 'Frontend Developer', 'Product Analyst', 'Data Engineer', 'Machine Learning Engineer'];
const bulkLocations = ['Bengaluru, India', 'Chennai, India', 'Hyderabad, India', 'Pune, India', 'Remote'];
const bulkSkillSets = [
  ['Python', 'SQL', 'Excel', 'Power BI'],
  ['React', 'TypeScript', 'CSS', 'Testing'],
  ['SQL', 'Python', 'Excel', 'Statistics'],
  ['Python', 'SQL', 'Spark', 'AWS'],
  ['Python', 'Pandas', 'Scikit-learn', 'Machine Learning'],
];

export const sampleBulkResumeCandidates: BulkResumeCandidate[] = bulkCandidateNames.map((name, index) => {
  const skills = bulkSkillSets[index % bulkSkillSets.length];
  const score = 62 + ((index * 7) % 34);
  const status: BulkResumeCandidate['status'] = index % 7 === 0 ? 'Needs Review' : index % 5 === 0 ? 'Processing' : 'Analyzed';
  return {
    id: `bulk-cand-${String(index + 1).padStart(3, '0')}`,
    name,
    email: `${name.toLowerCase().replace(/ /g, '.')}@example.com`,
    phone: `+91 90000 ${String(10000 + index).slice(-5)}`,
    location: bulkLocations[index % bulkLocations.length],
    resumeFile: `${name.replace(/ /g, '_')}_Resume.pdf`,
    targetRole: bulkRoles[index % bulkRoles.length],
    experience: index % 6,
    education: index % 2 === 0 ? 'B.S. Computer Science' : 'B.Tech Information Technology',
    skills,
    matchedSkills: skills.slice(0, 2 + (index % 3)),
    missingSkills: skills.slice(2 + (index % 2)),
    resumeScore: score,
    skillMatch: Math.max(52, score - 4),
    atsScore: Math.min(96, score + 8),
    experienceMatch: Math.max(55, score - 1),
    educationMatch: 72 + (index % 24),
    evidenceStrength: score >= 85 ? 'Strong' : score >= 72 ? 'Medium' : 'Weak',
    status,
  };
});


