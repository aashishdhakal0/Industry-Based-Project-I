"""Create the first administrator from environment variables, once.

This is the deploy-time replacement for `manage.py createsuperuser`, for hosts
(like Render's free tier) where an interactive shell is not available. It is
wired into start.sh before the content seed, so a brand-new deployment ends up
with an administrator who can sign in.

Safe by design, and safe to run on every redeploy:

  - It does nothing if ANY administrator already exists (idempotent).
  - It never modifies or overwrites an existing account.
  - It never logs the password (only the email is printed).
  - The account is created with role=ADMINISTRATOR and is_verified=True (and, as
    the bootstrap admin replacing createsuperuser, is_staff/is_superuser), so it
    can sign in at /admin/ without waiting for the emailed 2FA code.

Environment variables:
  ADMIN_EMAIL       (required) the administrator's email / login
  ADMIN_PASSWORD    (required) the administrator's password
  ADMIN_FIRST_NAME  (optional, default "Admin")
  ADMIN_LAST_NAME   (optional, default "User")
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the first administrator from ADMIN_* env vars, if none exists."

    def handle(self, *args, **options):
        User = get_user_model()

        # Idempotent: never touch anything if an administrator already exists.
        if User.objects.filter(role=User.Role.ADMINISTRATOR).exists():
            self.stdout.write("An administrator already exists; leaving accounts untouched.")
            return

        email = (os.environ.get("ADMIN_EMAIL") or "").strip().lower()
        password = os.environ.get("ADMIN_PASSWORD") or ""
        if not email or not password:
            self.stdout.write(
                "ADMIN_EMAIL / ADMIN_PASSWORD not set; skipping first-admin creation."
            )
            return

        # Never clobber an existing account that happens to share the email.
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                f"A user with {email} already exists; not modifying it."
            )
            return

        first = (os.environ.get("ADMIN_FIRST_NAME") or "Admin").strip()
        last = (os.environ.get("ADMIN_LAST_NAME") or "User").strip()

        # create_superuser sets is_staff, is_superuser, role=ADMINISTRATOR and
        # is_verified=True (see authentication.models.UserManager), exactly like
        # `createsuperuser` would. We add first/last name for a tidy record.
        user = User.objects.create_superuser(
            email=email, password=password, first_name=first, last_name=last,
        )

        # The app expects a one-to-one profile for every account.
        from authentication.models import UserProfile

        UserProfile.objects.get_or_create(user=user)

        # Deliberately no password in the output.
        self.stdout.write(self.style.SUCCESS(f"Created administrator {email}."))
