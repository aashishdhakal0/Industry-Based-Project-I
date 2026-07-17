"""Forms for account creation and sign-in.

Copy here is aimed at a non-technical adult: say what to do, in plain words,
before they get it wrong rather than after.
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """Public sign-up.

    Note what is *absent*: `role`. A self-selected role would let anyone register
    as an Administrator, so registration always produces a Student (see
    `save()`); instructors and administrators are created through the admin.
    """

    first_name = forms.CharField(
        max_length=150,
        label="First name",
        widget=forms.TextInput(attrs={"autocomplete": "given-name", "autofocus": True}),
    )
    last_name = forms.CharField(
        max_length=150,
        label="Last name",
        widget=forms.TextInput(attrs={"autocomplete": "family-name"}),
    )
    email = forms.EmailField(
        label="Email address",
        help_text="Your login, and where the confirmation link lands.",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    organisation = forms.CharField(
        max_length=255,
        required=False,
        label="Organisation",
        help_text="Optional. The business, council or school you're here for.",
        widget=forms.TextInput(attrs={"autocomplete": "organization"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "organisation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Copy note: this is the platform's first impression, and our reader is
        # a non-technical adult who has been nagged about passwords for twenty
        # years and ignores it. "At least 8 characters, one uppercase, one
        # symbol" produces Password1! — advice that is followed and useless.
        # Three random words is genuinely stronger, actually memorable, and
        # short enough to read. Say the useful thing, once.
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = (
            "Eight characters or more. Three random words beat one clever one."
        )
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = "Once more, to be sure."

        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"

    def clean_email(self):
        """Lower-case the address, then check it is free.

        `unique=True` is case-sensitive and `BaseUserManager.normalize_email`
        only lower-cases the *domain*, so without this `A@x.com` and `a@x.com`
        would become two accounts that both believe they own the same inbox.

        Telling the user the address is taken is enumerable, and that is a
        deliberate, documented trade-off — see risk 13 in docs/build-plan.md.
        Do not silently change this to a generic message.
        """
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "That email is already registered. Try logging in instead."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = User.Role.STUDENT

        # Inactive until the emailed link is opened. `is_active` does the
        # enforcing — Django's ModelBackend refuses inactive users on its own,
        # so a forgotten check in a view cannot let an unverified user in.
        # `is_verified` records *why*, which is what the rest of the platform reads.
        user.is_active = False
        user.is_verified = False

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Email + password.

    AuthenticationForm calls its identity field `username` regardless of what
    USERNAME_FIELD is, so the field below is named `username` but holds an
    email. Renaming it would mean reimplementing the form; relabelling it is
    enough, and the user never sees the internal name.
    """

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "autofocus": True, "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )

    def clean_username(self):
        """Lower-case before authenticating.

        Registration stores addresses lower-cased, and ModelBackend looks the
        user up with an exact match. Without this, someone who signs up as
        `meredith@x.com` and later types `Meredith@x.com` — which their phone
        will capitalise for them — gets "no such account" and no way to work
        out why.
        """
        return self.cleaned_data["username"].strip().lower()

    def clean(self):
        """Authenticate, and say something useful when it fails.

        Reimplemented rather than calling super() because of an ordering
        problem: ModelBackend rejects inactive users itself, returning None, so
        `confirm_login_allowed` — the hook meant for exactly this message — is
        never reached. An unverified user would just get "wrong password" and
        try their password again forever.

        Telling them the account exists but is unverified is enumerable, and is
        the same deliberate trade-off as the registration form. See risk 13 in
        docs/build-plan.md.
        """
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                if User.objects.filter(email=email, is_active=False).exists():
                    raise forms.ValidationError(
                        "You haven't confirmed your email address yet. Check your "
                        "inbox for the link we sent when you signed up.",
                        code="unverified",
                    )
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class TOTPTokenForm(forms.Form):
    """The six digits from the authenticator app."""

    token = forms.CharField(
        label="6-digit code",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "one-time-code",
                "autofocus": True,
                "class": "form-control",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
    )

    def clean_token(self):
        token = self.cleaned_data["token"].strip().replace(" ", "")
        if not token.isdigit():
            raise forms.ValidationError("The code is 6 numbers, with no letters.")
        return token
