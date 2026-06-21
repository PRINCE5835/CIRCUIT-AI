#!/usr/bin/env bash
set -euo pipefail

echo "=== BreadBoard AI - Development Setup ==="

echo "1. Setting up Backend..."
cd backend
pip install -r requirements/dev.txt
cd ..

echo "2. Setting up AI Engine..."
cd ai-engine
pip install -e .
cd ..

echo "3. Setting up Mobile App..."
cd apps/mobile_app
flutter pub get
cd ../..

echo "4. Initializing Database..."
cd backend
alembic upgrade head
cd ..

echo "5. Downloading AI Models..."
bash infrastructure/scripts/download_models.sh

echo "=== Setup Complete ==="
