# Technology Stack

> **Verification note.** Every version in this document was read from the live
> development environment on **23 July 2026** — the `.venv` interpreter, the
> installed packages (`pip freeze`), Django's own `get_version()`, and a
> `SHOW server_version` query against the running `nstp_db` database. None of
> these figures are quoted from the specification or from memory; where the
> build differs from the original spec, the difference and its reason are
> recorded in the "Deviations" section below.

## Core platform

| Component  | Version         | Verified from                                  |
| ---------- | --------------- | ---------------------------------------------- |
| Python     | **3.13.14**     | `.venv` interpreter (`python --version`)       |
| Django     | **5.2.16** (LTS)| `import django; django.get_version()`          |
| PostgreSQL | **18.4**        | live `SHOW server_version` on `nstp_db`        |

## Application dependencies

All packages are pinned in `requirements.txt` and were confirmed installed at
the exact same version in the active environment.

| Package          | Version | Role                                                   |
| ---------------- | ------- | ------------------------------------------------------ |
| Django           | 5.2.16  | Web framework (core, MVT architecture)                 |
| psycopg[binary]  | 3.2.9   | PostgreSQL database driver (version 3)                 |
| django-ratelimit | 4.1.0   | Login / per-IP rate limiting                           |
| django-csp       | 4.0     | Content-Security-Policy response headers               |
| django-tinymce   | 5.0.0   | Rich-text lesson authoring in the instructor CMS       |
| Pillow           | 11.3.0  | Image handling (profile avatars)                       |
| nh3              | 0.3.6   | Server-side HTML sanitiser (stored-XSS control)        |
| reportlab        | 5.0.0   | PDF certificate generation                             |
| python-decouple  | 3.8     | Configuration / secrets loaded from `.env`             |
| whitenoise       | 6.12.0  | Static-file serving in production                      |
| pytest           | 8.4.1   | Test runner                                            |
| pytest-django    | 4.11.1  | Django integration for pytest                          |
| coverage         | 7.10.1  | Test-coverage measurement                              |

**Authentication / MFA — no third-party package.** The second authentication
factor is a 6-digit code emailed to the user on each sign-in, built entirely on
Django's own signing and cryptographic primitives (`secrets` for code
generation). The earlier authenticator-app flow's dependencies — `django-otp`
and `qrcode` — were removed and are deliberately absent from `requirements.txt`.

## Deviations from the original specification

The specification (`docs/project-overview.md`) named several versions and
libraries that the build intentionally does not use. Each change was made for a
stated technical reason, not by accident.

1. **Django 5.2.16 LTS instead of 6.0.6.** Django 6.0 is not a Long-Term-Support
   release — its mainstream support ends August 2026. Django 5.2 LTS is
   supported until April 2028, beyond the lifetime of this project.
   Additionally, `django-tinymce` 5.0.0 declares support only through Django
   5.2, and `django-ratelimit` 4.1.0 is unverified against Django 6.0.

2. **Python 3.13.14 instead of 3.12.4.** Python 3.13 is the version installed in
   the development environment and is supported by both Django 5.2 and the
   PythonAnywhere hosting platform. Both ends of the toolchain were standardised
   on it.

3. **psycopg 3 (3.2.9) instead of psycopg2-binary.** Django's documentation
   flags psycopg2 support as likely to be deprecated and eventually removed;
   psycopg 3 is the recommended driver for new development.

4. **Two-factor authentication is an emailed 6-digit code, not an
   authenticator-app TOTP.** This is a deliberate usability/security trade-off
   for a non-technical audience. Removing the app-install requirement lets
   *every* account carry a second factor — restoring the universal coverage the
   specification wanted — at the cost that an emailed code is weaker than TOTP:
   it travels the network and rests in an inbox, whereas a TOTP secret never
   leaves the user's device. The code is single-use, expires in 10 minutes, is
   capped at 5 attempts, and is generated with `secrets`. **This should be
   presented as a trade-off made with eyes open, not as equivalent to app-based
   TOTP.** The `django-otp` and `qrcode` dependencies were removed as a result.

5. **nh3 added (not named in the specification).** Lesson body text is authored
   as HTML through TinyMCE and must be sanitised server-side before storage to
   prevent stored cross-site scripting. `nh3` — the maintained, Rust-based
   ammonia binding — performs this in `Lesson.save()`. The older common choice,
   `bleach`, is deprecated.

6. **PDF generation via `reportlab.platypus` / `reportlab.pdfgen.canvas.Canvas`,
   not "ReportLab's FPDF class".** ReportLab contains no `FPDF` class — FPDF is
   an unrelated PDF library. The specification's phrasing is therefore
   technically inaccurate; the correct ReportLab APIs are used instead.

7. **PostgreSQL 18 (18.4).** This matches the specification and is fully
   supported (Django 5.2 supports PostgreSQL 14+). Listed here for completeness;
   it is not a deviation.

### Related configuration-level deviations

These are not package pins but belong in any discussion of the stack:

- **Password hashing uses Django's default PBKDF2 (1,000,000 iterations)**, not
  the specification's 260,000. The spec's figure is a Django 3.2-era default and
  is roughly 74% weaker; Django's current default is stronger and is used as-is.

- **Gunicorn is not used.** PythonAnywhere runs its own WSGI server, which makes
  a separate Gunicorn process redundant.

## Open hosting item

PythonAnywhere's free tier does not provide PostgreSQL (MySQL is a paid tier;
PostgreSQL is a paid add-on). Production hosting for the PostgreSQL database is
therefore an unresolved decision for the client: pay for the add-on, migrate the
production database to MySQL, or host elsewhere (for example Render, Fly.io, or
Railway, which offer free PostgreSQL). Local development is PostgreSQL-only and
is unaffected.
