# Local Development Guide

## Prerequisites
- Python 3.11+
- Flutter 3.19+
- Ollama (latest)
- Docker Desktop (optional)

## Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/breadboard/breadboard-ai.git
cd breadboard-ai

# 2. Environment
cp .env.example .env

# 3. Backend
cd backend
pip install -r requirements/dev.txt
cd ..

# 4. AI Engine
cd ai-engine
pip install -e .
cd ..

# 5. Mobile App
cd apps/mobile_app
flutter pub get
cd ../..

# 6. Database
cd backend
alembic upgrade head
cd ..

# 7. Run
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: AI Engine
cd ai-engine && uvicorn engine.main:app --reload --port 8001

# Terminal 3: Web App
cd apps/web_app && flutter run -d chrome
```

## Testing
```bash
make test        # All Python tests
flutter test     # Flutter tests
```
