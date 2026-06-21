#!/usr/bin/env bash
set -euo pipefail
cd backend
python -m app.db.seeds
echo "Database seeded."
