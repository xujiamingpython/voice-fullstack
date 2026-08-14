"""应用配置：从 .env / 环境变量加载。"""
import os

from dotenv import load_dotenv

load_dotenv()

# ---------- 服务 ----------
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ---------- LLM（阿里云百炼 / Deepseek） ----------
ALIYUN_BAILIAN_API_KEY = os.getenv("ALIYUN_BAILIAN_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# ---------- ASR / TTS ----------
ALIYUN_ASR_APP_KEY = os.getenv("ALIYUN_ASR_APP_KEY", "")
ALIYUN_ASR_TOKEN = os.getenv("ALIYUN_ASR_TOKEN", "")
ALIYUN_ASR_WS_URL = os.getenv("ALIYUN_ASR_WS_URL", "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1")

ALIYUN_TTS_APP_KEY = os.getenv("ALIYUN_TTS_APP_KEY", "")
ALIYUN_TTS_TOKEN = os.getenv("ALIYUN_TTS_TOKEN", "")
ALIYUN_TTS_VOICE = os.getenv("ALIYUN_TTS_VOICE", "ailiao")
ALIYUN_TTS_WS_URL = os.getenv("ALIYUN_TTS_WS_URL", "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1")

# ---------- 高德地图 ----------
AMAP_JS_API_KEY = os.getenv("AMAP_JS_API_KEY", "")
AMAP_MCP_ENDPOINT = os.getenv("AMAP_MCP_ENDPOINT", "https://mcp.amap.com/sse")
AMAP_MCP_TOKEN = os.getenv("AMAP_MCP_TOKEN", "")

# ---------- 编排参数 ----------
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))

# ---------- 当前选中的 LLM 厂商 ----------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "aliyun")  # aliyun | deepseek
