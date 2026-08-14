"""FastAPI 应用入口。

启动: uvicorn app.main:app --reload --port 8000

路由：
    /api/health         健康检查
    /api/config         服务配置（音色/模型/能力开关）
    /api/tools          工具列表
    /api/asr            ASR 语音识别（multipart 上传）
    /api/tts            TTS 语音合成
    /api/chat           REST 对话（WS 不可用时的降级接口）
    /ws/chat            WebSocket 流式对话（主通道）
    /api/sessions/*     会话历史查询/删除
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import asr, chat, config_api, health, sessions, tts
from app.common.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Voice Full-Stack backend starting...")
    yield
    logger.info("👋 Backend shutting down.")


app = FastAPI(
    title="Voice Full-Stack API",
    description="ASR + LLM + 地图工具 + TTS 全链路语音助手后端（微信小程序端）",
    version="0.3.0",
    lifespan=lifespan,
)

# CORS：开发期允许所有来源；生产建议收紧为小程序域名白名单
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 业务路由
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(config_api.router, prefix="/api", tags=["config"])
app.include_router(asr.router, prefix="/api", tags=["asr"])
app.include_router(tts.router, prefix="/api", tags=["tts"])
# chat 路由路径自带 /api 与 /ws 前缀，单独挂载避免 WebSocket 被改写
app.include_router(chat.router, tags=["chat"])
app.include_router(sessions.router, prefix="/api", tags=["sessions"])
