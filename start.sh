#!/bin/bash

# Migrate the database (if needed)
python manage.py migrate --noinput

# Start your Django server in the background
python manage.py runserver 0.0.0.0:8000