"""Signed, time-limited email-verification tokens.

The token carries the user id, signed with SECRET_KEY. Nothing is stored: there
is no token table to migrate, clean up, or leak. Tampering fails the signature;
age is checked on load.

Consequence worth knowing: a signed token stays replayable until it expires. We
do not try to make it single-use (that would need the state we just avoided) —
instead the verify view is idempotent, so a second click is harmless. See
`authentication.views.verify`.
"""

from django.core import signing

# Namespaces the signature. A token minted for verification cannot be replayed
# against some other signed-value feature that shares SECRET_KEY.
VERIFICATION_SALT = "authentication.email-verification"

# Long enough to survive a weekend and a slow inbox; short enough that a
# forwarded link goes stale.
VERIFICATION_MAX_AGE = 60 * 60 * 48  # 48 hours


def make_verification_token(user):
    """Return a signed token identifying `user`."""
    return signing.dumps({"uid": user.pk}, salt=VERIFICATION_SALT)


def read_verification_token(token, max_age=VERIFICATION_MAX_AGE):
    """Return the user id in `token`.

    Raises `signing.SignatureExpired` if it is too old, or `signing.BadSignature`
    if it was tampered with or is malformed. Callers must distinguish the two:
    expired earns a fresh link, bad means something is wrong.
    """
    data = signing.loads(token, salt=VERIFICATION_SALT, max_age=max_age)
    return data["uid"]
