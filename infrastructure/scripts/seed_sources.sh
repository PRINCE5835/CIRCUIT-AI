#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../backend"
echo "Seeding priority sources into database..."
python -m app.db.seeds.seed_sources
echo "Done."
