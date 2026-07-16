# NSTP — System Architecture

Django **MVT** monolith. Chosen over REST+React in BN301: one codebase, one
deploy, server-rendered HTML. The team is five students on a 12-week build —
a split frontend would double the integration surface for no user-facing gain.

**Runtime:** Python 3.13 · Django 5.2 LTS · PostgreSQL 18 · Bootstrap 5.3.

---

## 1. The four apps

Separation is by **domain responsibility**, so team members rarely touch the
same files.

```
nstp/                  project config — settings, root urls, wsgi
├── authentication/    who you are        → User, UserProfile
├── modules/           what you learn     → Module, Lesson, Simulation, ProgressRecord
├── quizzes/           what you're tested on → Quiz, Question, Answer, QuizResult, WrongAnswer
└── certificates/      what you earn      → Certificate
```

**Dependency direction** (one-way; never import backwards):

```
certificates ──► quizzes ──► modules ──► authentication
```

`authentication` knows nothing about the others. `certificates` is the leaf —
it reads quiz results but nothing reads it. This keeps migrations orderable and
prevents circular imports.

---

## 2. The 12 models

### authentication
- **User** — extends `AbstractUser`. `email` is `USERNAME_FIELD` (unique);
  `role` ∈ {Student, Instructor, Administrator}; `is_verified` (False until the
  emailed signed link is clicked). **Set `AUTH_USER_MODEL` before first migrate.**
- **UserProfile** — `OneToOne(User)`. organisation, avatar, `last_active`,
  `streak_count`, `points`, `badges` (JSON list of earned badge ids).

### modules
- **Module** — title, description, difficulty, duration, `order_index`
  (sequential unlock), `is_published` (soft delete), `created_by → User`.
- **Lesson** — `FK(Module)`, `lesson_number`, title, `body_text` (TinyMCE HTML),
  `reading_time`, `is_active`. 4 per module.
- **Simulation** — `FK(Module)`, `scenario_text`, `decision_points` (JSON branching).
- **ProgressRecord** — `FK(User)`, `FK(Lesson)`, `completed_at`. One row per
  lesson completed. Completion % is *derived*, never stored.

### quizzes
- **Quiz** — `FK(Module)`, `time_limit`=30, `pass_mark`=70, `is_active`.
- **Question** — `FK(Quiz)`, `question_text`, difficulty, ordering,
  **`lesson_reference → Lesson`**.
- **Answer** — `FK(Question)`, `option_text`, `correct_answer` (bool),
  **`explanation_text`**. Exactly 4 per question.
- **QuizResult** — `FK(User)`, `FK(Quiz)`, `score`, `passed`, `attempt_number`,
  `submitted_at`.
- **WrongAnswer** — `FK(QuizResult)`, `FK(Question)`, `student_answer`,
  `correct_answer`. One row per incorrect response.

### certificates
- **Certificate** — `FK(User)`, UUID4 `code`, `issued_at`, `pdf_path`.

### ER summary
```
User ─1:1─ UserProfile
User ─1:*─ ProgressRecord ─*:1─ Lesson ─*:1─ Module
User ─1:*─ QuizResult ─*:1─ Quiz ─*:1─ Module
User ─1:*─ Certificate
Module ─1:1─ Simulation
Quiz ─1:*─ Question ─1:*─ Answer
Question ─*:1─ Lesson          (lesson_reference)
QuizResult ─1:*─ WrongAnswer ─*:1─ Question
```

### ⚠️ Two schema gaps in the spec
1. **`Question.lesson_reference` is missing from the spec's field list** but the
   AFE explicitly depends on it. **Add it.**
2. The spec groups feedback "by module section", but **no section/topic field
   exists** on Question. Rather than invent one, **group via
   `lesson_reference → Lesson`** — the lesson *is* the topic. One less field,
   same result, and it's already needed.

---

## 3. Request flow — Quiz Engine (Sprint 3)

The hard parts: a timer you cannot trust, answers that must survive a refresh,
and scoring that must be authoritative.

### Start
```
GET /quizzes/<module_id>/attempt/
  └─► @login_required, role=Student, module unlocked?
      └─► Quiz.objects.get(module=…, is_active=True)
          └─► pick 10 questions
              Question.objects.filter(quiz=q).order_by("?")[:10]
              (NOT random.sample() — that loads the whole bank into memory)
              └─► store ordered question ids + started_at in session
                  └─► prefetch_related("answers") → render form
```

### During
- JS counts down from `started_at + 30min`. **Client-side only — a hint, not a control.**
- Each selection POSTs (or writes to) `session["quiz_answers"][qid]`, so a
  refresh loses nothing.

### Submit
```
POST /quizzes/<module_id>/submit/
  └─► server recomputes elapsed from session started_at
      └─► if > time_limit → force-submit whatever exists
          └─► one query: Answer.objects.filter(question_id__in=ids, correct_answer=True)
              └─► score = correct/10*100 ; passed = score >= 70
                  └─► @transaction.atomic:
                        QuizResult(attempt_number = prior count + 1)
                        WrongAnswer.objects.bulk_create([...])
                      └─► run_adaptive_feedback(result)
                          └─► redirect → results page
```

**Non-negotiables**
- The **server** owns the clock. A browser timer is advisory only.
- The **server** owns scoring. Never accept a client-supplied score.
- `bulk_create` the WrongAnswers — not a save-per-loop.
- Wrap result + wrong answers in one transaction: a half-written attempt would
  corrupt the AFE's input.

---

## 4. Request flow — Adaptive Feedback Engine (Sprint 3)

**The product.** Turns "you got 55%" into "here's exactly what to revise, and why."

Input: a `QuizResult`. Output: a grouped, prioritised study plan.

```
run_adaptive_feedback(quiz_result)
│
├─ 1. Fetch every wrong answer, with everything it needs, in ONE query:
│     WrongAnswer.objects
│       .filter(quiz_result=quiz_result)
│       .select_related("question__lesson_reference")
│       .prefetch_related("question__answers")
│     ── select_related is mandatory: without it this is a textbook N+1.
│
├─ 2. For each wrong answer, pull two explanations from Answer.explanation_text:
│       • why the student's chosen option is wrong
│       • why the correct option is right
│     Both already in memory from the prefetch. Zero extra queries.
│
├─ 3. Group by question.lesson_reference  →  {Lesson: [WrongAnswer, ...]}
│     The lesson is the topic. (See schema gap #2.)
│
├─ 4. Per group, estimate revision time:
│       len(group) * lesson.reading_time
│
├─ 5. Prioritise: most wrong answers first — worst-understood topic on top.
│
└─ 6. Render results.html:
        score + pass/fail  →  per-question "why you were wrong"
                          →  study plan: [lesson, N mistakes, ~X min, link]
```

**Design notes**
- **Pure read + pure function.** It writes nothing. It can be re-run on any past
  `QuizResult` to reproduce identical feedback — which makes it testable and
  makes the results page safely refreshable.
- **Query budget: 2.** One for the wrong answers (joined), one for the prefetch.
  If this grows with the number of wrong answers, it's broken.
- It degrades honestly: a perfect score yields an empty plan and a congratulation,
  not an empty template.
- **Its quality is bounded entirely by `Answer.explanation_text`.** Bigyap's
  writing *is* the feature. Weak explanations = weak product, regardless of code.

---

## 5. Certificate flow (Sprint 5)

```
QuizResult saved
  └─► post_save signal
      └─► has this user passed all 6 module quizzes?
          └─► no  → stop
          └─► yes → get_or_create(Certificate, user=…)   ← idempotent
                    └─► uuid4() code
                        └─► ReportLab: SimpleDocTemplate / canvas.Canvas
                            (A4 landscape, AUSDAIS header, name, code, date,
                             6 modules, signature line)
                            └─► save media/certificates/<uuid>.pdf → pdf_path
```

**Warnings**
- `get_or_create` — a re-sat quiz must not mint a second certificate.
- The spec's *"ReportLab's FPDF class"* **does not exist**. FPDF is an unrelated
  library. Use `reportlab.platypus.SimpleDocTemplate` (flowables — better for a
  document with a list) or `reportlab.pdfgen.canvas.Canvas` (absolute placement —
  better for a fixed decorative layout). ReportLab **cannot render HTML.**
- PDF generation inside a signal blocks the response. Acceptable at this scale;
  if it drags, move it behind a "generate certificate" button.

---

## 6. Security architecture

| Layer | Control | Status |
|---|---|---|
| Transport | HTTPS/TLS, HSTS 1yr, SSL redirect | wired (`DEBUG=False`) |
| Headers | CSP, X-Frame-Options DENY, nosniff | wired (django-csp) |
| CSRF | Django middleware, all POSTs | default |
| SQL injection | ORM only, never raw SQL | convention |
| XSS | template auto-escape | default — **but sanitise TinyMCE HTML server-side** |
| Passwords | PBKDF2-SHA256, **1,000,000 iters** (Django default) | **do not override to spec's 260k** |
| 2FA | django-otp TOTP; QR rendered from `config_url` | pending Sprint 1 |
| Brute force | django-ratelimit 10/hr per IP → 429 | pending Sprint 1 |
| Access control | role check on **every** view, every request | convention |

**Known weaknesses**
- **TinyMCE is a stored-XSS vector.** Instructor HTML lands in `body_text` and
  renders in every student's browser. Auto-escaping would show raw tags, so it
  must render unescaped — meaning it **must be sanitised on save** (allow-list).
  This is the single most likely High finding in the ZAP scan.
- **Rate limiting uses LocMemCache** — per-process, so limits aren't shared
  across workers. Fine for PythonAnywhere's free single worker; wrong the moment
  it scales.

---

## 7. Deployment

Flow: GitHub → PythonAnywhere → venv → `.env` → `migrate` → `collectstatic`
(WhiteNoise) → WSGI config → HTTPS → final ZAP scan.

**🔴 Blocker:** PythonAnywhere's **free tier has no PostgreSQL** (MySQL is paid;
PG is a paid add-on). The spec's stated rationale — "free hosting with PostgreSQL
support" — is factually wrong. Options:
1. Paid PA plan (~$10/mo) — client decision.
2. MySQL in prod — but then prod ≠ dev, and PG-specific behaviour goes untested.
3. Host elsewhere with free PG (Render/Fly/Railway) — deviates from the spec.

Needs a decision **before Sprint 5**, not during it.

Also: **Gunicorn is redundant on PythonAnywhere** — PA runs its own WSGI server.
The spec's claim that Gunicorn "integrates with PythonAnywhere's infrastructure"
is wrong. It is not in `requirements.txt`.
