"""应用配置：从 .env / 环境变量加载。"""
import os

from dotenv import load_dotenv

load_dotenv()

# ---------- 服务 ----------
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "1") == "1"
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "data", "voice.db"))

# ---------- LLM（阿里云百炼 / Deepseek，OpenAI 兼容协议） ----------
ALIYUN_BAILIAN_API_KEY = os.getenv("ALIYUN_BAILIAN_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# ---------- ASR / TTS（dashscope SDK，兼容百炼 Key） ----------
# 统一使用 ALIYUN_BAILIAN_API_KEY；如需独立语音服务 token 可分别配置以下两项
ALIYUN_ASR_TOKEN = os.getenv("ALIYUN_ASR_TOKEN", "")
ALIYUN_TTS_TOKEN = os.getenv("ALIYUN_TTS_TOKEN", "")
ALIYUN_ASR_MODEL = os.getenv("ALIYUN_ASR_MODEL", "paraformer-realtime-v2")
ALIYUN_TTS_MODEL = os.getenv("ALIYUN_TTS_MODEL", "sambert-zhichu-v1")
ALIYUN_TTS_VOICE = os.getenv("ALIYUN_TTS_VOICE", "ailiao")  # 默认音色
TTS_VOICE_MAP = {  # 前端音色 → 模型/音色
    "voicy-female": ("sambert-zhichu-v1", "zhichu"),
    "voicy-male": ("sambert-zhida-v1", "zhida"),
    "voicy-child": ("sambert-zhihui-v1", "zhihui"),
    "voicy-cantonese": ("sambert-huihui-v1", "huihui"),
}

# ---------- 高德地图（Web 服务 REST，服务端检索） ----------
AMAP_SERVER_API_KEY = os.getenv("AMAP_SERVER_API_KEY", "")
AMAP_BASE_URL = "https://restapi.amap.com/v3"

# ---------- 腾讯位置服务（小程序 map 组件，可选） ----------
TENCENT_LBS_KEY = os.getenv("TENCENT_LBS_KEY", "")

# ---------- 编排参数 ----------
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "2000"))
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "北京")

# ---------- 当前选中的 LLM 厂商 ----------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "aliyun")  # aliyun | deepseek

# ---------- 系统提示词 ----------
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "你是「知行」，一款微信小程序中的 AI 语音导航助手。"
    "你的能力：听懂用户的语音提问，需要查天气、找地点、规划路线时调用对应工具，然后用简洁、口语化的中文回答。"
    "规则：1) 回答控制在 3 句话以内，适合语音播放；2) 涉及地点/路线时优先调用地图工具并给出关键信息；"
    "3) 工具返回的 POI 要挑选最相关的 1-3 个告诉用户；4) 不要编造工具未返回的数据。",
)
