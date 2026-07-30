# Authoring a module (the Module 1 gold standard)

Module 1 (`modules/content/module_one.py`) is the reference implementation. Every
other module copies its shape. This doc is the checklist so Modules 2 to 6 are
fast and consistent. There are no schema changes to make: add a `module_two.py`
in the same shape and register it in the seed.

## The shape (TryHackMe-style room)

- A **module** has **4 lessons**.
- A **lesson** renders as one scrollable **room**: a sticky "Progress X%" bar and
  a vertical stack of numbered, titled, collapsible `<details>` panels.
- A **lesson** is **4 to 8 task panels** whose `points` sum to **10** (banked at
  lesson end through the normal points path, so the economy never changes).
- A **panel is a meaty chunk of learning**: several short paragraphs of reading
  (often a diagram and a callout box) THEN one inline interactive at the bottom.
  The interactive is either:
  - **check**: one question, four options (exactly one correct), an explanation on
    every option, and a **hint**. A "Check answer" button grades it; a wrong try
    reveals the note and shows the hint; retry until correct.
  - **activity**: hands-on. One of `sort`, `inbox`, `spot`, `password`, `branch`.
- Completing a panel ticks its header, pops a "+N XP" toast, fills the progress
  bar, collapses it and opens the next. The last panel fires the celebration.
- Weight toward doing: every panel ends in an interactive. A pure reading panel
  (`kind: "concept"`, completed by a "Mark as complete" button) is allowed but
  rarely needed; prefer folding the reading into the panel that carries the check
  or activity. Each panel should have at least ~40 words of reading.

## Task (panel) data (as authored in `module_one.py`)

Each panel is one dict: a rich `body` (the reading) plus one interactive.

```python
# a check panel: reading THEN a question
{"key": "net-basics", "kind": "check", "points": 3,
 "title": "What a network actually is", "diagram": "data-travels",
 "body": "<p>...several paragraphs...</p>"
         "<div class=\"cy-callout\"><strong>Why this matters:</strong> ...</div>",
 "question": "...", "hint": "...",
 "options": [("A", True, "why right"), ("B", False, "why wrong"), ...]}

# an activity panel: reading THEN the hands-on activity
{"key": "cia-triad", "kind": "sort", "points": 3,
 "title": "The three questions security asks", "diagram": "cia-triad",
 "body": "<p>...reading...</p>",
 "payload": { ... see below ... }}
```

Use `<div class="cy-callout">...</div>` in a body for a highlighted point (the
sanitiser allows it).

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

XP per panel with a "+N XP" toast, the room's "Progress X%" bar filling, a
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
