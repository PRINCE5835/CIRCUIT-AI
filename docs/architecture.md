# BreadBoard AI - Architecture Overview

## High-Level Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Flutter App │────▶│   FastAPI    │────▶│  AI Engine   │
│  (Mobile+Web)│     │   Backend    │     │  (Microsvc)  │
└─────────────┘     └──────┬───────┘     └──────┬──────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐      ┌─────────────┐
                    │   SQLite    │      │   Ollama     │
                    │  (PostgreSQL)│      │  (Local LLM) │
                    └─────────────┘      └─────────────┘
```

## Key Design Decisions

1. **Monorepo** - Single repository for all services simplifies coordination
2. **Feature-first Flutter** - Clean Architecture per feature (data/domain/presentation)
3. **FastAPI + Pydantic v2** - Type-safe API layer with auto-docs
4. **Separation of concerns** - Backend (business logic) vs AI Engine (compute-heavy ML)
5. **Ollama** - Local LLM inference, no paid APIs
6. **SQLite → PostgreSQL** - Connection string swap for production scale

## Service Communication

- Frontend ↔ Backend: REST/JSON (HTTPS)
- Backend ↔ AI Engine: Internal REST/HTTP
- WebSocket: Real-time voice streaming
