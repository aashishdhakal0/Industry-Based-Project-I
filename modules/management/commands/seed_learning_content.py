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
from modules.content import module_one
from modules.models import Lesson, LessonTask, Module, Simulation
from quizzes.models import Answer, Question, Quiz

# (title, description, difficulty, four lesson titles)
MODULES = [
    (
        "Network Security Fundamentals",
        "How networks work, and where yours is most exposed.",
        Module.Difficulty.BEGINNER,
        [
            "What a network actually is",
            "Where the weak points are",
            "Wi-Fi, routers and the front door",
            "A simple security checklist",
        ],
    ),
    (
        "Recognising Cyber Threats",
        "The tactics used against Australian organisations today.",
        Module.Difficulty.BEGINNER,
        [
            "The shape of a modern attack",
            "Scams that target small teams",
            "Warning signs anyone can spot",
            "What to do when something feels off",
        ],
    ),
    (
        "Phishing & Social Engineering",
        "Identify fraudulent emails and calls before they succeed.",
        Module.Difficulty.INTERMEDIATE,
        [
            "Why phishing still works",
            "Reading an email like an investigator",
            "Phone calls and text messages",
            "Reporting it the right way",
        ],
    ),
    (
        "Secure Communication Practices",
        "Handling passwords, messages and files securely, as routine.",
        Module.Difficulty.INTERMEDIATE,
        [
            "Passwords without the pain",
            "Two-factor, explained simply",
            "Sharing files safely",
            "Keeping conversations private",
        ],
    ),
    (
        "Firewall & Network Defence",
        "The defences protecting your business, and how to maintain them.",
        Module.Difficulty.ADVANCED,
        [
            "What a firewall really does",
            "Updates are a security control",
            "Segmenting a small network",
            "Knowing when to ask for help",
        ],
    ),
    (
        "Incident Response",
        "A clear plan for the first hour after something goes wrong.",
        Module.Difficulty.ADVANCED,
        [
            "The first five minutes",
            "Who to call, and in what order",
            "Containing the damage",
            "Learning from an incident",
        ],
    ),
]


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


# Module 1's simulation is a real, playable phishing-inbox exercise. The others
# get a lighter placeholder scenario in the same shape, so the simulation
# engine has something to run everywhere.
PHISHING_SIM = {
    "kind": "inbox",
    "intro": "Three messages just landed in the shared inbox. For each one, "
    "decide whether it's safe or a scam — then see how you did.",
    "items": [
        {
            "id": "parcel",
            "from": "AusPost <no-reply@auspost-delivery.info>",
            "subject": "Your parcel is held — $2.99 release fee required",
            "preview": "We attempted delivery but a small customs fee is "
            "outstanding. Pay within 24 hours or your parcel is returned.",
            "scam": True,
            "tells": [
                "The address is auspost-delivery.info, not auspost.com.au.",
                "A small fee plus a tight deadline is a classic pressure tactic.",
                "Australia Post doesn't ask for delivery fees by email link.",
            ],
        },
        {
            "id": "invoice",
            "from": "Priya Sharma <priya@yourcouncil.gov.au>",
            "subject": "Re: March invoice — approved",
            "preview": "Hi, I've approved the March invoice for payment. Let me "
            "know if you need anything else before end of month. Thanks, Priya.",
            "scam": False,
            "tells": [
                "It's from a colleague on your own domain.",
                "It continues a conversation you were expecting.",
                "There's no link, no urgency and no request for credentials.",
            ],
        },
        {
            "id": "mfa",
            "from": "IT Security <security@micr0soft-support.com>",
            "subject": "Unusual sign-in — verify your account now",
            "preview": "We blocked a sign-in from a new device. Confirm it was "
            "you by entering your password at the link below within 15 minutes.",
            "scam": True,
            "tells": [
                "micr0soft-support.com uses a zero for the 'o' — a lookalike domain.",
                "Genuine services never ask you to confirm a password via a link.",
                "The 15-minute countdown exists to stop you thinking.",
            ],
        },
    ],
}


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

    Check/scenario options are stored in the task's JSON payload. Tasks no longer
    present in the content are pruned, so re-running mirrors the content exactly.
    """
    seen = []
    for order, t in enumerate(tasks, start=1):
        payload = {}
        if t["kind"] in ("check", "scenario"):
            payload = {
                "question": t.get("question", ""),
                "scenario": t.get("scenario", ""),
                "options": [
                    {"text": text, "correct": correct, "explanation": explanation}
                    for (text, correct, explanation) in t["options"]
                ],
            }
        LessonTask.objects.update_or_create(
            lesson=lesson,
            task_key=t["key"],
            defaults={
                "order": order,
                "kind": t["kind"].upper(),
                "points": t["points"],
                "title": t.get("title", ""),
                "body": t.get("body", ""),
                "diagram_key": t.get("diagram", ""),
                "payload": payload,
            },
        )
        seen.append(t["key"])
    lesson.tasks.exclude(task_key__in=seen).delete()


def _seed_module_one_quiz(module, lessons_by_number):
    """Seed Module 1's real quiz and its 15-question bank, idempotently.

    Questions key on (quiz, ordering) and options on (question, option_text), so
    re-running updates the wording in place rather than duplicating. Every option
    carries an explanation — the Adaptive Feedback Engine's fuel.
    """
    quiz_data = module_one.QUIZ
    quiz, _ = Quiz.objects.update_or_create(
        module=module,
        defaults={
            "pass_mark": quiz_data["pass_mark"],
            "is_active": True,
            "time_limit_minutes": 30,
        },
    )
    for ordering, q in enumerate(quiz_data["questions"], start=1):
        question, _ = Question.objects.update_or_create(
            quiz=quiz,
            ordering=ordering,
            defaults={
                "question_text": q["text"],
                "difficulty": q["difficulty"],
                "lesson_reference": lessons_by_number[q["lesson"]],
            },
        )
        for option_text, is_correct, explanation in q["options"]:
            Answer.objects.update_or_create(
                question=question,
                option_text=option_text,
                defaults={
                    "correct_answer": is_correct,
                    "explanation_text": explanation,
                },
            )
    return quiz


class Command(BaseCommand):
    help = "Create/refresh the six training modules, their lessons and simulations."

    @transaction.atomic
    def handle(self, *args, **options):
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
            module, _ = Module.objects.update_or_create(
                order_index=index,
                defaults={
                    "title": title,
                    "description": desc,
                    "difficulty": difficulty,
                    "is_published": True,
                    "created_by": author,
                    "duration_minutes": 40,
                },
            )

            # Module 1 ships with real, finished lesson content; the rest carry
            # the rich placeholder until their turn.
            real_lessons = module_one.LESSONS if index == 1 else None
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
                lesson, _ = Lesson.objects.update_or_create(
                    module=module, lesson_number=n, defaults=lesson_defaults
                )
                if real_lessons:
                    _seed_lesson_tasks(lesson, spec["tasks"])
                lessons_by_number[n] = lesson

            sim_data = PHISHING_SIM if index == 1 else _placeholder_sim(title)
            Simulation.objects.update_or_create(
                module=module,
                defaults={
                    "scenario_text": sim_data["intro"],
                    "decision_points": sim_data,
                    "outcome_text": {},
                },
            )

            if index == 1:
                quiz = _seed_module_one_quiz(module, lessons_by_number)
                self.stdout.write(
                    f"  module {index}: {title}  (4 lessons, 1 simulation, "
                    f"quiz with {quiz.questions.count()} questions)"
                )
            else:
                self.stdout.write(f"  module {index}: {title}  (4 lessons, 1 simulation)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(MODULES)} modules, "
                f"{len(MODULES) * 4} lessons, {len(MODULES)} simulations, "
                "Module 1 quiz."
            )
        )
