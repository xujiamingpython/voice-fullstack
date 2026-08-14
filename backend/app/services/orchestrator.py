"""LLM 编排核心：思考 → 调工具 → 看结果 → 再思考 的循环。

LLM LOOP:
  user text → [llm_thinking] → 流式输出 / tool_call
  → [tool_calling] → MCP 调用 → [tool_result] 回填 → 再次推理
"""
import asyncio
import json
import logging

from app import config
from app.infrastructure.asr_client import ASRClient
from app.infrastructure.llm_client import LLMClient
from app.infrastructure.mcp_client import MCPClient
from app.infrastructure.tts_client import TTSClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一个语音 AI 助手，名叫「灵语」。
你可以通过工具获取实时信息（地图、天气等）。
回答要简洁自然，适合语音播报，控制在 2-3 句话。
若工具调用失败，如实告知用户，不要编造结果。"""


class LLMOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.mcp = MCPClient()
        self.asr = ASRClient()
        self.tts = TTSClient()
        self._interrupted = asyncio.Event()

    def interrupt(self):
        self._interrupted.set()

    async def asr_transcribe(self, audio: bytes, fmt: str) -> str:
        return await self.asr.transcribe(audio, fmt=fmt)

    async def run(self, user_input: str, messages: list, on_event):
        """执行一次完整对话循环。"""
        self._interrupted.clear()
        messages.append({"role": "user", "content": user_input})

        for _round in range(config.MAX_TOOL_ROUNDS):
            if self._interrupted.is_set():
                break

            await on_event({"type": "llm_thinking"})
            reply_text = ""
            tool_calls = []

            # 流式获取 LLM 输出（含可能的工具调用）
            async for chunk in self.llm.stream(
                messages,
                tools=await self.mcp.list_tools(),
                system=SYSTEM_PROMPT,
            ):
                if chunk.get("text"):
                    reply_text += chunk["text"]
                    await on_event({"type": "llm_chunk", "text": chunk["text"]})
                if chunk.get("tool_call"):
                    tool_calls.append(chunk["tool_call"])

            if not tool_calls:
                messages.append({"role": "assistant", "content": reply_text})
                # 边生成边合成 TTS（分句）
                await self._speak(reply_text, on_event)
                await on_event({"type": "done"})
                return reply_text

            # 有工具调用 → 执行 → 回填 → 下一轮
            messages.append({"role": "assistant", "content": reply_text, "tool_calls": tool_calls})
            for tc in tool_calls:
                await on_event({"type": "tool_calling", "tool": tc["name"], "args": tc["args"]})
                try:
                    result = await self.mcp.call(tc["name"], tc["args"])
                    summary = json.dumps(result, ensure_ascii=False)[:500]
                except Exception as e:
                    result, summary = {"error": str(e)}, f"工具调用失败: {e}"
                await on_event({"type": "tool_result", "tool": tc["name"], "summary": summary})
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": json.dumps(result, ensure_ascii=False)})

        # 达到最大轮数兜底
        await on_event({"type": "done"})
        return reply_text if "reply_text" in dir() else ""

    async def _speak(self, text: str, on_event):
        """分句 → TTS → 推送音频（骨架：先整句合成）。"""
        if not text.strip():
            return
        try:
            await on_event({"type": "tts_start", "text": text[:100]})
            audio = await self.tts.synthesize(text)
            import base64
            await on_event({"type": "tts_audio", "data": base64.b64encode(audio).decode(), "format": "mp3"})
            await on_event({"type": "tts_end"})
        except Exception as e:
            logger.warning("TTS skipped: %s", e)
