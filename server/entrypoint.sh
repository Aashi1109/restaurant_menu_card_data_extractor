#!/bin/bash

# Start Celery worker in the background
celery -A src.worker.celery_app worker -f celery.logs -E --pool=solo &

# Run the main application
exec python -m src.main
