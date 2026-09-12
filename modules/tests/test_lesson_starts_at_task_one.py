"""Opening a lesson always starts at Task 1.

Regression guard for two defects that made a lesson appear to open past Task 1:
  1. The celebration overlay (`.cy-reward`) set display:flex with no [hidden]
     guard, so it rendered over every lesson on load, covering Task 1.
  2. The room auto-opened the first *incomplete* task, so a learner who had done
     Task 1 landed on Task 2.

The task-selection now always lands on Task 1 (server marks Task 1 current for a
fresh learner; lesson.js opens Task 1 on load). These tests assert the server
side; the client "always Task 1" landing is verified separately in a browser.
"""

import pytest
from django.urls import reverse

from modules.models import LessonTask, TaskProgress


@pytest.fixture
def client_student(client, student):
    client.force_login(student)
    return client


@pytest.fixture
def tasked_lesson(modules):
    """Give module 1 / lesson 1 a small ordered set of real tasks."""
    lesson = modules[0].lessons.order_by("lesson_number").first()
    for i in range(1, 4):
        LessonTask.objects.create(
            lesson=lesson, order=i, task_key=f"t{i}", kind=LessonTask.Kind.CHECK,
            title=f"Task {i}", points=2,
            payload={"question": f"Q{i}", "options": [
                {"text": "a", "correct": True, "explanation": "yes"},
                {"text": "b", "correct": False, "explanation": "no"},
            ]},
        )
    return lesson


def _panel_done_flags(body, task_ids):
    """Map each task id -> whether its panel carries data-done='1'."""
    out = {}
    for tid in task_ids:
        marker = f'data-task-id="{tid}"'
        i = body.index(marker)
        # the <details ...> opening tag ends at the next '>'
        tag = body[body.rindex("<details", 0, i): body.index(">", i)]
        out[tid] = 'data-done="1"' in tag
    return out


@pytest.mark.django_db
def test_fresh_learner_task_one_is_current_and_not_done(client_student, tasked_lesson):
    tasks = list(tasked_lesson.tasks.order_by("order"))
    body = client_student.get(reverse("learn:lesson", args=[1, 1])).content.decode()

    # Task 1's rail item is the current one; no task is marked done.
    first_item = body.split('data-for="%d"' % tasks[0].id)[0]
    # The <li> for task 1 carries is-current (find its class just before data-for).
    li = body[body.rindex("<li", 0, body.index('data-for="%d"' % tasks[0].id)):
              body.index('data-for="%d"' % tasks[0].id)]
    assert "is-current" in li
    assert "is-done" not in li

    flags = _panel_done_flags(body, [t.id for t in tasks])
    assert flags[tasks[0].id] is False


@pytest.mark.django_db
def test_task_one_stays_first_even_after_it_is_completed(client_student, student, tasked_lesson):
    tasks = list(tasked_lesson.tasks.order_by("order"))
    TaskProgress.objects.create(user=student, task=tasks[0])  # finish Task 1

    body = client_student.get(reverse("learn:lesson", args=[1, 1])).content.decode()
    flags = _panel_done_flags(body, [t.id for t in tasks])
    # Task 1 reads as done (server truth), but it is still the first panel in the
    # DOM, so the room opens it at the top rather than skipping to Task 2.
    assert flags[tasks[0].id] is True
    assert body.index('data-task-id="%d"' % tasks[0].id) < body.index('data-task-id="%d"' % tasks[1].id)


@pytest.mark.django_db
def test_celebration_overlay_is_hidden_on_load(client_student, tasked_lesson):
    body = client_student.get(reverse("learn:lesson", args=[1, 1])).content.decode()
    # The reward overlay ships hidden; only JS reveals it on completion.
    overlay = body[body.index('id="cy-reward"'): body.index('id="cy-reward"') + 120]
    assert "hidden" in overlay


@pytest.mark.django_db
def test_no_reward_flash_on_a_plain_lesson_load(client_student, tasked_lesson):
    body = client_student.get(reverse("learn:lesson", args=[1, 1])).content.decode()
    # The one-shot "Lesson complete. +N points" banner only appears after a
    # completion pops it from the session, never on a plain GET.
    assert "cy-flash" not in body
