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
- `scripts/tunnel/` — Tunnel scripts (serveo + Cloudflare)
- `scripts/monitor/` — Uptime monitoring scripts

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
- Backend: https://breadboard-backend.onrender.com (health: `/health`, AI: `/v1/ai/health`)
- Frontend (prod): https://webapp-six-eta-87.vercel.app (Flutter Web)
- Frontend (old): https://breadboardai.vercel.app
- Vercel token: `$(VERCEL_TOKEN)`
- Vercel project scope: `princenareshgamot-8750s-projects`
- Database: PostgreSQL (Render free tier, 1GB, db name: `breadboard`)
- Database URL (internal): `postgresql://breadboard:$(DB_PASSWORD)@dpg-d8tmg777f7vs73fa6blg-a/breadboard`
- Build: `render-build.sh` installs deps; `render-start.sh` runs migrations + gunicorn
- Blueprint: `render.yaml` defines web service + postgres db
- CORS origins: `https://breadboardai.vercel.app,https://webapp-six-eta-87.vercel.app` (set via env var `BACKEND_CORS_ORIGINS`)
- Render env-var API: `PUT /v1/services/{serviceId}/env-vars/{key}` (single, safe) vs `PUT /env-vars` (bulk, wipes DATABASE_URL)
- Flutter web build: `cd apps/web_app && flutter build web --dart-define=API_BASE_URL=https://breadboard-backend.onrender.com --release`
- Vercel deploy (prebuilt): `New-Item -ItemType Directory -Path .vercel/output/static -Force | Out-Null && Copy-Item build/web/* .vercel/output/static -Recurse -Force && vercel deploy --prebuilt --prod --token <TOKEN> --scope princenareshgamot-8750s-projects`
- Render deploy: push to main → auto-deploy; or API: `POST /v1/services/{serviceId}/deploys`

## Ollama Tunnels (Dual Tunnel Architecture)

### serveo.net (Primary — Chat, Generate, Health)
- Local Ollama runs at `http://localhost:11434` with models: `llava:latest` (7B, vision), `qwen2.5:1.5b`
- Node.js proxy (`scripts/tunnel/node_proxy.js`) on port 19994 forwards HTTP `/api/*` to Ollama
- STABLE subdomain: `https://breadboard-ai.serveousercontent.com` → port 19994 → Ollama 11434 (SSH key registered)
- SSH command: `ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R breadboard-ai:80:127.0.0.1:19994 serveo.net`
- Do NOT use `-N` flag (causes 502 Bad Gateway); do NOT use `-tt` flag
- `scripts/tunnel/tunnel.vbs` starts the tunnel invisibly (hidden window, no `-N` flag)
- `scripts/tunnel/start_tunnel.bat` starts proxy + tunnel in visible window (one-click)
- To start: run `scripts\tunnel\start_tunnel.bat`
- SSH key registered at https://console.serveo.net/ssh/keys:
  - `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEMdjQk/o0/mizAClNHY7OI5O/HoW9wGu6Yx86PBCYBS`
  - SHA256: `35rDBJV/U9MNawIqhRn6tFtC05TSPlKfQ13tmo6T9A4`
- **Known limitation**: serveo filters responses containing electronics/circuit instruction content (returns 502). Used only for `/v1/ai/chat` and `/v1/ai/generate` (general Q&A).

### Cloudflare Tunnel (Fallback — Circuit Generation Only)
- Cloudflare Tunnel has NO content filtering — handles all circuit/electronics content
- Binary at `D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\cloudflared.exe`
- Quick tunnel (ephemeral, URL changes each restart): `cloudflared tunnel --url http://localhost:19994`
- `scripts/tunnel/cloudflare_tunnel.vbs` starts it invisibly; `scripts/tunnel/start_cloudflare.bat` starts it visibly
- Auto-managed by `scripts/tunnel/cloudflare_manager.ps1` (auto-start via Startup folder)
- **Workflow to update**: start tunnel → get URL → set `CIRCUIT_OLLAMA_HOST` on Render → trigger deploy
- Render expects `CIRCUIT_OLLAMA_HOST` env var pointing to the current Cloudflare tunnel URL

### Dual-Tunnel Flow
```
User → Render Backend → POST /v1/ai/circuit/generate
  1. Try AI Engine (port 8001) → fails (not deployed)
  2. Try Ollama via serveo (OLLAMA_HOST) → blocked by filter → 502
  3. Try Ollama via Cloudflare (CIRCUIT_OLLAMA_HOST) → succeeds
```
- Fallback implemented in `AIService.circuit_generate_with_fallback()` at `backend/app/services/ai_service.py:133`
- Config: `backend/app/core/config.py:23` — `circuit_ollama_host` (env var `CIRCUIT_OLLAMA_HOST`)

### Env Vars (set via Render API)
- `OLLAMA_HOST` = `https://breadboard-ai.serveousercontent.com` (serveo, no change needed)
- `CIRCUIT_OLLAMA_HOST` = `https://<tunnel-id>.trycloudflare.com` (cloudflare, updates when tunnel restarts)
- Render API key: `$(RENDER_API_KEY)`
- Render Service ID: `srv-d8tmgsn7f7vs73fa74q0`
- Trigger Render deploy: `POST /v1/services/{serviceId}/deploys`
- Tunnel health check: GET `https://breadboard-ai.serveousercontent.com/api/tags` → JSON model list
- AI health check via backend: GET `https://breadboard-backend.onrender.com/v1/ai/health`

## Uptime Monitor
- Script: `scripts/monitor/uptime_monitor.ps1` (pings backend, AI health, frontend every 5 min)
- Auto-starts via VBS in Startup folder: `UptimeMonitor.vbs`
- Desktop shortcut: `StartUptimeMonitor.vbs`
- Logs to `$env:TEMP\uptime_monitor.log`
- Prevents Render free-tier spin-down (15 min inactivity timeout)
- For 24/7 coverage, sign up at https://uptimerobot.com (free, 5 monitors)

## Flutter APK Build
- Universal APK: `app-release.apk` (49.4MB, optimized with `--obfuscate --split-debug-info`)
- Per-ABI APKs (preferred for smaller size):
  - `app-arm64-v8a-release.apk` (17.5MB) — most modern devices
  - `app-armeabi-v7a-release.apk` (14.9MB) — older devices
  - `app-x86_64-release.apk` (18.9MB) — emulators/Chromebooks
- Build commands:
  - `flutter build apk --release --split-debug-info=build/debug-info --obfuscate` (universal)
  - `flutter build apk --release --split-per-abi --split-debug-info=build/debug-info --obfuscate` (per-ABI)
- Fixes applied for Flutter 3.44.1 compatibility:
  - `pubspec.yaml`: `audioplayers: ^5.2.1` → `^6.8.0` (compileSdk 33→34)
  - `android/gradle.properties`: added `kotlin.incremental=false` (cross-drive Kotlin cache bug C: vs D:)
- Known warnings (non-blocking): KGP applied by `audioplayers_android`, source/target value 8 obsolete

## Content Sourcing Rules
- Priority source order: Wikipedia → Electronics Tutorials → Arduino Docs → Raspberry Pi Docs → SparkFun → Adafruit → Open Source Circuits
- All AI-generated content MUST include source attribution with URLs
- Image sources: Wikipedia Commons or Wikimedia Commons only
- Store source URLs in `sources` table + `content_sources` junction
- Every component spec must include a datasheet URL when available
- Never fabricate URLs — omit if uncertain
