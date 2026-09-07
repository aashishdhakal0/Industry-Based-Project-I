#!/usr/bin/env bash
# Render START phase.
#
# The running service DOES sit on the private network, in the database's region,
# so the internal DATABASE_URL hostname resolves here (it does not during the
# build). This is the right place to run migrations on Render's free tier, which
# has no pre-deploy hook. Both commands below are idempotent.
set -o errexit

# Apply any pending migrations.
python manage.py migrate --no-input

# Seed the six learning modules, lessons and quizzes (content only, never
# accounts). Idempotent. If you want faster cold starts, delete this line after
# the first successful deploy and run it once from the Render Shell instead.
python manage.py seed_learning_content

# Hand off to Gunicorn. `exec` so it becomes PID 1 and receives Render's signals
# (graceful shutdown) directly.
exec gunicorn nstp.wsgi:application
