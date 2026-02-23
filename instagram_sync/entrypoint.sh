#!/bin/bash

echo "Running migrations"
python manage.py migrate

echo "Starting Django Server at http://localhost:8000"
exec "$@"
