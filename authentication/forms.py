"""Forms for account creation.

Copy here is aimed at a non-technical adult: say what to do, in plain words,
before they get it wrong rather than after.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

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
        help_text="You'll use this to log in. We'll send a link here to confirm it's you.",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    organisation = forms.CharField(
        max_length=255,
        required=False,
        label="Organisation (optional)",
        help_text="Your business, council or school — if you're here on their behalf.",
        widget=forms.TextInput(attrs={"autocomplete": "organization"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "organisation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = (
            "At least 8 characters. Avoid anything you'd guess about yourself — "
            "a few unrelated words together works well."
        )
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = "Type the same password again."

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
