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
**All six modules are 2 hands-on lessons each** (so **12 lessons total**; Modules
5 and 6 were consolidated 4→2 when rebuilt as the flagship modules). Every module
has a quiz of **exactly 10 questions** (not a
larger random-draw bank): `draw_questions` returns all 10, so the paper is fixed,
7/10 to pass. Each question is tightly tied to that module's actual lesson
content, is a deliberate mix of practical (scenario) and theoretical (knowledge)
items, traces to the lesson that teaches it via `lesson_reference`, and carries 4
options with exactly one correct and an explanation on **every** option (the AFE's
fuel). Per-lesson quiz spread is now 5+5 for every module.
Each module also carries a short **`Module.tagline`** motto (seeded from `TAGLINES`
in the seed, shown as an accent eyebrow on the overview). Content lives as plain
data in
`modules/content/module_<n>.py` (`LESSONS` + `QUIZ`), loaded by the seed via a
`CONTENT` registry; the per-module lesson count is driven by `MODULES` in the
seed (which prunes any lesson rows beyond the authored count, after the quiz is
reseeded so no `Question.lesson_reference` still points at a pruned lesson).
Lessons render as a scrollable TryHackMe-style **room** (numbered, collapsible
panels; XP per panel; sticky progress; a task-index rail). Voice is warm, plain
Australian English, **no em-dashes** (enforced by tests).

**The 5-task lesson format.** Every lesson is a five-panel room, 2 XP each,
banking 40 XP. **Module 1** uses: **1** Core `CHECK` · **2** `RESPOND` · **3**
picture-question `CHECK` · **4** `QUIZSET` · **5** applied `CHECK`. **Module 2 is
fully HANDS-ON** (rebuilt so every panel is a practical drill, not reading then
MCQ; the teaching happens through the interaction's per-item feedback): only
Task 3 stays the picture-question `CHECK`, and the rest are activities. L1 =
`SORT` (sort behaviours to malware type) · `BRANCH` (the call, then the car park)
· `CHECK` (fake-update) · `MAILSORT` (triage a mixed inbox) · `BRANCH` (tabletop
mini-incident). L2 = `CLASSIFY` (ransomware / breach / glitch) · `BRANCH`
(ransom-note-on-screen) · `CHECK` (ransom-screen) · `SEQUENCE` (order the
incident-response steps) · `BRANCH` (breach tabletop). Verified by executing
`activities.js` under `jsc` with a DOM shim: each activity fires `cy:solved` only
after it is correctly solved (harness in the session scratchpad).

**Realistic picture-question visuals** are CSP-safe HTML/CSS partials keyed in
`modules/templates/modules/_diagram.html` (a task's `diagram` field selects one;
it renders at the top of the panel regardless of task kind, so an interactive
drill can carry a picture too; partials bypass the nh3 sanitiser, so full
SVG/HTML/class is allowed, but no emoji and no external images — CSP is
`img-src 'self' data:`; use the `#i-*` SVG sprite icons). Styling lives in
`cybaroo.css`. The screenshot-style keys built so far: `router-admin`,
`secure-bars`, `scam-email`, `email-invoice`, `security-settings`,
`device-checklist` (M1), and for M2 **`fake-update`** (fake update pop-up),
**`ransom-screen`** (ransom lock screen), **`download-trap`** (a real download
link next to an ad-button), **`attachment-exe`** (an `Invoice.pdf.exe` double
extension), **`locked-files`** (a file explorer of `.locked` files), and
**`breach-email`** (a data-breach notice); for **M3** `sms-phish` (a smishing
text), `exec-email` (an annotated BEC email with red-flag callouts), `caller-id`
(a spoofable incoming-call screen); for **M4** `msg-encrypted` (encrypted-vs-open
compare), `secure-share` (public-vs-restricted share link), `wifi-evil-twin` (a
cafe Wi-Fi picker with a lookalike hotspot); and the **M1 hero** `net-scene` (a
dark data-flow scene, device → router → internet → server with terminal-style
callouts, used via `payload["hero"]` on L1 T1). Annotated figures share the
`cy-flag` callout classes, alongside the older schematic diagrams (`cia-triad`,
`malware-family`, `data-breach`, `ddos`, etc.).

**Picture-questions in M2** — each M2 lesson carries THREE: the Task 3 picture
CHECK, plus two more embedded on interactive panels as a `diagram` + an
`inline_check` (the same `_check_block.html` UI: question, hint, 4 explained
options, instant feedback). Because `lesson.js` counts every `[data-check-block]`
as a required completion slot (`slotsTotal = checks + activities`), the embedded
picture-question is mandatory AND the drill on that panel is preserved. L1 embeds
`download-trap` (on the delivery BRANCH) and `attachment-exe` (on the MAILSORT);
L2 embeds `locked-files` (on the ransom-note BRANCH) and `breach-email` (on the
breach tabletop BRANCH).

| # | Title | Lessons | Flagship / signature activity |
|---|---|---|---|
| 1 | **Network Security Fundamentals** | **Two deep lessons** (5-task format): What a network is, and what you protect · How attacks actually happen. (Lessons 3 and 4 were retired; their quiz questions were rebalanced into the two remaining lessons.) | The **`respond`** apply-it activity + **`quizset`** + picture-questions (`router-admin`, `secure-bars`, `cia-triad`, `scam-email`, `email-invoice`) |
| 2 | **Recognising Cyber Threats** | **Two DEEP, fully HANDS-ON lessons**: Know the threats: malware, and how it gets in · When it goes wrong: ransomware, breaches, and reacting | Every panel is a drill: **`sort`** malware behaviours · **`branch`** decision drills + tabletop mini-incidents · **`mailsort`** inbox triage · **`classify`** ransomware/breach/glitch · **`sequence`** the incident-response order · three picture-questions per lesson (`fake-update`/`download-trap`/`attachment-exe`; `ransom-screen`/`locked-files`/`breach-email`) |
| 3 | **Phishing & Social Engineering** (motto "They hack the human. Verify anyway.") | **Two hands-on lessons**: The con, and the channels it comes through · Read it like an analyst: spot, verify, report | Multi-channel: `classify` (email/SMS/voice/BEC) · `branch` CEO **AI voice-clone** call + BEC + tabletops · `mailsort` · `spot` · picture figures (`sms-phish`, `exec-email`, `caller-id`) |
| 4 | **Secure Communication Practices** (motto "Before you hit send, think.") | **Two hands-on lessons**: Before you hit send: what 'secure' really means · Sharing safely: files, links, and Wi-Fi | A "before you hit send" checklist: `sort` encrypted-vs-open · `classify` · `branch` send/share decisions · `harden` the mobile workspace · picture figures (`msg-encrypted`, `secure-share`, `wifi-evil-twin`) |
| 5 | **Firewall & Network Defence** (motto "Set the rules. Watch them hold.") | **Two DEEP flagship lessons** (rebuilt 4→2): The firewall: reading the rules · Defence in depth: segment, connect safely, watch for trouble | The new **`firewall`** rule-reading activity (ordered first-match rule table + traffic to judge) · **`segment-flow`**/**`firewall-flow`** animated heroes · `classify` (device→zone segmentation) · `branch` (remote access / VPN) · **`netmap`** · `sort` (default-deny) |
| 6 | **Incident Response** (motto "Panic is optional. A plan is not.") | **Two DEEP flagship lessons** (rebuilt 4→2): When the alert fires: detect and contain · Clean up, come back, and the law | The new **`tabletop`** activity (staged incident + live situation board), one continuing Geelong dental-practice ransomware scenario across both lessons covering detect→contain→eradicate→recover→review · `incident-escalation`/`recovery-board` animated heroes · `sequence` (six phases) · `classify` (notifiable-or-not) · maps to the Privacy Act 1988 NDB scheme |

### Interactive activity types (all built; driven by `static/js/activities.js`)
Each activity reads a CSP-safe `{{ payload|json_script }}` block and fires
`cy:solved` when complete. `LessonTask.Kind` enumerates them:
- **inbox** — inspect one email; tap every "tell"
- **spot** — real vs fake (message cards, or a `variant:"login"` page mock-up)
- **password** — live strength meter + checklist; solved at Strong
- **branch** — multi-step scenario with consequences; solved at an ending
- **classify** (M2–M6) — read each alert, pick its category, teaching feedback
- **mailsort** (M2, M3) — a mixed inbox; mark each email Genuine/Phishing
- **harden** (M4) — secure each part of a workspace ("At risk" → "Secured")
- **netmap** (M5) — tap every weakness on a network map
- **sequence** (M2, M6) — put shuffled steps into the correct order
- **sort** (M2–M6) — tap a chip, tap its bucket (e.g. sort behaviours to malware type)
- **respond** (M1) — realistic "what would you do?" situations; pick the sound
  action, see the consequence; the reusable **apply-it** workhorse
- **quizset** (M1) — a mixed mini-quiz in one panel: mcq / true-false / fill /
  match sub-questions; fires `cy:solved` when all are answered
- **check** / mid-panel **inline_check** — apply-it MCQs (question + hint + 4
  options with per-option explanations)
- **firewall** (M5) — an ordered, first-match firewall rule table + traffic to
  judge ALLOW/BLOCK; a correct verdict flags the deciding rule. Payload
  `{prompt, rules:[{n,action:"ALLOW"|"DENY",desc}], traffic:[{text,verdict:"ALLOW"|"BLOCK",rule,why}]}`
- **tabletop** (M6) — a staged incident-response exercise with a **live situation
  board** (systems / data / clock / notification) that updates on each decision;
  sound calls bring it back to green, poor calls escalate it but the exercise
  continues and teaches; solved after a short debrief. Payload
  `{prompt, scenario, board:[{id,label,state:"ok"|"warn"|"bad",value}], stages:[{phase,title,prompt,options:[{label,outcome:"good"|"bad",consequence,board:{id:{state,value}}}]}]}`

**Animated "watch it unfold" sequences (the video substitute).** CSP forbids
external video, so the "wow" dynamic moments are **pure-CSS keyframe animations**
rendered as `_diagram.html` partials, auto-playing, `prefers-reduced-motion`-safe
(each freezes at a clear resting state). Carried on a task via `payload["hero"]`
(same mechanism as the M1 hero). Four so far: **`firewall-flow`** (a packet
arrives, is inspected, allowed or blocked), **`segment-flow`** (infection spreads
on a flat network vs contained on a segmented one), **`incident-escalation`** (two
timelines racing: no-plan climbs, with-plan flatlines), **`recovery-board`**
(systems flip down→restoring→online in sequence). Styling + `@keyframes` live in
`cybaroo.css`; verified render + that reduced-motion disables them.

Authoring reference: **`docs/module-authoring.md`** (the Module 1 gold standard —
panel shape, payload contracts, voice rules). Copy it to add/extend a module.

### Quiz engine + Adaptive Feedback Engine
- `quizzes/services.py` draws 10 questions (`order_by('?')[:10]`; each bank is now
  exactly 10, so it returns all of them), grades **server-side** against the stored
  `correct_answer` flag (never trusts the client), pass mark **70%** (7/10), records
  a `QuizResult` (+ `WrongAnswer` rows), awards +200 on a first pass.
- `quizzes/feedback.py` (the AFE) reads the `WrongAnswer`/`explanation_text` rows
  and builds a per-lesson **study plan** shown on the result page: which lessons
  to revise (ranked by where mistakes clustered) and why each answer was wrong.

### Gamification engine (`modules/gamification.py`)
- **Records are the truth.** `UserProfile.points` is a **cache recomputed** from
  `ProgressRecord` (lessons) + distinct passed `QuizResult` (quizzes) on every
  completion — never incremented, so it cannot drift. Points = lessons×50 +
  passed_quizzes×250 (**12 lessons** now, since all six modules are 2 hands-on
  lessons each, + 6 quizzes = **2100, the ceiling**). The constants live in
  `gamification.py` (`POINTS_PER_LESSON`/`POINTS_PER_QUIZ`); the level curve
  `_points_to_reach` uses `POINTS_PER_LESSON` as its constant, so curve and
  economy scale together (level 2 after four lessons, etc.).
  Tier thresholds: Bronze 0 · Silver 200 · Gold 500 · Platinum 1000 · Diamond 2000
  (gaps 200/300/500/1000, each tier harder-won than the last).
  A fully finished course (2100) now **reaches Diamond** (2000+), the top tier,
  earned on the final quiz. Rescaled from 40/200 on 2026-08-20 so completion lands
  in Diamond rather than Platinum.
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
- **Simulation** (`/learn/m/N/simulation/`): **Modules 1 and 2 have a scene-based
  branching simulation** — a visual, scene-by-scene story, **exactly 2 (rich)
  decision scenes** each (backdrop illustration + narrative + choices; each choice
  reveals a consequence and advances; a progress stepper and a score-based
  ending). Data shape `{"kind": "scenes", start, scenes{id:{backdrop,title,
  narrative,choices:[{label,outcome,consequence,to}]}}}` in the seed
  (`MODULE1_SIM`/`MODULE2_SIM`); driven by the scene engine in
  `static/js/cybaroo.js`, which posts `{score,total,path}` to the unchanged
  `complete_simulation` endpoint. **Scene classes use the `cy-scn*` namespace, NOT
  `cy-scene` — `cy-scene` is the landing-page hero animation (grid + child
  stacking); reusing it made the scene art and text overlap in one square (a real
  bug that was fixed).** Each backdrop is a composed CSS "device window"
  illustration (`cy-scn--email/attach/ransom/win`). Modules 3–6 still use the
  older judge-the-inbox placeholder (`kind:"inbox"`), which the same JS still
  handles. Verified end-to-end under `jsc` (walks the good path, posts a perfect
  score, returns to the module).
- **Real quiz page** (`/learn/m/N/quiz/`, `quiz.html` + `static/js/quiz.js` +
  `.cy-quiz*`): a one-question-at-a-time stepper with a progress bar. It is
  **interactive, Kahoot/Duolingo-style**: options are neutral until the learner
  selects one, then quiz.js reveals correct/incorrect + the explanation and
  **locks** the question (it disables the other radios but keeps the chosen one
  enabled so it still submits), and enables Next. Each option ships `data-correct`
  + a hidden explanation to the client (same pattern as the in-lesson CHECK
  activities); **grading stays server-side** on submit (`submit_quiz` against the
  stored `correct_answer`) — the reveal is purely visual. A per-question
  difficulty tag uses ONE flat muted style (no per-level colours). No-JS falls
  back to a plain form with a single Submit. Verified by a `jsc` DOM harness
  (select → reveal → lock → Next).
- **Quiz review (DEBUG only)** (`/learn/m/N/quiz/review/`, `quiz_review.html` +
  `.cy-qr*`): a **separate** developer content-review page (different template and
  classes from the real quiz) listing every question with the correct answer
  marked and all explanations shown at once — that show-everything behaviour is
  its whole purpose. The view raises `Http404` when `DEBUG=False`, so it never
  exists in production; a "Review all questions (dev)" link shows on the module
  overview only when `settings.DEBUG`. Both pages share ONE type scale (Bricolage
  question anchor, Instrument-Sans options, smaller secondary explanations) and
  the flat difficulty tag, but the real quiz never reveals answers upfront and the
  review page never becomes interactive. The real quiz gate (`_all_lessons_done`)
  is untouched; this is separate from the DEBUG dev-unlock that lets you open the
  actual quiz without finishing lessons.
- **Module overview** (`/learn/m/N/`, `overview.html`): a designed **roadmap** —
  each lesson is a card with its **task chips** (per-task done state; each chip
  has a per-kind colour + icon), then a simulation card and a quiz card, with a
  connecting spine and the completion moment. The view passes `lesson.task_list`
  (tasks with `.done`, `.chip_label`, `.chip_icon`, `.chip_kind` from `_TASK_CHIP`)
  and `debug`. **Its classes use the `cy-mroad*` namespace, NOT `cy-road` —
  `cy-road` is the dashboard's horizontal progress track, whose styles leaked in
  when reused. The CTA text colour is set with `.cy-mroad a.cy-mroad__cta`
  (specificity 0,2,1) so it beats the global `.cy-body a { color: cyan }` (0,1,1);
  without that, the "Start" button was cyan-on-cyan and invisible (a fixed bug).**

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

### Two-mode lesson treatment: reading vs question (DONE, all modules)
**"Visually distinguish reading content from interactive activities across ALL
lessons."** Solved entirely in the **shared** `cybaroo.css` (no per-module work),
so it applies to every module automatically, now and going forward:
- **Reading mode** — `.cy-panel__body .cy-prose` gets a calm neutral card
  (`--cy-surface` bg, `--cy-border`, rounded, padded) with a small monospace
  **"Reading"** eyebrow via `::before`. A body-prose block that follows a check or
  activity (`.cy-check ~ .cy-prose`, `.cy-panel__do ~ .cy-prose`) suppresses the
  eyebrow so it doesn't repeat; a `.cy-task__scenario` prose block reads
  **"Scenario"** instead; a first-child prose block drops its top margin.
- **Question / interactive mode** — `.cy-panel__do` and `.cy-check` keep the
  tinted violet/cyan gradient card + top accent bar (`::before`) + the cyan
  `.cy-panel__do-label` pill. Same theme, complementary tones — one product, two
  clear modes, not two apps.
The approved direction was confirmed against a published artifact preview first.
CSS cache-buster is `css/cybaroo.css?v=25` in `templates/base.html` (bump on any
CSS change, then `collectstatic`, then hard-refresh).

### Visual identity: "Cyan & Teal command console" re-theme (DONE, 2026-08-22)
The platform is themed as a **vivid-but-matte cyan/teal command console on a
matte-black textured background** (earlier violet/cyan, muted-teal, and Cobalt &
Coral directions were all superseded). It is token-driven in `cybaroo.css`
`:root`; the two accent token FAMILIES now carry the two accents:
- **Cyan** (PRIMARY — CTAs, "current/you are here", active progress, correct):
  `--cy-violet #00d9ff` / soft `#5be7ff` / deep `#0899b8`.
- **Teal** (SECONDARY — structure, secondary actions, streak/energy):
  `--cy-cyan #00e5cc` / soft `#4fecd8`.
- **Gold** (tier badges + achievement): `--cy-gold #e6b455` (tier metals brushed).
- **Red** (errors, wrong answers, streak-at-risk, warn): `--cy-flame #ff4d4d` and
  `--cy-danger #ff4d4d`.
- Ground: matte black `--cy-bg #06080c`, surfaces `#0e141d`/`#141d29`/`#1c2836`,
  borders `#24344a`/`#33465f`; text `#e9f1f8`.
**`--cy-flame` was split by rule**: it historically served BOTH streak (energy)
and wrong/at-risk (error). A selector-keyword classifier re-pointed each usage —
`streak`/`--safe`/energy → teal (`var(--cy-cyan)`), `wrong`/`is-bad`/`at_risk`/
`warn`/`fail` → red (`var(--cy-danger)`). If adding new "wrong" or "streak" CSS,
use `--cy-danger` for errors and `--cy-cyan` for streak, NOT `--cy-flame`.
**Textured background**: `body.cy-body` carries a pure-CSS blueprint grid + circuit
dots + faint cyan/teal glows (`background-attachment: fixed`), faint enough for AA
readability (copy sits on solid panels). Module tiles in
`modules/presentation.py` `TILES` (cyan/teal set); badge tiles in `badges.py`.
**Type** is **Archivo** + **JetBrains Mono** (self-hosted). Applies to every
student surface (dashboard, overview, lesson, simulation, quiz, certificate) and
the shared shell. "One colour, one purpose"; WCAG AA on all surfaces. Re-theme
flow: options preview → chosen-direction full preview → real templates.
**Polish (2026-08-22):** (1) text neutrals shifted sky-blue (`--cy-text-2
#a6bce0`, `--cy-text-3 #8ea0cc`) — cooler, less green. (2) A per-tier **glow**
behind the profile badge (`.cy-chip__av` box-shadow halo + blurred `::before`
using each tier's `--tier-glow`, alphas bumped ~.5–.6; gentle pulse gated by
`prefers-reduced-motion`). (3) The dashboard **stats redesigned** for real
hierarchy: dominant 2.2rem display number, mono label, a thin cyan `.cy-pstat__bar`
(points→tier, level→level), then a separated sub-line ("**160** to Silver"); the
level stat dropped its ring for an icon+number; secondary stats (`.cy-mstat`)
restructured (big number + `/total` + mono label via `.cy-mstat__top`).
**Final polish (2026-08-24):** primary text `--cy-text → #f5f7fa` (crisp near-white,
"black + white + one electric accent"); `.cy-btn--primary` overridden to the
brightest cyan (`linear-gradient(120deg,#22e0ff,#00c8f0)` + dark ink `#04121a`,
button-only so the shared `--cy-grad-cta` and its 14 hero fills are untouched);
**all correct-answer states unified to bright cyan** — leftover greens (`#6bbf7e`,
`rgba(129,201,149,*)` in the quiz/review) and `.is-right`/`.is-correct` teal usages
were routed to `--cy-violet`/`--cy-violet-soft`. Correct = cyan, wrong = red
(`--cy-danger #ff4d4d`), streak/structure = teal. css `?v=29`.

### People-scene picture-questions on Task 2 (M3, M4) (DONE)
M3 and M4 Lesson 1 Task 2 (the send/share scenario BRANCH) now carry a **custom
SVG people scene** (own-origin, CSP-safe, no external images, no emoji) plus an
`inline_check` picture-question read straight off the scene, alongside the BRANCH
drill. Two new figures in **`_diagram.html`** (bypass nh3, full SVG allowed):
- **`scene-vish`** (M3) — a worried worker on the phone at a bank-transfer screen
  ($48,500 / PAY NOW), speech bubble "transfer $48,500 right now, and keep it
  quiet", sticky note. Vishing / AI voice-clone. **Replaced the old `caller-id`
  figure** (M3 no longer uses `caller-id`).
- **`scene-send`** (M4) — two colleagues at a monitor composing an email to a
  personal address with a medical form attached (`Client_medical_form.pdf`), a
  concerned colleague pointing. Insecure send. (M4 L1 T2 previously had no figure.)
The BRANCH controller ignores the extra `inline_check` in the payload (same
pattern as M2's embedded picture-questions); `lesson.js` renders it as a required
`[data-check-block]` completion slot. `.cy-ppl` in `cybaroo.css` frames the scene.

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
- **Static caching / `?v=N` cache-buster.** Four versions: the room scripts in
  `lesson.html` load as `js/lesson.js?v=N` and `js/activities.js?v=N`
  (**currently `?v=17`**); `cybaroo.css` in `templates/base.html` loads as
  `css/cybaroo.css?v=N` (**currently `?v=25`**); `cybaroo.js` in `base.html` loads
  as `js/cybaroo.js?v=N` (**currently `?v=3`**, simulation + UI bits); and
  `quiz.js` in `quiz.html` loads as `js/quiz.js?v=N` (**currently `?v=2`**, the
  interactive quiz stepper). After ANY change to `lesson.js`/`activities.js`: bump
  in `lesson.html`. After `quiz.js`: bump in `quiz.html`. After `cybaroo.css` or
  `cybaroo.js`: bump in `base.html`. Then in every case: run
  `collectstatic --noinput` (and once with `DEBUG=False` for the WhiteNoise
  manifest), and **hard-refresh** the browser. In DEBUG (unhashed
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
- **Bespoke simulation pages for Modules 3–6** — Modules 1 and 2 now have real
  scene-based branching simulations; Modules 3–6 still use the judge-the-inbox
  placeholder.
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
`User 1─* QuizResult *─1 Quiz`; `User 1─* Certificate`; `Module 1─* Lesson (2 per
module, all six)`;
`Module 1─1 Simulation`; `Module 1─1 Quiz`; `Quiz 1─* Question (exactly 10, all
drawn)`; `Question 1─* Answer (exactly 4, one correct)`; **`Question *─1 Lesson`**
(`lesson_reference` — required by the AFE); `QuizResult 1─* WrongAnswer *─1
Question`; `Lesson 1─* LessonTask *─1 TaskProgress`.

Key fields: `User.role ∈ {STUDENT, INSTRUCTOR, ADMINISTRATOR}`, `is_verified`.
`Module.order_index` (sequential lock), `is_published` (soft delete), difficulty.
`Answer.correct_answer` (bool), **`explanation_text`** (the AFE's fuel).
`Quiz.pass_mark=70`. `LessonTask.kind ∈` the activity enum + CHECK/CONCEPT.
Latest migration: **`modules/migrations/0015_alter_lessontask_kind.py`** (adds the
`FIREWALL` + `TABLETOP` kinds; 0014 added `Module.tagline`; 0012 added `quizset`;
0013 added `LessonTask.image`). Lesson-count reductions (M3/M4 and M5/M6 all 4→2)
are pure seed data, no migration. The **hero** figure (incl. the M5/M6 animated
sequences) is stored in a task's `payload["hero"]` (no migration), rendered by
`lesson.html` above the panel's own diagram.
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
