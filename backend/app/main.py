"""FastAPI 应用入口。

启动: uvicorn app.main:app --reload --port 8000
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import asr, chat, health, tts
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
    description="ASR + LLM + MCP + TTS 全链路语音助手后端",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS：开发期允许所有来源；生产建议收紧
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(asr.router, prefix="/api", tags=["asr"])
app.include_router(tts.router, prefix="/api", tags=["tts"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
