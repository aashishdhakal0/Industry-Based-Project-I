# NSTP — BN304 Build Plan (solo)

Six sprints, weeks 13–24. `[x]` done · `[ ]` pending · `[!]` blocked.

**Built solo by Aashish Dhakal (MIT235300).** Every task below is his. Owner
initials have been dropped — they encoded a five-way split that no longer exists.

---

## Read this first — the scope problem

The original plan assumed five people working in parallel. Solo, the same scope
does not fit the calendar, and pretending otherwise is how projects arrive at
week 24 with six half-built features and no demo.

| | Hours |
|---|---|
| Available (12 weeks @ ~16 h/wk, realistic for a student carrying other units) | **~190** |
| Engineering as specced | ~190 |
| Content as specced (19,200 words + 90 questions + 360 explanations) | **~70–85** |
| **Total** | **~260–275** |

**Roughly 1.5× over.** So this plan does two things the old one didn't:

1. **Builds vertically, not horizontally.** The old plan finished all modules,
   then all quizzes, then all dashboards, then certificates in week 22. Run out
   of time and you have nothing that works end-to-end. This plan drives **one
   complete student journey** — register → learn → quiz → adaptive feedback →
   certificate — by the end of Sprint 4, then scales content into it.
2. **Names the cuts up front** (below), rather than discovering them in week 23.

> **The cut list needs supervisor/client sign-off.** Take it to Dr. Naser
> Mahmood and Hussain Riaz early — a documented, deliberate de-scope is a
> professional decision; the same cut made silently in week 23 is a failure.

### Cut list — in the order they go

| Cut | Saves | Rationale |
|---|---|---|
| **6 modules → 3** | ~35 h | The differentiator is the AFE, not volume. Three modules prove every mechanic. |
| **Simulations** | ~15 h | Vaguest part of the spec (open questions 3 & 4). No assessment weight. First to go. |
| **Bespoke instructor CMS** | ~12 h | **The Django admin already does content CRUD** — and it's built. Ship admin-as-CMS; build the bespoke UI only if Sprint 5 has slack. |
| **Badges + CSV export** | ~8 h | Gamification garnish. Streak/points stay (cheap, visible). |
| **Question bank 15 → 12/module** | ~8 h | Still a genuine random draw of 10. |

Take all five and the build lands near ~190 h. Take none and it doesn't land.

### What is NOT cuttable

Auth + RBAC · the quiz engine · **the Adaptive Feedback Engine** · certificates ·
**≥80% test coverage** · the ZAP scan + remediation · deployment · the report.
These are either the product's reason to exist or explicitly graded.

---

## Sprint 0 — Setup ✅

- [x] Restructure loose Desktop files into `nstp_project/`
- [x] `git init`, `.gitignore` (venv, db.sqlite3, .env, .DS_Store), initial commit
- [x] Decide runtime: Python 3.13 + Django 5.2 LTS + PostgreSQL 18 *(deviation documented)*
- [x] Build `.venv` on Python 3.13.14; pin `requirements.txt`; verify every import
- [x] Save spec → `docs/project-overview.md`
- [x] Wire `settings.py` — 4 apps, django-otp + OTPMiddleware ordering, TinyMCE,
      WhiteNoise, CSP, decouple, en-au/Melbourne, security headers
- [x] `.env` + `.env.example`; `manage.py check` clean
- [x] Write `CLAUDE.md`, `docs/architecture.md`, `docs/build-plan.md`
- [x] Add git remote → github.com/aashishdhakal0/Industry-Based-Project-I
- [x] `BN304-Development` branch, pushed and tracking `origin`
- [x] Least-privilege `nstp` DB role + `scripts/create_db_role.sql`
- [!] **Decide production DB host** — PythonAnywhere free tier has **no PostgreSQL**

---

## Sprint 1 — Weeks 13–14 — Setup & Core Authentication

> Everything downstream rests on this. Get it right rather than fast.

### 1.1 Models ✅ *(the ordering trap — survived)*
- [x] `authentication.User(AbstractUser)` — email `USERNAME_FIELD` (unique), `role`, `is_verified`
- [x] **`AUTH_USER_MODEL` set before the first `migrate`** ← the one that can't be undone
- [x] `UserProfile` — 1:1 User, organisation, avatar, last_active, streak_count, points, badges
- [x] Remaining 10 models across modules/quizzes/certificates
- [x] **`Question.lesson_reference → Lesson`** (missing from spec; the AFE needs it)
- [x] `makemigrations` → review generated SQL → `migrate` (25 migrations, green)
- [x] Register all 12 in the Django admin (`UserAdmin` rebuilt around email)

### 1.2 Registration ← **next**
- [ ] `RegistrationForm` — first/last name, email, password ×2, organisation
- [ ] Validate: email unique (case-insensitive), Django password validators, match
- [ ] Create User (`is_active=False`) + UserProfile **atomically**
- [ ] Verification email — signed, time-limited token (`django.core.signing`)
- [ ] Verify view → `is_verified=True`, `is_active=True`, one-shot
- [ ] Templates: register · check-your-inbox · verified · expired-link
- [ ] Console email backend in dev; SMTP deferred to deploy

### 1.3 Login + 2FA ✅
- [x] Email+password login (not username), lower-cased so autocapitalise can't lock anyone out
- [x] TOTP setup: create `TOTPDevice`, render QR **from `config_url`** as an inline data URI
- [x] Confirm-and-activate device (never trust an unconfirmed device)
- [x] Second-step TOTP prompt on subsequent logins
- [x] **Role-based 2FA** — mandatory for Instructors/Administrators, optional for
      Students. *Deviation from the spec; rationale in CLAUDE.md. Defend it in the report.*
- [x] `LOGIN_URL` now points at the real view; the `/admin/login/` stopgap is gone
- [x] Role routing after login via `authentication.utils.role_home_url`
- [x] `?next=` honoured, and validated against open redirect
- [x] Update `UserProfile.last_active` on login (streak builds on this in Sprint 4)
- [x] Templates: login · 2FA setup (QR + manual key) · 2FA prompt · 429

> `django-otp` renders QR automatically **only in the admin**. The user-facing
> flow builds it from `TOTPDevice.config_url` via `qrcode`. Spec is wrong here.

> **No session until both factors pass.** Between password and code the user's
> id sits in the session and nothing else — `login()` is called only once the
> code verifies. django-otp's own examples log the user in first and gate
> afterwards, which means a real authenticated session exists in that window
> and every view must remember to ask `is_verified()` rather than
> `is_authenticated`. The first one that forgets is the hole.

### 1.4 RBAC
- [ ] Groups: Students, Instructors, Administrators
- [ ] Custom permission `modules.can_manage_content`
- [ ] Role-check decorator/mixin, applied per-view
- [ ] Assign group on registration by role

### 1.5 Rate limiting — *partly done, pulled forward*
- [x] `@ratelimit` 10/hr per IP on **login** and the **2FA prompt**
- [x] Friendly 429 page (plain language, not a stack trace)
- [x] `conftest.py` disables it per-test and clears the counter cache between tests
- [ ] `@ratelimit` on **register** — still to do

> Pulled the login limit forward into 1.3: a login form without one is a
> brute-force target, and a sprint is not a reasonable window to leave it bare.
> TOTP has a second layer — `TOTPDevice` carries django-otp's `ThrottlingMixin`,
> so wrong codes back off per-device regardless of IP.

### 1.6 CI — *do this early; it pays for itself all semester*
- [ ] `.github/workflows/ci.yml` — install, PG service, pytest, fail PR on red
- [ ] `pytest.ini`; `RATELIMIT_ENABLE=False` in tests
- [ ] Branch protection on `BN304-Development`

### 1.7 Tests (write alongside, not after)
- [ ] Registration: valid · duplicate email · weak password · mismatch
- [ ] Verification: valid · expired · tampered · replayed token
- [ ] Login: right · wrong · unverified · 2FA on/off
- [ ] RBAC: each role hitting each other's views → 403

---

## Sprint 2 — Weeks 15–16 — Modules, Lessons & Module 1 Content

> Goal: a student can read a real lesson. Content authoring moves **into the
> admin** — the bespoke CMS is deferred (see cut list).

- [ ] Module list — published only, ordered by `order_index`
- [ ] Annotate completion % from `ProgressRecord` count
- [ ] **Sequential lock** — module N needs N−1 complete
- [ ] Enforce the lock **in the view**, not just the template
- [ ] Bootstrap cards: progress bar, lock icon, one clear CTA
- [ ] Lesson viewer + "mark complete" → `ProgressRecord` (+10 pts)
- [ ] **Sanitise TinyMCE HTML on save (allow-list)** ← the stored-XSS control
- [ ] `base.html` + the shared visual language (do it once, here)
- [ ] **Module 1 — 4 lessons ≥800 words**
- [ ] Tests: lock returns 403 · sanitiser neutralises `<script>` · completion maths

> Lesson HTML renders unescaped, so **sanitising on save is the only thing
> standing between an author and stored XSS in every student's browser.**
> This is not deferrable — the sanitiser ships with the first lesson.

---

## Sprint 3 — Weeks 17–18 — Quiz + Adaptive Feedback Engine ⚠️

> Hardest sprint and the product's whole reason to exist. Protect it. If
> anything slips, it slips *into* here from elsewhere — never out of here.

### 3.1 Quiz engine
- [ ] Draw 10 via `order_by("?")[:10]` (**not** `random.sample` on a queryset)
- [ ] Persist question ids + `started_at` in the session
- [ ] Render questions + 4 options (`prefetch_related`)
- [ ] JS 30-min countdown, auto-submit
- [ ] **Server-side time check on submit** (the client timer is advisory)
- [ ] Answers → session, survive refresh
- [ ] Score server-side: correct/10×100 vs 70%
- [ ] `@transaction.atomic`: QuizResult + `bulk_create(WrongAnswer)`
- [ ] `attempt_number` = prior attempts + 1

### 3.2 Adaptive Feedback Engine — **the differentiator**
- [ ] `run_adaptive_feedback(quiz_result)` in `quizzes/utils.py`
- [ ] One query: `select_related("question__lesson_reference")` + prefetch answers
- [ ] Pull both explanations (chosen-wrong + correct)
- [ ] Group by `lesson_reference`
- [ ] Revision estimate = mistakes × `lesson.reading_time_minutes`
- [ ] Prioritise by mistake count, descending
- [ ] Results page: score → per-question why → study plan with lesson links
- [ ] Empty state: 100% → congratulate, don't render a blank plan

### 3.3 Module 1 quiz content
- [ ] 12 questions × 4 options, **every option with an `explanation_text`**

### 3.4 Tests
- [ ] Scoring boundaries: 0 · 6/10 (fail) · **7/10 (pass, exact)** · 10
- [ ] Expired timer force-submits · refresh preserves answers
- [ ] AFE groups correctly; **assert query count ≤ 2** (N+1 guard)
- [ ] AFE on a perfect score returns an empty plan

---

## Sprint 4 — Weeks 19–20 — Certificates & Dashboards → **journey complete**

> Certificates move **up** from Sprint 5. By the end of this sprint one student
> can go register → learn → quiz → feedback → certificate. That is the demo, the
> UAT script, and the thing you show the client. Everything after is scale.

### 4.1 Certificates
- [ ] `post_save` on QuizResult → **passed the quiz for every published module?**
- [ ] `get_or_create(Certificate)` — **idempotent**, no duplicates on re-sit
- [ ] UUID4 code
- [ ] PDF via **`reportlab.platypus` / `pdfgen.canvas`** — *not* "FPDF" (doesn't exist)
- [ ] A4 landscape: AUSDAIS header, name, UUID, date, modules, signature
- [ ] Save `media/certificates/<uuid>.pdf` → `pdf_path`
- [ ] Download view — **owner only** (don't leak by guessable URL)
- [ ] Public verify-by-UUID page

> **Design change:** the trigger is *"every published module"*, not *"all 6"*.
> Hard-coding 6 means the journey cannot complete — or be demoed, or tested —
> until all six exist. Data-driven, it works with 3 and still works with 6.

### 4.2 Dashboards
- [ ] Student: modules done (`Count`), avg score (`Avg`), points, streak
- [ ] Points = lessons×10 + passed quizzes×50
- [ ] Streak: compare `last_active` to today (**Melbourne local date**)
- [ ] Instructor: own modules, enrolments, avg scores
- [ ] Admin: all users annotated w/ completions, last score, last active
- [ ] ~~Badges~~ · ~~CSV export~~ — cut; reinstate only with Sprint 5 slack
- [ ] Tests: aggregation correctness · streak across a date boundary

> Dashboards are the #1 N+1 risk. `select_related`/`prefetch_related`, or the
> free-tier CPU quota will bite.

---

## Sprint 5 — Weeks 21–22 — Content Scale-out & Hardening

> Now — and only now — pour content into a machine that provably works.

- [ ] **Module 2** — 4 lessons + 12 questions with explanations
- [ ] **Module 3** — 4 lessons + 12 questions with explanations
- [ ] Deploy to staging
- [ ] OWASP ZAP active scan → triage High/Med/Low/Info
- [ ] Remediate **all High + Medium**
- [ ] Verify CSP / X-Frame-Options / HSTS actually present in responses
- [ ] Re-scan to confirm
- [ ] OWASP Top 10 review doc
- [ ] *Slack only:* bespoke instructor CMS · badges · CSV · simulations · modules 4–6

> Expect the stored-XSS path to be the headline ZAP finding. The Sprint 2
> sanitiser is the fix — this is where it gets proven.

---

## Sprint 6 — Weeks 23–24 — Testing, Deploy, Report

- [ ] Views: auth'd/unauth'd, status codes, template, DB writes
- [ ] Models: constraints, custom methods · Forms: registration, login, validation
- [ ] **coverage ≥80%** across views/models/forms
- [ ] UAT from the prototype workflows, 3 roles
- [ ] Usability testing with representative non-technical users
- [ ] Log prototype-vs-live discrepancies
- [!] **Resolve PostgreSQL hosting** (blocker — decide by Sprint 4, not 5)
- [ ] Clone on host; venv; `pip install -r requirements.txt`
- [ ] `.env` with production values; `DEBUG=False`; **fresh `SECRET_KEY`**
- [ ] `migrate`; create superuser; `collectstatic`; WSGI → `nstp.settings`
- [ ] HTTPS on; verify redirect + HSTS; `manage.py check --deploy` clean
- [ ] Final ZAP scan against production
- [ ] Technical documentation · user manuals ×3 roles · logbook current
- [ ] Final report + ACS CBOK mapping
- [ ] Handover to Dr. Naser Mahmood / AUSDAIS

> Coverage ≥80% in the final sprint is only survivable if tests were written
> alongside each sprint. Retrofitting 80% in two weeks, solo, is not realistic.
> **The per-sprint test tasks are the mitigation. Do not defer them.**

---

## Risk register

| # | Risk | Impact | Mitigation |
|---|---|---|---|
| 1 | ~~`AUTH_USER_MODEL` set after first migrate~~ | — | ✅ **Retired.** Set before first migrate; verified |
| 2 | **Solo build, 1.5× over budget** | 🔴 nothing ships end-to-end | Vertical slice by Sprint 4; cut list signed off early |
| 3 | **Bus factor 1** — illness/exams = pure slip, no cover | 🔴 total | Small commits, push daily, CI green. Flag slips to Hussain Riaz *early* |
| 4 | **PythonAnywhere free tier has no PostgreSQL** | 🔴 can't deploy as specced | Decide by **Sprint 4**: pay / MySQL / Render–Fly–Railway |
| 5 | Weak `explanation_text` | 🔴 the differentiator dies | It *is* the product. Write M1's before building the AFE — they're the spec |
| 6 | TinyMCE stored XSS | 🔴 High ZAP finding | Sanitise on save (Sprint 2); prove in Sprint 5 |
| 7 | Sprint 3 (quiz+AFE) overruns | 🟠 cascades | Hardest sprint. Slack flows *in*, never out |
| 8 | Coverage retrofitted at the end | 🟠 misses 80% | Test-alongside each sprint; CI fails red PRs |
| 9 | N+1 in dashboards/AFE | 🟠 free-tier CPU | `select_related`; assert query counts |
| 10 | Content slips to the end | 🟠 empty demo | M1 in Sprint 2 — before the quiz engine needs it |
| 11 | Public repo | 🟡 secret leak is permanent | `.env` gitignored + verified clean. Fresh prod `SECRET_KEY` |
| 12 | django-ratelimit undeclared on 3.13/5.2 | 🟡 breaks on upgrade | Verified importable; pinned; retest on any bump |
| 13 | **User enumeration on register** — ✅ *accepted, deliberate* | 🟡 expect a Low/Med ZAP finding | **Decided Sprint 1.2.** See below |

### Accepted risk — user enumeration on the registration form

The register form tells the user plainly: *"That email is already registered."*
This is enumerable — anyone can test whether an address has an NSTP account —
and **ZAP will likely flag it in Sprint 5. That finding is expected, not a
defect.** Do not "fix" it without revisiting this decision.

**Why.** Our users are non-technical Australians, and CLAUDE.md commits to plain
language and one obvious next action per screen. The OWASP-preferred alternative
— always saying "check your inbox", and emailing existing users a "you already
have an account" note — hides the answer behind an inbox round-trip. For a
developer that's a fair trade; for a small-business owner who simply forgot they
signed up, it's a dead end that teaches them nothing.

**What makes it acceptable.** The asset is low-value: enumeration reveals only
that an address has a training-platform login. No payment data, no PII beyond an
email the attacker already holds. Rate limiting (task 1.5) caps attempts at
10/hr/IP, so bulk harvesting is impractical.

**Say this in the report.** A documented trade-off between two competing
requirements is a design decision. The same behaviour left unexplained is a bug.

---

## Open questions for the client / supervisor

1. **The cut list** — 3 modules not 6, no simulations, admin-as-CMS, no badges/CSV.
   Solo, the full scope is ~1.5× the available hours. **Which cuts are acceptable?**
   *(blocker — ask now, not in week 23)*
2. **Production database host** — PA free tier has no PostgreSQL. Pay, or move? *(blocker)*
3. **Question bank size** — spec says both "ten questions per module" and "a bank of
   more than ten allowing random selection". Which? A real draw needs ≥12.
4. **Certificate trigger** — "all six modules" or "all published modules"? The latter
   is what makes a reduced build demonstrable. Proposing the latter.
5. **`Simulation.outcome_text`** — spec describes one field holding *"each possible
   outcome"*; a single text field can't. JSON keyed by decision path? *(moot if cut)*
6. **Certificate re-issue** — re-sit after certification: reissue or keep the original?
7. **Are the 4 lessons/module fixed?** Completion maths assumes it; nothing enforces it.
