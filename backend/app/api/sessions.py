"""会话 API：查询 / 删除会话历史（游客模式按 session_id）。"""
import logging

from fastapi import APIRouter

from app.services.conversation import conversation_store

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, limit: int = 50):
    """返回会话历史消息列表。"""
    history = await conversation_store.history(session_id, limit=limit)
    return {
        "session_id": session_id,
        "count": len(history),
        "messages": history,
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话全部历史。"""
    await conversation_store.clear(session_id)
    return {"ok": True, "session_id": session_id}
