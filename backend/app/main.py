"""FastAPI 应用入口。

启动: uvicorn app.main:app --reload --port 8000

当前为「基础骨架」阶段：仅挂载健康检查。
业务路由（asr / tts / chat）在需求文档与 UI 设计评审确认后开发（见 docs/）。
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
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
    description="ASR + LLM + MCP + TTS 全链路语音助手后端（微信小程序端）",
    version="0.2.0",
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

# 路由注册（业务路由待文档评审后开发）
app.include_router(health.router, prefix="/api", tags=["health"])
