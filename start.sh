#!/usr/bin/env bash
# Render START phase.
#
# The running service sits on the private network, in the database's region, so
# the internal DATABASE_URL hostname resolves here (it does not during the
# build). This is the right place to touch the database on Render's free tier,
# which has no pre-deploy hook.
set -o errexit

# 1. Migrations MUST succeed — without the schema the app cannot serve. If this
#    fails the service intentionally does not start (check the region match).
python manage.py migrate --no-input

# 2. Create the first administrator from ADMIN_* env vars, if none exists.
#    Idempotent and best-effort: a failure here (e.g. vars unset) must never
#    stop the site from coming up, so it is non-fatal.
python manage.py ensure_admin || echo "ensure_admin skipped (non-fatal)."

# 3. Seed the six learning modules, lessons and quizzes (content only, never
#    accounts). Idempotent and best-effort: if it fails the site still starts,
#    just without freshly seeded content. Delete this line and run it once from
#    a shell if you want faster cold starts.
python manage.py seed_learning_content || echo "Content seeding failed (non-fatal); starting anyway."

# 4. Hand off to Gunicorn. `exec` so it becomes PID 1 and receives Render's
#    signals (graceful shutdown) directly.
exec gunicorn nstp.wsgi:application
