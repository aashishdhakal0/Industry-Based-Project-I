# Cybaroo (NSTP) — Complete System Explanation

A study guide to the **whole project**, in plain English, referencing the real
files, functions and code. Read it top to bottom to understand everything, or
jump to a part. Written so you can explain any piece to your lecturer and answer
follow-up questions.

**What the project is:** Cybaroo is the product name for the **Network Security
Training Platform (NSTP)** — a web app that teaches essential cyber-safety to
**non-technical Australians** (small businesses, councils, schools) through six
interactive modules, a graded quiz per module, gamification, a personalised
study plan (the Adaptive Feedback Engine), and an administrator console for
overseeing learners. Client: AUSDAIS PTY LTD. Unit: MIT capstone BN304.

> A note on scope: the original design documented "12 models across 4 apps". As
> the build progressed we added the interactive "room" learning format and an
> admin management console, so the running system now has **five apps** and a
> few more models. This document describes what the code actually does today,
> and flags anything not yet built.

---

# PART 1: THE FOUNDATION

## 1.1 The tech stack, and why each piece

Everything is pinned in `requirements.txt`. The versions were chosen
deliberately; the reasons are written into that file's comments.

| Package | Version | What it does | Why this choice |
|---|---|---|---|
| **Python** | 3.13 | The programming language everything is written in. | It is what is installed locally and on PythonAnywhere, and is supported by Django 5.2. The spec said 3.12.4; we standardised on 3.13 at both ends. |
| **Django** | 5.2.16 LTS | The web framework: routing, ORM, templates, auth, admin, security. | 5.2 is a **Long-Term-Support** release supported until April 2028. The spec asked for 6.0.6, but 6.0 is *not* LTS (support ends 2026-08), and `django-tinymce` only declares support through 5.2. Choosing LTS means security patches for the project's whole life. |
| **psycopg[binary]** | 3.2.9 | The PostgreSQL database driver (lets Python talk to Postgres). | The spec said `psycopg2-binary`, but Django's own docs flag psycopg2 as heading for deprecation; **psycopg 3** is recommended for new work. |
| **django-ratelimit** | 4.1.0 | Limits how often an IP can hit a view (brute-force defence). | Used on the login views (10 requests/hour/IP). |
| **django-csp** | 4.0 | Adds a **Content-Security-Policy** HTTP header, controlling what the browser is allowed to load/run. | A strong defence against cross-site scripting (XSS): even if malicious script got onto a page, the browser refuses to run it. |
| **django-tinymce** | 5.0.0 | A rich-text editor for authoring lesson content in the admin. | Lets non-developers write formatted lessons. Its HTML output is sanitised before storage (see nh3). |
| **Pillow** | 11.3.0 | Image handling (used by the avatar `ImageField`). | Django needs it for any image upload field. |
| **nh3** | 0.3.6 | **HTML sanitiser** — strips dangerous tags/attributes from stored HTML. | The stored-XSS control. Rust-based, maintained (the old `bleach` is deprecated). Applied in `Lesson.save()` / `LessonTask.save()`. |
| **reportlab** | 5.0.0 | PDF generation library. | For the downloadable certificate (designed; PDF generation is planned, see Part 6). The spec mentioned "ReportLab's FPDF class" — no such class exists; FPDF is a different library. |
| **python-decouple** | 3.8 | Reads settings/secrets from a `.env` file via `config()`. | Keeps secrets (SECRET_KEY, DB password) out of the code and out of the public git repo. |
| **whitenoise** | 6.12.0 | Serves static files (CSS/JS) directly from Django in production. | Simple static serving without a separate web server, fine for PythonAnywhere. |
| **pytest / pytest-django** | 8.4.1 / 4.11.1 | The test framework. | Cleaner, more expressive tests than Django's built-in runner. |
| **coverage** | 7.10.1 | Measures how much code the tests exercise. | Shows gaps in test coverage. |

**Database:** PostgreSQL 18 (`nstp_db`), matching the spec. Configured in
`settings.py` `DATABASES`. Local development is Postgres-only.

## 1.2 Project structure — the apps and folders

Django organises code into **apps** (self-contained feature modules). Ours:

```
nstp_project/
├── nstp/                 ← the project config (settings, root URLs, WSGI)
│   ├── settings.py       ← all configuration
│   ├── urls.py           ← the root URL map
│   └── context_processors.py  ← injects {{ site_name }} into every template
├── authentication/       ← accounts: User, login, 2FA, registration, roles
├── modules/              ← the learning content: modules, lessons, tasks, gamification
├── quizzes/              ← the quiz engine + the Adaptive Feedback Engine
├── certificates/         ← the completion certificate model (PDF planned)
├── staff/                ← the Administrator management console (added later)
├── templates/            ← shared HTML templates (app_base.html, etc.)
├── static/               ← CSS (cybaroo.css) and JS (activities.js, lesson.js)
├── docs/                 ← specifications and this document
├── requirements.txt      ← pinned dependencies
├── manage.py             ← Django's command-line entry point
└── .venv/                ← the Python virtual environment
```

**What lives where (the rule of thumb):** models describe data, views handle
requests, templates render HTML, `services.py`/`gamification.py`/`grading.py`
hold reusable business logic, `urls.py` maps URLs to views, and `tests/` proves
it all works. Business logic is kept out of templates and (mostly) out of views.

## 1.3 How Django works, using our project as the example

Django follows **MVT: Model – View – Template** (its take on MVC).

- **Model** = a Python class describing a database table. Example:
  `modules/models.py::Module` describes the `modules` table. You never write SQL
  — you use the **ORM** (Object-Relational Mapper): `Module.objects.filter(
  is_published=True)` becomes a `SELECT ... WHERE is_published = true`.

- **View** = a Python function that takes a web request and returns a response.
  Example: `modules/views.py::dashboard(request)` gathers a student's real
  progress and renders a template.

- **Template** = an HTML file with placeholders. Example: `dashboard.html` uses
  `{{ profile.points }}` and `{% for %}` loops to display the data the view
  passed in.

**The request lifecycle** (what happens on every page load):

1. The browser requests a URL, e.g. `/learn/m/1/`.
2. Django looks it up in `nstp/urls.py`, which `include()`s `modules/urls.py`,
   which maps `m/<int:order_index>/` to `views.module_overview`.
3. **Middleware** runs first (listed in `settings.py MIDDLEWARE`): security
   headers, the CSP header, session loading, CSRF checking, authentication.
4. The **view** runs: it queries the database via the ORM, applies logic, and
   picks a template.
5. The **template** renders to HTML, which is returned to the browser.

**URLs:** `nstp/urls.py` is the root map. It routes `/admin/` to Django's admin,
`/dashboard/` to the student dashboard, `/learn/` into `modules/urls.py`,
`/manage/` into `staff/urls.py`, and everything else into
`authentication/urls.py`.

**Migrations:** when you change a model, Django generates a **migration** (a
versioned script describing the schema change) with `makemigrations`, and
applies it to the database with `migrate`. Migrations live in each app's
`migrations/` folder. Example: `authentication/migrations/0002_...` added the
`flagged` field to `UserProfile`. This is how the database schema stays in sync
with the models, reproducibly, across machines.

**The ORM (a few real examples):**
- `Module.objects.filter(is_published=True).order_by("order_index")` — the six
  modules in order.
- `ProgressRecord.objects.filter(user=user).values("lesson__module").annotate(
  n=Count("lesson"))` — how many lessons a student has done, grouped by module,
  in one query (aggregation, done in the database, not in Python).
- `select_related` / `prefetch_related` — pre-load related rows in one query to
  avoid the "N+1" problem (one query per row). Used heavily on the dashboard and
  the AFE.

## 1.4 The database — every model and how they relate

Models grouped by app, with their key fields and the reason for the design.

### authentication
- **`User`** (table `users`) — a platform account. Extends Django's
  `AbstractUser`. Key fields: `email` (unique, the login identifier),
  `role` ∈ {STUDENT, INSTRUCTOR, ADMINISTRATOR}, `is_verified` (has the email
  link been used), plus Django's `is_active`, `is_staff`, `is_superuser`.
  `username` is removed (`username = None`). See §1.5.
- **`UserProfile`** (table `user_profiles`) — one-to-one with `User`. Holds
  gamification/profile state: `organisation`, `avatar`, `last_active`,
  `streak_count`, `points` (a **cache**, see Part 4), `badges` (a JSON list of
  earned badge ids), and `flagged` / `flag_reason` (admin "needs attention").
  *Why separate from User:* keeps login/identity concerns apart from
  progress/display concerns.

### modules
- **`Module`** (table `modules`) — one of the six courses. Fields: `title`,
  `description`, `difficulty`, `duration_minutes`, `order_index` (drives the
  sequential lock), `is_published` (**soft-delete** flag — we never hard-delete
  content), `created_by`.
- **`Lesson`** (table `lessons`) — belongs to a Module (`module` FK). Fields:
  `lesson_number` (order within the module), `title`, `body_text` (HTML,
  sanitised on save), `reading_time_minutes`, `is_active` (soft-delete).
  Constraint: `unique(module, lesson_number)`.
- **`Simulation`** (table `simulations`) — one per module; the branching
  scenario. `scenario_text`, `decision_points` (JSON tree), `outcome_text`
  (JSON). *Why JSON:* a branching tree can't fit in one flat text field.
- **`ProgressRecord`** (table `progress_records`) — **one row per lesson a
  student completes**. `user` FK, `lesson` FK, `completed_at`. Constraint:
  `unique(user, lesson)` — a lesson counts once, so re-reading can't inflate
  points. This table is the *source of truth* for progress.
- **`LessonTask`** (table `lesson_tasks`) — one interactive step ("panel")
  inside a lesson. `kind` (the activity type enum), `task_key`, `order`,
  `points`, `title`, `body` (sanitised HTML), `diagram_key`, `payload` (JSON
  config for the interactive widget). Constraint: `unique(lesson, task_key)`.
- **`TaskProgress`** (table `task_progress`) — one row per task a student
  finishes. `unique(user, task)`. When a student has a row for every task in a
  lesson, the engine banks the whole lesson via a `ProgressRecord`.
- **`SimulationResult`** (table `simulation_results`) — one row per simulation
  run. `score`, `total`, `path` (JSON of the decisions made). `unique(user,
  simulation)` — re-running overwrites rather than piling up.

### quizzes
- **`Quiz`** (table `quizzes`) — one per module (`OneToOne`). `pass_mark`
  (default 70), `time_limit_minutes`, `is_active`.
- **`Question`** (table `questions`) — belongs to a Quiz. `question_text`,
  `difficulty`, `ordering`, and crucially **`lesson_reference`** (FK to the
  Lesson that teaches this topic). *Why:* the Adaptive Feedback Engine uses it to
  tell you which lesson to revise. `on_delete=PROTECT` so you can't delete a
  lesson that questions depend on.
- **`Answer`** (table `answers`) — one of four options for a Question.
  `option_text`, `correct_answer` (bool — exactly one is true), and
  **`explanation_text`** (why this option is right/wrong — the AFE's fuel).
- **`QuizResult`** (table `quiz_results`) — one row per attempt. `user`, `quiz`,
  `score` (percentage), `passed` (bool), `attempt_number`, `submitted_at`.
  Constraint: `unique(user, quiz, attempt_number)`.
- **`WrongAnswer`** (table `wrong_answers`) — one row per answered-wrong
  question in an attempt. `quiz_result`, `question`, `student_answer` (what they
  picked), `correct_answer` (what they should have). The AFE's durable input.

### certificates
- **`Certificate`** (table `certificates`) — issued when a student passes all six
  quizzes. `code` (a UUID4 public verification id), `issued_at`, `pdf_path`. The
  model exists; the PDF generation and public verify page are planned (Part 6).

### staff
- **`AdminAction`** (table `admin_actions`) — the **audit log**. `actor` (which
  admin), `action` (add_user, role_change, deactivate, …), `target_user`,
  `summary`, `created_at`. Append-only in practice; `on_delete=SET_NULL` so the
  record survives even if the actor's account is later deleted.

**How they relate (the map):**
```
User 1─1 UserProfile
User 1─* ProgressRecord *─1 Lesson
User 1─* QuizResult *─1 Quiz
User 1─* TaskProgress *─1 LessonTask
User 1─* Certificate
User 1─* AdminAction (as actor and as target)
Module 1─* Lesson (4 each)
Module 1─1 Simulation, Module 1─1 Quiz
Lesson 1─* LessonTask
Quiz 1─* Question (a bank of ~40; 10 drawn per attempt)
Question 1─* Answer (exactly 4, one correct)
Question *─1 Lesson  (lesson_reference — required by the AFE)
QuizResult 1─* WrongAnswer *─1 Question
```

**Why the schema is shaped this way:** the central design principle is
**"records are the truth"**. Progress and achievement are stored as *event rows*
(`ProgressRecord`, `QuizResult`, `TaskProgress`, `WrongAnswer`), never as
mutable counters. Anything derived — points, level, module completion %, grade —
is *recomputed* from those rows on demand. That makes the data impossible to
corrupt by a missed increment and impossible to cheat by replaying an action
(the `unique(...)` constraints stop double-counting). See Part 4.

## 1.5 The custom user model — email login, set before the first migration

Ordinarily Django logs users in by **username**. We log in by **email**, because
a username is one more thing a non-technical adult has to invent and remember;
their email is something they already know. That requires a **custom user
model** (`authentication/models.py::User`):

```python
class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"

    username = None                                   # remove username entirely
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"        # log in with email
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()         # a manager that creates users keyed on email
```

`UserManager` (same file) overrides `create_user`/`create_superuser` to require
an email instead of a username.

**"Set before the first migrate":** the setting
`AUTH_USER_MODEL = "authentication.User"` (in `settings.py`) tells Django which
model is the user. This *must* be set before the very first `migrate`, because
half the database (permissions, foreign keys to the user) is built around it.
Changing it afterwards is famously painful — so it was fixed at the start and
must never change. The settings file carries a comment saying exactly this.

---

# PART 2: AUTHENTICATION & SECURITY

## 2.1 Registration and email verification

**The flow** (`authentication/views.py::register`):
1. A visitor fills in `RegistrationForm` (first/last name, email, password,
   optional organisation). Notice what is **absent**: a `role` field. Letting a
   user pick their own role would be a privilege-escalation hole (anyone could
   register as Administrator), so `RegistrationForm.save()` forces it:
   ```python
   user.role = User.Role.STUDENT
   user.is_active = False      # cannot log in yet
   user.is_verified = False    # records *why* they're inactive
   ```
   `is_active = False` is the real enforcement: Django's `ModelBackend` refuses
   to authenticate an inactive user *automatically*, so even a forgotten check
   in a view cannot let an unverified account in.
2. The user and their `UserProfile` are created together in a database
   **transaction** (`transaction.atomic`) — either both exist or neither does.
3. A verification email is sent containing a signed link, and the user is shown
   a "check your inbox" page.

**The signed, time-limited token** (`authentication/tokens.py`): we do **not**
store tokens in a database. Instead we use `django.core.signing`:
```python
def make_verification_token(user):
    return signing.dumps({"uid": user.pk}, salt=VERIFICATION_SALT)
```
`signing.dumps` packs the user id into a string and signs it with the project's
`SECRET_KEY`. The link is `/verify/<token>/`. When opened,
`read_verification_token` calls `signing.loads(token, salt=..., max_age=48h)`,
which:
- fails with `BadSignature` if the token was tampered with (the signature won't
  match), or
- fails with `SignatureExpired` if it's older than 48 hours.

*Why no token table:* nothing to store, migrate, clean up, or leak. The `salt`
namespaces the signature so a verification token can't be replayed against some
other signed feature. The trade-off: a signed token is replayable until it
expires — so the `verify` view is written to be **idempotent** (clicking twice
is harmless; an already-verified account is just told "you're good").

On success, `verify` sets `is_verified = True` and `is_active = True`, and the
account can now log in.

## 2.2 Login and the emailed 6-digit 2FA code

Login is **two factors**: password, then a 6-digit code emailed to the user.
The subtle, important design decision is that **no session exists until *both*
factors pass**. Between the two steps only a user id sits in the session — that
is not a login, so it can't reach any protected page.

**Step 1 — password** (`authentication/views.py::login_view`):
- Rate-limited to 10 POSTs/hour/IP (`@ratelimit`); over the limit renders a
  plain-language 429 page.
- Django's `AuthenticationForm` checks the email + password (against the PBKDF2
  hash — see §2.4). The password is never stored or compared in plain text.
- On success it does **not** log the user in. It generates a code, stores a
  *hash* of it in the session, and emails the code:
  ```python
  code = make_login_code()
  _start_pending(request, user, next_target, hash_login_code(code))
  _send_login_code(request, user, code)
  return redirect("authentication:login_code")
  ```

**Generating the code** (`authentication/utils.py::make_login_code`):
```python
upper = 10 ** settings.LOGIN_CODE_LENGTH        # 1_000_000
return str(secrets.randbelow(upper)).zfill(settings.LOGIN_CODE_LENGTH)
```
It uses **`secrets`**, not `random`. `random` is a Mersenne-Twister PRNG seeded
from the clock and its output is predictable from prior output — fine for
shuffling quiz questions, catastrophic for a security code. `secrets` is
cryptographically secure. `zfill` zero-pads so every code is exactly 6 digits
(a variable-length code leaks information and looks broken).

**Storing the code** (`hash_login_code`): the code is **hashed** before it goes
in the session, with `salted_hmac(..., code)` keyed off `SECRET_KEY`. Sessions
get dumped into logs and fixtures; storing the code in plain text there would be
careless. It's a fast hash on purpose — this is a 6-digit number with a
10-minute life and a 5-attempt cap, not a password.

**Step 2 — the code** (`login_code` view):
- `_pending_user(request)` returns the half-authenticated user only if the
  pending id exists, the account is still active, and it's within the 10-minute
  window (`PENDING_MAX_AGE`). An abandoned half-login expires — "a loaded gun on
  a shared machine".
- The submitted code is compared with `check_login_code`, which uses
  **`constant_time_compare`** (not `==`). Ordinary string comparison returns as
  soon as it finds a difference, so *how long it takes* leaks how much of the
  code was right — a real timing attack on a 6-digit secret. Constant-time
  comparison closes that.
- **Attempt cap:** the session counts attempts; after
  `LOGIN_CODE_MAX_ATTEMPTS` (5) the code is destroyed and the user must start
  over (which emails a fresh code to the victim's inbox — a signal something's
  wrong). Six digits is a million combinations; without a cap an attacker who
  has the password could just try them all.
- **Single-use / expiry:** the pending state is cleared on success
  (`_clear_pending`), on too many attempts, and on timeout. `resend_login_code`
  issues a fresh code and resets the attempt count but **not** the clock, so
  pressing "resend" forever can't hold a half-login open indefinitely.

Only when the code checks out does `_complete_login` call Django's `login()`,
creating the real session, and route the user by role.

**Why an emailed code rather than an authenticator app (TOTP):** installing an
authenticator was too much friction for non-technical users, and the result was
that many accounts would have *no* second factor at all. An emailed code removes
the barrier so **every** account carries a second factor. It is weaker than TOTP
(the code travels the network and sits in an inbox) — this is a **documented,
accepted trade-off**, framed honestly, not a claim of equivalence. Our users'
realistic threat is a reused password, not a targeted mailbox breach.

## 2.3 Role-based routing and the "log in as…" buttons

After login, `authentication/utils.py::role_home_url` decides where the user
lands:
```python
if user.role == User.Role.ADMINISTRATOR:
    return reverse("staff:overview")     # the in-app admin dashboard
return reverse("dashboard")              # students (and instructors) → dashboard
```
Administrators go to the Cybaroo admin console; everyone else to the student
dashboard. `/admin/` (Django's raw admin) stays available separately.

**The login page's two big buttons** ("Log in as Student" / "Log in as
Administrator") are an *institutional-style* front door (like a university's
"sign in" page). The critical security property: **choosing a button does not
grant a role.** The button only carries a cosmetic `?as=student|admin` value
that changes the form's heading. Authentication is unchanged — the role a user
actually ends up with is always read from **their account** in
`role_home_url`, never from the button. So clicking "Log in as Administrator"
and typing a Student's credentials signs you in as that Student. `login_view`
validates the `as` value against a fixed set and ignores anything else; there is
no `<select role>` anywhere. (Tested in
`authentication/tests/test_role_login.py`.)

There are also **demo accounts** (`seed_demo_accounts` command) with known
credentials so a supervisor can review both experiences through the normal
secure form. There is no login *bypass* in the codebase.

## 2.4 Every security measure, explained

- **Password hashing (PBKDF2).** Django never stores passwords; it stores a
  one-way **PBKDF2** hash (salted, ~1,000,000 iterations in Django 5.2). We
  deliberately do **not** override `PASSWORD_HASHERS`: the spec's "260,000
  iterations" is Django 3.2-era and ~74% weaker. `AUTH_PASSWORD_VALIDATORS`
  enforces minimum length, not-common, not-all-numeric, not-similar-to-your-
  details.
- **Rate limiting** (`django-ratelimit`). The login views are capped at
  10/hour/IP so the password/code steps aren't a free brute-force target.
- **Content-Security-Policy** (`django-csp`, configured in `settings.py`):
  ```python
  "script-src": ["'self'"],          # only our own JS may run
  "img-src": ["'self'", "data:"],
  "frame-ancestors": ["'none'"],     # the site can't be framed (clickjacking)
  ```
  Even if an attacker injected a `<script>`, the browser would refuse to run it
  because it isn't from `'self'`. (This is why our JS uses no inline handlers.)
- **HTML sanitisation with nh3.** Lesson HTML renders **unescaped** so authors
  can format it — which would be a stored-XSS hole if raw HTML were stored.
  `modules/models.py::sanitise_lesson_html` runs every lesson/task body through
  `nh3.clean` against an **allow-list** (`h2,h3,p,ul,strong,a,img,…`) on
  `save()`, stripping `<script>`, `<iframe>`, event handlers and `javascript:`
  URLs, and forcing `rel="noopener noreferrer"` on links. *Sanitising on the way
  in* means the database only ever holds clean HTML, so every read path is safe
  by construction — you can't forget to sanitise at a call site. (Tested in
  `modules/tests/test_sanitiser.py`.)
- **CSRF protection.** Django's built-in Cross-Site-Request-Forgery tokens
  protect every POST form (`{% csrf_token %}`); logout and all state-changing
  admin actions are POST-only so they can't be triggered by a stray `<img>` tag.
- **Least-privilege database role.** The app connects to Postgres as a role
  (`nstp`) that has only the privileges it needs, owning nothing it shouldn't —
  so a compromise of the app can't, say, drop unrelated databases.
- **The admin audit log** (`staff.AdminAction`). Every privileged action records
  who did it, to whom, and when — the difference between an incident you can
  investigate and one you can't.
- **Admin safeguards.** You **cannot change your own role or deactivate
  yourself**, and you **cannot demote/deactivate the last active
  Administrator** — so no sequence of clicks can lock the platform out of its own
  administration (`staff/useractions.py`, §7).
- **Secure cookies / transport (production).** When `DEBUG=False`:
  `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS for
  a year, `X_FRAME_OPTIONS = "DENY"`, `SECURE_CONTENT_TYPE_NOSNIFF`. Cookies are
  `HTTPONLY` always.
- **No secrets in the repo.** `SECRET_KEY`, DB password, etc. come from `.env`
  via `python-decouple`; `.env` is gitignored and never committed (the repo is
  public).
- **The ORM only, never raw SQL** — which also means SQL injection is not
  possible, because user input is always parameterised by the ORM.

---

# PART 3: THE LEARNING SYSTEM

## 3.1 Modules, lessons, and the interactive task system

There are **six modules**, each with **four lessons**. A lesson is not a wall of
text — it is a **TryHackMe-style "room"**: a scrollable column of numbered,
collapsible **task panels** (`LessonTask` rows), each teaching one small thing
and then making you *do* something. A panel's `kind` decides what it is:

- **CONCEPT** — a short teaching intro with a "Mark as complete" button.
- **CHECK / inline_check** — an apply-it multiple-choice question (question +
  hint + 4 options, each with its own explanation).
- an **interactive activity** — driven by JavaScript from a CSP-safe JSON
  `payload` (see below).

Content is authored as plain Python data in `modules/content/module_<n>.py`
(`LESSONS` + `QUIZ`) and **seeded** into the database rows by the
`seed_learning_content` management command. Authoring in code and seeding into
rows means the lesson view and the progress logic can stay generic and
database-driven.

**The interactive activities** (config in `LessonTask.payload`, rendered by
`static/js/activities.js`). Each activity type is a controller in a
`CONTROLLERS` registry; each reads its JSON config from a
`<script type="application/json">` block (Django's `json_script` filter) and,
when the learner finishes, fires a bubbling **`cy:solved`** DOM event:

| Kind | What the learner does |
|---|---|
| **sort** | Tap a chip, tap the bucket it belongs in (e.g. sort items into the CIA triad). |
| **inbox** | Inspect one email broken into zones and tap every suspicious "tell". |
| **spot** | Two cards (or a fake login-page mock-up) — click the scam one. |
| **password** | Type into a live strength meter + checklist; solved at "Strong". |
| **branch** | A multi-step scenario with consequences; solved at an ending. |
| **classify** | Read each alert, pick its category from a shared list, get teaching feedback. |
| **mailsort** | A mixed inbox; mark each whole email Genuine or Phishing. |
| **harden** | Secure each part of a fictional workspace, "At risk" → "Secured". |
| **netmap** | Tap every weakness on a network map. |
| **sequence** | Put shuffled steps into the correct order (e.g. the incident-response lifecycle). |
| **respond** | Realistic "what would you do?" situations — pick the sound action, see the consequence. |

**How it's wired** (`static/js/lesson.js`): each panel can hold "slots"
(a check block, an activity, or a mark-complete button). When an activity fires
`cy:solved`, a single delegated listener on the room finds the panel and calls
`satisfySlot(panel)`; when all a panel's slots are done, `markPanelDone` fires,
which POSTs completion to the server and updates the XP bar, the progress ring,
and the task-index rail. If JS fails or a config is broken, a `fallback` lets the
learner continue rather than getting stuck. Correctness of the *formative*
activities is judged client-side for instant feedback; the *graded* assessment is
the quiz (graded server-side, trusting nothing from the client — Part 5).

## 3.2 Sequential module locking — enforced server-side (the 403)

You can only open Module N once Module N−1 is complete. This is a **real access
control**, not a hidden link. `modules/gamification.py::module_progress` computes
each module's `unlocked` flag (the previous module must be complete), and every
content view checks it and returns a real **HTTP 403** if you jump ahead:

```python
# modules/views.py::module_overview
if not g.is_module_unlocked(request.user, module):
    return _locked_response(request, module)   # renders modules/locked.html, status=403
```

The same guard sits on `lesson`, `simulation`, and the quiz views. Hiding a link
in the template is *presentation*; the 403 in the view is the *control*. (A
DEBUG-only switch unlocks everything in local development for content review;
production and the test suite keep the lock — `settings.DEBUG` gated. The 403 is
directly tested: `modules/tests/test_views.py::test_a_locked_module_overview_
returns_403` and friends.)

## 3.3 How progress is recorded as a student works

1. A student finishes a task → the browser POSTs to
   `modules/views.py::complete_task`.
2. That view calls `modules/gamification.py::complete_task(user, task)`, which
   creates a `TaskProgress` row (`unique(user, task)`, so it's idempotent).
3. When the student has a `TaskProgress` row for **every** task in the lesson,
   the engine banks the whole lesson by creating a `ProgressRecord`
   (`unique(user, lesson)`) worth `POINTS_PER_LESSON` (10), and recomputes the
   profile.
4. `complete_task` returns JSON — points done, whether the lesson completed, and
   the reward for the celebration overlay — which `lesson.js` uses to animate the
   bar and pop the reward.

So the durable truth is a trail of `TaskProgress` and `ProgressRecord` rows; the
XP bar is just those rows counted.

---

# PART 4: GAMIFICATION

Everything gamified lives in `modules/gamification.py`. Its guiding rule, stated
at the top of the file:

> **Records are the truth, the profile is a cache.**

`UserProfile.points` is **never incremented**. It is **recomputed** from the
records every time something changes:

```python
POINTS_PER_LESSON = 10
POINTS_PER_QUIZ = 50

def points_from_counts(counts):
    return (counts["lessons_completed"] * POINTS_PER_LESSON
            + counts["passed_quizzes"] * POINTS_PER_QUIZ)
```

`_counts(user)` derives `lessons_completed` from `ProgressRecord` rows and
`passed_quizzes` from **distinct** passed `QuizResult` rows.
`refresh_profile(user)` recomputes points, streak and badges and saves them.

**Why recompute instead of increment?** Two reasons:
- **It cannot drift.** An incrementing counter goes wrong the first time an
  increment is missed or double-applied, and then it's silently wrong forever.
  A recomputed value is always exactly what the records say.
- **It cannot be cheated.** Because points come from *distinct* passed quizzes
  and *unique* lesson rows, replaying an action does nothing — passing a quiz you
  already passed adds no points; re-reading a lesson adds nothing. The
  `unique(...)` database constraints enforce this at the lowest level.

**Levels** are a **pure function of points** — never stored:
```python
def _points_to_reach(level):
    return 10 * (level - 1) * (level + 2)     # 40, 100, 180, 280, 400, 540 …
```
`level_for_points(points)` finds the level and how far through it you are. All 24
lessons + 6 quizzes = 540 XP lands exactly on level 7, so the ceiling maps to
finishing the course. Each level also has a **rank name** (`RANKS`: "Cyber
Aware" → "Cyber Legend").

**Streaks** advance on activity. `streak_status(profile)` interprets the stored
`streak_count` against `last_active`: if the last activity was today it's
"safe", yesterday it's "at risk", older and the streak has **lapsed** and it
honestly shows 0 (it never displays a stale number). Streak/date logic takes an
injectable date so it can be tested without mocking the clock.

**Badges** are a catalogue in code (`modules/badges.py`, 11 badges across tiers:
first lesson, streaks, module completions, perfect scores, etc.). Earned badge
ids live in `UserProfile.badges` (a JSON list). Badges are awarded **one-way**
from the stats during `refresh_profile` (`badge_catalogue.newly_earned`), so once
earned they stay earned.

---

# PART 5: THE QUIZ + ADAPTIVE FEEDBACK ENGINE (the signature feature)

## 5.1 Taking a quiz — draw, take, save-as-you-go, grade server-side

**Drawing the paper** (`quizzes/services.py::draw_questions`): each quiz has a
bank of ~40 questions; **10 are drawn at random per attempt**:
```python
quiz.questions.prefetch_related(
    Prefetch("answers", queryset=Answer.objects.order_by("id"))
).order_by("?")[:n]
```
`order_by("?")` randomises **in the database** (`ORDER BY RANDOM()`) and then
slices to 10 — it never loads the whole bank into Python (the trap CLAUDE.md
warns about with `random.sample()` on a queryset).

**The gate** (`quizzes/views.py::quiz`): the quiz opens only if the module is
unlocked (`is_module_unlocked`, 403 if not) **and** every lesson in it is done
(`_all_lessons_done`, else redirected back to finish the lessons) — learn first,
then prove it.

**Holding the paper stable:** the drawn question ids and the answers-so-far are
stored in the **session** (`SESSION_KEY = "quiz_attempt"`), so a refresh can't
redraw a different set of questions or wipe progress.

**Save-as-you-go** (`save_answer`): as the student picks each option, a small
`fetch` POST records it into the session (progressive enhancement). The final
form submit is still authoritative; this just means a mid-quiz refresh doesn't
lose answers.

**Grading — server-side, never trusting the client**
(`quizzes/services.py::grade_and_record`):
- The presented questions are re-loaded from the database by id, with their real
  answers.
- `_grade` looks up each chosen answer id **against the question's own options
  from the database** and checks the stored `correct_answer` flag. The client
  only ever sends *which option id* it picked; it can't tell the server that a
  wrong answer is right.
- `score_of` = percentage correct over all 10 (blanks count as wrong).
- `passed = score >= quiz.pass_mark` (70%).
- A `QuizResult` row is created (with the next `attempt_number`), and the reward
  comes from `refresh_profile` recomputing from truth (so a first pass yields
  +50 and any quiz badges; a repeat pass yields no fresh points).

## 5.2 How wrong answers are recorded

In the same transaction, one **`WrongAnswer`** row is created per
answered-but-wrong question:
```python
WrongAnswer.objects.bulk_create([
    WrongAnswer(quiz_result=result, question=gq.question,
                student_answer=gq.chosen, correct_answer=gq.correct)
    for gq in graded
    if gq.answered and not gq.is_correct and gq.correct is not None
])
```
Each row remembers **what the student picked** and **what was correct**. (A blank
scores as wrong but records no row — there's no chosen option to store.) These
rows are the durable input the Adaptive Feedback Engine reads.

## 5.3 The Adaptive Feedback Engine (AFE), step by step

This is the product's differentiator. Instead of "you scored 60%", it turns a
graded attempt into a **personalised study plan**. It lives in
`quizzes/feedback.py::analyse(quiz_result)` and is **pure and read-only** — it
runs on every result view, in essentially one prefetched query so it never N+1s
(a test, `test_analyse_is_a_single_query`, enforces this).

Step by step:

1. **Load the mistakes.** Read the attempt's `WrongAnswer` rows, prefetching in
   one query the question, the question's `lesson_reference` (and that lesson's
   module), and both the chosen and correct `Answer` rows:
   ```python
   wrongs = (WrongAnswer.objects.filter(quiz_result=quiz_result)
             .select_related("question", "question__lesson_reference",
                             "question__lesson_reference__module",
                             "student_answer", "correct_answer")
             .order_by("question__ordering"))
   ```
2. **Explain each mistake.** For each wrong answer, build a `FeedbackItem`
   carrying the question text, *your* option and **why it's wrong**
   (`student_answer.explanation_text`), the correct option and **why it's right**
   (`correct_answer.explanation_text`), and the source lesson. The explanations
   are the ones authored on each `Answer` — the whole product rests on the
   quality of that field.
3. **Trace each mistake to its lesson.** Every `Question` has a
   `lesson_reference`. As we walk the wrong answers we tally mistakes per lesson
   in a dictionary `by_lesson = {lesson_id: [lesson, count]}`.
4. **Rank the lessons.** Build a `RevisionLesson` per lesson, sorted **most-
   missed first** (ties fall back to reading order):
   ```python
   for lesson, count in sorted(by_lesson.values(),
       key=lambda e: (-e[1], e[0].module.order_index, e[0].lesson_number)):
   ```
5. **Return the plan.** A `Feedback` object with the itemised explanations and
   the ranked "revise these lessons" plan, shown on the result page.

**Worked example (a student gets 3 wrong):** Suppose on the Module 3 (Phishing)
quiz the student misses Q2, Q5 and Q9. Q2 and Q9 both trace (via
`lesson_reference`) to *Lesson 1 — "The con behind the click"*; Q5 traces to
*Lesson 4 — "Reading an email like an investigator"*. The AFE:
- creates 3 `FeedbackItem`s, each saying *"You chose X — [why X is wrong]. The
  answer was Y — [why Y is right]."*
- tallies: Lesson 1 → 2 mistakes, Lesson 4 → 1 mistake.
- produces the plan **["Lesson 1 (2 mistakes)", "Lesson 4 (1 mistake)"]**, most-
  missed first, each with its reading time.

So the student doesn't just see a score — they see *exactly which two lessons to
revise, in priority order, and why each answer was wrong*. That is the Adaptive
Feedback Engine.

---

# PART 6: CERTIFICATES & GRADING

## 6.1 The certificate (on-screen now; PDF planned)

When a student completes all six modules, the **Certificate** page
(`modules/views.py::certificate`) renders a premium on-screen certificate design
populated with their real data (name, the six modules) and a progress state
until all six are done. Each student gets a **stable sample verification code**
derived with `uuid.uuid5` from their id, so it looks like a real credential
without pretending to be one.

The **downloadable, verifiable PDF is not yet built**. The plan (and the model)
exist: `certificates/models.py::Certificate` has a UUID4 `code` and a `pdf_path`;
the intent is to generate the PDF lazily with **ReportLab** on first download,
cache it under `MEDIA_ROOT/certificates/`, and expose a public `/verify/<code>/`
page so anyone can confirm a certificate is genuine. `certificates/views.py` is
currently an empty stub and the app is not yet routed in `nstp/urls.py`. (The
spec's "ReportLab FPDF class" is a mistake — ReportLab has no such class; the
real tools are `reportlab.pdfgen.canvas.Canvas` or `reportlab.platypus`.)

## 6.2 The grading tiers (Distinction / Merit / Pass)

`modules/grading.py` turns quiz scores into performance tiers — a client
request. It is **pure and derived entirely from `QuizResult`** (no grade field,
no new model). The bands:

```python
DISTINCTION  ≥ 90
MERIT        80–89
PASS         70–79
NOT_YET      0–69          # attempted but below the pass mark
NOT_STARTED                # never attempted a quiz
```

- `tier_for_score(score)` maps a percentage to a band (None → NOT_STARTED).
- `best_scores_by_module(user)` gets, in one query, the student's **best** score
  per module (`Max("score")`), so a strong retake counts, not an early fail.
- `module_tier(user, module)` = the tier of that module's best score.
- `overall_grade(user)` / `grade_from_scores(scores)` = the tier of the **mean**
  of the best scores across the modules the student has attempted (an untouched
  module doesn't drag the average down).

Because it reads the same `QuizResult` rows the gamification engine trusts, a
grade can never disagree with "did they pass". The admin dashboard (Part 7) shows
each learner's per-module and overall tier, and a distribution across the cohort.
(Band maths tested in `staff/tests/test_grading.py`.)

---

# PART 7: THE ADMIN MANAGEMENT CONSOLE (the `staff` app, at `/manage/`)

A polished in-platform experience so Administrators don't have to use Django's
raw `/admin/`. Every view is behind `authentication/decorators.py::
administrator_required`, which returns a real **HTTP 403** for a signed-in
non-administrator and redirects anonymous users to log in — a control, not a
hidden menu.

**Overview** (`/manage/`) — a personalised welcome header, KPI cards (total
learners, completed the course, completion rate as a donut, average score), a
grade-tier distribution, a "learners by organisation" bar chart, a "needs
attention" list (flagged learners + a 14-day-inactive heuristic), and a recent-
activity feed from the audit log. It has three states: a designed empty state
(no accounts), an encouraging "quiet" state (accounts exist but nobody's
started — instead of rows of zeros), and the full populated dashboard.

**Learners** (`/manage/learners/`) — a sortable, filterable table of every
Student: modules completed, grade tier, points, last active. Sort by name /
completion / grade / activity; filter by tier; **export to CSV**. The data is
assembled in `staff/services.py::collect_learners` in a **fixed number of
aggregate queries** regardless of learner count (dashboards are the classic N+1
risk).

**Learner detail** (`/manage/learners/<id>/`) — one person's full picture:
per-module progress and grade, every quiz attempt, badges, an activity timeline,
and the **action panel**.

**The actions** (each its own POST endpoint in `staff/useractions.py`, admin-
only, CSRF-protected, and written to the audit log):
- **Change role** (Student / Instructor / Administrator).
- **Activate / deactivate** an account.
- **Resend verification** email.
- **Nudge** — email the learner an encouraging reminder.
- **Flag / unflag** as "needs attention" (with an optional reason).
- **Add user** (`/manage/users/new/`) — create a staff member or student and
  assign a role. An admin assigning a role is legitimate (unlike self-service
  sign-up). Promoting to Administrator grants the in-app dashboard only, **not**
  Django superuser powers (least privilege).
- **Content** (`/manage/content/`) — list the modules and their status, with a
  publish/unpublish toggle (soft-delete via `is_published`).

**The safeguards (why it can't be abused):**
```python
# staff/useractions.py
if target.pk == request.user.pk:            # not yourself
    ... "You can't change your own role."
if new_role != ADMINISTRATOR and _is_last_active_admin(target):
    ... "This is the last active Administrator — promote someone else first."
```
So you cannot lock yourself out, and you cannot remove the platform's last
administrator. Every mutating action re-checks the target on the server. For
demos there is also `seed_demo_learners`, which creates 15 realistic fictional
learners (varied names, orgs, a natural spread of progress) so the dashboard can
be shown populated; it is idempotent and `--clear`able, and (honestly) computes
their points/grades from real seeded records, never typed in.

**The audit log** (`staff.AdminAction`, written by `services.log_action`) records
who did what to whom and when, and is surfaced on the overview and each learner's
history — accountability for privileged actions, which matters on a security
platform.

---

# PART 8: TESTING & TOOLS

## 8.1 The test suite

Tests are written with **pytest + pytest-django** and live in each app's
`tests/` folder (config in `pytest.ini`: `DJANGO_SETTINGS_MODULE = nstp.settings`,
`addopts = --strict-markers -q`). `pytest --collect-only` reports **421 tests**
(the raw `def test_` count is 383; the difference is `@pytest.mark.parametrize`
expanding one test into many cases). A full run re-seeds the real six-module
content, so it takes a couple of minutes.

**Breakdown by app (collected):**

| App | Tests | Focus |
|---|---|---|
| `authentication` | 68 | registration, login, 2FA, role-first login, template hygiene |
| `modules` | 138 | student views, the 403 lock, gamification, presentation, sanitiser |
| `quizzes` | 122 | quiz engine, the AFE, and per-module content contracts |
| `staff` | 60 | admin console access control, actions, grading, demo-seed |
| `tests/` (project) | 33 | public pages, dashboard, asset integrity, no-leak checks |
| `certificates` | 0 | placeholder (PDF not built yet) |

**Every test file, and what it covers:**
- `authentication/tests/`: `test_registration` (form, inactive-until-verified,
  signed token, idempotent verify), `test_login` (password step + the rate-limit
  opt-in tests asserting 429), `test_two_factor` (the emailed code — generation,
  hashing, constant-time compare, attempt cap, expiry), `test_role_login` (the
  role framing **cannot** grant a role), `test_templates` (clean render, no
  multiline-comment leak).
- `modules/tests/`: `test_views` (browser/overview/lesson/completion/simulation;
  the real 403 lock; points awarded once), `test_gamification` (points/levels/
  streaks/badges — "numbers come from records, can't drift or double-count"),
  `test_presentation` (rank, streak status, nearest reward, greeting),
  `test_sanitiser` (lesson HTML sanitised on save — the stored-XSS control), plus
  a `conftest.py` that builds a small real content tree.
- `quizzes/tests/`: `test_views` (the gate, paper, save, submit, result),
  `test_services` (draw/grade/record/award/unlock — no point drift on retakes),
  `test_feedback` (the AFE: grouping, ranking, explanations, and the single-query
  test), `test_content` + `test_module_two…six` (each module's content contract:
  activities well-formed and solvable, panel points sum to 10, hints present,
  **no em-dashes**, quiz bank valid for the AFE), and `test_module_one_journey`
  (a full end-to-end: learn → quiz unlocks → pass → next module opens).
- `staff/tests/`: `test_manage` (access control 403s, every user action + the
  self/last-admin guardrails, the empty/quiet/populated states), `test_admin_
  dashboard` (aggregates, sort/filter, CSV, organisation breakdown), `test_
  grading` (the tier bands), `test_seed_demo_learners` (spread, honest numbers,
  idempotent, `--clear`).
- `tests/test_pages.py` (project-level): the public landing page and dashboard
  render cleanly, the dashboard is shut to anonymous users, plus **asset-
  integrity** checks (every CSS animation references a real keyframe, every
  vendored font exists on disk, retired typefaces are gone).

**Notable techniques worth mentioning to your lecturer:**
- **Fixtures** build small deterministic worlds (a content tree; a quiz bank where
  "option 0 is always correct" so expected grades are known; a rich admin `world`).
- **`conftest.py` disables rate limiting** for most tests (all test clients share
  one IP, so it would otherwise flake depending on collection order) and clears
  the cache between tests; three login tests opt back in to assert the limit
  actually fires (429).
- **Date injection, not clock-mocking** — streak/level/calendar logic takes a
  `today=` parameter, so time-based behaviour is tested with fixed dates
  (`TODAY = date(2026, 7, 18)`) rather than a mocking library.
- **Tests force `DEBUG=False`**, so the production sequential-lock and quiz-gate
  are exercised (the DEBUG review-unlock is inactive under test).
- **Security is tested as behaviour** — real 403s from the view (locked module,
  locked lesson, locked quiz, admin URLs for non-admins), the stored-XSS guard at
  the model save path, and the last-admin / self-action guardrails.
- **Content-hygiene tests** — a shared `assert_renders_clean` checks no template
  tokens (`{{`, `{%`, `{#`) leak into any rendered screen; a walker flags any
  multiline `{# #}` comment (which renders literally); `no em-dashes` and `no
  emoji` are asserted across all lesson/quiz content and every screen.
- **Query-count guards** bound the hot paths with `django_assert_max_num_queries`:
  `module_progress` ≤ 4, the module browser ≤ 18, the AFE ≤ 1, the quiz draw ≤ 2 —
  so a future change that introduces an N+1 fails the test.

**Why testing matters here:** this is a *security* product where "records are the
truth" and access controls must hold. Tests are how we prove the guarantees
(points can't be inflated, a role can't be self-granted, a locked module returns
403, grading matches scores, the AFE stays one query) stay true as the code
changes. They also let a teammate change code confidently — a regression is
caught before it ships.

## 8.2 Git / GitHub workflow, and the deviations from spec

**Workflow:** work happens on a **feature branch** (currently
`feature/login-and-2fa`) → pull request → the `BN304-Development` branch.
`main` is never committed to directly. Commit messages are co-authored. The repo
is **public**, so nothing secret may ever be committed (`.env` is gitignored and
has never been in history).

**Deviations from the original spec, with reasons** (all deliberate and
documented — do not "correct" them back):

| Spec said | We use | Why |
|---|---|---|
| Django 6.0.6 | **5.2 LTS** | 6.0 isn't LTS (support ends 2026-08); 5.2 is supported to 2028-04; tinymce only supports ≤5.2. |
| Python 3.12.4 | **3.13** | What's installed and supported by Django 5.2 + PythonAnywhere. |
| psycopg2-binary | **psycopg 3** | Django flags psycopg2 for deprecation. |
| PBKDF2 260k iterations | **Django default (~1,000,000)** | The spec's number is Django 3.2-era and ~74% weaker; never override the hasher. |
| django-otp TOTP app for 2FA | **6-digit code emailed each login** | Removes the authenticator-app friction for non-technical users, so *every* account gets a second factor. Weaker than TOTP; an accepted, documented trade-off. |
| "ReportLab's FPDF class" | **`reportlab.pdfgen.canvas` / `platypus`** | ReportLab has no FPDF class; FPDF is a different library. |
| Gunicorn on PythonAnywhere | **not used** | PythonAnywhere runs its own WSGI server. |

**Still to do (honest status):** the certificate PDF + public verify page;
bespoke simulations for Modules 2–6 (Module 1's is real, the rest use a generic
placeholder); a content-accuracy review of the Optus/Medibank and Privacy-Act
material; and a hosting decision (PythonAnywhere's free tier has no PostgreSQL).

---

# APPENDIX A — The 5 most likely lecturer questions (with strong answers)

**Q1. "Why did you deviate from the spec on the framework version, the database
driver, 2FA, and the password hasher?"**
Because each spec choice was either not the safest or not the most maintainable
option, and we made an engineering judgement and documented it. Django 5.2 is
LTS (patched to 2028) where 6.0 is not; psycopg 3 is the recommended driver as
psycopg2 heads for deprecation; we kept Django's ~1,000,000-iteration PBKDF2
because the spec's 260,000 is an old, ~74% weaker number. For 2FA we chose an
emailed code over an authenticator app: the app was too much friction for non-
technical users and would have left many accounts with no second factor at all,
so the emailed code gives *universal* coverage — weaker than TOTP, which we
state plainly as an accepted trade-off. Every deviation is written down with its
reason, so they're decisions, not accidents.

**Q2. "How do you stop a student from cheating their points or grade?"**
Points are never stored as a mutable counter — they're **recomputed** from the
records (`ProgressRecord` and *distinct passed* `QuizResult` rows) every time,
in `gamification.refresh_profile`. Database `unique(...)` constraints mean a
lesson counts once and a quiz pass counts once, so replaying an action does
nothing. Quiz grading is done **server-side** in `quizzes/services.py`: the
client only sends which option id it picked, and the server checks it against the
`correct_answer` flag loaded from the database — it can't declare its own score.
Grades derive from the same `QuizResult` rows, so a grade can never disagree with
whether the student actually passed.

**Q3. "Walk me through your login security."**
Two factors, and no session until both pass. Password is checked against a salted
PBKDF2 hash (never plaintext), rate-limited to 10/hour/IP. On success we *don't*
log in — we generate a 6-digit code with `secrets` (cryptographically secure),
store only its salted-HMAC **hash** in the session, and email the code. The
second step compares with `constant_time_compare` (defeats timing attacks),
allows five attempts, and expires after ten minutes; the pending state is
single-use and cleared on success. Only then does `login()` create a real
session. Between the two steps only a user id sits in the session, which can't
reach any protected page.

**Q4. "What is the Adaptive Feedback Engine and how does it actually work?"**
It's the product's differentiator: instead of a bare score, it produces a
personalised study plan. When a quiz is graded we store a `WrongAnswer` row per
mistake (what they picked, what was correct). `quizzes/feedback.py::analyse`
reads those rows, and for each mistake pulls the *explanation* text off both the
chosen and correct answers, and the *source lesson* via the question's
`lesson_reference` foreign key. It tallies mistakes per lesson and returns a
ranked "revise these lessons, most-missed first" plan plus the per-question
explanations. So a student who gets three questions wrong is told exactly which
lessons to revise, in priority order, and why each answer was wrong. It's built
to run in a single database query (there's a test enforcing that).

**Q5. "How is your admin area secured, and how do you prevent an admin from
locking everyone out?"**
Every `/manage/` view is wrapped in `administrator_required`, which returns a
real 403 for non-administrators (not just a hidden link), and all state-changing
actions are POST + CSRF and written to an audit log (`AdminAction`) recording who
did what to whom. Two guardrails prevent lockout: you can't change your own role
or deactivate yourself, and you can't demote or deactivate the last active
Administrator — both checked server-side on every action. Adding a user can
assign a role (a legitimate admin act), but promoting to Administrator grants
only the in-app dashboard, not Django superuser powers.

---

# APPENDIX B — Step by step: what happens when a user logs in

1. The user opens `/login/` and sees the role-first page (two buttons). They
   click one; it opens the normal email + password form (the button only changes
   the heading — it grants nothing).
2. They submit email + password. `login_view` runs; the **rate limiter** checks
   this IP hasn't exceeded 10 login POSTs this hour.
3. Django's `AuthenticationForm` looks up the user by email and verifies the
   password against the stored **PBKDF2 hash**. Django also refuses the login if
   the account is `is_active=False` (unverified).
4. On success the view **does not log the user in.** It calls `make_login_code()`
   (`secrets`, 6 digits), stores the user id + a **hash** of the code + a
   timestamp in the session (`_start_pending`), and emails the code
   (`_send_login_code`). It redirects to `/login/code/`.
5. The user types the code. `login_code` fetches the pending user (must still be
   active and within the 10-minute window) and compares the code with
   **`constant_time_compare`**. Wrong codes count toward a **5-attempt cap**;
   too many and the code is destroyed.
6. On the correct code, `_complete_login` calls Django's `login()` (now a real
   session exists), records the login for the streak (`record_login`), clears the
   pending state, and redirects via `role_home_url`.
7. `role_home_url` sends an **Administrator** to `/manage/` (the admin console)
   and everyone else to `/dashboard/`. The role comes from the *account*, never
   from the button they clicked.

---

# APPENDIX C — Step by step: how the Adaptive Feedback Engine works

1. **At submit**, `quizzes/services.py::grade_and_record` grades the 10 presented
   questions server-side and writes a `QuizResult`, plus one **`WrongAnswer`**
   row per answered-wrong question (storing the chosen and correct `Answer`).
2. **On the result page**, `quiz_result` calls
   `quizzes/feedback.py::analyse(result)`.
3. `analyse` loads that attempt's `WrongAnswer` rows in **one prefetched query**,
   pulling the question, its `lesson_reference` (+module), and both answers.
4. For each wrong answer it builds a **`FeedbackItem`**: the question, *your*
   option + **why it's wrong** (`student_answer.explanation_text`), the correct
   option + **why it's right** (`correct_answer.explanation_text`), and the
   source lesson.
5. It tallies mistakes **per lesson** in `by_lesson = {lesson_id: [lesson,
   count]}`, using the question's `lesson_reference`.
6. It builds a **`RevisionLesson`** per lesson and sorts them **most-missed
   first** (ties broken by reading order), each with its reading time.
7. It returns a `Feedback` object (the itemised explanations + the ranked plan),
   which the result template shows as "Here's why you missed these, and the
   lessons to revise, in priority order."

*Example:* miss Q2, Q5, Q9; Q2 and Q9 map to Lesson 1, Q5 to Lesson 4 → the plan
is **[Lesson 1 (2 mistakes), Lesson 4 (1 mistake)]**.

---

# APPENDIX D — Glossary

- **MVT (Model–View–Template):** Django's architecture. Model = data/table, View
  = request handler, Template = HTML.
- **ORM (Object-Relational Mapper):** write Python (`Module.objects.filter(...)`)
  instead of SQL; Django generates the query.
- **Migration:** a versioned script that changes the database schema to match the
  models (`makemigrations` / `migrate`).
- **Model / field / foreign key:** a model is a table; a field is a column; a
  foreign key is a link from a row in one table to a row in another.
- **`select_related` / `prefetch_related`:** pre-load related rows in one query to
  avoid the "N+1 queries" problem.
- **Custom user model:** our `User`, which logs in by email and carries `role`
  and `is_verified`.
- **`AUTH_USER_MODEL`:** the setting naming the user model; must be set before the
  first migration.
- **PBKDF2:** the slow, salted, one-way password-hashing algorithm Django uses.
- **`secrets` vs `random`:** `secrets` is cryptographically secure (used for the
  2FA code); `random` is predictable (fine for shuffling questions only).
- **Salted HMAC / `django.core.signing`:** keyed hashing/signing tied to
  `SECRET_KEY`, used to hash the 2FA code and to sign verification tokens.
- **`constant_time_compare`:** a comparison that always takes the same time, to
  avoid timing attacks.
- **2FA (two-factor authentication):** a second proof of identity beyond the
  password — here, an emailed 6-digit code.
- **CSRF (Cross-Site Request Forgery):** an attack where another site makes your
  browser submit a request; blocked by Django's CSRF tokens on POST forms.
- **XSS (Cross-Site Scripting):** injecting malicious script into a page; blocked
  by **nh3** sanitisation on input and the **CSP** header on output.
- **CSP (Content-Security-Policy):** an HTTP header telling the browser what it's
  allowed to load/run (we allow scripts only from `'self'`).
- **nh3:** the HTML sanitiser that strips dangerous tags/attributes from stored
  lesson HTML.
- **Rate limiting:** capping how often an action can be attempted (login: 10/hr/IP).
- **Least-privilege:** giving a component (the DB role) only the permissions it
  needs and nothing more.
- **Soft delete:** hiding content with a flag (`is_published=False`,
  `is_active=False`) instead of deleting the row, so history is preserved.
- **Idempotent:** doing something twice has the same effect as doing it once (the
  verify link; recording a lesson via a `unique` constraint).
- **Records are the truth / recompute-don't-increment:** the core principle —
  store events, derive totals; never keep a counter that could drift or be
  cheated.
- **Gamification:** points, levels, streaks and badges that reward progress.
- **AFE (Adaptive Feedback Engine):** turns wrong answers into a ranked,
  explained study plan.
- **Grading tier:** Distinction/Merit/Pass/Not-yet, derived from best quiz scores.
- **Audit log (`AdminAction`):** a record of every privileged admin action.
- **Sequential lock:** you must finish Module N−1 before Module N; enforced as a
  403 in the view.
- **Seed / management command:** a script run via `manage.py` that loads data
  (e.g. `seed_learning_content`, `seed_demo_learners`).
- **Fixture (tests):** a reusable set-up that builds test data for a test.
- **`cy:solved`:** the custom DOM event an interactive activity fires when the
  learner completes it; `lesson.js` listens for it to mark a panel done.
- **LTS (Long-Term Support):** a release line that gets security patches for years
  (Django 5.2 → 2028).

---

*This document reflects the codebase on branch `feature/login-and-2fa`. If code
changes, re-read the referenced files (they carry extensive explanatory comments)
and update this file to match. Test count and per-app breakdown verified with
`pytest --collect-only` (421 tests collected).*
