# CLAUDE.md — NSTP project context

Persistent context. Work from this file, not `docs/project-overview.md` (long).
Read the spec only when this file is genuinely insufficient.

## What this is

**Network Security Training Platform (NSTP)** — web-based cybersecurity training
for **non-technical Australians**: small businesses, local councils, schools.
Client: **AUSDAIS PTY LTD** (Bundoora, Melbourne). Rep: Dr. Naser Mahmood.
Academic supervisors: Hussain Riaz, Dr. Belal Chowdhury.
MIT capstone, BN301 (design, done) → **BN304 (build, weeks 13–24, current)**.

**Differentiator:** the **Adaptive Feedback Engine** — instead of "you scored
55%", it analyses every wrong answer and generates a personalised study plan.

### Users
Non-technical Australian adults. **Plain language, zero jargon, one obvious next
action per screen.** Premium but dead simple. Clarity > cleverness. Accessibility
is a requirement, not a nice-to-have.

### Team
| Person | ID | Owns |
|---|---|---|
| Aashish Dhakal | MIT235300 | Backend + project lead (all models/views/logic, deploy) |
| Sudip Subedi | MIT235301 | Frontend — Bootstrap 5 templates, JS timer |
| Anuska Lamsal | MIT236433 | UI design, PDF certificate template, usability testing |
| Khadka Shrees | MIT236189 | Tests (pytest-django), OWASP ZAP, docs |
| Bigyap Ghimire | MIT235163 | Content — 24 lessons ≥800 words, quiz Qs + explanations |

## Stack (as built — deviations from spec are deliberate)

- **Python 3.13.14** · **Django 5.2.16 LTS** · **PostgreSQL 18** (psycopg 3)
- Bootstrap 5.3 (CDN-free, MVT — no REST/React)
- django-otp (TOTP 2FA) + qrcode · django-tinymce · django-ratelimit · django-csp
- ReportLab (PDF) · Pillow · python-decouple · WhiteNoise
- pytest-django + coverage.py · GitHub Actions CI · PythonAnywhere hosting

### Deviations from spec — do not "fix" these back
| Spec says | We use | Why |
|---|---|---|
| Django 6.0.6 | **5.2 LTS** | 6.0 not LTS; support ends 2026-08. 5.2 → 2028-04. tinymce declares ≤5.2 |
| Python 3.12.4 | **3.13.14** | What's installed; supported by Django 5.2 + PythonAnywhere |
| psycopg2-binary | **psycopg 3** | Django marks psycopg2 as deprecation-track |
| PBKDF2 260k iters | **Django default (1,000,000)** | Spec's number is Django 3.2-era and 74% *weaker*. Never override |
| "ReportLab's FPDF class" | **`reportlab.platypus` / `pdfgen.canvas.Canvas`** | ReportLab has no FPDF class. FPDF is a different library |
| django-otp "handles QR display" | **render QR from `TOTPDevice.config_url`** | django-otp auto-QR is admin-only |
| Gunicorn on PythonAnywhere | **not used** | PA runs its own WSGI server; gunicorn is redundant |

### Unresolved blocker
**PythonAnywhere's free tier has no PostgreSQL** (MySQL is paid; PG is a paid
add-on). Spec's hosting rationale is wrong. Options: pay (~$10/mo), switch prod
to MySQL, or host elsewhere (Render/Fly/Railway free PG). **Needs client decision.**

## The 12 models → 4 apps

```
authentication/   User (AbstractUser), UserProfile
modules/          Module, Lesson, Simulation, ProgressRecord
quizzes/          Quiz, Question, Answer, QuizResult, WrongAnswer
certificates/     Certificate
```

### Relationships
```
User 1─1 UserProfile
User 1─* ProgressRecord *─1 Lesson
User 1─* QuizResult     *─1 Quiz
User 1─* Certificate
Module 1─* Lesson          (4 per module)
Module 1─1 Simulation
Module 1─1 Quiz
Quiz   1─* Question        (bank >10; 10 drawn per attempt)
Question 1─* Answer        (exactly 4: A–D, one correct)
Question *─1 Lesson        <-- lesson_reference: REQUIRED by the AFE
QuizResult 1─* WrongAnswer *─1 Question
```

**Key fields**
- `User`: email = `USERNAME_FIELD` (unique), `role` ∈ {Student, Instructor, Administrator}, `is_verified`
- `UserProfile`: organisation, avatar, `last_active`, `streak_count`, `points`, `badges` (JSON)
- `Module`: `order_index` (sequential lock), `is_published` (soft delete), difficulty
- `Lesson`: `body_text` (TinyMCE HTML), `reading_time`
- `Answer`: `correct_answer` (bool), **`explanation_text`** ← the AFE's fuel
- `Quiz`: `time_limit`=30min, `pass_mark`=70%
- `Certificate`: UUID4 `code`, `pdf_path`

**Points:** 10/lesson, 50/quiz passed. **Pass mark:** 70%. **Modules unlock sequentially.**

## The 6 sprints (weeks 13–24)

1. **13–14 Setup + Auth** — 4 apps, 12 models, migrations, registration + email verify, 2FA/TOTP, RBAC, GitHub Actions CI
2. **15–16 Modules + CMS** — Module/Lesson/Simulation, Instructor CMS (CBVs + TinyMCE), student browser w/ sequential lock. Content M1–M2
3. **17–18 Quiz + Adaptive Feedback Engine** — ⚠️ hardest. Timer, session persistence, scoring, AFE
4. **19–20 Dashboards** — student/instructor/admin, ORM aggregation, badges, streaks, CSV export
5. **21–22 Certificates + Hardening** — ReportLab PDF, UUID, OWASP ZAP, remediation
6. **23–24 Testing + Deploy** — pytest ≥80% coverage, UAT, PythonAnywhere, final report

## Conventions

- **MVT only.** No DRF, no React. One codebase.
- **ORM only — never raw SQL.** (Also the SQL-injection control.)
- Business logic in views/services, not templates. Reusable helpers → `<app>/utils.py`.
- Models singular (`Module`), tables plural via Django default.
- Templates: `<app>/templates/<app>/<name>.html`. Base at `templates/base.html`.
- Secrets via `config()` from python-decouple. **Never** hard-code, never commit `.env`.
- Australian English in all UI copy and comments (`organisation`, not `organization`).
- Format: 4-space indent, double quotes, ~88 cols.
- Branches: feature branch → PR → `BN304-Development`. Never commit to `main` directly.

## Always do

- Run `.venv/bin/python manage.py check` after touching settings.
- Add `lesson_reference` FK on `Question` — the AFE cannot work without it.
- Decorate every view with an auth/role check. Assume nothing from the URL.
- `select_related`/`prefetch_related` on dashboard + AFE queries (N+1 kills these).
- Write the test alongside the code (Khadka reviews, but don't hand him a vacuum).
- Use Django's built-in password hashing, CSRF, and template escaping as-is.

## Never do

- **Never** set `AUTH_USER_MODEL` after the first migration. It's near-irreversible.
- Never override `PASSWORD_HASHERS` to the spec's 260k iterations.
- Never use `|safe` on user input. Lesson HTML from TinyMCE must be **sanitised** server-side.
- Never `DEBUG=True` in production; never commit `.env` or a real `SECRET_KEY`.
- Never hard-delete Modules/Lessons — soft-delete via `is_published=False` (preserves QuizResults).
- Never trust `random.sample()` on a large queryset — it loads all rows.
- Never generate the PDF synchronously inside a request if it can be deferred.

## State (2026-07-16)

Done: repo restructured into `nstp_project/`, git `main`, `.venv` on 3.13,
all deps installed + imports verified, `settings.py` fully wired, `.env` +
`.env.example`, spec saved to `docs/`. `manage.py check` clean.

**Not started:** all 12 models (files are empty stubs), all views, all templates.

**Next:** Sprint 1 task 1 — create `authentication.User` and **uncomment
`AUTH_USER_MODEL` in settings.py before the first `migrate`**.

**Repo:** github.com/aashishdhakal0/Industry-Based-Project-I — remote not yet
configured locally; branch is `main`, spec calls for `BN304-Development`.
