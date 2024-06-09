#!/bin/bash

# Start Celery worker in the background
celery -A server.src.worker.celery_app worker --loglevel=info -E --pool=solo &

# Run the main application
exec python -m server.src.main
