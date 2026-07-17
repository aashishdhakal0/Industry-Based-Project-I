"""Shared pytest fixtures."""

import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def disable_rate_limiting(settings):
    """Turn rate limiting off for every test, and clear the counter cache.

    Rate limits are per-IP and every test client shares one IP, so left on, the
    eleventh login test in a run would get a 429 instead of the thing it
    asserts — and which test broke would depend on collection order. That's the
    worst kind of flake: real, intermittent, and blamed on the wrong code.

    The cache clear matters just as much. django-ratelimit counts in the cache,
    LocMemCache persists for the whole process, so counts leak between tests
    even with the limit disabled.

    Tests that assert the limit *works* opt back in via the `rate_limiting`
    fixture below.
    """
    settings.RATELIMIT_ENABLE = False
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def rate_limiting(settings):
    """Opt back into rate limiting, for the tests that verify it fires."""
    settings.RATELIMIT_ENABLE = True
    cache.clear()
    yield
    cache.clear()
