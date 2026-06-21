"""
Context manager — maintains conversation history and RAG context
for multi-turn LLM interactions across features.
"""
# flake8: noqa: E501

from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Turn:
    role: str  # "user" | "assistant" | "system"
    content: str
    source_urls: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    id: str
    features: str  # "circuit_generation" | "learning" | "repair" | "component"
    turns: list[Turn] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def message_history(self) -> list[dict]:
        return [{"role": t.role, "content": t.content} for t in self.turns]

    @property
    def token_estimate(self) -> int:
        return sum(len(t.content.split()) * 1.3 for t in self.turns)


class ContextManager:
    """Manages conversation sessions with automatic truncation."""

    def __init__(self, max_tokens: int = 4096):
        self._sessions: dict[str, Session] = {}
        self.max_tokens = max_tokens

    def create_session(self, session_id: str, features: str) -> Session:
        session = Session(id=session_id, features=features)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def add_turn(self, session_id: str, role: str, content: str, sources: list[str] | None = None) -> Session:
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(session_id, "general")
        session.turns.append(Turn(role=role, content=content, source_urls=sources or []))
        self._truncate_if_needed(session)
        return session

    def add_system_message(self, session_id: str, content: str) -> Session:
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(session_id, "general")
        if not session.turns or session.turns[0].role != "system":
            session.turns.insert(0, Turn(role="system", content=content))
        return session

    def get_chat_history(self, session_id: str, include_system: bool = True) -> list[dict]:
        session = self._sessions.get(session_id)
        if not session:
            return []
        if include_system:
            return session.message_history
        return [t for t in session.message_history if t["role"] != "system"]

    def clear_session(self, session_id: str):
        self._sessions.pop(session_id, None)

    def _truncate_if_needed(self, session: Session):
        """Remove oldest user/assistant turns while keeping system message."""
        while session.token_estimate > self.max_tokens and len(session.turns) > 2:
            for i, t in enumerate(session.turns):
                if t.role in ("user", "assistant"):
                    session.turns.pop(i)
                    break

    def build_messages(self, session_id: str, system_prompt: str, user_message: str) -> list[dict]:
        """Build the full message list for an LLM call: system + history + user."""
        messages = [{"role": "system", "content": system_prompt}]
        session = self._sessions.get(session_id)
        if session:
            messages.extend(session.message_history)
        messages.append({"role": "user", "content": user_message})
        return messages


# Singleton
context_manager = ContextManager()
