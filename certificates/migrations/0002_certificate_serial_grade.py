"""Add the public serial and the academic grade to Certificate.

The table has no rows yet (issuing was not previously built), so adding the
unique `serial` with a one-off empty default is safe; every real row is created
through `Certificate.save()`, which fills the serial from the UUID.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("certificates", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="certificate",
            name="serial",
            field=models.CharField(
                default="",
                editable=False,
                help_text="Public, human-readable verification code (CYB-XXXX-XXXX-XXXX).",
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="certificate",
            name="grade",
            field=models.CharField(
                blank=True,
                help_text="Overall academic grade at issue (Distinction / Merit / Pass).",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="certificate",
            name="serial",
            field=models.CharField(
                editable=False,
                help_text="Public, human-readable verification code (CYB-XXXX-XXXX-XXXX).",
                max_length=20,
                unique=True,
            ),
        ),
    ]
