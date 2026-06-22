# BreadBoard AI

Voice-first electronics learning platform. Speak in natural language — get circuit diagrams, component lists, cost estimates & breadboard verification instantly.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Flutter + Dart (Mobile + Web) |
| Backend | Python + FastAPI |
| AI Engine | FastAPI + Ollama (local LLMs) |
| Database | MySQL 8 + async SQLAlchemy |
| Speech | Whisper / Vosk (optional) |
| Vision | OpenCV / YOLO (optional) |

## Project Structure

```
apps/
  mobile_app/       — Android + iOS app
  web_app/          — Flutter web app
  admin_panel/      — Admin web panel
  teacher_dashboard/— Teacher dashboard
  packages/shared/  — Shared Flutter package (core, design, widgets)
backend/            — FastAPI Python backend
ai-engine/          — AI/ML Python microservice
shared/             — Shared types, schemas, constants
infrastructure/     — Docker, K8s, monitoring
```

## Quick Start

### Prerequisites
- Python 3.11+
- Flutter 3.x
- MySQL 8.0
- Ollama

### 1. Database
```bash
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'breadboard'@'localhost' IDENTIFIED BY 'breadboard'; CREATE DATABASE IF NOT EXISTS breadboard; GRANT ALL ON breadboard.* TO 'breadboard'@'localhost';"
cd backend && alembic upgrade head
```

### 2. Backend
```bash
cd backend
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. AI Engine
```bash
cd ai-engine
pip install -e .
uvicorn engine.main:app --host 0.0.0.0 --port 8001
```

### 4. Flutter (Mobile or Web)
```bash
cd apps/mobile_app && flutter run          # Android/iOS
cd apps/web_app && flutter run -d chrome   # Web
```

### Android Emulator Note
Auto-detects `10.0.2.2` for host connectivity. Override with:
```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000 --dart-define=AI_ENGINE_URL=http://10.0.2.2:8001
```

## Environment Variables

Copy `.env.example` to `.env` in `backend/` and configure:
- `DATABASE_URL` — MySQL connection string
- `JWT_SECRET_KEY` — JWT signing secret
- `OLLAMA_HOST` — Ollama server URL
- `OLLAMA_MODEL` — Default LLM model
