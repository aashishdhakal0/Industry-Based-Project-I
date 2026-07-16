# NSTP — BN304 Build Plan

Six sprints, weeks 13–24. `[x]` done · `[ ]` pending · `[!]` blocked.

**Legend:** AD = Aashish · SS = Sudip · AL = Anuska · KS = Khadka · BG = Bigyap

---

## Sprint 0 — Setup (done ahead of Sprint 1)

- [x] Restructure loose Desktop files into `nstp_project/`
- [x] `git init`, `.gitignore` (venv, db.sqlite3, .env, .DS_Store), initial commit
- [x] Decide runtime: Python 3.13 + Django 5.2 LTS + PostgreSQL 18 *(deviation documented)*
- [x] Build `.venv` on Python 3.13.14
- [x] Pin `requirements.txt`; install; verify every import
- [x] Save spec → `docs/project-overview.md` (in git)
- [x] Wire `settings.py` — 4 apps, django-otp + plugin, OTPMiddleware ordering,
      TinyMCE, WhiteNoise, CSP, decouple, en-au/Melbourne, security headers
- [x] `.env` + `.env.example`; `manage.py check` clean
- [x] Delete stale Python 3.9 venv
- [x] Write `CLAUDE.md`, `docs/architecture.md`, `docs/build-plan.md`
- [ ] Add git remote → github.com/aashishdhakal0/Industry-Based-Project-I
- [ ] Create `BN304-Development` branch; make it the PR target
- [!] **Decide production DB host** — PythonAnywhere free tier has **no PostgreSQL**

---

## Sprint 1 — Weeks 13–14 — Setup & Core Authentication

> Everything downstream rests on this. Get it right rather than fast.

### 1.1 Models — the ordering trap
- [ ] **`authentication.User(AbstractUser)`** — email `USERNAME_FIELD` (unique), `role`, `is_verified` — **AD**
- [ ] **Uncomment `AUTH_USER_MODEL` in settings.py** ← *before any migrate* — **AD**
- [ ] `UserProfile` — 1:1 User, organisation, avatar, last_active, streak_count, points, badges JSON — **AD**
- [ ] Remaining 10 models across modules/quizzes/certificates — **AD**
- [ ] Add **`Question.lesson_reference → Lesson`** (missing from spec; AFE needs it) — **AD**
- [ ] `makemigrations` → review generated SQL → `migrate` — **AD**
- [ ] Register all 12 in Django admin — **AD**

> ⚠️ **`AUTH_USER_MODEL` must be set before the first `migrate`.** Getting this
> wrong means dropping the DB and starting over. It is the single highest-cost
> mistake available in this sprint.

### 1.2 Registration
- [ ] Form: first/last name, email, password ×2, role, organisation — **AD**
- [ ] Validate: email unique, Django password validators, passwords match — **AD**
- [ ] Create User (inactive) + UserProfile atomically — **AD**
- [ ] Verification email — signed, time-limited URL (`django.core.signing`) — **AD**
- [ ] Verify view → `is_verified=True`, activate — **AD**
- [ ] Templates: register, "check your inbox", verified, expired-link — **SS**

### 1.3 Login + 2FA
- [ ] Email+password login (not username) — **AD**
- [ ] TOTP setup: create `TOTPDevice`, render QR **from `config_url`** — **AD**
- [ ] Confirm-and-activate device (never trust unconfirmed) — **AD**
- [ ] Second-step TOTP prompt on subsequent logins — **AD**
- [ ] Update `UserProfile.last_active` + streak on login — **AD**
- [ ] Templates: login, 2FA setup (QR + manual key), 2FA prompt — **SS**

> `django-otp` renders QR automatically **only in the admin**. The user-facing
> flow must build it from `TOTPDevice.config_url` via `qrcode`. Spec is wrong here.

### 1.4 RBAC
- [ ] Groups: Students, Instructors, Administrators — **AD**
- [ ] Custom permission `modules.can_manage_content` — **AD**
- [ ] Role-check decorator/mixin, applied per-view — **AD**
- [ ] Assign group on registration by role — **AD**

### 1.5 Rate limiting
- [ ] `@ratelimit` 10/hr per IP on login + register — **AD**
- [ ] Friendly 429 page (plain language, not a stack trace) — **SS**

### 1.6 CI
- [ ] `.github/workflows/ci.yml` — install, PG service, pytest, fail PR on red — **KS**
- [ ] Branch protection on `BN304-Development` — **AD**
- [ ] `pytest.ini` / `pyproject` config; `RATELIMIT_ENABLE=False` in tests — **KS**

### 1.7 Sprint 1 tests
- [ ] Registration: valid, duplicate email, weak password, mismatch — **KS**
- [ ] Verification: valid / expired / tampered token — **KS**
- [ ] Login: right, wrong, unverified, 2FA on/off — **KS**
- [ ] RBAC: each role hitting each other's views → 403 — **KS**

---

## Sprint 2 — Weeks 15–16 — Modules & CMS

### 2.1 Student browser
- [ ] Module list, published only, by `order_index` — **AD**
- [ ] Annotate completion % from ProgressRecord count — **AD**
- [ ] **Sequential lock** — module N needs N−1 complete — **AD**
- [ ] Enforce lock **in the view**, not just the template — **AD**
- [ ] Bootstrap cards: progress bar, lock icon, one clear CTA — **SS**
- [ ] Lesson viewer + "mark complete" → ProgressRecord (+10 pts) — **AD**/**SS**

### 2.2 Instructor CMS
- [ ] `CreateView` / `UpdateView` for Module — **AD**
- [ ] `DeleteView` = **soft delete** (`is_published=False`) — **AD**
- [ ] Lesson CRUD with TinyMCE `body_text` — **AD**
- [ ] **Sanitise TinyMCE HTML on save (allow-list)** ← stored-XSS control — **AD**
- [ ] Image upload via Pillow — validate type, resize, strip EXIF — **AD**
- [ ] Gate all CMS views on `can_manage_content` — **AD**
- [ ] CMS templates — **SS**

> Lesson HTML must render unescaped, so **sanitising on save is the only thing
> standing between an instructor and stored XSS in every student's browser.**

### 2.3 Content
- [ ] Module 1 — 4 lessons ≥800 words — **BG**
- [ ] Module 2 — 4 lessons ≥800 words — **BG**
- [ ] Simulations for M1–M2 (`decision_points` JSON) — **BG**

### 2.4 Tests
- [ ] Lock logic: locked module returns 403, not a template lie — **KS**
- [ ] CMS permissions; student cannot reach CMS — **KS**
- [ ] Sanitiser: `<script>` in lesson body is neutralised — **KS**

---

## Sprint 3 — Weeks 17–18 — Quiz + Adaptive Feedback Engine ⚠️

> Hardest sprint and the product's whole point. Budget slack here.

### 3.1 Quiz engine
- [ ] Draw 10 via `order_by("?")[:10]` (**not** `random.sample` on a queryset) — **AD**
- [ ] Persist question ids + `started_at` in session — **AD**
- [ ] Render questions + 4 options (`prefetch_related`) — **AD**/**SS**
- [ ] JS 30-min countdown, auto-submit — **SS**
- [ ] **Server-side time check on submit** (client timer is advisory) — **AD**
- [ ] Answers → session, survive refresh — **AD**
- [ ] Score server-side: correct/10×100 vs 70% — **AD**
- [ ] `@transaction.atomic`: QuizResult + `bulk_create(WrongAnswers)` — **AD**
- [ ] `attempt_number` = prior attempts + 1 — **AD**

### 3.2 Adaptive Feedback Engine
- [ ] `run_adaptive_feedback(quiz_result)` in `quizzes/utils.py` — **AD**
- [ ] One query: `select_related("question__lesson_reference")` + prefetch answers — **AD**
- [ ] Pull both explanations (chosen-wrong + correct) — **AD**
- [ ] Group by `lesson_reference` — **AD**
- [ ] Revision estimate = mistakes × `lesson.reading_time` — **AD**
- [ ] Prioritise by mistake count, descending — **AD**
- [ ] Results page: score → per-question why → study plan w/ lesson links — **SS**
- [ ] Empty state: 100% → congratulate, don't render a blank plan — **SS**

### 3.3 Tests
- [ ] Scoring boundaries: 0, 6/10 (fail), **7/10 (pass, exact)**, 10 — **KS**
- [ ] Expired timer force-submits — **KS**
- [ ] Refresh mid-quiz preserves answers — **KS**
- [ ] AFE groups correctly; **assert query count ≤ 2** (N+1 guard) — **KS**
- [ ] AFE on a perfect score returns an empty plan — **KS**

---

## Sprint 4 — Weeks 19–20 — Dashboards

- [ ] Student: modules done (`Count`), avg score (`Avg`), points, streak — **AD**
- [ ] Points = lessons×10 + passed quizzes×50 — **AD**
- [ ] Streak: compare `last_active` to today (**Melbourne local date**) — **AD**
- [ ] `badges.py` — id, name, icon, condition fn — **AD**
- [ ] Award after lesson/quiz/login; only unearned — **AD**
- [ ] Instructor dashboard: own modules, enrolments, avg scores — **AD**
- [ ] Admin: all users annotated w/ completions, last score, last active — **AD**
- [ ] CSV export (`csv` + Content-Disposition) — **AD**
- [ ] Templates ×3 — **SS**
- [ ] Visual pass — colour, type, spacing, icons — **AL**
- [ ] Tests: aggregation correctness, badge edges, CSV headers — **KS**

> Dashboards are the #1 N+1 risk. `select_related`/`prefetch_related` or the
> free-tier CPU quota will bite.

---

## Sprint 5 — Weeks 21–22 — Certificates & Hardening

### 5.1 Certificates
- [ ] `post_save` on QuizResult → all 6 passed? — **AD**
- [ ] `get_or_create(Certificate)` — **idempotent**, no duplicates on re-sit — **AD**
- [ ] UUID4 code — **AD**
- [ ] PDF via **`reportlab.platypus` / `pdfgen.canvas`** — *not* "FPDF" (doesn't exist) — **AL**
- [ ] A4 landscape: AUSDAIS header/seal, name, UUID, date, 6 modules, signature — **AL**
- [ ] Save `media/certificates/<uuid>.pdf` → `pdf_path` — **AD**
- [ ] Download view — **owner only** (don't leak by guessable URL) — **AD**
- [ ] Public verify-by-UUID page — **AD**/**SS**

### 5.2 Hardening
- [ ] Deploy staging — **AD**
- [ ] OWASP ZAP active scan — **KS**
- [ ] Triage High/Med/Low/Info — **KS**
- [ ] Remediate **all High + Medium** — **KS**/**AD**
- [ ] Verify CSP/X-Frame-Options/HSTS actually present in responses — **KS**
- [ ] Re-scan to confirm — **KS**
- [ ] OWASP Top 10 review doc — **KS**

> Expect the TinyMCE stored-XSS path to be the headline finding. Sanitiser
> (2.2) is the fix — this is where it gets proven.

---

## Sprint 6 — Weeks 23–24 — Testing, Deploy, Report

### 6.1 Tests
- [ ] Views: auth'd/unauth'd, status codes, template, DB writes — **KS**
- [ ] Models: constraints, custom methods — **KS**
- [ ] Forms: registration, login, CMS validation — **KS**
- [ ] **coverage ≥80%** across views/models/forms — **KS**
- [ ] UAT from the 9 prototype workflows, 3 roles — **KS**/**SS**/**AL**
- [ ] Usability testing w/ representative non-technical users — **AL**
- [ ] Log prototype-vs-live discrepancies — **all**

### 6.2 Deploy
- [!] **Resolve PostgreSQL hosting** (blocker — decide by Sprint 5) — **AD**
- [ ] Clone repo on host; venv; `pip install -r requirements.txt` — **AD**
- [ ] `.env` with production values; `DEBUG=False`; fresh `SECRET_KEY` — **AD**
- [ ] `migrate`; create superuser — **AD**
- [ ] `collectstatic` (WhiteNoise manifest storage) — **AD**
- [ ] WSGI config → `nstp.settings` — **AD**
- [ ] HTTPS on; verify redirect + HSTS — **AD**
- [ ] Seed all 6 modules of content — **BG**
- [ ] Final ZAP scan against production — **KS**
- [ ] `manage.py check --deploy` clean — **AD**

### 6.3 Report
- [ ] Technical documentation — **KS**
- [ ] User manuals ×3 roles — **KS**
- [ ] Meeting logbook current — **KS**
- [ ] Final report + ACS CBOK mapping — **all**
- [ ] Handover to Dr. Naser Mahmood / AUSDAIS — **AD**

---

## Risk register

| # | Risk | Impact | Mitigation |
|---|---|---|---|
| 1 | `AUTH_USER_MODEL` set after first migrate | 🔴 rebuild DB | Sprint 1 task **1.1**, before any migrate |
| 2 | **PythonAnywhere free tier has no PostgreSQL** | 🔴 can't deploy as specced | Decide by Sprint 5: pay / MySQL / other host |
| 3 | Weak `explanation_text` | 🔴 the differentiator dies | BG drafts early; review M1 explanations in Sprint 2 |
| 4 | TinyMCE stored XSS | 🔴 High ZAP finding | Sanitise on save (2.2); prove in 5.2 |
| 5 | Sprint 3 (quiz+AFE) overruns | 🟠 cascades | Hardest sprint — protect it; cut scope elsewhere |
| 6 | N+1 in dashboards/AFE | 🟠 free-tier CPU | `select_related`; assert query counts in tests |
| 7 | django-ratelimit undeclared on 3.13/5.2 | 🟠 breaks on upgrade | Verified importable now; pin; retest on any bump |
| 8 | 19,200 words of content | 🟠 slips to the end | 2 modules/sprint from Sprint 2 |
| 9 | Question bank = exactly 10 | 🟡 "random" draw isn't random | Spec conflict — need ≥15/module. Confirm with BG |
| 10 | 5 devs, one repo | 🟡 merge pain | App-per-owner boundaries; small PRs |

---

## Open questions for the client / supervisor

1. **Production database host** — PA free tier has no PostgreSQL. Pay, or move? *(blocker)*
2. **Question bank size** — spec says both "ten questions per module" and "a bank
   of more than ten allowing random selection". Which? Random draw needs ≥15.
3. **`Simulation.outcome_text`** — spec describes one field holding *"each possible
   outcome"*. A single text field can't. Make it JSON keyed by decision path?
4. **Simulation scoring** — do simulations affect points/completion, or are they
   practice only? Not stated.
5. **Certificate re-issue** — if a student re-sits after certification, reissue or keep original?
6. **Are the 4 lessons/module fixed?** Completion maths assumes it; nothing enforces it.
