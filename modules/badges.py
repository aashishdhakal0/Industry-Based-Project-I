"""The achievement badge catalogue.

Badges are defined in code, not the database: they are product rules, not
content, and a rule with an `evaluate` function does not belong in a table. What
IS data — which badges a given student has earned — lives in
`UserProfile.badges` (a jsonb list of ids on PostgreSQL).

Each badge's `evaluate(stats)` reads a plain dict of the student's current
figures (see gamification.collect_stats) and returns True once earned. Awarding
is one-way: `gamification.refresh_profile` adds any newly-true badge to the
profile and never removes one, so a badge earned is a badge kept even if the
underlying number later changes.

Adding a badge here makes it live everywhere — dashboard, celebration moments —
with no migration.
"""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Badge:
    id: str
    name: str
    description: str
    icon: str  # an id in templates/_icons.html
    evaluate: Callable[[dict], bool]


# Order matters only for display — earned-then-locked, roughly by reach.
CATALOGUE = [
    Badge(
        id="first_lesson",
        name="First step",
        description="Complete your first lesson.",
        icon="i-book",
        evaluate=lambda s: s["lessons_completed"] >= 1,
    ),
    Badge(
        id="first_module",
        name="Module one down",
        description="Finish every lesson in a module.",
        icon="i-layers",
        evaluate=lambda s: s["modules_completed"] >= 1,
    ),
    Badge(
        id="first_simulation",
        name="Hands on",
        description="Complete your first simulation.",
        icon="i-target",
        evaluate=lambda s: s["simulations_completed"] >= 1,
    ),
    Badge(
        id="sharp_eye",
        name="Sharp eye",
        description="Get a perfect score in a simulation.",
        icon="i-shield",
        evaluate=lambda s: s["perfect_simulations"] >= 1,
    ),
    Badge(
        id="streak_3",
        name="On a roll",
        description="Keep a 3-day streak.",
        icon="i-flame",
        evaluate=lambda s: s["streak"] >= 3,
    ),
    Badge(
        id="halfway",
        name="Halfway there",
        description="Complete three modules.",
        icon="i-bolt",
        evaluate=lambda s: s["modules_completed"] >= 3,
    ),
    Badge(
        id="graduate",
        name="Fully trained",
        description="Complete every module.",
        icon="i-award",
        evaluate=lambda s: s["published_modules"] > 0
        and s["modules_completed"] >= s["published_modules"],
    ),
]

BY_ID = {b.id: b for b in CATALOGUE}


def newly_earned(stats, already_earned):
    """Ids of badges the stats now satisfy that aren't already held."""
    held = set(already_earned or [])
    return [b.id for b in CATALOGUE if b.id not in held and b.evaluate(stats)]
