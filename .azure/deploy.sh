#!/bin/bash

echo "Starting deployment script..."

# Activate virtual environment
source /antenv/bin/activate
echo "Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script completed" 