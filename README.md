# Three Business Systems Django Teaching App

This project is a beginner-friendly Django web application for an undergraduate web applications class. It simulates three business systems that communicate through APIs while remaining inside one Django project for simplicity.

The project contains three Django apps:

- `hr` — HR creates job postings, reviews applicants, and hires candidates.
- `external_jobs` — a public third-party job site where anonymous candidates view jobs and apply.
- `employee_system` — a protected internal employee system where hired candidates become employee profiles.

The app is intentionally not API-only. Each app has normal Django pages, templates, forms, and navigation. The APIs are used for system-to-system communication.

## Learning goals

Students can use this project to study:

- Django models, views, templates, and forms
- Django REST Framework APIs
- API-to-API communication
- role-based permissions with Django groups
- how AI can add value to an existing web application
- the idea of microservices while keeping everything in one simple Django project

## Setup in GitHub Codespaces or locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver 0.0.0.0:8000
```

In Codespaces, open the forwarded port for port 8000.

## Sample users

The seed command creates these users. The password for all sample users is:

```text
password123
```

| Username | Role |
|---|---|
| `hr_user` | HR group |
| `employee_user` | EmployeeSystem group |
| `admin` | Superuser |

## API tokens

The project uses simplified static API tokens from environment variables. This is intentionally simple for teaching. Real production systems should use stronger authentication such as OAuth, signed JWTs, mTLS, scoped service accounts, rotation, logging, and rate limiting.

Default demo tokens are in `.env.example`:

```text
HR_API_TOKEN=class-hr-token
EXTERNAL_JOBS_API_TOKEN=class-external-jobs-token
EMPLOYEE_SYSTEM_API_TOKEN=class-employee-system-token
```

## API flow

1. HR creates a job posting.
2. HR optionally uses Gemini to generate the description.
3. HR approves and publishes the job.
4. HR sends the job posting to the external job site API.
5. Candidate views and applies on the external job site.
6. External job site sends the application to HR API.
7. HR reviews the candidate.
8. HR marks candidate as hired.
9. HR sends hired candidate to employee system API.
10. Employee system creates an employee profile.

## Permissions model

The app uses Django authentication, groups, and simple permission checks.

Anonymous users can view public job postings and submit applications through the external job site. They cannot access HR pages or employee system pages.

HR users can create, edit, approve, and publish job postings. They can review applications, change candidate statuses, and trigger employee creation.

Employee system users can view employee records and employee profiles. They cannot create job postings or approve candidates unless also placed in the HR group.

Superusers can access everything, including Django admin.

## Gemini integration

Gemini support lives in:

```text
hr/services/gemini_service.py
```

It reads `GEMINI_API_KEY` from the environment. If the key is missing, the app returns a clearly marked placeholder description so the app works during class without credentials.

## Service files to inspect

These files show API-to-API communication:

```text
hr/services/external_jobs_client.py
hr/services/employee_system_client.py
external_jobs/services/hr_client.py
```

These files are useful for explaining how one system can call another system through an API, even though all three apps are inside the same Django project.

## Important pages

```text
/                         Home
/jobs/                    Public external job listings
/hr/                      HR dashboard
/employees/               Employee system dashboard
/admin/                   Django admin
```

## API endpoints

```text
POST /jobs/api/job-postings/       HR publishes a job to the external job site
GET  /jobs/api/job-postings/list/  External job postings list
POST /hr/api/applications/         External job site sends application to HR
GET  /hr/api/approved-jobs/        Approved HR jobs
POST /employees/api/employees/     HR creates employee profile after hiring
```

Protected API calls expect this header format:

```text
Authorization: Token class-hr-token
```

Use the matching token for each system.

## Tests

Run:

```bash
python manage.py test
```

The tests demonstrate that public pages are accessible, protected dashboards require appropriate users, and token-protected API endpoints accept or reject requests correctly.

## Suggested teaching path

Start with the HTML pages and forms so students see normal Django behavior. Then show how publishing a job calls an API instead of directly writing to another app's model. Then show the candidate application flow from the public site back to HR. Finally, show the hire flow into the protected employee system.

This keeps the idea of microservices visible without requiring Docker Compose, Kubernetes, Celery, Redis, or cloud deployment.
