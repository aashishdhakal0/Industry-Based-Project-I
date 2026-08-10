"""Seed believable demo learners so the Administrator dashboard looks alive.

Fifteen fictional-but-realistic people, spread across a handful of small
Australian organisations, with a natural range of progress: a couple who have
finished the whole course (one Distinction, one Merit), several partway, a few
scraping a Pass, a couple who barely started, and some who have gone quiet long
enough to trip the "needs attention" heuristic.

Honesty by construction:
  - We create the real records (ProgressRecord + QuizResult), then let the
    gamification engine RECOMPUTE points, level and badges from them
    (refresh_profile). Points therefore always match progress — they are never
    typed in by hand.
  - Grades fall out of the quiz scores via modules.grading, so a learner's tier
    always matches the marks we gave them.

Idempotent: re-running wipes each demo learner's progress and rebuilds it, so a
demo you poked at resets cleanly. `--clear` removes the demo learners entirely.
The command owns a fixed set of email addresses, which is what keeps this data
clearly separate from real accounts.

    .venv/bin/python manage.py seed_demo_learners
    .venv/bin/python manage.py seed_demo_learners --clear
"""

from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from authentication.models import User, UserProfile
from modules import gamification as g
from modules.grading import grade_from_scores, tier_for_score
from modules.models import Module, ProgressRecord
from quizzes.models import QuizResult

DEMO_PASSWORD = "Demo-Learner-2026!"

# Each learner is described by the shape of their journey; everything derived
# (points, level, grade, badges) is computed from it, not stated here.
#
#   done          modules fully finished (all lessons + quiz passed), 1..done
#   scores        the passing quiz mark for each of those modules (len == done)
#   partial       lessons done in the NEXT module (0-3), i.e. in progress
#   current_fail  a not-yet-passing mark on that in-progress module's quiz, or None
#   retakes       positions (1-based) of a done module the learner failed once first
#   days_ago      when they were last active
#   streak        stored day streak (only shows on the dashboard if still live)
#   flag          reason string if an admin has flagged them, else None
LEARNERS = [
    # --- Finished the course -------------------------------------------------
    dict(first="Priya", last="Nadesan", email="priya.nadesan@gmail.com",
         org="Brunswick Family Dental", done=6, scores=[94, 89, 96, 91, 93, 90],
         partial=0, current_fail=None, retakes=[], days_ago=0, streak=8, flag=None),
    dict(first="Grace", last="Nguyen", email="grace.nguyen@yarraridgeps.vic.edu.au",
         org="Yarra Ridge Primary School", done=6, scores=[90, 93, 88, 95, 91, 92],
         partial=0, current_fail=None, retakes=[3], days_ago=1, streak=5, flag=None),
    dict(first="Daniel", last="Papadopoulos", email="d.papadopoulos@riversideshire.gov.au",
         org="Riverside Shire Council", done=6, scores=[82, 78, 85, 80, 88, 79],
         partial=0, current_fail=None, retakes=[2], days_ago=4, streak=0, flag=None),
    dict(first="Yasmin", last="Farah", email="yasmin.farah@gmail.com",
         org="Yarra Ridge Primary School", done=6, scores=[80, 84, 81, 87, 83, 82],
         partial=0, current_fail=None, retakes=[], days_ago=2, streak=3, flag=None),
    # --- Partway through -----------------------------------------------------
    dict(first="Aisha", last="Rahman", email="aisha.rahman@outlook.com",
         org="Yarra Ridge Primary School", done=5, scores=[88, 91, 84, 90, 86],
         partial=2, current_fail=64, retakes=[], days_ago=1, streak=9, flag=None),
    dict(first="Sofia", last="Russo", email="sofia.russo@milkwoodcafe.com.au",
         org="Milkwood Cafe", done=4, scores=[85, 79, 88, 83],
         partial=1, current_fail=None, retakes=[2], days_ago=3, streak=4, flag=None),
    dict(first="Liam", last="O'Brien", email="liam.obrien@bigpond.com",
         org="Coastline Plumbing & Gas", done=4, scores=[76, 71, 74, 79],
         partial=1, current_fail=None, retakes=[], days_ago=8, streak=0, flag=None),
    dict(first="Hiroshi", last="Tanaka", email="h.tanaka@outlook.com",
         org="Tanaka Web Design", done=4, scores=[73, 77, 70, 72],
         partial=0, current_fail=None, retakes=[], days_ago=6, streak=0, flag=None),
    dict(first="Jack", last="Thompson", email="jackt87@gmail.com",
         org="Coastline Plumbing & Gas", done=3, scores=[71, 70, 72],
         partial=0, current_fail=None, retakes=[], days_ago=11, streak=0, flag=None),
    dict(first="Fatima", last="El-Masri", email="f.elmasri@brunswickdental.com.au",
         org="Brunswick Family Dental", done=2, scores=[74, 73],
         partial=2, current_fail=66, retakes=[], days_ago=9, streak=0, flag=None),
    # --- Just started / barely engaged --------------------------------------
    dict(first="Ethan", last="Wilson", email="ethan.wilson@gmail.com",
         org="", done=0, scores=[], partial=2, current_fail=None, retakes=[],
         days_ago=3, streak=1, flag=None),
    # --- Needs attention: flagged and/or gone quiet 14+ days ----------------
    dict(first="Mohammed", last="Ali", email="mohammed.ali@bigpond.com",
         org="Riverside Shire Council", done=2, scores=[72, 75],
         partial=1, current_fail=None, retakes=[], days_ago=21, streak=0,
         flag="Fell behind after module 2"),
    dict(first="Isabella", last="Costa", email="bella.costa@gmail.com",
         org="Brunswick Family Dental", done=1, scores=[77],
         partial=0, current_fail=None, retakes=[], days_ago=18, streak=0, flag=None),
    dict(first="Chloe", last="Martin", email="chloe.m@iinet.net.au",
         org="Milkwood Cafe", done=1, scores=[81],
         partial=0, current_fail=None, retakes=[], days_ago=16, streak=0, flag=None),
    dict(first="Noah", last="Smith", email="noah.smith@coastlineplumbing.com.au",
         org="Coastline Plumbing & Gas", done=0, scores=[], partial=1,
         current_fail=None, retakes=[], days_ago=25, streak=0, flag=None),
]

DEMO_EMAILS = [p["email"] for p in LEARNERS]


class Command(BaseCommand):
    help = "Seed realistic demo learners for the Administrator dashboard."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove the demo learners instead of creating them.",
        )

    def handle(self, *args, clear=False, **options):
        if clear:
            deleted, _ = User.objects.filter(email__in=DEMO_EMAILS).delete()
            self.stdout.write(self.style.SUCCESS(f"Removed the demo learners ({deleted} rows)."))
            return

        modules = list(
            Module.objects.filter(is_published=True)
            .order_by("order_index")
            .prefetch_related("lessons")
        )
        if len(modules) < 6:
            raise CommandError(
                "The six modules aren't seeded yet. Run "
                "`manage.py seed_learning_content` first."
            )
        quiz_of = {}
        for m in modules:
            quiz = getattr(m, "quiz", None)
            if quiz is None:
                raise CommandError(f"Module {m.order_index} has no quiz — seed content first.")
            quiz_of[m.id] = quiz

        now = timezone.now()
        for persona in LEARNERS:
            self._seed_one(persona, modules, quiz_of, now)

        self._print_sample()

    @transaction.atomic
    def _seed_one(self, p, modules, quiz_of, now):
        user, _ = User.objects.get_or_create(
            email=p["email"],
            defaults={"first_name": p["first"], "last_name": p["last"]},
        )
        user.first_name = p["first"]
        user.last_name = p["last"]
        user.role = User.Role.STUDENT
        user.is_active = True
        user.is_verified = True
        user.set_password(DEMO_PASSWORD)
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Wipe this learner's progress so the rebuild is idempotent.
        ProgressRecord.objects.filter(user=user).delete()
        QuizResult.objects.filter(user=user).delete()

        last_active = now - timedelta(days=p["days_ago"])

        # Build the journey as an ordered list of (model_object, timestamp_field)
        # so we can backdate everything along one believable timeline.
        events = []

        def add_lesson(lesson):
            rec = ProgressRecord.objects.create(user=user, lesson=lesson)
            events.append((rec, "completed_at"))

        def add_quiz(quiz, score, passed, attempt):
            res = QuizResult.objects.create(
                user=user, quiz=quiz, score=score, passed=passed, attempt_number=attempt
            )
            events.append((res, "submitted_at"))

        for i in range(p["done"]):
            module = modules[i]
            for lesson in module.lessons.all().order_by("lesson_number"):
                if lesson.is_active:
                    add_lesson(lesson)
            quiz = quiz_of[module.id]
            score = p["scores"][i]
            if (i + 1) in p["retakes"]:
                add_quiz(quiz, max(52, score - 11), False, 1)  # a near miss first
                add_quiz(quiz, score, True, 2)
            else:
                add_quiz(quiz, score, True, 1)

        # In-progress module: some lessons, and maybe a not-yet-passing attempt.
        if p["partial"] and p["done"] < len(modules):
            module = modules[p["done"]]
            lessons = [l for l in module.lessons.all().order_by("lesson_number") if l.is_active]
            for lesson in lessons[: p["partial"]]:
                add_lesson(lesson)
            if p["current_fail"] is not None:
                add_quiz(quiz_of[module.id], p["current_fail"], False, 1)

        self._backdate(events, last_active)

        # Set activity/streak, THEN recompute points + badges from the records
        # (refresh_profile preserves the streak/last_active we set here).
        # Route the org through the resolver so a managed Organisation record
        # (and the FK) exists, keeping the console's org list coherent.
        from staff import services

        org = services.resolve_organisation(p["org"])
        profile.org = org
        profile.organisation = org.name if org else ""
        profile.flagged = bool(p["flag"])
        profile.flag_reason = p["flag"] or ""
        profile.last_active = last_active
        profile.streak_count = p["streak"]
        profile.save(
            update_fields=["org", "organisation", "flagged", "flag_reason",
                           "last_active", "streak_count"]
        )

        g.refresh_profile(user, bump_streak=False)

    @staticmethod
    def _backdate(events, end):
        """Spread events evenly along a believable window ending at `end`."""
        n = len(events)
        if n == 0:
            return
        span = timedelta(days=min(30, max(4, n)))
        start = end - span
        for k, (obj, field) in enumerate(events):
            frac = k / (n - 1) if n > 1 else 1.0
            when = start + (end - start) * frac
            type(obj).objects.filter(pk=obj.pk).update(**{field: when})

    def _print_sample(self):
        """Show the seeded learners exactly as the dashboard will compute them."""
        from staff import services

        rows = {r.user.email: r for r in services.collect_learners()}
        demo = [rows[e] for e in DEMO_EMAILS if e in rows]
        demo.sort(key=lambda r: (r.overall_score is None, -(r.overall_score or 0)))

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Seeded demo learners:"))
        self.stdout.write(
            "  " + "Name".ljust(20) + "Organisation".ljust(26)
            + "Mods".ljust(6) + "Grade".ljust(14) + "Pts".ljust(6)
            + "Lvl".ljust(5) + "Last active".ljust(13) + "Flags"
        )
        self.stdout.write("  " + "-" * 104)
        for r in demo:
            grade = r.tier.name + (f" {r.overall_score}%" if r.overall_score is not None else "")
            if r.last_active is None:
                last = "never"
            elif r.days_inactive == 0:
                last = "today"
            else:
                last = f"{r.days_inactive}d ago"
            flags = []
            if r.flagged:
                flags.append("flagged")
            if r.inactive:
                flags.append("inactive")
            self.stdout.write(
                "  " + r.name.ljust(20) + (r.user.profile.organisation or "—").ljust(26)
                + f"{r.modules_completed}/{r.modules_total}".ljust(6)
                + grade.ljust(14) + str(r.points).ljust(6)
                + str(r.level).ljust(5) + last.ljust(13) + ", ".join(flags)
            )

        stats = services.overview(list(rows.values()))
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Dashboard now: {stats['total_learners']} learners · "
            f"{stats['completed_course']} finished · {stats['completion_rate']}% completion · "
            f"avg {stats['average_score']}% · {len(stats['attention'])} need attention."
        ))
        self.stdout.write(f"(All demo learners share the password: {DEMO_PASSWORD})")
