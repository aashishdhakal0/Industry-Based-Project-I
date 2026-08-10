"""Show/hide password toggle.

The behaviour itself (typing "type" between password/text, swapping the icon
and aria-label) lives in plain JS in static/js/cybaroo.js — there's no headless
browser in this suite to exercise it. What's tested here is the contract the
JS depends on and the accessibility requirements that must hold on first
render, before any script has run:

  - a real <button type="button">, never a checkbox, so it can't submit
  - aria-controls pointing at the actual input id, so the JS finds the right
    field
  - aria-pressed="false" and an aria-label of "Show password" as the resting
    state
  - the input itself still type="password" on a fresh page load, so a user
    with JS disabled or broken never gets a field that's silently in a
    different state than the button claims
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def toggle_buttons(html):
    """Every `data-password-toggle` button tag, as raw HTML."""
    return re.findall(r"<button[^>]*data-password-toggle[^>]*>", html)


def assert_well_formed_toggle(button_html, html):
    assert 'type="button"' in button_html, "toggle must not be able to submit the form"
    assert 'aria-pressed="false"' in button_html
    assert 'aria-label="Show password"' in button_html

    match = re.search(r'aria-controls="([^"]+)"', button_html)
    assert match, "toggle has no aria-controls"
    input_id = match.group(1)

    input_match = re.search(
        rf'<input[^>]*id="{re.escape(input_id)}"[^>]*>', html
    )
    assert input_match, f"no input with id={input_id!r} for the toggle to control"
    assert 'type="password"' in input_match.group(0), (
        "the field the toggle controls must default to hidden"
    )


@pytest.mark.django_db
def test_login_password_field_has_a_toggle(client):
    # /login/ with no ?as= is the role chooser, not the form itself.
    html = client.get(reverse("authentication:login") + "?as=student").content.decode()
    buttons = toggle_buttons(html)
    assert len(buttons) == 1
    assert_well_formed_toggle(buttons[0], html)


@pytest.mark.django_db
def test_registration_password_fields_have_toggles(client):
    html = client.get(reverse("authentication:register")).content.decode()
    buttons = toggle_buttons(html)
    # password1 (new password) and password2 (confirm) — exactly the two
    # password fields UserCreationForm ships, and no others.
    assert len(buttons) == 2
    for button in buttons:
        assert_well_formed_toggle(button, html)


@pytest.mark.django_db
def test_reset_confirm_password_fields_have_toggles(client, django_user_model):
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    user = django_user_model.objects.create_user(
        email="toggle@example.com", password="x" * 14, is_verified=True
    )
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse(
        "authentication:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    response = client.get(url, follow=True)
    html = response.content.decode()

    buttons = toggle_buttons(html)
    assert len(buttons) == 2  # new_password1, new_password2
    for button in buttons:
        assert_well_formed_toggle(button, html)


@pytest.mark.django_db
def test_toggle_button_is_not_a_checkbox_anywhere(client):
    """A checkbox that toggles visibility can also submit a form on Enter in
    some browsers, and screen readers announce it as a checked/unchecked
    state rather than a shown/hidden one. Neither is what's wanted here."""
    login_html = client.get(reverse("authentication:login") + "?as=student").content.decode()
    register_html = client.get(reverse("authentication:register")).content.decode()
    for html in (login_html, register_html):
        for button in toggle_buttons(html):
            assert 'type="checkbox"' not in button
