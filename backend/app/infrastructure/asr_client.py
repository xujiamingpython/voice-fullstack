"""ASR 客户端：阿里云智能语音（dashscope Recognition，一句话识别）。
输入：本地音频文件（mp3/aac/wav）→ 输出：中文文本。
未配置 Key 时降级为模拟识别（mock=True）。
"""
import asyncio
import logging

from app import config

logger = logging.getLogger(__name__)


class ASRClient:
    def __init__(self):
        self.api_key = config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_ASR_TOKEN
        self.model = config.ALIYUN_ASR_MODEL

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def transcribe(self, audio_path: str) -> dict:
        """识别音频文件，返回 {text, mock}。"""
        if not self.available:
            logger.warning("[asr] no API key, using mock transcription")
            return {"text": self._mock(audio_path), "mock": True}

        try:
            text = await asyncio.to_thread(self._call_dashscope, audio_path)
            if text:
                return {"text": text, "mock": False}
            raise RuntimeError("empty result")
        except Exception as e:
            logger.error("[asr] transcribe failed: %s", e)
            return {"text": self._mock(audio_path), "mock": True, "error": str(e)}

    def _call_dashscope(self, audio_path: str) -> str:
        """dashscope 一句话识别（本地文件自动上传）。"""
        import dashscope
        from dashscope.audio.asr import Recognition

        dashscope.api_key = self.api_key
        result = Recognition.call(
            model=self.model,
            file_urls=[audio_path],
            language_hints=["zh"],
        )
        if result and result.status_code == 200:
            sentences = getattr(result, "sentences", None) or []
            if sentences:
                return "".join(s.get("text", "") for s in sentences if s.get("text"))
            output = getattr(result, "output", None)
            if isinstance(output, dict):
                return output.get("text", "")
        raise RuntimeError(f"dashscope asr failed: {getattr(result, 'message', '')}")

    def _mock(self, audio_path: str) -> str:
        # 演示模式固定返回一个示例问题（真实实现需配置 ASR Key）
        return "今天北京天气怎么样？"


asr_client = ASRClient()
