#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create and activate a virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Upgrade pip and install the project's dependencies
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt

# Apply database migrations
echo "Making migrations..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear
