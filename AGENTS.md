# BreadBoard AI - opencode Agent Instructions

## Project Structure
- `apps/mobile_app/` — Flutter mobile app (Android + iOS)
- `apps/web_app/` — Flutter web app
- `apps/admin_panel/` — Admin web panel
- `apps/teacher_dashboard/` — Teacher web dashboard
- `apps/packages/shared/` — Shared Flutter package (core, design system, widgets)
- `backend/app/` — FastAPI Python backend
- `ai-engine/` — AI/ML Python microservice
- `shared/` — Shared types, schemas, constants
- `infrastructure/` — Docker, K8s, monitoring

## Commands
- Lint Python: `cd backend && flake8 app tests` or `cd ai-engine && flake8 engine tests`
- Test Python: `cd backend && pytest` or `cd ai-engine && pytest`
- Test Python unit only: `cd backend && python -m pytest tests/unit/ -v`
- Test Flutter: `cd apps/mobile_app && flutter test`
- Test Flutter web: `cd apps/web_app && flutter test test/`
- Analyze Flutter: `cd apps/web_app && flutter analyze`
- Format Python: `black --line-length=100 backend/ ai-engine/`
- Migrate DB: `cd backend && alembic upgrade head`
- Make migration: `cd backend && alembic revision --autogenerate -m "description"`
- Seed sources: `cd backend && python -m app.db.seeds.seed_sources`
- Docker up: `docker-compose -f infrastructure/docker/docker-compose.yml up -d`
- Pub get: `cd apps/mobile_app && flutter pub get`
- Shared pub get: `cd apps/packages/shared && flutter pub get`

## Conventions
- Python: black (100 chars), isort, flake8, mypy
- Dart: flutter_lints, Dart fix
- No paid APIs — all AI via Ollama + local models
- Database: PostgreSQL (production/Render), MySQL (local Docker), SQLite (tests)
- Feature-first Clean Architecture in Flutter
- `DATABASE_URL` auto-detects async driver: `postgresql://` → +asyncpg, `mysql://` → +aiomysql
- NEVER commit `.github/workflows/` (PAT lacks workflow scope)

## Deployment (Render + Vercel)
- Backend: https://breadboard-backend.onrender.com (health: `/health`)
- Frontend: https://breadboardai.vercel.app
- Database: PostgreSQL (Render free tier, 1GB)
- Build: `render-build.sh` installs deps; `render-start.sh` runs migrations + gunicorn
- Blueprint: `render.yaml` defines web service + postgres db
- CORS: Update `render.yaml` → `BACKEND_CORS_ORIGINS` for new frontend URLs
- Flutter web build: `cd apps/web_app && flutter build web --dart-define=API_BASE_URL=https://breadboard-backend.onrender.com --release`
- Vercel: Deploy `build/web` folder; or use `vercel.json` in repo
- Render deploy: push to main → auto-deploy; or Manual Deploy from dashboard

## Content Sourcing Rules
- Priority source order: Wikipedia → Electronics Tutorials → Arduino Docs → Raspberry Pi Docs → SparkFun → Adafruit → Open Source Circuits
- All AI-generated content MUST include source attribution with URLs
- Image sources: Wikipedia Commons or Wikimedia Commons only
- Store source URLs in `sources` table + `content_sources` junction
- Every component spec must include a datasheet URL when available
- Never fabricate URLs — omit if uncertain
