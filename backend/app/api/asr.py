"""ASR API：POST /api/asr，multipart 上传录音文件 → 返回识别文本。"""
import logging
import os
import tempfile
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.infrastructure.asr_client import asr_client

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXT = {".mp3", ".wav", ".aac", ".m4a", ".pcm", ".amr"}


@router.post("/asr")
async def asr_upload(file: UploadFile = File(...), session_id: str = Form("guest")):
    """识别录音。返回 {text, mock, session_id}。"""
    ext = os.path.splitext(file.filename or "")[1].lower() or ".mp3"
    if ext not in ALLOWED_EXT:
        # 兼容无扩展名（微信临时文件）场景
        ext = ".mp3"

    # 微信上传大小一般 < 1MB；防御性限制 10MB
    MAX_BYTES = 10 * 1024 * 1024
    content = await file.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="音频文件过大")

    tmp_path = os.path.join(tempfile.gettempdir(), f"asr_{uuid.uuid4().hex}{ext}")
    try:
        with open(tmp_path, "wb") as f:
            f.write(content)
        result = await asr_client.transcribe(tmp_path)
        return {**result, "session_id": session_id}
    except Exception as e:
        logger.exception("[asr] upload failed")
        raise HTTPException(status_code=500, detail=f"语音识别失败：{e}")
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
