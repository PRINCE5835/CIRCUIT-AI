# ADR-001: Use FastAPI for Backend

**Status:** Accepted

**Context:** Need a Python backend with async support, type safety, and auto-generated docs.

**Decision:** Use FastAPI with Pydantic v2 schemas.

**Consequences:**
- Automatic OpenAPI documentation
- Async endpoint support for streaming responses
- Built-in validation via Pydantic
