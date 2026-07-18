"""Shared fixtures for the modules tests: a small, real content tree."""

import pytest
from django.contrib.auth import get_user_model

from modules.models import Lesson, Module, Simulation

User = get_user_model()


@pytest.fixture
def author(db):
    return User.objects.create_user(
        email="author@example.com", password="x" * 14, role=User.Role.ADMINISTRATOR
    )


@pytest.fixture
def student(db):
    return User.objects.create_user(
        email="student@example.com", password="x" * 14, is_verified=True
    )


def _module(author, index, *, lessons=4, published=True):
    module = Module.objects.create(
        title=f"Module {index}",
        description="…",
        order_index=index,
        is_published=published,
        created_by=author,
    )
    for n in range(1, lessons + 1):
        Lesson.objects.create(
            module=module,
            lesson_number=n,
            title=f"Lesson {n}",
            body_text="<p>Placeholder.</p>",
            reading_time_minutes=5,
        )
    Simulation.objects.create(
        module=module,
        scenario_text="…",
        decision_points={"kind": "inbox", "items": [{"id": "a", "scam": True}]},
    )
    return module


@pytest.fixture
def modules(author):
    """Three published modules, four lessons each — enough to test the lock."""
    return [_module(author, i) for i in (1, 2, 3)]


@pytest.fixture
def make_module(author):
    def _factory(index, **kwargs):
        return _module(author, index, **kwargs)

    return _factory
