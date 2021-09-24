#!/bin/bash

# Activate virtual environment
source myvenv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Make migrations and migrate to database
python manage.py makemigrations
python manage.py migrate