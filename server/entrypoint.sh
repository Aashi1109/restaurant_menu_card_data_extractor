#!/bin/bash

#mkdir -p /app/temp

# Start Celery worker in the background
celery -A server.src.worker.celery_app worker --loglevel=info -E --pool=solo --logfile=/app/server/src/logs/celery.logs &

# Run the main application
exec python -m server.src.main