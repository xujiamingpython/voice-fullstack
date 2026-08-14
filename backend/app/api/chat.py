"""对话 API：WebSocket 流式 / REST 降级同步。

事件协议（WS 推送）：
    llm_thinking / tool_calling / tool_result / llm_chunk / tts_audio / tts_end / done / error
前端消息：{type:'text', content, settings?} / {type:'ping'} / {type:'interrupt'}
"""
import logging
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from app.services.conversation import conversation_store
from app.services.orchestrator import orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

# 同一 session 并发处理保护（微信端按会话串行，防御重复发送）
_processing: set[str] = set()


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="guest")
    settings: Optional[dict] = None


async def _safe_send(websocket: WebSocket, event: dict) -> bool:
    """发送事件；客户端断开时返回 False。"""
    try:
        await websocket.send_json(event)
        return True
    except Exception:
        return False


@router.websocket("/ws/chat")
async def ws_chat(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket.query_params.get("session_id", "guest")
    logger.info("[ws] connected: %s", session_id)
    try:
        while True:
            raw = await websocket.receive_json()
            mtype = raw.get("type", "text")

            if mtype == "ping":
                await _safe_send(websocket, {"type": "pong"})
                continue

            if mtype == "interrupt":
                await _safe_send(websocket, {"type": "interrupted"})
                continue

            if mtype != "text":
                continue

            text = (raw.get("content") or "").strip()
            if not text:
                await _safe_send(websocket, {"type": "error", "code": "EMPTY_INPUT", "message": "内容为空"})
                continue

            if session_id in _processing:
                await _safe_send(websocket, {"type": "error", "code": "BUSY", "message": "上一条消息还在处理中"})
                continue

            _processing.add(session_id)
            try:
                settings = raw.get("settings") or {}

                async def on_event(event: dict):
                    return await _safe_send(websocket, event)

                await orchestrator.run(text, session_id, on_event, settings)
            finally:
                _processing.discard(session_id)
    except WebSocketDisconnect:
        logger.info("[ws] disconnected: %s", session_id)
    except Exception as e:
        logger.exception("[ws] error: %s", session_id)
        await _safe_send(websocket, {"type": "error", "code": "WS_ERROR", "message": str(e)})


@router.post("/api/chat")
async def chat_rest(req: ChatRequest):
    """REST 降级同步接口：WS 不可用时前端调用。返回聚合后的完整回复。"""
    events: list[dict] = []
    reply_parts: list[str] = []

    async def on_event(event: dict):
        events.append(event)
        if event.get("type") == "llm_chunk" and event.get("text"):
            reply_parts.append(event["text"])
        # 保留工具结果用于前端渲染
        return True

    await orchestrator.run(req.text, req.session_id, on_event, req.settings or {})

    return {
        "reply": "".join(reply_parts),
        "events": events,
    }


@router.post("/api/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    """清空某个会话的历史消息（前端设置页「清空历史」调用）。"""
    await conversation_store.clear(session_id)
    return {"ok": True, "session_id": session_id}
