#!/usr/bin/env bash
# Render BUILD phase.
#
# The build runs in a build environment that does NOT sit on the private
# service network, so it cannot reliably resolve the internal database hostname
# (dpg-xxxxx-a). Anything that touches the database therefore belongs in the
# START phase, not here (see start.sh). This script only does work that needs no
# database: installing packages and collecting static files.
set -o errexit

# 1. Install pinned dependencies.
pip install -r requirements.txt

# 2. Gather static files into STATIC_ROOT for WhiteNoise to serve.
#    (DEBUG is False in production, so this uses the compressed manifest storage.)
python manage.py collectstatic --no-input
