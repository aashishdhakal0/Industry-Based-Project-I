"""Seed the six modules, their lessons and their simulations.

Idempotent: run it as often as you like. Everything keys on a natural unique
field (module order_index, lesson number, one simulation per module) via
get_or_create / update_or_create, so re-running updates in place rather than
duplicating.

The lesson bodies are CLEARLY-MARKED PLACEHOLDERS — the real ≥800-word lessons
come after the system is signed off. They are deliberately rich (headings,
lists, a callout, a table) so the reading experience and the sanitiser are
exercised against real structure, not a single paragraph.

Content is data, not schema: this is a management command, not a data migration,
so it stays re-runnable and out of the migration history.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from authentication.models import User
from modules.content import (
    module_five,
    module_four,
    module_one,
    module_six,
    module_three,
    module_two,
)
from modules.gamification import POINTS_PER_LESSON
from modules.models import Lesson, LessonTask, Module, Simulation
from quizzes.models import Answer, Question, Quiz

# Task points are authored against a 10-XP-per-lesson base (each lesson's tasks
# sum to 10 in the content files). The live economy scales that up, so multiply
# every task's points by the same factor here — the tasks then sum to
# POINTS_PER_LESSON exactly, and the in-lesson XP bar matches what the lesson banks.
_POINTS_SCALE = POINTS_PER_LESSON // 10

# Modules with finished, interactive content (LESSONS + QUIZ), keyed by
# order_index. Adding a module is data-only: write modules/content/module_N.py in
# the Module 1 shape and register it here. Anything not listed falls back to the
# rich placeholder until its turn.
CONTENT = {
    1: module_one,
    2: module_two,
    3: module_three,
    4: module_four,
    5: module_five,
    6: module_six,
}

# (title, description, difficulty, four lesson titles)
MODULES = [
    (
        "Network Security Fundamentals",
        "How networks work, and where yours is most exposed.",
        Module.Difficulty.BEGINNER,
        [
            "What a network is, and what you protect",
            "How attacks actually happen",
        ],
    ),
    (
        "Recognising Cyber Threats",
        "Malware and how it gets in, the real Australian breaches, and how to react.",
        Module.Difficulty.BEGINNER,
        [
            "Know the threats: malware, and how it gets in",
            "When it goes wrong: ransomware, breaches, and reacting",
        ],
    ),
    (
        "Phishing & Social Engineering",
        "The con behind the click, across every channel, and how to spot it.",
        Module.Difficulty.INTERMEDIATE,
        [
            "The con, and the channels it comes through",
            "Read it like an analyst: spot, verify, report",
        ],
    ),
    (
        "Secure Communication Practices",
        "What secure really means, and how to communicate that way as routine.",
        Module.Difficulty.INTERMEDIATE,
        [
            "Before you hit send: what 'secure' really means",
            "Sharing safely: files, links, and Wi-Fi",
        ],
    ),
    (
        "Firewall & Network Defence",
        "The defences around your whole business, and how to spot where they are missing.",
        Module.Difficulty.ADVANCED,
        [
            "The firewall: reading the rules that guard your network",
            "Defence in depth: segment, connect safely, and watch for trouble",
        ],
    ),
    (
        "Incident Response",
        "A calm, six-phase plan for what to do when something goes wrong.",
        Module.Difficulty.ADVANCED,
        [
            "When the alert fires: detect and contain",
            "Clean up, come back, and the law: eradicate, recover, review",
        ],
    ),
]

# A short motto/framing line per module (by order_index), shown as an accent
# eyebrow on the module overview.
TAGLINES = {
    1: "Know your network. Guard every door.",
    2: "Name the threat. Stop the spread.",
    3: "They hack the human. Verify anyway.",
    4: "Before you hit send, think.",
    5: "Set the rules. Watch them hold.",
    6: "Panic is optional. A plan is not.",
}


def _placeholder_body(module_title, lesson_title):
    return f"""
<p><strong>Placeholder lesson.</strong> This stands in for the full lesson on
&ldquo;{lesson_title}&rdquo; from <em>{module_title}</em>. The finished lesson
will run to around 800 words in plain English; this version exists so the
reading experience, progress tracking and content structure can be built and
tested first.</p>

<h2>What this lesson will cover</h2>
<ul>
  <li>The one idea that matters most, stated plainly.</li>
  <li>A real Australian example you'll recognise.</li>
  <li>The single habit that prevents most problems.</li>
</ul>

<h3>A worked example</h3>
<p>The real lesson walks through a situation you might actually meet at work,
step by step, and points out exactly where the risk is and what to do about it.</p>

<blockquote>Key point: you don't need to be technical to stay safe — you need to
know what to look for, and to slow down when something feels rushed.</blockquote>

<h3>Quick reference</h3>
<table>
  <thead><tr><th>If you see&hellip;</th><th>Do this</th></tr></thead>
  <tbody>
    <tr><td>An unexpected urgent request</td><td>Stop and verify another way.</td></tr>
    <tr><td>A link you weren't expecting</td><td>Don't click — check the address first.</td></tr>
  </tbody>
</table>

<p>The full lesson ends with a short recap and leads into the next one.</p>
""".strip()


# --- Scene-based branching simulations (Modules 1 and 2) -------------------
# A visual, scene-by-scene story: each scene has a backdrop illustration (styled
# by cybaroo.css from `backdrop`), a narrative, and choices. Picking one reveals
# its consequence, then Continue advances to the next scene, ending in a summary.
# cybaroo.js drives it and posts score/total/path to complete_simulation.

MODULE1_SIM = {
    "kind": "scenes",
    "intro": "Two situations, one ordinary morning at a small clinic. Read each "
    "one carefully, weigh your options, and make the call. See how it plays out.",
    "start": "invoice",
    "scenes": {
        "invoice": {
            "backdrop": "email",
            "title": "9:00am, an invoice that is not quite right",
            "narrative": "An email arrives from a supplier you deal with every "
            "month. It says their bank account has changed, and this month's "
            "invoice, which really is due, must now go to a new account by end of "
            "day. The wording is polite and the logo looks right. The reply-to "
            "address is a little different from usual, and there is quiet pressure "
            "to pay today. What do you do?",
            "choices": [
                {"label": "Ring the supplier on the number you already have and confirm the change",
                 "outcome": "good", "to": "ransom",
                 "consequence": "You call the number from last month's statement, "
                 "not one from the email. The supplier knows nothing about any "
                 "change: their own account is the same as always. The email was a "
                 "scam, and by verifying through a channel you already trust, you "
                 "stopped a real payment from going to a stranger. A changed bank "
                 "account plus time pressure is the classic invoice scam."},
                {"label": "Pay the new account now so the invoice is not late",
                 "outcome": "bad", "to": "ransom",
                 "consequence": "The money lands in a criminal's account and is "
                 "almost impossible to recover. The invoice was real, but the "
                 "bank-account change was not. A genuine change of payment details "
                 "is always worth a quick phone call to a number you already have, "
                 "however routine the email looks."},
                {"label": "Reply to the email to ask whether the new account is genuine",
                 "outcome": "bad", "to": "ransom",
                 "consequence": "If the email is a scam, your question goes straight "
                 "to the scammer, who cheerfully confirms the new account is real. "
                 "Replying can never verify a suspicious message. Reach the sender a "
                 "different way, on a number or address you already trust."},
            ],
        },
        "ransom": {
            "backdrop": "ransom",
            "title": "2:30pm, a colleague calls you over",
            "narrative": "Every file on their screen has been renamed, and a red "
            "message demands payment in Bitcoin to unlock them. A countdown is "
            "ticking. Around the office, a couple of other people say their shared "
            "files have just stopped opening too. Everyone is looking at you. What "
            "is your first move?",
            "choices": [
                {"label": "Disconnect that computer from the network, then report it straight away",
                 "outcome": "good", "to": "end",
                 "consequence": "Exactly right. Pulling it off the network first "
                 "stops the ransomware spreading further across the shared drive and "
                 "other machines, and reporting it quickly brings the right help. "
                 "With a tested backup, the files can be restored, and nothing is "
                 "paid to the attacker. Contain, report, recover."},
                {"label": "Pay the ransom quickly, before the countdown runs out",
                 "outcome": "bad", "to": "end",
                 "consequence": "Paying is unreliable, funds more crime, and leaves "
                 "the door it came through wide open, so it can happen again. The "
                 "countdown exists precisely to rush you into paying. Contain it "
                 "first, then recover from a backup instead."},
                {"label": "Tell everyone to keep working so no unsaved work is lost",
                 "outcome": "bad", "to": "end",
                 "consequence": "Every extra second connected, more files and more "
                 "machines are locked. Staying on the network to save a little "
                 "unsaved work costs far more than it saves. The first move is "
                 "always to disconnect and contain the spread."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "That is the morning handled",
            "narrative": "Two very different situations, one steady instinct behind "
            "both: slow down, verify through a channel you trust, and when "
            "something goes wrong, contain it and report it before you do anything "
            "else. That calm habit is worth more than any single piece of "
            "technology.",
        },
    },
}

MODULE2_SIM = {
    "kind": "scenes",
    "intro": "Two moments from a week when a threat came knocking. Recognise it, "
    "then handle it. Make each call and see the consequence before moving on.",
    "start": "attach",
    "scenes": {
        "attach": {
            "backdrop": "attach",
            "title": "Monday, an attachment that wants opening",
            "narrative": "An unexpected email arrives, addressed to the accounts "
            "inbox, with an attachment named Invoice_4471.pdf.exe and a short note "
            "urging you to open it for the amount due. It looks like an invoice at a "
            "glance, and the sender name reads Accounts. Something about the file "
            "name is not right. What do you do?",
            "choices": [
                {"label": "Do not open it, and report it to whoever looks after IT",
                 "outcome": "good", "to": "lock",
                 "consequence": "Well spotted. The double extension, .pdf.exe, means "
                 "the real file type is the last one: .exe, a program that runs "
                 "code, dressed up to look like a harmless PDF. Opening it would run "
                 "malware. Not opening it, and reporting it, protects you and warns "
                 "everyone else who got the same email."},
                {"label": "Open it to see what the invoice says",
                 "outcome": "bad", "to": "lock",
                 "consequence": "Opening it runs the hidden program and infects the "
                 "machine in seconds. The tell was in the file name all along: "
                 ".pdf.exe is a program wearing a PDF disguise. When a file name "
                 "ends in .exe, or in a double extension, do not open it."},
                {"label": "Forward it to a colleague to check whether it is real",
                 "outcome": "bad", "to": "lock",
                 "consequence": "Forwarding a booby-trapped attachment just puts the "
                 "next person one careless click from infection. Do not pass a "
                 "suspicious file around. Report it to IT, who can check it safely "
                 "and warn the whole team."},
            ],
        },
        "lock": {
            "backdrop": "ransom",
            "title": "Wednesday, the files start locking",
            "narrative": "On another computer, files are renaming themselves one "
            "after another, and a message demands Bitcoin to unlock them. It is "
            "spreading to the shared drive that the whole office uses. Two days ago "
            "you dodged the attachment, but something else has got in. You have a "
            "few seconds to act well. What is your first move?",
            "choices": [
                {"label": "Disconnect the machine from the network straight away",
                 "outcome": "good", "to": "end",
                 "consequence": "Exactly. Isolating the machine first is the single "
                 "most useful thing you can do: it stops the ransomware reaching the "
                 "shared drive and other computers. From there you report it, and "
                 "restore from a tested backup rather than paying a cent."},
                {"label": "Pay the Bitcoin quickly to get everyone back to work",
                 "outcome": "bad", "to": "end",
                 "consequence": "Paying is unreliable and funds more crime, and the "
                 "way in stays open, so it can strike again. Speed matters here, but "
                 "the right fast action is to disconnect and contain, not to pay. "
                 "Recover from a backup instead."},
                {"label": "Keep working and hope it stops on its own",
                 "outcome": "bad", "to": "end",
                 "consequence": "It will not stop on its own. Every second the "
                 "machine stays connected, more files and more computers are locked. "
                 "The first move is always to pull it off the network and contain "
                 "the spread."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "That is the week handled",
            "narrative": "You read the threat before it opened, and when a second "
            "one got through, you contained it fast and recovered without paying. "
            "Recognising trouble early and reacting calmly, contain then report "
            "then restore, is what keeps a small business standing when something "
            "goes wrong.",
        },
    },
}

MODULE_SIMS = {1: MODULE1_SIM, 2: MODULE2_SIM}


def _placeholder_sim(module_title):
    return {
        "kind": "inbox",
        "intro": f"A short interactive scenario for {module_title}. The full "
        "version will present realistic situations to judge. This placeholder "
        "keeps the same shape so the exercise runs end to end.",
        "items": [
            {
                "id": "safe",
                "from": "A trusted colleague",
                "subject": "A normal, expected request",
                "preview": "This message is exactly what it appears to be.",
                "scam": False,
                "tells": ["Expected, from someone you know, no pressure."],
            },
            {
                "id": "scam",
                "from": "An unfamiliar sender",
                "subject": "An urgent request you weren't expecting",
                "preview": "Act now or something bad happens — the usual pressure.",
                "scam": True,
                "tells": ["Unexpected, urgent, and pushing you to act fast."],
            },
        ],
    }


def _seed_lesson_tasks(lesson, tasks):
    """Seed a lesson's interactive tasks idempotently (keyed on task_key).

    Each activity carries its own `payload` config verbatim (sort/inbox/spot/
    password/branch); legacy check/scenario tasks build theirs from options.
    Tasks no longer present in the content are pruned, so re-running mirrors the
    content exactly.
    """
    from modules.models import sanitise_lesson_html

    def _options(pairs):
        return [
            {"text": text, "correct": correct, "explanation": explanation}
            for (text, correct, explanation) in pairs
        ]

    seen = []
    for order, t in enumerate(tasks, start=1):
        if t["kind"] in ("check", "scenario"):
            payload = {
                "question": t.get("question", ""),
                "scenario": t.get("scenario", ""),
                "hint": t.get("hint", ""),
                "options": _options(t["options"]),
            }
        else:
            payload = dict(t.get("payload", {}))
        # Optional mid-panel check and a second reading block, rendered between
        # the main body and the panel's end interactive. body2 is sanitised
        # (it is HTML rendered with |safe); the payload itself is not.
        if t.get("inline_check"):
            ic = t["inline_check"]
            payload["inline_check"] = {
                "question": ic.get("question", ""),
                "hint": ic.get("hint", ""),
                "options": _options(ic["options"]),
            }
        if t.get("body2"):
            payload["body2"] = sanitise_lesson_html(t["body2"])
        # Optional "hero" figure: a diagram partial rendered at the very top of
        # the panel as a visual anchor, above the panel's own diagram/body.
        if t.get("hero"):
            payload["hero"] = t["hero"]
        LessonTask.objects.update_or_create(
            lesson=lesson,
            task_key=t["key"],
            defaults={
                "order": order,
                "kind": t["kind"].upper(),
                "points": t["points"] * _POINTS_SCALE,
                "title": t.get("title", ""),
                "body": t.get("body", ""),
                "diagram_key": t.get("diagram", ""),
                "payload": payload,
                "image": t.get("image", {}),
            },
        )
        seen.append(t["key"])
    lesson.tasks.exclude(task_key__in=seen).delete()


def _seed_module_quiz(module, content, lessons_by_number, force=False):
    """Seed a module's real quiz and its question bank, idempotently.

    Questions key on (quiz, ordering) and options on (question, option_text). When
    content is revised, stale rows are pruned: options no longer in a question and
    questions beyond the current bank are removed, so re-running mirrors the
    content exactly rather than leaving a question with two "correct" options.
    Every option carries an explanation, the Adaptive Feedback Engine's fuel.

    A question an admin has edited in the console (admin_edited=True) is left
    exactly as they left it — question row AND its answers — unless the seed is
    run with --force. This is how a reseed can't silently wipe an admin's edit.
    """
    quiz_data = content.QUIZ
    quiz, _ = Quiz.objects.update_or_create(
        module=module,
        defaults={
            "pass_mark": quiz_data["pass_mark"],
            "is_active": True,
            "time_limit_minutes": 30,
        },
    )
    for ordering, q in enumerate(quiz_data["questions"], start=1):
        question, created = Question.objects.get_or_create(
            quiz=quiz,
            ordering=ordering,
            defaults={
                "question_text": q["text"],
                "difficulty": q["difficulty"],
                "lesson_reference": lessons_by_number[q["lesson"]],
            },
        )
        # Admin-locked question: leave it and its answers untouched.
        if not created and question.admin_edited and not force:
            continue
        if not created:
            question.question_text = q["text"]
            question.difficulty = q["difficulty"]
            question.lesson_reference = lessons_by_number[q["lesson"]]
            if force:
                question.admin_edited = False
            question.save()
        current_texts = []
        for option_text, is_correct, explanation in q["options"]:
            Answer.objects.update_or_create(
                question=question,
                option_text=option_text,
                defaults={
                    "correct_answer": is_correct,
                    "explanation_text": explanation,
                },
            )
            current_texts.append(option_text)
        # Drop options left over from an earlier version of this question.
        question.answers.exclude(option_text__in=current_texts).delete()
    # Drop questions beyond the current bank size.
    quiz.questions.filter(ordering__gt=len(quiz_data["questions"])).delete()
    return quiz


class Command(BaseCommand):
    help = "Create/refresh the six training modules, their lessons and simulations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite content even where an admin has edited it in the "
            "console (admin_edited=True), and clear that flag. Use this to reset "
            "content back to the authored source in modules/content/. Without it, "
            "admin-edited modules, lessons and questions are left untouched.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options["force"]
        author = (
            User.objects.filter(is_superuser=True).order_by("pk").first()
            or User.objects.order_by("pk").first()
        )
        if author is None:
            raise CommandError(
                "No users exist to own the content. Create a superuser first: "
                "manage.py createsuperuser"
            )

        for index, (title, desc, difficulty, lesson_titles) in enumerate(MODULES, start=1):
            module, created = Module.objects.get_or_create(
                order_index=index,
                defaults={
                    "title": title,
                    "tagline": TAGLINES.get(index, ""),
                    "description": desc,
                    "difficulty": difficulty,
                    "is_published": True,
                    "created_by": author,
                    "duration_minutes": 40,
                },
            )
            # Refresh content on an existing module unless an admin has edited it
            # in the console. Publish state (is_published) is deliberately set
            # only on create, so an admin's publish/unpublish also survives a
            # reseed.
            if not created and (force or not module.admin_edited):
                module.title = title
                module.tagline = TAGLINES.get(index, "")
                module.description = desc
                module.difficulty = difficulty
                module.duration_minutes = 40
                if force:
                    module.admin_edited = False
                module.save()

            # Registered modules ship with real, finished lesson content; the
            # rest carry the rich placeholder until their turn.
            content = CONTENT.get(index)
            real_lessons = content.LESSONS if content else None
            lessons_by_number = {}
            for n, lesson_title in enumerate(lesson_titles, start=1):
                if real_lessons:
                    spec = real_lessons[n - 1]
                    # Task-based lesson: body_text is just a short intro; the
                    # teaching lives in the interactive tasks.
                    lesson_defaults = {
                        "title": spec["title"],
                        "body_text": f"<p>{spec['intro']}</p>",
                        "reading_time_minutes": spec["reading_time_minutes"],
                        "is_active": True,
                    }
                else:
                    lesson_defaults = {
                        "title": lesson_title,
                        "body_text": _placeholder_body(title, lesson_title),
                        "reading_time_minutes": 8,
                        "is_active": True,
                    }
                lesson, lesson_created = Lesson.objects.get_or_create(
                    module=module, lesson_number=n, defaults=lesson_defaults
                )
                # Refresh an existing lesson's content unless an admin edited it.
                # is_active is set only on create, so a lesson-level publish/
                # unpublish also survives a reseed.
                if not lesson_created and (force or not lesson.admin_edited):
                    lesson.title = lesson_defaults["title"]
                    lesson.body_text = lesson_defaults["body_text"]
                    lesson.reading_time_minutes = lesson_defaults["reading_time_minutes"]
                    if force:
                        lesson.admin_edited = False
                    lesson.save()
                # Interactive tasks are code-authored (not editable in the
                # console), so they always mirror the content file.
                if real_lessons:
                    _seed_lesson_tasks(lesson, spec["tasks"])
                lessons_by_number[n] = lesson

            sim_data = MODULE_SIMS.get(index) or _placeholder_sim(title)
            Simulation.objects.update_or_create(
                module=module,
                defaults={
                    "scenario_text": sim_data["intro"],
                    "decision_points": sim_data,
                    "outcome_text": {},
                },
            )

            n_lessons = len(lesson_titles)
            if content:
                quiz = _seed_module_quiz(module, content, lessons_by_number, force=force)
                # Now that every question points at an authored lesson (1..n), any
                # lesson rows beyond the authored count are unreferenced and safe to
                # prune, so a reseed mirrors a module that deliberately ships fewer
                # lessons (for example Module 2's two deep lessons).
                module.lessons.filter(lesson_number__gt=n_lessons).delete()
                self.stdout.write(
                    f"  module {index}: {title}  ({n_lessons} lessons, 1 simulation, "
                    f"quiz with {quiz.questions.count()} questions)"
                )
            else:
                self.stdout.write(
                    f"  module {index}: {title}  ({n_lessons} lessons, 1 simulation)"
                )

        total_lessons = sum(len(lesson_titles) for *_, lesson_titles in MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(MODULES)} modules, "
                f"{total_lessons} lessons, {len(MODULES)} simulations, "
                f"and {len(CONTENT)} interactive quizzes."
            )
        )
