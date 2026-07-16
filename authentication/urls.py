"""Account URLs."""

from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/check-inbox/", views.check_inbox, name="check_inbox"),
    # The "you're all set" screen is rendered by `verify` itself rather than
    # given its own URL — it is the *result* of opening the link, not a page a
    # user could meaningfully navigate to.
    path("verify/<str:token>/", views.verify, name="verify"),
]
