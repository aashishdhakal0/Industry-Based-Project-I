# CLAUDE.md — NSTP / Cybaroo project context

Persistent context and **handover document**. A fresh Claude Code session (new
account, no chat history) should be able to continue seamlessly from this file
alone. Work from this file; read the full spec in `docs/` only when this is
genuinely insufficient.

Last updated: 2026-08-15. Branch: `feature/login-and-2fa`.

---

## 1. Project overview

**Network Security Training Platform (NSTP)**, product-named **Cybaroo** — a
web-based cybersecurity training platform for **non-technical Australians**:
small businesses, local councils, schools. Premium but dead simple.

- **Client:** AUSDAIS PTY LTD (Bundoora, Melbourne). Rep: Dr. Naser Mahmood.
- **Academic supervisors:** Hussain Riaz, Dr. Belal Chowdhury.
- **Unit:** MIT capstone, **BN304 (build, weeks 13–24)**. BN301 (design) is done.
- **Audience:** non-technical Australian adults. Plain language, zero jargon,
  one obvious next action per screen. Accessibility is a requirement.
- **Overall goal:** teach essential cyber-safety through six interactive modules,
  a graded quiz per module, gamification, and a completion certificate.
- **Differentiator — the Adaptive Feedback Engine (AFE):** instead of "you scored
  55%", it analyses every wrong answer and generates a personalised study plan.

### Team
| Person | ID | Owns |
|---|---|---|
| Aashish Dhakal | MIT235300 | Backend + project lead (models/views/logic, deploy) |
| Sudip Subedi | MIT235301 | Frontend — Bootstrap 5 templates, JS timer |
| Anuska Lamsal | MIT236433 | UI design, PDF certificate template, usability testing |
| Khadka Shrees | MIT236189 | Tests (pytest-django), OWASP ZAP, docs |
| Bigyap Ghimire | MIT235163 | Content — lessons, quiz questions + explanations |

---

## 2. Tech stack & environment

- **Python 3.13.14** · **Django 5.2.16 LTS** · **PostgreSQL 18** (psycopg 3.2.9)
- **reportlab 5.0.0** (certificate PDF), Pillow, python-decouple, WhiteNoise
- Bootstrap 5.3 vendored (CDN-free), **MVT only — no DRF, no React**
- django-tinymce, django-ratelimit, django-csp, nh3 (HTML sanitiser), qrcode
- pytest-django + coverage.py · GitHub Actions CI · PythonAnywhere (intended host)
- Settings module: **`nstp/settings.py`** (`ROOT_URLCONF = "nstp.urls"`).
  `SITE_NAME` (default "Cybaroo") is injected as `{{ site_name }}` via
  `nstp.context_processors.site` — never hard-code the name.

### Database & .env
- **Database:** `nstp_db` on PostgreSQL 18. Local dev is Postgres-only
  (`db.sqlite3` was deleted).
- **Least-privilege role:** `nstp` (has `CREATE`; owns nothing it should not).
- **.env** (via `python-decouple`'s `config()`): holds `SECRET_KEY`, `DEBUG`,
  `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SITE_NAME`, email
  settings. **`.env` is gitignored and has never been committed** (verified
  absent from history — the repo is PUBLIC, so nothing secret may ever land in a
  commit). A committed **`.env.example`** documents the keys without values. The
  DB password is Aashish's own local Postgres password; it is not in the repo.
- `AUTH_USER_MODEL = "authentication.User"` was set **before the first migrate** —
  the near-irreversible step is done and correct. Never change it now.

### Running it locally
```bash
# from the repo root (/Users/asis/Desktop/nstp_project on the current machine)
.venv/bin/python manage.py check                    # after touching settings
.venv/bin/python manage.py migrate                  # apply migrations
.venv/bin/python manage.py seed_learning_content    # (re)seed all 6 modules — idempotent
.venv/bin/python manage.py runserver                # http://127.0.0.1:8000/
.venv/bin/python -m pytest -q                       # the test suite (~350 tests)
.venv/bin/python manage.py collectstatic --noinput  # after ANY JS/CSS change
```
- The virtualenv is **`.venv/`** (Python 3.13). Always invoke `.venv/bin/python`.
- Superuser: `dhakalaashish75@gmail.com` (ADMINISTRATOR, verified). Signing in at
  `/login/` emails a 6-digit code (dev: it prints to the console backend).
  `/admin/` keeps its own login and never asks for a code.
- The dev server currently runs with **`DEBUG=True`**.

### DEBUG-only dev unlock (currently active — how to revert)
For content review, two sequential gates are disabled **when `DEBUG=True` only**;
production (`DEBUG=False`, incl. the test suite) keeps them enforced.
1. **`modules/gamification.py`** → `module_progress()`: `review_unlock =
   bool(settings.DEBUG)` and `unlocked=review_unlock or prev_complete`. In dev,
   every module is unlocked without finishing the previous one.
2. **`quizzes/views.py`** → `_all_lessons_done()`: `if settings.DEBUG: return
   True`. In dev, a quiz opens without finishing that module's lessons first.

**To restore the real locks in local dev:** delete the `settings.DEBUG` branch in
each (search `review_unlock` and `if settings.DEBUG:`). Both are committed and
DEBUG-gated, so a real deploy is already locked. The sequential lock is a real
control enforced in the **view** as a 403 (never merely a hidden link).

---

## 3. What's been built (exhaustive)

### Authentication (done, merged)
- Registration mints **Students only** (`role` is deliberately absent from the
  form — self-selection would be privilege escalation). Accounts are
  `is_active=False` until a signed 48h email-verification token is opened.
- Login is email + password (lower-cased), rate-limited 10/hr/IP, `?next=`
  validated against open redirect. **No session exists until both factors pass** —
  between password and code only a user id sits in the session.
- **2FA is a 6-digit code emailed on every sign-in** (not authenticator TOTP —
  see §4). Single-use, expires 10 min, capped at 5 attempts (hashed into the
  session, counted ourselves), generated with `secrets`.
- Role-based routing via `authentication/utils.role_home_url`: staff
  Administrators → Django admin; others → dashboard.

### The six modules — all content-complete in the interactive "room" format
Each module = **4 lessons**, ~18–19 collapsible task **panels**, and a **40-
question quiz** (10 per lesson, 10 drawn per attempt). Content lives as plain
data in `modules/content/module_<n>.py` (`LESSONS` + `QUIZ`), loaded by the seed
via a `CONTENT` registry. Lessons render as a scrollable TryHackMe-style **room**
(numbered, collapsible panels; XP per panel; sticky progress; a task-index rail).
Voice is warm, plain Australian English, **no em-dashes** (enforced by tests).

| # | Title | Lessons | Flagship / signature activity |
|---|---|---|---|
| 1 | **Network Security Fundamentals** | What a network is, and what you protect · How attacks actually happen · Locking your front door · Putting it all together | Rebalanced toward **DOING**: the new **`respond`** apply-it activity throughout + the "Docklands Dental" **branch** |
| 2 | **Recognising Cyber Threats** | The malware family · Ransomware, and attacks on the whole business · The big breaches: Optus and Medibank · Recognising and reacting | **`classify`** — diagnose alerts as legit vs a type of attack |
| 3 | **Phishing & Social Engineering** | The con behind the click · Phishing and its sharper cousins · Beyond the inbox · Reading an email like an investigator | **`mailsort`** — triage a realistic mixed inbox (genuine vs phishing) |
| 4 | **Secure Communication Practices** | What 'secure' really means · Proving it is you · Sharing information safely · Working securely anywhere | **`harden`** — secure a fictional employee's whole workspace step by step |
| 5 | **Firewall & Network Defence** | The firewall: your network's gatekeeper · Segmentation: contain the trouble · Remote access and the VPN · Alerts, patches, and finding the gaps | **`netmap`** — find the weaknesses in a fictional business network |
| 6 | **Incident Response** | Why a plan beats panic · Spot it and stop it · Clean up and come back · The law, and the whole response | ransomware-morning **`branch`** + **`sequence`** (order the six-phase lifecycle); maps to the Privacy Act 1988 NDB scheme |

### Interactive activity types (all built; driven by `static/js/activities.js`)
Each activity reads a CSP-safe `{{ payload|json_script }}` block and fires
`cy:solved` when complete. `LessonTask.Kind` enumerates them:
- **sort** — tap a chip, tap its bucket (e.g. the CIA-triad sort)
- **inbox** — inspect one email; tap every "tell"
- **spot** — real vs fake (message cards, or a `variant:"login"` page mock-up)
- **password** — live strength meter + checklist; solved at Strong
- **branch** — multi-step scenario with consequences; solved at an ending
- **classify** (M2) — read each alert, pick its category, teaching feedback
- **mailsort** (M3) — a mixed inbox; mark each email Genuine/Phishing
- **harden** (M4) — secure each part of a workspace ("At risk" → "Secured")
- **netmap** (M5) — tap every weakness on a network map
- **sequence** (M6) — put shuffled steps into the correct order
- **respond** (M1 rework) — realistic "what would you do?" situations; pick the
  sound action, see the consequence; the reusable **apply-it** workhorse
- **check** / mid-panel **inline_check** — apply-it MCQs (question + hint + 4
  options with per-option explanations)

Authoring reference: **`docs/module-authoring.md`** (the Module 1 gold standard —
panel shape, payload contracts, voice rules). Copy it to add/extend a module.

### Quiz engine + Adaptive Feedback Engine
- `quizzes/services.py` draws 10 questions, grades **server-side** against the
  stored `correct_answer` flag (never trusts the client), pass mark **70%**,
  records a `QuizResult` (+ `WrongAnswer` rows), awards +200 on a first pass.
- `quizzes/feedback.py` (the AFE) reads the `WrongAnswer`/`explanation_text` rows
  and builds a per-lesson **study plan** shown on the result page: which lessons
  to revise (ranked by where mistakes clustered) and why each answer was wrong.

### Gamification engine (`modules/gamification.py`)
- **Records are the truth.** `UserProfile.points` is a **cache recomputed** from
  `ProgressRecord` (lessons) + distinct passed `QuizResult` (quizzes) on every
  completion — never incremented, so it cannot drift. Points = lessons×40 +
  passed_quizzes×200 (all 24 lessons + 6 quizzes = 2160, the ceiling). The
  constants live in `gamification.py` (`POINTS_PER_LESSON`/`POINTS_PER_QUIZ`); the
  level curve `_points_to_reach` and the Bronze→Diamond `TIERS` scale with them.
  Tier thresholds: Bronze 0 · Silver 200 · Gold 500 · Platinum 1000 · Diamond 2000.
- **Level** is a pure function of points. **Streak** advances on activity (date
  injected for tests). **Badges**: catalogue in code (`modules/badges.py`), earned
  ids in `UserProfile.badges` (jsonb), awarded one-way from `student_stats`.
- **Per-panel progress:** `LessonTask` + `TaskProgress` record each panel done;
  the engine banks the lesson (+40 via `ProgressRecord`) when all a lesson's tasks
  are complete. `SimulationResult` records the separate simulation exercise.
- **Module complete** = all lessons done AND (if gated) its quiz passed → unlocks
  the next module; the module overview shows a "Module complete" moment with a
  "Start Module N" / "See your certificate" CTA.

### Student surfaces
- **Dashboard** (`/dashboard/`): real points/level/streak/badges/progress, a
  study **activity calendar**, a roadmap, recent activity, nearest-badge nudge.
- **Badges** (`/learn/badges/`): the achievement gallery, earned vs locked.
- **Certificate** (`/learn/certificate/`): on-screen premium certificate design
  populated with real data + an earned/progress state. **The downloadable PDF is
  NOT yet built** (a plan exists: `certificates/` app has a `Certificate` model
  with a UUID4 `code` + `pdf_path`; generate lazily with ReportLab on download,
  cache under `MEDIA_ROOT/certificates/`, plus a public `/verify/<code>/`).
- **Simulation** (`/learn/m/N/simulation/`): Module 1 has a real playable
  phishing-inbox simulation; Modules 2–6 use a generic placeholder (see §6).

### Recent lesson layout / design work
- **Focused room mode:** in a lesson the app shell drops the left sidebar and
  shows a slim sticky **focus bar** (a clear "← Back to <module>" button, the
  lesson count, the Cybaroo mark). Set by `focus=True` in the lesson view;
  `app_base.html` swaps the sidebar for the focus bar. Other pages keep the
  sidebar. Fully responsive.
- **Task-index rail:** a fixed-width left rail lists the lesson's tasks (numbered,
  live done/current/to-do status, titles that wrap — never truncate) with
  jump-to-task, plus a Module › Lesson breadcrumb and a systematic header (tasks
  done · XP · %). The whole room is one contained, centred 74rem grid. On mobile
  the rail collapses to a compact scrollable status strip. `lesson.js` keeps the
  rail in sync and wires the jump links.

### IN-PROGRESS TASK (not started in code — pick this up next)
**"Visually distinguish reading content from interactive activities across ALL
lessons."** The reading/teaching prose and the interactive activity currently
look identical (flat dark), so lessons feel monotonous. The plan (approved
direction, no code written yet): in the **shared** `lesson.html` + `cybaroo.css`,
give the activity a distinct "widget" treatment (tinted/bordered container with
an accent header like "Your task" + a per-kind icon), make callouts/checks/full-
activities visually varied so the eye gets landmarks, and make option buttons
more engaging (hover/selected/correct/wrong). Show ONE reworked lesson (a faithful
artifact preview is a good way, since the dev server can't be screenshotted here)
before it goes everywhere. The `artifact-design` skill was loaded for this. No
files changed yet for it.

---

## 4. Key decisions & deviations from spec (do NOT "fix" back)
| Spec says | We use | Why |
|---|---|---|
| Django 6.0.6 | **5.2 LTS** | 6.0 not LTS; support ends 2026-08. 5.2 → 2028-04. tinymce declares ≤5.2 |
| Python 3.12.4 | **3.13.14** | What's installed; supported by Django 5.2 + PythonAnywhere |
| psycopg2-binary | **psycopg 3** | Django marks psycopg2 as deprecation-track |
| PBKDF2 260k iters | **Django default (1,000,000)** | Spec's number is Django 3.2-era and ~74% *weaker*. Never override `PASSWORD_HASHERS` |
| "ReportLab's FPDF class" | **`reportlab.pdfgen.canvas.Canvas` / `platypus`** | ReportLab has no FPDF class; FPDF is a different library |
| django-otp TOTP app for 2FA | **6-digit code emailed on every login** | Deliberate usability/security trade-off (below). Restores universal coverage the spec wanted; weaker than TOTP, accepted with eyes open |
| Gunicorn on PythonAnywhere | **not used** | PA runs its own WSGI server |

**Why 2FA is an emailed code, not an authenticator app:** installing an
authenticator was too much friction for non-technical Students. An emailed code
removes that barrier so *every* account carries a second factor (matching the
spec on *who* is protected). It is weaker than TOTP (an email code travels the
network and sits in an inbox), which is the accepted cost — our users' realistic
threat is a reused password, not a targeted mailbox breach. **Present this as a
trade-off, not as equivalent to TOTP.**

---

## 5. Important gotchas (critical for a new session)
- **Static caching / `?v=N` cache-buster.** The room scripts in `lesson.html` are
  loaded as `js/lesson.js?v=N` and `js/activities.js?v=N`. **Current version:
  `?v=13`.** After ANY change to `lesson.js`, `activities.js`, or `cybaroo.css`:
  1) **bump `?v=N`** in `lesson.html` (both scripts), 2) run
  `collectstatic --noinput`, 3) **hard-refresh** the browser. In DEBUG (unhashed
  static) a browser will otherwise serve a stale copy via a `304`, which looks
  like "the JS is empty / my change did nothing." This has bitten us repeatedly —
  a `Content-Length: 0` in the Network tab is almost always a `304`, not a real
  empty file.
- **Multi-line `{# … #}` Django comments leak.** Django `{# #}` comments are
  single-line only; a multi-line one renders `{#` literally into the page. Use
  `{% comment %}…{% endcomment %}`. Content/template-hygiene tests check for leaks.
- **`json_script` legitimately contains `}}`.** When scanning rendered HTML for
  template leaks, strip `<script type="application/json">…</script>` blocks first,
  or only check opening tokens `{{` / `{%` / `{#`.
- **Verify JS by executing it, not just loading it.** We use JavaScriptCore
  (`jsc`) with a small DOM shim to actually fire handlers and prove activities
  `cy:solved` (see prior harnesses). Confirm served bytes are non-zero.
- **Voice rule is enforced.** No em-dashes / en-dashes anywhere in lesson or quiz
  content — `test_lesson_content_has_no_em_dashes` / `test_quiz_content_...` fail
  otherwise. Use commas, colons, full stops, parentheses.
- **Test-suite quirks:** tests force **`DEBUG=False`** (so the DEBUG dev-unlock is
  inactive under test and the sequential lock is exercised). Streak/date logic is
  tested by **injecting the date**, never by mocking the clock. The Postgres test
  DB can be held by a stale run — if you see "database test_nstp_db already exists
  / being accessed", `pkill -9 -f pytest` and re-run with `--create-db`. The full
  suite takes ~2 min (it re-seeds real content), so it often lands in the
  background; read the output file for the summary rather than trusting a piped
  exit code.

---

## 6. What's left to do
- **Grading / tier system (client request, NOT built).** Distinction 90–100 /
  Merit 80–89 / Pass 70–79 / Not-yet <70, by quiz score. Show a tier badge per
  module + an overall course grade across the six quizzes; distinct high-perf
  badges (Distinction, Perfect score 100%, "Top of the class" = Distinction
  average); the certificate reflects the overall grade; an admin/instructor view
  of each student's per-module + overall tier. A detailed plan was drafted (best-
  of-attempts drives a module's tier; derive everything from `QuizResult`, no new
  model). Not implemented.
- **Certificate PDF** (ReportLab) — designed on-screen; the downloadable,
  verifiable PDF is not built (plan in §3).
- **Content accuracy review** of all six modules (especially the Optus/Medibank
  facts in M2 and the Privacy Act / NDB material in M6 — kept factual and framed
  as general information, but worth a domain review).
- **Administrator & Instructor dashboards** — still on Django's raw admin; no
  in-app staff oversight page yet.
- **Bespoke simulation pages for Modules 2–6** — currently the generic placeholder
  phishing-inbox; Module 1's is real.
- **The current in-progress visual-distinction task** (§3) — not started in code.
- **Deployment + hosting decision (UNRESOLVED BLOCKER).** PythonAnywhere's free
  tier has **no PostgreSQL** (MySQL is paid; PG is a paid add-on). Options: pay
  (~$10/mo), switch prod to MySQL, or host elsewhere (Render/Fly/Railway free PG).
  **Needs a client decision.**

---

## 7. The 12 models → 4 apps
```
authentication/   User (AbstractUser, email = USERNAME_FIELD), UserProfile
modules/          Module, Lesson, Simulation, ProgressRecord
                  (+ LessonTask, TaskProgress, SimulationResult for the room format)
quizzes/          Quiz, Question, Answer, QuizResult, WrongAnswer
certificates/     Certificate  (UUID4 code, pdf_path — PDF gen not built)
```
Relationships: `User 1─1 UserProfile`; `User 1─* ProgressRecord *─1 Lesson`;
`User 1─* QuizResult *─1 Quiz`; `User 1─* Certificate`; `Module 1─* Lesson (4)`;
`Module 1─1 Simulation`; `Module 1─1 Quiz`; `Quiz 1─* Question (bank of 40, draw
10)`; `Question 1─* Answer (exactly 4, one correct)`; **`Question *─1 Lesson`**
(`lesson_reference` — required by the AFE); `QuizResult 1─* WrongAnswer *─1
Question`; `Lesson 1─* LessonTask *─1 TaskProgress`.

Key fields: `User.role ∈ {STUDENT, INSTRUCTOR, ADMINISTRATOR}`, `is_verified`.
`Module.order_index` (sequential lock), `is_published` (soft delete), difficulty.
`Answer.correct_answer` (bool), **`explanation_text`** (the AFE's fuel).
`Quiz.pass_mark=70`. `LessonTask.kind ∈` the activity enum + CHECK/CONCEPT.
Latest migration: **`modules/migrations/0010_alter_lessontask_kind.py`**.
**Never** hard-delete Modules/Lessons — soft-delete via `is_published=False` /
`is_active=False` (preserves QuizResults).

---

## 8. Working conventions
- **Branch:** work on a feature branch (currently **`feature/login-and-2fa`**) →
  PR → **`BN304-Development`**. **Never commit to `main` directly.** `main` is
  untouched.
- **Repo:** `github.com/aashishdhakal0/Industry-Based-Project-I` (PUBLIC). Remote
  is configured. **Push needs a PAT** (osxkeychain); read is anonymous. Because
  the repo is public, **nothing secret may ever land in a commit** (`.env` is
  gitignored and absent from history).
- **Commit messages** end with:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Git user is "Asis".
- **Voice:** warm, confident, plain **Australian English** (`organisation`, not
  `organization`), one obvious next action per screen, **no em-dashes**.
- **MVT only. ORM only — never raw SQL** (also the SQL-injection control). Business
  logic in views/services; reusable helpers in `<app>/utils.py`. Secrets via
  `config()`. Decorate every view with an auth/role check. `select_related` /
  `prefetch_related` on dashboard + AFE queries. Never `|safe` on unsanitised
  input (lesson HTML is sanitised server-side via nh3 in `save()`).
- **Format:** 4-space indent, double quotes, ~88 cols.
- **Authoring a module:** follow **`docs/module-authoring.md`**; add
  `modules/content/module_<n>.py` and register it in the seed's `CONTENT` dict.

---

## Always do
- Run `.venv/bin/python manage.py check` after touching settings.
- After any JS/CSS change: bump `?v=N`, `collectstatic`, hard-refresh.
- Keep `lesson_reference` on every `Question` — the AFE needs it.
- Write the test alongside the code (Khadka reviews; don't hand him a vacuum).
- Use Django's built-in password hashing, CSRF, template escaping as-is.

## Never do
- **Never** set `AUTH_USER_MODEL` after the first migration.
- Never override `PASSWORD_HASHERS` to the spec's 260k iterations.
- Never use `|safe` on user input; sanitise TinyMCE/lesson HTML server-side.
- Never `DEBUG=True` in production; never commit `.env` or a real `SECRET_KEY`.
- Never hard-delete Modules/Lessons — soft-delete via `is_published=False`.
- Never trust `random.sample()` on a large queryset (loads all rows). Use the
  seed's draw logic / DB-side sampling.
