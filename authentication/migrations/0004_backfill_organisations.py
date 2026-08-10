"""Backfill Organisation records from the existing free-text organisation field.

For every distinct non-empty `UserProfile.organisation` string, create a matching
Organisation and point the profile's FK at it. After this, the FK and the text
mirror agree for all existing data. Reverse is a no-op (the text field is kept,
so nothing is lost if the FK is dropped).
"""

from django.db import migrations


def backfill(apps, schema_editor):
    UserProfile = apps.get_model("authentication", "UserProfile")
    Organisation = apps.get_model("authentication", "Organisation")

    names = (
        UserProfile.objects.exclude(organisation="")
        .exclude(organisation__isnull=True)
        .values_list("organisation", flat=True)
        .distinct()
    )
    for name in names:
        clean = name.strip()
        if not clean:
            continue
        org, _ = Organisation.objects.get_or_create(name=clean)
        UserProfile.objects.filter(organisation=name).update(org=org)


def unbackfill(apps, schema_editor):
    # No-op: the text mirror is retained, so dropping the FK loses nothing.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_organisation_userprofile_org"),
    ]

    operations = [
        migrations.RunPython(backfill, unbackfill),
    ]
