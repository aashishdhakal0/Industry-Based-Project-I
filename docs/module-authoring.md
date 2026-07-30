# Authoring a module (the Module 1 gold standard)

Module 1 (`modules/content/module_one.py`) is the reference implementation. Every
other module copies its shape. This doc is the checklist so Modules 2 to 6 are
fast and consistent. There are no schema changes to make: add a `module_two.py`
in the same shape and register it in the seed.

## The shape

- A **module** has **4 lessons**.
- A **lesson** is **5 to 8 ordered tasks** whose `points` sum to **10** (banked at
  lesson end through the normal points path, so the economy never changes).
- A **task** is one of:
  - **concept**: a punchy chunk of 2 to 4 sentences, usually paired with a
    diagram. Finished with the foot "Got it" button.
  - **check**: one question, four options (exactly one correct), an explanation on
    every option, and a **hint**. Instant per-option feedback; the hint also
    appears after a wrong answer.
  - **activity**: hands-on. One of `sort`, `inbox`, `spot`, `password`, `branch`.
- **Ordering rule:** never two concept tasks in a row. Weight the lesson toward
  doing. (Enforced by `test_never_two_concept_tasks_in_a_row`.)

## Task data (as authored in `module_one.py`)

```python
# concept
{"key": "net-intro", "kind": "concept", "points": 1,
 "title": "...", "diagram": "data-travels", "body": "<p>...</p>"}

# check (option tuples are (text, is_correct, explanation))
{"key": "net-check", "kind": "check", "points": 2,
 "title": "Quick check", "question": "...", "hint": "...",
 "options": [("A", True, "why right"), ("B", False, "why wrong"), ...]}

# activity (config in payload)
{"key": "cia-sort", "kind": "sort", "points": 3, "title": "...",
 "payload": { ... see below ... }}
```

## Activity payload contracts

- **sort** `{prompt, buckets:[{id,label}], items:[{id,text,bucket,why}]}` — solved
  when every item is in its correct bucket. Wrong drop nudges and retries.
- **inbox** `{prompt, avatar, parts:[{id,zone,text,bad,why}]}` — tap the parts that
  are `bad`; solved when all are found. A "found X of Y" counter tracks progress.
- **spot** `{prompt, left, right, fake:'left'|'right', why}`. Default renders
  message cards (`{sender,text}`). Add `variant:"login"` with `left/right =
  {url, brand}` to render two login-page mockups (address bar plus a form) for a
  real-vs-lookalike domain.
- **password** `{prompt, target:'strong', common:[...], tips:[...]}` — live meter
  and checklist (length, a mix or a few words, not common); solved at Strong.
  Purely client-side; nothing is sent or stored.
- **branch** `{prompt, start, nodes:{id:{text, choices:[{label,to,feedback,
  outcome}]}}}` — solved on reaching an ending (a node with no choices). Poor
  choices route through a short consequence node and converge.

Activities render from a CSP-safe `{{ payload|json_script }}` block and are driven
by `static/js/activities.js`, which fires `cy:solved` when complete.

## Diagram catalogue (`modules/templates/modules/_diagram.html`)

CSS/SVG only (CSP blocks external images). Reference by `diagram` key on a task:
`cia-triad`, `data-travels`, `phishing-email`, `two-factor`, `defence-in-depth`.
Add new keys as a new `{% elif key == "..." %}` branch plus CSS.

## Quiz contract

`QUIZ = {"pass_mark": 70, "questions": [...]}`. At least 20 questions (Module 1
has 28), roughly evenly spread across the four lessons (10 are drawn per attempt).
Each question: `{lesson, difficulty, text, options: [(text, is_correct,
explanation) x4]}` with exactly one correct option and an explanation on **every**
option. The explanations are what the Adaptive Feedback Engine reads back, so they
must teach, not just say right or wrong.

## Voice (non-negotiable)

Warm, confident, human. Plain Australian English for non-technical readers. Short
chunks, no walls of text. Every idea ties to "why this matters to you and what to
do". Concrete local scenarios (a clinic, a council desk, a cafe, a school). **No
em-dashes or en-dashes**, no filler. Use commas, colons, full stops and
parentheses. Enforced by `test_lesson_content_has_no_em_dashes` and
`test_quiz_content_has_no_em_dashes`.

## Gamification (free, do not re-invent)

XP per task with a "+N XP" toast, a per-lesson "Task X of Y" progress bar, a
lesson-complete celebration, and the module-complete moment on passing the quiz
(which unlocks the next module and advances the certificate). Streaks, level and
badges all recompute from real records; keep task points summing to 10 and it all
just works.

## Navigation and static (must stay intact)

The room JS is referenced with a `?v=` cache-buster in `lesson.html`. **Bump it
whenever `lesson.js` or `activities.js` changes** so browsers cannot serve a stale
copy. After any JS change: run `python manage.py collectstatic`, confirm the served
file is non-zero, and that back / continue / activity-gates-continue / final
navigate still work.

## To add Module N

1. Create `modules/content/module_two.py` with `LESSONS` and `QUIZ` in this shape.
2. Point the seed at it (extend `seed_learning_content`) and register the module's
   title and lesson titles.
3. Copy the content tests, pointed at the new module.
4. Re-seed, run the suite, `collectstatic`.
