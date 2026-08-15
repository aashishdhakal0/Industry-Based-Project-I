"""Account models: who a user is, and their gamification profile."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager for a User keyed on email rather than username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMINISTRATOR)
        # A superuser is created from the console, so there is no email link to
        # click — treat it as verified.
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """A platform account.

    Email replaces username as the login identifier. `role` drives every
    permission check; `is_verified` gates access until the emailed link is used.
    """

    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"

    # AbstractUser ships a username field; email replaces it entirely.
    username = None

    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    is_verified = models.BooleanField(
        default=False,
        help_text="True only once the emailed verification link has been used.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    @property
    def is_administrator(self):
        return self.role == self.Role.ADMINISTRATOR

    # There is deliberately no `requires_2fa` here any more.
    #
    # It existed to exempt Students from setting up an authenticator app, which
    # was the right call while an app was the price of entry. The second factor
    # is now a code emailed to an address they have already confirmed — no app,
    # no setup, nothing to install — so the barrier that justified the
    # exemption is gone, and every account gets the code.
    #
    # That also puts us back in line with the spec on coverage: it asks for 2FA
    # on all accounts, and we now deviate only on the method. See the
    # deviations table in CLAUDE.md.


class Organisation(models.Model):
    """A workplace a cohort of learners belongs to (a council, school, business).

    The canonical record an administrator manages. `UserProfile.organisation`
    (free text) is kept as a synced mirror of `name` so the existing rollup,
    search, CSV export and templates keep working unchanged; the FK is the source
    of truth for management (create, assign, click-into-detail).
    """

    name = models.CharField(max_length=255, unique=True)
    sector = models.CharField(
        max_length=120, blank=True,
        help_text="e.g. Local council, School, Small business, Not-for-profit.",
    )
    contact_email = models.EmailField(blank=True)
    notes = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "organisations"
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended profile and gamification state for a User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    organisation = models.CharField(max_length=255, blank=True)
    org = models.ForeignKey(
        Organisation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        help_text="Canonical organisation link. The `organisation` text field "
        "mirrors this record's name.",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    last_active = models.DateTimeField(null=True, blank=True)
    streak_count = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(
        default=0, help_text="10 per lesson completed, 50 per quiz passed."
    )
    badges = models.JSONField(
        default=list, blank=True, help_text="List of earned badge identifiers."
    )
    flagged = models.BooleanField(
        default=False,
        help_text="Marked by an administrator as needing attention "
        "(e.g. the learner has fallen behind).",
    )
    flag_reason = models.CharField(max_length=255, blank=True)
    celebrated_tier = models.PositiveSmallIntegerField(
        default=0,
        help_text="Highest tier index the student has already been congratulated "
        "for. The dashboard fires a one-time celebration when they climb past it.",
    )
    console_theme = models.CharField(
        max_length=5,
        choices=[("dark", "Dark"), ("light", "Light")],
        default="dark",
        help_text="An administrator's remembered light/dark choice for the console.",
    )

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return f"Profile for {self.user.email}"
