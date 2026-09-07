"""Forms for the Administrator dashboard."""

from django import forms
from django.contrib.auth.password_validation import validate_password

from authentication.models import Organisation, User
from modules.models import Lesson, Module
from quizzes.models import Question


def _style(fields):
    """Give every widget the console's field styling (see .form-control)."""
    for field in fields.values():
        css = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = (css + " form-control").strip()


class AddUserForm(forms.ModelForm):
    """An administrator creates an account and assigns its role.

    Unlike public registration, this form DOES carry a role field — an admin
    assigning a role is a legitimate act, not the privilege escalation that a
    self-selected role on public sign-up would be. The account is created
    active and admin-vouched verified, with an initial password the admin sets
    (run through Django's validators). Promoting to Administrator grants the
    in-app dashboard (role-gated); it does not grant Django is_staff/superuser.
    """

    first_name = forms.CharField(max_length=150, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")
    email = forms.EmailField(label="Email address")
    role = forms.ChoiceField(choices=User.Role.choices, label="Role")
    organisation = forms.CharField(max_length=255, required=False, label="Organisation")
    password = forms.CharField(
        label="Initial password",
        widget=forms.PasswordInput,
        help_text="Eight or more characters. Ask them to change it after first sign-in.",
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inherit the platform's field styling (see .form-control in cybaroo.css).
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def save(self, commit=True):
        from authentication.models import UserProfile

        user = User(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role=self.cleaned_data["role"],
            # Admin-created and admin-vouched: usable straight away.
            is_active=True,
            is_verified=True,
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            from . import services

            user.save()
            profile = UserProfile.objects.create(user=user)
            org = services.resolve_organisation(self.cleaned_data.get("organisation", ""))
            services.assign_learner_org(profile, org)
        return user


class OrganisationForm(forms.ModelForm):
    """Create or edit an organisation. `name` is unique — the model constraint
    gives a clean inline collision error rather than a database 500."""

    class Meta:
        model = Organisation
        fields = ("name", "sector", "contact_email", "training_due", "notes")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
            "training_due": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].help_text = "The organisation's name. Must be unique."
        self.fields["sector"].help_text = "Optional. e.g. Local council, School, Small business."
        self.fields["training_due"].help_text = "Optional. The date staff should complete training by. Drives overdue reporting."
        _style(self.fields)


class ModuleEditForm(forms.ModelForm):
    """Edit a module's own fields.

    `order_index` is editable, with the model's unique constraint doing the
    collision check for us: ModelForm validation rejects a value another module
    already uses (excluding this one), so a clash is a clean inline error rather
    than a database 500. It still drives the sequential unlock chain, so the help
    text is explicit about the 1-6 order.
    """

    class Meta:
        model = Module
        fields = ("title", "description", "difficulty", "duration_minutes", "order_index")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order_index"].label = "Order in the course"
        self.fields["order_index"].help_text = (
            "Its position in the 1-6 unlock order. Must be unique across modules."
        )
        _style(self.fields)


class LessonEditForm(forms.ModelForm):
    """Edit a lesson's editable fields.

    `body_text` is HTML: it is sanitised on the way in by Lesson.save() (nh3),
    so nothing here can inject script into a learner's browser. is_active is not
    here — it is a separate POST toggle, like module publish.
    """

    class Meta:
        model = Lesson
        fields = ("title", "reading_time_minutes", "body_text")
        widgets = {"body_text": forms.Textarea(attrs={"rows": 10, "spellcheck": "false"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style(self.fields)


class QuestionEditForm(forms.Form):
    """Edit one quiz question and its answer options.

    Built dynamically around the question's existing answers (the model holds
    exactly four). Two invariants are enforced here so a bad edit can never
    reach the quiz engine or the Adaptive Feedback Engine:

      - exactly one option is correct — `correct` is a single-choice radio, so
        one and only one can win;
      - every explanation is non-empty — it is the AFE's fuel, shown to a
        learner who picks that option, so an empty one is a real defect.

    Answer text and explanations are plain text (rendered escaped by the quiz
    templates), so no HTML sanitisation is needed here.
    """

    question_text = forms.CharField(
        label="Question", widget=forms.Textarea(attrs={"rows": 3})
    )

    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        self.answers = list(question.answers.order_by("id"))

        for i, answer in enumerate(self.answers):
            self.fields[f"option_text_{i}"] = forms.CharField(
                label=f"Option {chr(65 + i)}",
                max_length=500,
                initial=answer.option_text,
            )
            self.fields[f"explanation_{i}"] = forms.CharField(
                label="Explanation",
                widget=forms.Textarea(attrs={"rows": 2}),
                initial=answer.explanation_text,
            )

        correct_index = next(
            (str(i) for i, a in enumerate(self.answers) if a.correct_answer), None
        )
        self.fields["correct"] = forms.ChoiceField(
            label="Correct answer",
            choices=[(str(i), chr(65 + i)) for i in range(len(self.answers))],
            widget=forms.RadioSelect,
            initial=correct_index,
        )

        self.fields["question_text"].initial = question.question_text
        _style({k: v for k, v in self.fields.items() if k != "correct"})

    def answer_rows(self):
        """Bound fields grouped per answer, for a clean template."""
        rows = []
        for i in range(len(self.answers)):
            rows.append(
                {
                    "letter": chr(65 + i),
                    "index": str(i),
                    "option": self[f"option_text_{i}"],
                    "explanation": self[f"explanation_{i}"],
                }
            )
        return rows

    def save(self):
        self.question.question_text = self.cleaned_data["question_text"]
        self.question.admin_edited = True  # lock against a reseed overwrite
        self.question.save(update_fields=["question_text", "admin_edited"])

        chosen = self.cleaned_data["correct"]
        for i, answer in enumerate(self.answers):
            answer.option_text = self.cleaned_data[f"option_text_{i}"]
            answer.explanation_text = self.cleaned_data[f"explanation_{i}"]
            answer.correct_answer = str(i) == chosen
            answer.save(
                update_fields=["option_text", "explanation_text", "correct_answer"]
            )
        return self.question
