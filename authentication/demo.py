"""The pre-made demo accounts, defined in exactly one place.

The seed command creates them and the tests assert against them, both reading
from here so the credentials can never drift.

These accounts exist so a supervisor can review both experiences: they sign in
through the normal, secure login form (email + password + 2FA) using the
credentials below — there is no login bypass anywhere in the codebase. The
credentials are review credentials for a training demo, not secrets.
"""

from .models import User

DEMO_ACCOUNTS = {
    "admin": {
        "email": "demo.admin@cybaroo.example",
        "password": "Demo-Admin-2026!",
        "first_name": "Demo",
        "last_name": "Administrator",
        "role": User.Role.ADMINISTRATOR,
        # A demo Administrator has to actually land in and use the admin, which
        # needs both flags. is_superuser so every model is visible without
        # hand-granting permissions.
        "is_staff": True,
        "is_superuser": True,
    },
    "student": {
        "email": "demo.student@cybaroo.example",
        "password": "Demo-Student-2026!",
        "first_name": "Demo",
        "last_name": "Student",
        "role": User.Role.STUDENT,
        "is_staff": False,
        "is_superuser": False,
    },
}
