#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser using environment variables (will fail if user exists, but deploy continues)
python manage.py createsuperuser --noinput || true