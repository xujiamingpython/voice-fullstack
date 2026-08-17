"""ASR 客户端：阿里云智能语音（dashscope Recognition，实时识别）。
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
        # dashscope 1.9.1 用 paraformer-realtime-v2 做文件识别
        self.model = "paraformer-realtime-v2"

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
        """dashscope 实时识别（本地文件模式）。"""
        import dashscope
        from dashscope.audio.asr import Recognition, RecognitionCallback

        dashscope.api_key = self.api_key

        class _CB(RecognitionCallback):
            pass

        recognition = Recognition(
            model=self.model,
            callback=_CB(),
            format="mp3",
            sample_rate=16000,
        )
        result = recognition.call(file=audio_path)

        if result and getattr(result, "status_code", 0) == 200:
            output = result.get("output") or {}
            sentences = output.get("sentence") or []
            texts = [s.get("text", "") for s in sentences if s.get("text")]
            return "".join(texts)

        raise RuntimeError(
            f"dashscope asr failed: {getattr(result, 'message', '') or getattr(result, 'code', '')}"
        )

    def _mock(self, audio_path: str) -> str:
        return "今天北京天气怎么样？"


asr_client = ASRClient()
