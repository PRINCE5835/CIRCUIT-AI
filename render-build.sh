#!/usr/bin/env bash
set -euo pipefail

cd backend

# Install dependencies
pip install -r requirements/prod.txt

# Run database migrations (PYTHONPATH required for 'app' module)
PYTHONPATH=. alembic upgrade head
