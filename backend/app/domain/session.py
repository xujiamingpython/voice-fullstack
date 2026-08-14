"""领域模型：游客会话。"""
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Session:
    """游客会话（session_id 由前端生成，后端按此存储对话）。"""

    session_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
