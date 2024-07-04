#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
# python /code/wait_for_postgres.py

# Run the database loading script
echo "Running database loading script..."
python /code/LoadingDB.py

# Start the application
echo "Starting application..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000
