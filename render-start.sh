#!/usr/bin/env bash
set -euo pipefail

cd backend

# Run database migrations
PYTHONPATH=. alembic upgrade head

# Start the application
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT --timeout 120
