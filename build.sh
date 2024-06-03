#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip and install the project's dependencies
 pip install --upgrade pip
 pip install -r requirements.txt

# Apply database migrations
echo "Making migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
