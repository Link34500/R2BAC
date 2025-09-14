#!/bin/sh
set -e

# Collect static + migrate
python src/manage.py collectstatic --noinput
python src/manage.py makemigrations
python src/manage.py migrate

# Démarrer Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 3 src.r2bac.wsgi:application
