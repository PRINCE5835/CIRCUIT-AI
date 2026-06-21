# ADR-002: Feature-First Clean Architecture in Flutter

**Status:** Accepted

**Context:** Need a scalable Flutter architecture that supports 12+ features without tight coupling.

**Decision:** Each feature follows Clean Architecture with data/domain/presentation layers.

**Consequences:**
- Features can be developed in parallel
- Domain logic is testable without Flutter dependencies
- Consistent pattern across all features
