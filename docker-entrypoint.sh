#!/bin/sh
python manage.py migrate
gunicorn agenda_me.wsgi:application -w 3 -b 0.0.0.0:8000