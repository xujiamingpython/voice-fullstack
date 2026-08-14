"""ASR REST 接口：单次音频识别。

POST /api/asr
  multipart/form-data: file=<audio bytes>
  query: format=webm|wav|pcm (默认 wav)
"""
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.infrastructure.asr_client import ASRClient

logger = logging.getLogger(__name__)
router = APIRouter()

asr_client = ASRClient()


@router.post("/asr")
async def transcribe(
    file: UploadFile = File(...),
    format: str = Form("wav"),
):
    try:
        audio = await file.read()
        if not audio:
            raise HTTPException(status_code=400, detail="empty audio")
        text = await asr_client.transcribe(audio, fmt=format)
        return {"text": text}
    except Exception as e:
        logger.exception("ASR failed")
        raise HTTPException(status_code=502, detail=f"asr failed: {e}")
