#!/usr/bin/env bash

# exit on error
set -o errexit

# Modify this line as needed for your packege manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static assets files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
