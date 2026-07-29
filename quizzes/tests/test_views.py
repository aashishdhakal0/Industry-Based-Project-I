"""Taking a quiz through the views: the gate, the paper, save, submit, result.

The load-bearing assertions are the gate (a real redirect/403 from the view, not
a hidden link) and that submit grades and routes to a result that reflects the
real outcome.
"""

import pytest
from django.urls import reverse

from modules import gamification as g
from quizzes.models import Answer, Quiz

from .conftest import _build_bank


@pytest.fixture
def client_student(client, student):
    client.force_login(student)
    return client


def finish_lessons(user, module):
    for lesson in module.lessons.order_by("lesson_number"):
        g.complete_lesson(user, lesson)


def correct_answer_id(question):
    return Answer.objects.get(question=question, correct_answer=True).id


def take_and_get_attempt(client, module):
    """GET the quiz (draws + stores the paper) and return the attempt dict."""
    client.get(reverse("learn:quiz", args=[module.order_index]))
    return client.session["quiz_attempt"]


# --------------------------------------------------------------------------
# The gate
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_quiz_requires_login(client, quiz):
    resp = client.get(reverse("learn:quiz", args=[quiz.module.order_index]))
    assert resp.status_code == 302 and "/login/" in resp.url


@pytest.mark.django_db
def test_quiz_redirects_back_to_the_module_until_lessons_are_done(client_student, quiz):
    resp = client_student.get(reverse("learn:quiz", args=[quiz.module.order_index]))
    assert resp.status_code == 302
    assert resp.url == reverse("learn:module", args=[quiz.module.order_index])


@pytest.mark.django_db
def test_quiz_of_a_locked_module_is_a_403(client_student, quiz, make_module):
    locked = make_module(2)
    Quiz.objects.create(module=locked, pass_mark=70)
    resp = client_student.get(reverse("learn:quiz", args=[2]))
    assert resp.status_code == 403


@pytest.mark.django_db
def test_a_module_with_no_active_quiz_has_no_quiz_page(client_student, make_module, student):
    m = make_module(1)
    finish_lessons(student, m)
    resp = client_student.get(reverse("learn:quiz", args=[1]))
    assert resp.status_code == 404


# --------------------------------------------------------------------------
# The paper
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_quiz_renders_ten_questions_once_lessons_are_done(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    html = client_student.get(reverse("learn:quiz", args=[quiz.module.order_index])).content.decode()
    assert html.count("data-quiz-q") == 10
    assert "data-quiz" in html and "quiz.js" in html


@pytest.mark.django_db
def test_the_drawn_paper_is_stable_across_a_refresh(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    first = take_and_get_attempt(client_student, quiz.module)["question_ids"]
    second = take_and_get_attempt(client_student, quiz.module)["question_ids"]
    assert first == second


@pytest.mark.django_db
def test_saving_an_answer_persists_it_to_the_session(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    attempt = take_and_get_attempt(client_student, quiz.module)
    qid = attempt["question_ids"][0]
    aid = correct_answer_id_by_id(qid)
    resp = client_student.post(
        reverse("learn:quiz_save", args=[quiz.module.order_index]),
        {"question": qid, "answer": aid},
    )
    assert resp.status_code == 200 and resp.json()["saved"] is True
    assert client_student.session["quiz_attempt"]["responses"][str(qid)] == aid


def correct_answer_id_by_id(question_id):
    return Answer.objects.get(question_id=question_id, correct_answer=True).id


# --------------------------------------------------------------------------
# Submit + result
# --------------------------------------------------------------------------


def submit(client, module, question_ids, *, correct):
    """Submit the paper answering the first `correct` questions correctly."""
    data = {}
    for n, qid in enumerate(question_ids):
        if n < correct:
            data[f"q{qid}"] = correct_answer_id_by_id(qid)
        else:
            wrong = Answer.objects.filter(question_id=qid, correct_answer=False).first()
            data[f"q{qid}"] = wrong.id
    return client.post(reverse("learn:quiz_submit", args=[module.order_index]), data)


@pytest.mark.django_db
def test_a_passing_submit_records_the_result_and_shows_the_pass_page(
    client_student, quiz, student, make_module
):
    make_module(2)
    finish_lessons(student, quiz.module)
    ids = take_and_get_attempt(client_student, quiz.module)["question_ids"]

    resp = submit(client_student, quiz.module, ids, correct=10)
    assert resp.status_code == 302
    assert resp.url == reverse("learn:quiz_result", args=[quiz.module.order_index])

    html = client_student.get(resp.url).content.decode()
    assert "100" in html
    assert "passed" in html.lower()
    assert "+50 points" in html
    # the next module is offered
    assert reverse("learn:module", args=[2]) in html


@pytest.mark.django_db
def test_a_failing_submit_shows_the_retake_page(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    ids = take_and_get_attempt(client_student, quiz.module)["question_ids"]

    resp = submit(client_student, quiz.module, ids, correct=4)
    html = client_student.get(resp.url).content.decode()
    assert "40" in html
    assert reverse("learn:quiz", args=[quiz.module.order_index]) in html  # retake link


@pytest.mark.django_db
def test_submitting_with_no_attempt_in_progress_bounces_to_the_quiz(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    resp = client_student.post(reverse("learn:quiz_submit", args=[quiz.module.order_index]), {})
    assert resp.status_code == 302
    assert resp.url == reverse("learn:quiz", args=[quiz.module.order_index])


@pytest.mark.django_db
def test_result_without_any_attempt_redirects_to_the_quiz(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    resp = client_student.get(reverse("learn:quiz_result", args=[quiz.module.order_index]))
    assert resp.status_code == 302
    assert resp.url == reverse("learn:quiz", args=[quiz.module.order_index])


# --------------------------------------------------------------------------
# Shell + hygiene
# --------------------------------------------------------------------------

import re

LEAKS = ["{#", "#}", "{%", "%}", "{{", "}}"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


@pytest.mark.django_db
def test_quiz_and_result_pages_are_clean_and_in_the_app_shell(client_student, quiz, student):
    finish_lessons(student, quiz.module)
    ids = take_and_get_attempt(client_student, quiz.module)["question_ids"]
    submit(client_student, quiz.module, ids, correct=10)

    for url in [
        reverse("learn:quiz", args=[quiz.module.order_index]),
        reverse("learn:quiz_result", args=[quiz.module.order_index]),
    ]:
        html = client_student.get(url).content.decode()
        assert 'class="cy-side__nav"' in html
        for token in LEAKS:
            assert token not in html, f"{url} leaked {token!r}"
        assert not EMOJI.findall(html), f"{url} contains emoji"
