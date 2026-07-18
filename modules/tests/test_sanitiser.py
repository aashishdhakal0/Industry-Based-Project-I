"""Lesson HTML is sanitised on save — the stored-XSS control (a CLAUDE.md never).

Lessons render unescaped, so the database must never hold a script. These test
the model's save path, because that's the guarantee: clean in the column, safe
at every read.
"""

import pytest

from modules.models import Lesson, sanitise_lesson_html


@pytest.mark.parametrize(
    "dirty,banned",
    [
        ("<p>hi</p><script>alert(1)</script>", "<script"),
        ('<img src=x onerror="alert(1)">', "onerror"),
        ('<a href="javascript:alert(1)">x</a>', "javascript:"),
        ('<div onclick="steal()">x</div>', "onclick"),
        ("<iframe src='https://evil'></iframe>", "<iframe"),
    ],
)
def test_dangerous_markup_is_stripped(dirty, banned):
    assert banned not in sanitise_lesson_html(dirty)


def test_legitimate_rich_content_survives():
    html = (
        "<h2>Title</h2><p>Body with <strong>bold</strong> and "
        '<a href="https://cyber.gov.au">a link</a>.</p>'
        "<ul><li>one</li><li>two</li></ul>"
    )
    clean = sanitise_lesson_html(html)
    for kept in ["<h2>", "<strong>", "<ul>", "<li>", "cyber.gov.au"]:
        assert kept in clean


def test_links_gain_noopener():
    """Every surviving link gets rel=noopener noreferrer, so a lesson can't
    reach back into our tab via window.opener."""
    clean = sanitise_lesson_html('<a href="https://example.com">x</a>')
    assert "noopener" in clean


@pytest.mark.django_db
def test_lesson_save_sanitises_the_body(author):
    """The guarantee is at the model, not the view: whatever route writes a
    lesson, the column comes out clean."""
    from modules.models import Module

    module = Module.objects.create(
        title="M", order_index=1, is_published=True, created_by=author
    )
    lesson = Lesson.objects.create(
        module=module,
        lesson_number=1,
        title="L",
        body_text="<p>ok</p><script>alert(1)</script>",
    )
    lesson.refresh_from_db()
    assert "<script" not in lesson.body_text
    assert "<p>ok</p>" in lesson.body_text
