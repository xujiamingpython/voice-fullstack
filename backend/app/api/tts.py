"""TTS REST 接口：单次文本转语音。

POST /api/tts
  json: {"text": "你好", "voice": "ailiao"}
  返回: audio/mp3 二进制流
"""
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.infrastructure.tts_client import TTSClient

logger = logging.getLogger(__name__)
router = APIRouter()

tts_client = TTSClient()


class TTSRequest(BaseModel):
    text: str
    voice: str = "ailiao"


@router.post("/tts")
async def synthesize(req: TTSRequest):
    try:
        if not req.text.strip():
            raise HTTPException(status_code=400, detail="empty text")
        audio = await tts_client.synthesize(req.text, voice=req.voice)
        from fastapi.responses import Response
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as e:
        logger.exception("TTS failed")
        raise HTTPException(status_code=502, detail=f"tts failed: {e}")
