"""seed_learning_content must work against a brand-new, empty database with no
users at all (the state of a fresh production deploy). It should not require a
pre-existing owner; Module.created_by is nullable for exactly this reason."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from modules.models import Module

User = get_user_model()


@pytest.mark.django_db
def test_seed_runs_on_empty_database_with_no_users():
    assert User.objects.count() == 0
    call_command("seed_learning_content")        # must not raise
    assert Module.objects.count() == 6
    # With no user to own it, created_by is None rather than an error.
    assert Module.objects.filter(created_by__isnull=True).count() == 6


@pytest.mark.django_db
def test_seed_assigns_an_owner_when_one_exists():
    admin = User.objects.create_superuser(
        email="owner@example.com", password="x" * 14,
        first_name="Ada", last_name="Ops",
    )
    call_command("seed_learning_content")
    # Every module is owned by the (super)user, mirroring the deploy order where
    # ensure_admin runs before the seed.
    assert Module.objects.exclude(created_by=admin).count() == 0
