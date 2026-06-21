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
- Test Flutter: `cd apps/mobile_app && flutter test`
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
- MySQL 8 with async SQLAlchemy (aiomysql)
- Feature-first Clean Architecture in Flutter

## Content Sourcing Rules
- Priority source order: Wikipedia → Electronics Tutorials → Arduino Docs → Raspberry Pi Docs → SparkFun → Adafruit → Open Source Circuits
- All AI-generated content MUST include source attribution with URLs
- Image sources: Wikipedia Commons or Wikimedia Commons only
- Store source URLs in `sources` table + `content_sources` junction
- Every component spec must include a datasheet URL when available
- Never fabricate URLs — omit if uncertain
