#!/bin/bash

python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run your Django migrations
python manage.py migrate

# Run migrations and collect static files
python manage.py collectstatic --noinput
#python manage.py runserver