#!/bin/sh

echo 'Running migrations...'
python manage.py migrate

echo 'Compiling SCSS files...'
python manage.py compilescss

echo 'Collecting static filecs...'
python manage.py collectstatic --no-input

echo 'Compiling translations...'
python manage.py compilemessages

echo 'Starting Django Server...'
mkdir -p /var/run/gunicorn
gunicorn &

wait