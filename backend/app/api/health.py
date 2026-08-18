"""健康检查：返回服务与外部依赖状态。"""
import logging

from fastapi import APIRouter

from app import config

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.2.0",
        "deps": {
            "llm_aliyun": bool(config.ALIYUN_BAILIAN_API_KEY),
            "llm_deepseek": bool(config.DEEPSEEK_API_KEY),
            "llm_tencent": bool(config.TENCENT_HUNYUAN_API_KEY),
            "asr": bool(config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_ASR_TOKEN),
            "tts": bool(config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_TTS_TOKEN),
            "amap": bool(config.AMAP_SERVER_API_KEY),
            "tencent_lbs": bool(config.TENCENT_LBS_KEY),
        },
    }
