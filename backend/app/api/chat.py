"""WebSocket 对话接口：承载整段对话事件流。

ws://host/ws/chat?session_id=xxx

客户端 → 服务端:
  {"type": "audio_chunk", "data": "<base64>", "format": "webm"}
  {"type": "audio_end"}
  {"type": "text", "content": "..."}
  {"type": "interrupt"}
  {"type": "ping"}

服务端 → 客户端:
  {"type": "asr_partial" | "asr_final" | "llm_thinking" | "tool_calling" |
   "tool_result" | "llm_chunk" | "tts_audio" | "tts_end" | "done" | "error", ...}
"""
import asyncio
import base64
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.common.logger import new_request_id
from app.services.orchestrator import LLMOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

orchestrator = LLMOrchestrator()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket, session_id: str = "default"):
    await websocket.accept()
    new_request_id()
    logger.info("WS connected session=%s", session_id)

    # 对话上下文（内存版；后续可换 SQLite）
    messages: list[dict] = []
    audio_buffer = bytearray()
    listening = False

    async def send(event: dict):
        await websocket.send_json(event)

    try:
        while True:
            raw = await websocket.receive()
            if "text" in raw:
                msg = raw["text"]
                data = json_loads(msg) or {"type": "unknown"}
                t = data.get("type")

                if t == "text":
                    # 纯文本输入 → 直接走 LLM 编排
                    await orchestrator.run(data.get("content", ""), messages, send)

                elif t == "audio_chunk":
                    listening = True
                    audio_buffer.extend(base64.b64decode(data.get("data", "")))

                elif t == "audio_end":
                    if listening and audio_buffer:
                        # ASR 识别录音 → 文本 → LLM 编排
                        text = await orchestrator.asr_transcribe(bytes(audio_buffer), data.get("format", "webm"))
                        await send({"type": "asr_final", "text": text})
                        await orchestrator.run(text, messages, send)
                    audio_buffer.clear()
                    listening = False

                elif t == "interrupt":
                    orchestrator.interrupt()
                    await send({"type": "interrupted"})

                elif t == "ping":
                    await send({"type": "pong"})

            elif "bytes" in raw:
                # 二进制音频帧
                audio_buffer.extend(raw["bytes"])

    except WebSocketDisconnect:
        logger.info("WS disconnected session=%s", session_id)
    except Exception:
        logger.exception("WS error")
        try:
            await send({"type": "error", "code": "INTERNAL", "message": "internal error"})
        except Exception:
            pass


def json_loads(s: str):
    import json
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None
