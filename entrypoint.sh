#!/bin/sh

echo 'Installing requirements...'
pip install -r requirements.txt

echo 'Running migrations...'
python manage.py migrate

echo 'Compiling SCSS files...'
python manage.py compilescss

echo 'Collecting static filecs...'
python manage.py collectstatic --no-input

echo 'Compiling translations...'
python manage.py compilemessages

echo 'Starting Django Server...'
exec "$@"