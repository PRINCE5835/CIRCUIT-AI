#!/usr/bin/env bash
set -euo pipefail

echo "Build starting..."

cd backend

pip install -r requirements/prod.txt

echo "Build complete."
