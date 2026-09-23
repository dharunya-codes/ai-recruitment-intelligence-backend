# HALO Backend API Integration Guide

## Base URL

Local development uses `http://127.0.0.1:8010`. The API is currently unversioned; versioning was reviewed for Phase 19 and no `/api/v1` prefix was added because existing clients use the current paths.

Interactive documentation is available at `/docs` and the machine-readable contract at `/openapi.json`.

## Authentication

Protected requests use:

```http
Authorization: Bearer <access_token>
```

Company/HR authentication:

```http
POST /auth/register
POST /auth/login
GET /auth/me
```

Candidate authentication:

```http
POST /candidate/auth/register
POST /candidate/auth/login
GET /candidate/auth/me
GET /candidate/me
```

`/candidate/auth/me` and `/candidate/me` are both GET endpoints. Roles are `COMPANY_ADMIN`, `HR`, and `CANDIDATE`.

- `COMPANY_ADMIN` and `HR` access company-owned jobs, resumes, verification, assessments, and HR reports.
- `CANDIDATE` accesses only candidate-owned resumes, analyses, verification, assessments, and candidate reports.
- Unauthorized resources return `404` where ownership is intentionally hidden. Missing or invalid authentication returns `401`.

Example login:

```json
{"email":"candidate@example.com","password":"StrongPassword123"}
```

The response contains an access token and token type. Passwords, hashes, secrets, and API keys are never returned.

## Company and Jobs

```http
GET /companies/me
GET /jobs
POST /jobs
GET /jobs/{job_id}
PUT /jobs/{job_id}
DELETE /jobs/{job_id}
POST /jobs/{job_id}/jd
GET /jobs/{job_id}/requirements
```

Jobs and requirements are restricted to the authenticated user's company. Job creation requires a title and description. JD descriptions are 10 to 100,000 characters.

Example job creation:

```json
{"title":"Backend Developer","description":"Python and Docker are required."}
```

## Resumes and Analysis

Company upload:

```http
POST /jobs/{job_id}/resumes
```

Candidate upload:

```http
POST /candidate/resumes
GET /candidate/resumes
GET /candidate/resumes/{resume_id}
```

Uploads use `multipart/form-data` with the field name `file`. Supported files are PDF and DOCX, with a 10 MB maximum. The server uses generated storage names; the original filename is not used as a filesystem path.

Company analysis:

```http
GET /resumes/{resume_id}/analysis
GET /resumes/{resume_id}/text
```

Standalone candidate analysis:

```http
POST /candidate/analysis/{resume_id}
GET /candidate/analyses
```

Candidate analysis accepts `target_role` and an optional `job_description`. Without a JD, the score is `ROLE_COMPATIBILITY`; with a JD, it is `JOB_MATCH`.

## Verification

Company routes:

```http
POST /verification/{resume_id}/generate
GET /verification/{resume_id}/questions
POST /verification/questions/{question_id}/answer
GET /verification/{resume_id}/status
```

Candidate routes use the same deterministic verification behavior:

```http
POST /candidate/verification/{resume_id}/generate
POST /candidate/verification/questions/{question_id}/answer
```

Candidate-provided verification remains separate from resume evidence.

## Assessment

Company routes:

```http
POST /assessment/{resume_id}/generate
GET /assessment/{assessment_id}
POST /assessment/questions/{question_id}/answer
POST /assessment/{assessment_id}/submit
POST /assessment/{assessment_id}/evaluate
GET /assessment/{assessment_id}/result
GET /assessment/{assessment_id}/status
```

Candidate routes use candidate ownership:

```http
POST /candidate/assessment/{resume_id}/generate
POST /candidate/assessment/questions/{question_id}/answer
POST /candidate/assessment/{assessment_id}/submit
POST /candidate/assessment/{assessment_id}/evaluate
```

Lifecycle:

```text
NOT_STARTED -> IN_PROGRESS -> SUBMITTED -> EVALUATED
```

Answers can be submitted before `SUBMITTED`. Answers become immutable after submission/evaluation. Evaluation is available only after submission. Assessment results contain question feedback, category scores, strengths, and improvement areas.

## Reports

```http
POST /reports/{resume_id}/generate
GET /reports/{resume_id}
POST /reports/{resume_id}/regenerate
```

Generation is idempotent for existing reports. Regeneration refreshes the report. Company users may receive authorized candidate and HR reports. Candidate users receive only their candidate report. Resume evidence and candidate-provided verification are represented as separate sources.

## Candidate Intelligence

```http
GET /candidate/analysis/{resume_id}/readiness
GET /candidate/analysis/{resume_id}/improvement-plan
GET /candidate/analysis/{resume_id}/resume-quality
GET /candidate/analysis/{resume_id}/skill-priorities
GET /candidate/analysis/{resume_id}/career-intelligence
GET /candidate/analysis/{resume_id}/actions
GET /candidate/analysis/{resume_id}/projects
GET /candidate/analysis/{resume_id}/evidence-builder
GET /candidate/analysis/{resume_id}/roadmap
GET /candidate/analysis/{resume_id}/progress
POST /candidate/analysis/{resume_id}/career-question
```

These endpoints provide role alignment, evidence gaps, readiness dimensions, project recommendations, improvement actions, supported roadmaps, historical progress, and constrained career questions. They do not make hiring decisions or rank candidates.

Supported career question types are defined in OpenAPI and include `WHAT_SHOULD_I_IMPROVE`, `WHAT_SKILL_IS_MISSING`, `WHY_IS_MY_MATCH_SCORE_LOW`, `WHAT_EVIDENCE_IS_MISSING`, `WHAT_SHOULD_I_PRACTICE`, `WHAT_PROJECT_SHOULD_I_BUILD`, and `WHAT_SHOULD_I_VERIFY`.

HR decision-support endpoints:

```http
GET /analysis/{resume_id}/career-intelligence
GET /analysis/{resume_id}/evidence-consistency
POST /analysis/multi-job
```

Multi-job analysis returns independent job-by-job results for authorized company jobs. It does not rank candidates or jobs.

## Errors and Limits

Application errors use:

```json
{"detail":"Human-readable message"}
```

Common status codes:

- `200` successful read/update/action
- `201` created resource
- `400` invalid file or request
- `401` missing/invalid/expired token
- `404` missing or unauthorized resource
- `413` upload exceeds 10 MB
- `422` schema, lifecycle, or analysis validation failure
- `429` configured rate limit exceeded

Authentication, registration, upload, and expensive analysis/report routes have lightweight in-memory rate limits. The current response is `429`; clients should retry later. No `Retry-After` header is currently emitted.

## CORS and Environment

Configure explicit frontend origins with `CORS_ORIGINS`, for example:

```env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Do not use wildcard origins with credentialed authentication. Relevant configuration is documented in `.env.example`, including `DATABASE_URL`, `JWT_SECRET_KEY`, `ENVIRONMENT`, GenAI settings, and rate limits.

## Collections and Privacy

Current list endpoints return bounded collections without pagination. Pagination can be introduced when deployment scale requires it. Ownership checks occur before private data is returned. Resume file paths, passwords, JWT secrets, API keys, and unrelated private company data are not API response fields.
