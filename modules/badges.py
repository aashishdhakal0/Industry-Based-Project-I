"""The achievement badge catalogue.

Badges are defined in code, not the database: they are product rules, not
content, and a rule with an `evaluate` function does not belong in a table. What
IS data — which badges a given student has earned — lives in
`UserProfile.badges` (a jsonb list of ids on PostgreSQL).

Each badge's `evaluate(stats)` reads a plain dict of the student's current
figures (see gamification.student_stats) and returns True once earned. Awarding
is one-way: `gamification.refresh_profile` adds any newly-true badge to the
profile and never removes one, so a badge earned is a badge kept even if the
underlying number later changes.

Presentation lives here too — each badge carries a tier (for grouping the
gallery), a distinct icon, and its own two-stop gradient, so the collection
reads as a set of distinct collectibles rather than one shape repeated. None of
that touches awarding. Adding a badge makes it live everywhere with no migration.
"""

from dataclasses import dataclass
from typing import Callable

# Tier order for the gallery — a progression from first steps to mastery.
TIERS = ["Getting Started", "Knowledge", "Milestones", "Streaks"]


@dataclass(frozen=True)
class Badge:
    id: str
    name: str
    description: str  # doubles as the "how to earn it" line on a locked badge
    icon: str         # a distinct id in templates/_icons.html
    tier: str
    tile_a: str       # gradient start
    tile_b: str       # gradient end
    evaluate: Callable[[dict], bool]
    # Presentation only — never touches awarding. Given the stats dict, returns
    # (effort, phrase) for an unearned badge to power the "almost there" nudge,
    # or None if it isn't meaningfully close. `effort` is a rough lessons-worth
    # so the nearest reward can be picked across different badge types.
    hint: Callable[[dict], tuple] = None


CATALOGUE = [
    # --- Getting Started ---
    Badge(
        id="first_lesson", name="First step",
        description="Complete your first lesson.",
        icon="i-book", tier="Getting Started", tile_a="#00d9ff", tile_b="#00d9ff",
        evaluate=lambda s: s["lessons_completed"] >= 1,
        hint=lambda s: (1, "1 lesson from your first badge")
        if s["lessons_completed"] == 0 else None,
    ),
    Badge(
        id="first_module", name="Module one down",
        description="Finish every lesson in a module.",
        icon="i-layers", tier="Getting Started", tile_a="#00d9ff", tile_b="#00d9ff",
        evaluate=lambda s: s["modules_completed"] >= 1,
        hint=lambda s: (4, "Finish a module to earn a badge")
        if s["modules_completed"] == 0 else None,
    ),
    Badge(
        id="first_simulation", name="Hands on",
        description="Complete your first simulation.",
        icon="i-target", tier="Getting Started", tile_a="#00d9ff", tile_b="#00d9ff",
        evaluate=lambda s: s["simulations_completed"] >= 1,
    ),

    # --- Knowledge ---
    Badge(
        id="first_quiz", name="Quiz cracked",
        description="Pass your first quiz.",
        icon="i-check-circle", tier="Knowledge", tile_a="#00d9ff", tile_b="#5be7ff",
        evaluate=lambda s: s["passed_quizzes"] >= 1,
    ),
    Badge(
        id="sharp_eye", name="Sharp eye",
        description="Get a perfect score in a simulation.",
        icon="i-eye", tier="Knowledge", tile_a="#00d9ff", tile_b="#5be7ff",
        evaluate=lambda s: s["perfect_simulations"] >= 1,
    ),

    # --- Milestones ---
    Badge(
        id="halfway", name="Halfway there",
        description="Complete three modules.",
        icon="i-rocket", tier="Milestones", tile_a="#00d9ff", tile_b="#00d9ff",
        evaluate=lambda s: s["modules_completed"] >= 3,
        hint=lambda s: (
            (3 - s["modules_completed"]) * 4,
            f"{3 - s['modules_completed']} module{'s' if 3 - s['modules_completed'] != 1 else ''} from halfway",
        )
        if 0 < 3 - s["modules_completed"] <= 2 else None,
    ),
    Badge(
        id="points_100", name="Century",
        description="Earn 100 points.",
        icon="i-gem", tier="Milestones", tile_a="#00d9ff", tile_b="#5be7ff",
        evaluate=lambda s: s["points"] >= 100,
        hint=lambda s: (max(1, (100 - s["points"]) // 10), f"{100 - s['points']} points from a badge")
        if 0 < 100 - s["points"] <= 40 else None,
    ),
    Badge(
        id="graduate", name="Fully trained",
        description="Complete every module.",
        icon="i-award", tier="Milestones", tile_a="#e6c06a", tile_b="#00e5cc",
        evaluate=lambda s: s["published_modules"] > 0
        and s["modules_completed"] >= s["published_modules"],
    ),

    # --- Streaks ---
    Badge(
        id="streak_3", name="On a roll",
        description="Keep a 3-day streak.",
        icon="i-flame", tier="Streaks", tile_a="#00e5cc", tile_b="#e6b455",
        evaluate=lambda s: s["streak"] >= 3,
        hint=lambda s: (
            3 - s["streak"],
            f"{3 - s['streak']} day{'s' if 3 - s['streak'] != 1 else ''} from a 3-day streak",
        )
        if 0 < 3 - s["streak"] else None,
    ),
    Badge(
        id="streak_7", name="Week strong",
        description="Keep a 7-day streak.",
        icon="i-calendar", tier="Streaks", tile_a="#00e5cc", tile_b="#e6b455",
        evaluate=lambda s: s["streak"] >= 7,
        hint=lambda s: (7 - s["streak"], f"{7 - s['streak']} days from your 7-day streak")
        if 3 <= s["streak"] < 7 else None,
    ),
    Badge(
        id="streak_30", name="Unstoppable",
        description="Keep a 30-day streak.",
        icon="i-crown", tier="Streaks", tile_a="#e6b455", tile_b="#e6c06a",
        evaluate=lambda s: s["streak"] >= 30,
        hint=lambda s: (30 - s["streak"], f"{30 - s['streak']} days from your 30-day streak")
        if 7 <= s["streak"] < 30 else None,
    ),
]

BY_ID = {b.id: b for b in CATALOGUE}


def newly_earned(stats, already_earned):
    """Ids of badges the stats now satisfy that aren't already held."""
    held = set(already_earned or [])
    return [b.id for b in CATALOGUE if b.id not in held and b.evaluate(stats)]


def nearest_unearned(stats, already_earned):
    """The closest unearned badge with a hint, as (badge, phrase), or None.

    Presentation only — powers the dashboard's "almost there" nudge. Picks the
    smallest effort among unearned badges whose hint applies.
    """
    held = set(already_earned or [])
    candidates = []
    for b in CATALOGUE:
        if b.id in held or b.hint is None:
            continue
        result = b.hint(stats)
        if result:
            effort, phrase = result
            candidates.append((effort, b, phrase))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0])
    _, badge, phrase = candidates[0]
    return badge, phrase


def grouped(already_earned):
    """The catalogue grouped into tiers for the gallery, with per-tier and
    overall earned counts. Presentation only."""
    held = set(already_earned or [])
    tiers = []
    for tier_name in TIERS:
        items = [
            {"badge": b, "earned": b.id in held}
            for b in CATALOGUE
            if b.tier == tier_name
        ]
        tiers.append({
            "name": tier_name,
            "items": items,
            "earned": sum(1 for i in items if i["earned"]),
            "total": len(items),
        })
    return tiers
