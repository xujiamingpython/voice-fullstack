"""阿里云智能语音 ASR 客户端（骨架：预留流式 WebSocket 实现）。"""
import logging

from app import config

logger = logging.getLogger(__name__)


class ASRClient:
    def __init__(self):
        self.app_key = config.ALIYUN_ASR_APP_KEY
        self.token = config.ALIYUN_ASR_TOKEN
        self.ws_url = config.ALIYUN_ASR_WS_URL

    async def transcribe(self, audio: bytes, fmt: str = "wav") -> str:
        """单次音频识别 → 文本。

        TODO(v0.1):
          1. 若 fmt != wav/pcm，先用 ffmpeg 转 pcm(16k, mono)
          2. 建立 NLS WebSocket 连接（wss://nls-gateway.../ws/v1）
          3. 发送 StartTranscription 请求（appkey + token + 音频参数）
          4. 分片发送音频，接收 SentenceBegin/SentenceEnd 事件
          5. 拼接文本返回
        """
        raise NotImplementedError("ASR 客户端待实现：接入阿里云智能语音 NLS WebSocket")

    async def stream_recognize(self, audio_iter):
        """流式识别（骨架）。"""
        raise NotImplementedError("流式识别待实现")
