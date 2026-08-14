"""TTS API：POST /api/tts，文本 → base64 mp3 音频。"""
import base64
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.infrastructure.tts_client import tts_client

logger = logging.getLogger(__name__)
router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    voice: str = Field(default="voicy-female")
    session_id: str = Field(default="guest")


@router.post("/tts")
async def tts_synth(req: TTSRequest):
    """合成语音。返回 {audio: base64 mp3}；未配置 Key 时返回 {audio: null, mock: true}。"""
    audio = await tts_client.synthesize(req.text, req.voice)
    if not audio:
        return {"audio": None, "mock": True, "message": "未配置 TTS Key，跳过语音合成"}
    return {"audio": base64.b64encode(audio).decode(), "format": "mp3", "mock": False}
