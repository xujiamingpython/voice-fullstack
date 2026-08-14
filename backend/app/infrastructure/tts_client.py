"""阿里云智能语音 TTS 客户端（骨架：预留流式 WebSocket 实现）。"""
import logging

from app import config

logger = logging.getLogger(__name__)


class TTSClient:
    def __init__(self):
        self.app_key = config.ALIYUN_TTS_APP_KEY
        self.token = config.ALIYUN_TTS_TOKEN
        self.ws_url = config.ALIYUN_TTS_WS_URL
        self.voice = config.ALIYUN_TTS_VOICE

    async def synthesize(self, text: str, voice: str = "") -> bytes:
        """文本转语音 → mp3 字节流。

        TODO(v0.3):
          1. 建立 NLS WebSocket 连接
          2. 发送 RunTTS 请求（appkey + token + voice + format=mp3）
          3. 发送文本，接收 AudioBinary 事件累积音频
          4. 收到 SentenceEnd 后结束，返回完整音频
        """
        raise NotImplementedError("TTS 客户端待实现：接入阿里云智能语音 NLS WebSocket")

    async def synthesize_stream(self, text: str):
        """流式合成（骨架：按句返回音频块）。"""
        raise NotImplementedError("流式合成待实现")
