"""TTS 客户端：阿里云智能语音（dashscope SpeechSynthesizer）。
输出：mp3 音频 bytes。未配置 Key 时返回 None（前端降级为纯文字）。
"""
import asyncio
import logging

from app import config

logger = logging.getLogger(__name__)


class TTSClient:
    def __init__(self):
        self.api_key = config.ALIYUN_BAILIAN_API_KEY or config.ALIYUN_TTS_TOKEN

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def synthesize(self, text: str, voice_id: str = "voicy-female") -> bytes | None:
        if not text:
            return None
        if not self.available:
            logger.warning("[tts] no API key, skip synthesis")
            return None
        try:
            return await asyncio.to_thread(self._call_dashscope, text, voice_id)
        except Exception as e:
            logger.error("[tts] synthesize failed: %s", e)
            return None

    def _call_dashscope(self, text: str, voice_id: str) -> bytes:
        import dashscope
        from dashscope.audio.tts import SpeechSynthesizer

        dashscope.api_key = self.api_key
        model, voice = config.TTS_VOICE_MAP.get(voice_id, (config.ALIYUN_TTS_MODEL, config.ALIYUN_TTS_VOICE))
        result = SpeechSynthesizer.call(
            model=model,
            text=text[:500],  # 单次上限保护
            voice=voice,
            format="mp3",
            sample_rate=16000,
        )
        if result and result.get_audio_data():
            return result.get_audio_data()
        raise RuntimeError("empty audio")


tts_client = TTSClient()
