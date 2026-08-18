"""配置 API：前端设置页初始化所需的服务配置与工具列表。"""
import logging

from fastapi import APIRouter

from app import config
from app.infrastructure.tools_client import TOOL_LABELS, TOOL_SCHEMAS

logger = logging.getLogger(__name__)
router = APIRouter()

# 前端音色配置（与 miniprogram/pages/settings/settings.js 对齐）
VOICES = [
    {"id": "voicy-female", "name": "女声·温柔", "desc": "知性"},
    {"id": "voicy-male", "name": "男声·磁性", "desc": "沉稳"},
    {"id": "voicy-child", "name": "童声", "desc": "活泼"},
    {"id": "voicy-cantonese", "name": "粤语", "desc": "地道"},
]

MODELS = {
    "aliyun": ["qwen-turbo", "qwen-plus", "qwen-max"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "tencent": ["hy3", "hunyuan-role-latest"],
}


@router.get("/config")
async def get_config():
    """服务配置（模型/音色/能力开关）。"""
    return {
        "llm_provider": config.LLM_PROVIDER,
        "llm_model": _current_model(),
        "models": MODELS,
        "voices": VOICES,
        "default_city": config.DEFAULT_CITY,
        "max_input_chars": config.MAX_INPUT_CHARS,
        "max_tool_rounds": config.MAX_TOOL_ROUNDS,
        "deps": {
            "llm": bool(config.ALIYUN_BAILIAN_API_KEY or config.DEEPSEEK_API_KEY or config.TENCENT_HUNYUAN_API_KEY),
            "asr": bool(config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_ASR_TOKEN),
            "tts": bool(config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_TTS_TOKEN),
            "amap": bool(config.AMAP_SERVER_API_KEY),
        },
    }


def _current_model() -> str:
    """返回当前选中 provider 的模型名。"""
    if config.LLM_PROVIDER == "tencent":
        return config.TENCENT_HUNYUAN_MODEL
    if config.LLM_PROVIDER == "deepseek":
        return config.DEEPSEEK_MODEL
    return config.LLM_MODEL


@router.get("/tools")
async def get_tools():
    """可用工具列表（前端设置页白名单）。"""
    return [
        {"name": label, "key": key, "description": _schema_desc(key)}
        for key, label in TOOL_LABELS.items()
    ]


def _schema_desc(tool_key: str) -> str:
    for s in TOOL_SCHEMAS:
        if s["function"]["name"] == tool_key:
            return s["function"].get("description", "")
    return ""
