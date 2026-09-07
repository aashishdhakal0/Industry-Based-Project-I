#!/usr/bin/env bash
# Render build script. Runs on every deploy, before the service starts.
# Exit immediately if any step fails, so a broken deploy never goes live.
set -o errexit

# 1. Install pinned dependencies.
pip install -r requirements.txt

# 2. Gather static files into STATIC_ROOT for WhiteNoise to serve.
#    (DEBUG is False in production, so this uses the compressed manifest storage.)
python manage.py collectstatic --no-input

# 3. Apply database migrations to the Render Postgres database.
python manage.py migrate --no-input

# 4. Seed the six learning modules, lessons and quizzes. This command is
#    idempotent (safe to run on every deploy) and only touches course content,
#    never user accounts or demo data.
python manage.py seed_learning_content
