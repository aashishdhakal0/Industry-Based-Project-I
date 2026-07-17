"""
Django settings for the Network Security Training Platform (NSTP).

Runtime: Python 3.13 + Django 5.2 LTS + PostgreSQL 18.
See docs/project-overview.md for the spec and CLAUDE.md for deviations.

Secrets are read from a .env file via python-decouple. Never hard-code them
and never commit .env (see .gitignore).
"""

from pathlib import Path

from decouple import Csv, config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


# --- Security-critical config (from .env) ---------------------------------

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())


# --- Applications ----------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "django_otp",
    "django_otp.plugins.otp_totp",
    "tinymce",
    # Project apps
    "authentication",
    "modules",
    "quizzes",
    "certificates",
]

MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must sit directly after SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # OTPMiddleware MUST come after AuthenticationMiddleware.
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nstp.urls"


# --- Branding --------------------------------------------------------------
#
# The single source of truth for the platform's name. Templates read it as
# {{ site_name }} via nstp.context_processors.site; Python reads
# settings.SITE_NAME. Never hard-code the name anywhere else — changing it
# should mean editing this line and nothing else.

SITE_NAME = config("SITE_NAME", default="Cybaroo")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Puts SITE_NAME in every template as {{ site_name }}.
                "nstp.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "nstp.wsgi.application"


# --- Custom user model -----------------------------------------------------
#
# The spec REQUIRES a custom user model: email is the unique login identifier,
# plus `role` (Student/Instructor/Administrator) and `is_verified`. Stock
# auth.User cannot do email-as-username or carry those fields.
#
# Set before the first migrate, as required. Changing this after the initial
# migration is extremely painful to reverse — do not touch it.

AUTH_USER_MODEL = "authentication.User"

# Where login_required sends anonymous users. reverse_lazy because the URLconf
# isn't loaded yet when settings are read.
#
# LOGIN_REDIRECT_URL is only a fallback: the login view routes by role via
# authentication.utils.role_home_url, so an Administrator lands in the admin
# and everyone else on the dashboard. This value applies when something else in
# Django does the redirecting.
LOGIN_URL = reverse_lazy("authentication:login")
LOGIN_REDIRECT_URL = reverse_lazy("dashboard")


# --- Database --------------------------------------------------------------
#
# PostgreSQL 18 in production (spec). DB_ENGINE lets local dev fall back to
# SQLite until PostgreSQL is installed — production must always be postgresql.

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=str(BASE_DIR / "db.sqlite3")),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default=""),
        "PORT": config("DB_PORT", default=""),
    }
}


# --- Password validation ---------------------------------------------------
#
# NOTE: PASSWORD_HASHERS is deliberately NOT overridden. Django 5.2's default
# PBKDF2 hasher uses 1,000,000 iterations. The spec's "260,000 iterations"
# would be a 74% REDUCTION in work factor — it was Django 3.2's default, and
# the spec's claim that it "exceeds OWASP's current recommendations" is stale.
# Django's default is stronger and tracks OWASP guidance on every release.

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Two-factor authentication (django-otp) --------------------------------

OTP_TOTP_ISSUER = "AUSDAIS NSTP"


# --- Internationalisation --------------------------------------------------
#
# End users are Australian. en-au + Melbourne time so dates, times and spelling
# render correctly for them (and login-streak maths uses local dates).

LANGUAGE_CODE = "en-au"
TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_TZ = True


# --- Static & media --------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise's manifest storage hashes every static file and then *refuses* to
# resolve one that isn't in the manifest, so it only works after collectstatic.
# That is exactly what we want in production and exactly wrong everywhere else:
# under runserver, and in tests (which force DEBUG=False), it turns a missing
# manifest into a 500 on any page that calls {% static %}.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}


# --- Security headers ------------------------------------------------------
#
# Enforced only when DEBUG is off, so local dev over http still works.

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# django-csp 4.x config. TinyMCE needs inline styles in the CMS.
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "frame-ancestors": ["'none'"],
    }
}


# --- Email -----------------------------------------------------------------
#
# Registration sends a time-limited signed verification URL. Console backend in
# dev prints the email to the terminal instead of sending it.

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@ausdais.com.au")


# --- Rate limiting (django-ratelimit) --------------------------------------
#
# Requires a cache. LocMemCache is per-process, so limits are NOT shared across
# workers — acceptable for the single-worker PythonAnywhere free tier only.

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "nstp-ratelimit",
    }
}
RATELIMIT_ENABLE = config("RATELIMIT_ENABLE", default=True, cast=bool)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
