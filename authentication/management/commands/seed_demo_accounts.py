"""Create (or refresh) the demo Administrator and Student accounts.

Idempotent: run it as often as you like. It creates the two accounts if they
are missing and, if they already exist, resets their password, role, flags and
profile back to the known-good demo state, so a demo account someone poked at
during review is one command away from clean again.

    .venv/bin/python manage.py seed_demo_accounts

A supervisor reviews both experiences by signing in through the normal, secure
login form with these credentials: the login page's "Log in as Student /
Administrator" buttons open that form framed for the role, and the account's
own role decides where they land. There is no login bypass.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from authentication.demo import DEMO_ACCOUNTS
from authentication.models import User, UserProfile


class Command(BaseCommand):
    help = "Create or refresh the demo Administrator and Student accounts."

    @transaction.atomic
    def handle(self, *args, **options):
        for who, spec in DEMO_ACCOUNTS.items():
            user, created = User.objects.get_or_create(
                email=spec["email"],
                defaults={
                    "first_name": spec["first_name"],
                    "last_name": spec["last_name"],
                },
            )

            # Set (or reset) everything that defines the demo state, so an
            # existing account is brought back to known-good rather than left
            # in whatever state review nudged it into.
            user.first_name = spec["first_name"]
            user.last_name = spec["last_name"]
            user.role = spec["role"]
            user.is_staff = spec["is_staff"]
            user.is_superuser = spec["is_superuser"]
            user.is_active = True
            user.is_verified = True
            user.set_password(spec["password"])
            user.save()

            # Every user needs a profile or the dashboard queries break.
            UserProfile.objects.get_or_create(user=user)

            verb = "Created" if created else "Refreshed"
            self.stdout.write(
                f"  {verb} {who}: {spec['email']}  /  {spec['password']}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "\nDemo accounts ready. Give your supervisor the credentials above.\n"
                "They sign in at /login/ via the normal form (email + password + "
                "2FA code); the role buttons just frame that form."
            )
        )
