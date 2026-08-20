"""The full interactive Module 1 journey, end to end, on the real seeded content.

Learn (task by task) → the quiz unlocks → pass → Module 2 opens. This is the
integration test that proves the interactive lessons, the points banking, and
the quiz gate all fit together.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules import gamification as g
from modules.models import Module, ProgressRecord
from quizzes.models import Answer

User = get_user_model()


@pytest.fixture
def seeded_client(client, db):
    # An owner for the seeded content, then a fresh learner to drive.
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner@example.com", password="x" * 14, is_verified=True
    )
    client.force_login(student)
    return client, student


def work_through_lesson(client, module, lesson):
    """Complete every task in a lesson, one at a time, like the room does."""
    result = None
    for task in lesson.tasks.order_by("order"):
        resp = client.post(
            reverse("learn:complete_task", args=[module.order_index, lesson.lesson_number]),
            {"task": task.id},
        )
        assert resp.status_code == 200
        result = resp.json()
    return result


@pytest.mark.django_db
def test_the_full_interactive_module_one_journey(seeded_client):
    client, student = seeded_client
    m1 = Module.objects.get(order_index=1)

    # The first lesson renders as an interactive room, not a wall of text.
    first = m1.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[1, first.lesson_number])).content.decode()
    assert "data-room" in page and "lesson.js" in page

    # Work through both lessons, task by task; each banks on its last task.
    for lesson in m1.lessons.order_by("lesson_number"):
        final = work_through_lesson(client, m1, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 50

    # Two lessons banked = 100 points, two ProgressRecords.
    assert ProgressRecord.objects.filter(user=student, lesson__module=m1).count() == 2
    assert g.get_profile(student).points == 100

    # The overview now offers the quiz.
    overview = client.get(reverse("learn:module", args=[1])).content.decode()
    assert "Take the quiz" in overview

    # Take and pass the quiz (answer every drawn question correctly).
    client.get(reverse("learn:quiz", args=[1]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {
        f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids
    }
    client.post(reverse("learn:quiz_submit", args=[1]), answers)
    result = client.get(reverse("learn:quiz_result", args=[1])).content.decode()
    assert "passed" in result.lower()

    # Module 1 is complete and Module 2 has unlocked; points now include the quiz.
    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[1].complete is True
    assert progress[2].unlocked is True
    assert g.get_profile(student).points == 350  # 100 (2 lessons) + 250 quiz

    # Returning to the module now shows a clear completion moment with a way on
    # to Module 2 — the student is never left wondering what happens next.
    overview = client.get(reverse("learn:module", args=[1])).content.decode()
    assert "cy-moddone" in overview
    assert "Module 01 complete" in overview
    assert "Start Module 2" in overview
    assert reverse("learn:module", args=[2]) in overview
