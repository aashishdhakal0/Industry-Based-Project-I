"""Backfill celebrated_tier to each profile's CURRENT tier.

Without this, existing students would get a retroactive "You reached Gold"
celebration the next time they open the dashboard, for a tier they earned long
ago. Setting the marker to where they already are means the celebration only
fires on the NEXT genuine tier-up. Thresholds mirror gamification.TIERS.
"""

from django.db import migrations

# (min_points for Bronze, Silver, Gold, Platinum, Diamond) — keep in step with
# modules.gamification.TIERS.
TIER_FLOORS = [0, 100, 220, 380, 540]


def _tier_index(points):
    index = 0
    for i, floor in enumerate(TIER_FLOORS):
        if points >= floor:
            index = i
    return index


def backfill(apps, schema_editor):
    UserProfile = apps.get_model("authentication", "UserProfile")
    for profile in UserProfile.objects.all().only("id", "points", "celebrated_tier"):
        idx = _tier_index(profile.points or 0)
        if profile.celebrated_tier != idx:
            profile.celebrated_tier = idx
            profile.save(update_fields=["celebrated_tier"])


def unbackfill(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0005_userprofile_celebrated_tier"),
    ]

    operations = [
        migrations.RunPython(backfill, unbackfill),
    ]
