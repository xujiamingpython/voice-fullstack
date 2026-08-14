"""会话管理：SQLite 按 session_id 存储对话（游客模式）。"""
import asyncio
import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone

from app import config

logger = logging.getLogger(__name__)

_lock = threading.Lock()


class ConversationStore:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # 复用模块级锁（SQLite 跨实例共享连接风险防护）
        self._lock = _lock
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._lock:
            conn = self._conn()
            try:
                conn.execute(
                    """CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL DEFAULT '',
                        tool_calls TEXT,
                        created_at TEXT NOT NULL
                    )"""
                )
                conn.execute(
                    """CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id, id)"""
                )
                conn.commit()
            finally:
                conn.close()

    # ---------- 同步实现（线程池包装） ----------
    def _append_sync(self, session_id: str, role: str, content: str, tool_calls: list = None):
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            conn = self._conn()
            try:
                conn.execute(
                    "INSERT INTO messages(session_id, role, content, tool_calls, created_at) VALUES (?,?,?,?,?)",
                    (session_id, role, content, json.dumps(tool_calls or [], ensure_ascii=False), now),
                )
                conn.commit()
            finally:
                conn.close()

    def _history_sync(self, session_id: str, limit: int = 20) -> list:
        conn = self._conn()
        try:
            rows = conn.execute(
                "SELECT role, content, tool_calls FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
            msgs = []
            for r in reversed(rows):
                tc = json.loads(r["tool_calls"] or "[]")
                item = {"role": r["role"], "content": r["content"]}
                if tc:
                    item["tool_calls"] = tc
                msgs.append(item)
            return msgs
        finally:
            conn.close()

    def _clear_sync(self, session_id: str):
        with self._lock:
            conn = self._conn()
            try:
                conn.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
                conn.commit()
            finally:
                conn.close()

    # ---------- 异步接口 ----------
    async def append(self, session_id: str, role: str, content: str, tool_calls: list = None):
        await asyncio.to_thread(self._append_sync, session_id, role, content, tool_calls)

    async def history(self, session_id: str, limit: int = 20) -> list:
        return await asyncio.to_thread(self._history_sync, session_id, limit)

    async def clear(self, session_id: str):
        await asyncio.to_thread(self._clear_sync, session_id)


conversation_store = ConversationStore()
