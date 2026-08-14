"""对话会话管理（骨架：内存实现，后续可换 SQLite / Redis）。"""
import logging
import uuid
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Session:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    title: str = "新会话"
    messages: list = field(default_factory=list)
    created_at: float = 0.0
    updated_at: float = 0.0

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "messages": self.messages,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(id=session_id)
        return self._sessions[session_id]

    def list(self) -> list[dict]:
        return [s.to_dict() for s in self._sessions.values()]

    def delete(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None
