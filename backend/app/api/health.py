"""健康检查：返回服务与外部依赖状态。"""
import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0",
        "deps": {
            "aliyun_bailian": bool(__import__("app.config", fromlist=["ALIYUN_BAILIAN_API_KEY"]).ALIYUN_BAILIAN_API_KEY),
            "asr": bool(__import__("app.config", fromlist=["ALIYUN_ASR_APP_KEY"]).ALIYUN_ASR_APP_KEY),
            "tts": bool(__import__("app.config", fromlist=["ALIYUN_TTS_APP_KEY"]).ALIYUN_TTS_APP_KEY),
            "amap": bool(__import__("app.config", fromlist=["AMAP_JS_API_KEY"]).AMAP_JS_API_KEY),
        },
    }
