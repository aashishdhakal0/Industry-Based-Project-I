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
| django-otp TOTP app for 2FA | **6-digit code emailed on every login** | See below — deliberate; email codes are weaker than TOTP, accepted trade-off |
| Gunicorn on PythonAnywhere | **not used** | PA runs its own WSGI server; gunicorn is redundant |

#### Why 2FA is an emailed code, not an authenticator app

The spec asks for TOTP via an authenticator app. We send a 6-digit code to the
email address the user has already confirmed, on every sign-in. Deliberate, and
there are two things to say about it — one in our favour, one against.

**Coverage is back to universal, which the spec wanted.** An earlier version of
this build made TOTP mandatory only for Instructors/Administrators and optional
for Students, because installing an authenticator app was too much to ask of a
non-technical Student. An emailed code removes that barrier — no app, no setup,
nothing to install, just a number in an inbox they already know how to use — so
every account can carry the second factor without the friction that forced the
exemption. We now match the spec on *who* is protected.

**Email codes are weaker than TOTP. This is the accepted cost, stated plainly.**
A TOTP secret never leaves the user's device; an email code travels the
network and sits in an inbox, so anyone who has compromised the email account,
or can read mail in transit, can complete the login. Email is also the channel
most likely to delay or drop the code. We judge this acceptable because our
users' realistic threat is a reused password, not a targeted mailbox breach,
and a second factor they'll actually use beats a stronger one they won't. **Do
not present this as equivalent to app-based TOTP in the report — present it as
a usability/security trade-off made with eyes open.**

The code is single-use, expires in 10 minutes, is capped at 5 attempts (we hash
it into the session and count tries ourselves — django-otp's throttling went
with the library), and is generated with `secrets`, never `random`.

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

**Environment:** repo restructured into `nstp_project/`, `.venv` on 3.13, all
deps installed + imports verified, `settings.py` fully wired, `.env` +
`.env.example`, spec saved to `docs/`. `manage.py check` clean.

**Database — migrated.** All 12 models are written and applied to PostgreSQL 18
(`nstp_db`, via the least-privilege `nstp` role, which has CREATE). All 25
migrations green. `AUTH_USER_MODEL = "authentication.User"` was set *before* the
first `migrate` — the near-irreversible step is done and correct, so the risk in
row 1 of the build-plan risk register is now retired. `db.sqlite3` deleted; local
dev is Postgres-only.

**Admin — registered.** All 12 models plus `Group` and `otp_totp.TOTPDevice` are
in the admin, verified by driving every changelist and add form (14/14 → 200) and
by creating a user through the add form end-to-end. `authentication/admin.py`
rebuilds Django's stock `UserAdmin` around `email` — the stock one hardcodes
`username`, which our model drops, so it cannot simply be subclassed.

**Superuser:** `dhakalaashish75@gmail.com` (ADMINISTRATOR, verified). Password is
Aashish's own; hash confirmed `pbkdf2_sha256` @ 1,000,000 iterations.
Signing in at `/login/` now emails a 6-digit code (dev: it prints to the
console backend). `/admin/` keeps its own login and never asks for a code.

**Auth — done.** Sprint 1.2 (registration + email verification) and 1.3 (login +
role-based 2FA) are built, tested and merged. Registration mints Students only
(`role` is deliberately absent from the form — self-selection would be privilege
escalation); accounts are `is_active=False` until a signed 48h token is opened.
Login is email+password, lower-cased, rate-limited 10/hr/IP, with `?next=`
validated against open redirect. **No session exists until both factors pass** —
between password and code only a user id sits in the session.

**Design system — done.** Cybaroo identity: near-black base, violet→cyan
gradients, Space Grotesk + JetBrains Mono vendored locally, 16-icon SVG sprite,
no emoji anywhere. Landing, About, Modules, dashboard, and a DEBUG-only
`/styleguide/`. **The gradient carries dark ink, never white** — white measures
1.81:1 at the cyan end. Rule documented at the top of `cybaroo.css`.

**Not started:** modules/lessons/quizzes/AFE/certificates — all views, all
content. `/dashboard/` renders placeholder numbers from
`nstp/placeholder_content.py` (Sprint 2 deletes it).

**Next:** Sprint 1.4 — RBAC groups + per-view role checks. Then 1.6 CI.

**Repo:** github.com/aashishdhakal0/Industry-Based-Project-I — remote **is**
configured; `BN304-Development` is pushed and tracks `origin`, currently at
`79040d6`. `main` untouched at `4d68b51`. Push needs a PAT (osxkeychain);
read is anonymous because **the repo is public** — so nothing secret may ever
land in a commit. `.env` has never been committed; verified absent from history.
