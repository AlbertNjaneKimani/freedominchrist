#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install system dependencies for psycopg2
apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    python3-dev

# Create and activate a virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Check Python version and pip version
python --version
pip --version

# Upgrade pip and install the project's dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
echo "Making migrations..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear
