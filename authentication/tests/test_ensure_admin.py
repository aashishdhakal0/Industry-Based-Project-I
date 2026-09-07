"""The `ensure_admin` bootstrap command: create the first administrator from
environment variables, safely and idempotently, for hosts with no shell."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()
PASSWORD = "correct-horse-battery-9"


def _run(monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    call_command("ensure_admin")


@pytest.mark.django_db
def test_creates_first_admin_from_env(monkeypatch):
    _run(monkeypatch, ADMIN_EMAIL="Owner@Example.com", ADMIN_PASSWORD=PASSWORD,
         ADMIN_FIRST_NAME="Ada", ADMIN_LAST_NAME="Ops")
    u = User.objects.get(email="owner@example.com")          # normalised lower
    assert u.role == User.Role.ADMINISTRATOR
    assert u.is_verified is True
    assert u.is_staff is True and u.is_superuser is True     # can reach /admin/
    assert u.check_password(PASSWORD)
    assert u.first_name == "Ada" and u.last_name == "Ops"
    assert hasattr(u, "profile")                              # profile created


@pytest.mark.django_db
def test_is_idempotent_when_an_admin_exists(monkeypatch):
    User.objects.create_user(
        email="existing.admin@example.com", password=PASSWORD, first_name="X",
        last_name="Y", role=User.Role.ADMINISTRATOR,
    )
    before = User.objects.count()
    _run(monkeypatch, ADMIN_EMAIL="new.admin@example.com", ADMIN_PASSWORD=PASSWORD)
    assert User.objects.count() == before                    # nothing created
    assert not User.objects.filter(email="new.admin@example.com").exists()


@pytest.mark.django_db
def test_does_nothing_without_env_vars(monkeypatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    call_command("ensure_admin")
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_never_overwrites_a_non_admin_with_the_same_email(monkeypatch):
    student = User.objects.create_user(
        email="taken@example.com", password="original-pass-word", first_name="S",
        last_name="T", role=User.Role.STUDENT,
    )
    _run(monkeypatch, ADMIN_EMAIL="taken@example.com", ADMIN_PASSWORD=PASSWORD)
    student.refresh_from_db()
    assert student.role == User.Role.STUDENT                  # untouched
    assert student.check_password("original-pass-word")      # password not changed


@pytest.mark.django_db
def test_output_never_contains_the_password(monkeypatch, capsys):
    _run(monkeypatch, ADMIN_EMAIL="owner@example.com", ADMIN_PASSWORD=PASSWORD)
    out = capsys.readouterr().out
    assert PASSWORD not in out
    assert "owner@example.com" in out                        # email is fine to log
