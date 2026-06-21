#!/usr/bin/env bash
set -euo pipefail
cd backend
alembic upgrade head
echo "Migrations complete."
