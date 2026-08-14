"""LLM 编排核心：思考 → 调工具 → 再思考 的 LOOP，流式推送事件。"""
import asyncio
import json
import logging
import time
from typing import Callable, Optional

from app import config
from app.infrastructure.llm_client import LLMClient
from app.infrastructure.tools_client import TOOL_LABELS, TOOL_SCHEMAS, amap_tools
from app.infrastructure.tts_client import tts_client
from app.services.conversation import conversation_store

logger = logging.getLogger(__name__)

# 白名单中文名 → 工具名
WHITELIST_TO_TOOL = {v: k for k, v in TOOL_LABELS.items()}


class LLMOrchestrator:
    def __init__(self):
        self.llm = LLMClient()

    def _filter_tools(self, enabled_names: list) -> list:
        """按白名单过滤工具 schema。enabled_names 为中文名列表（来自前端设置）。"""
        if not enabled_names:
            return list(TOOL_SCHEMAS)
        enabled_tools = set()
        for name in enabled_names:
            tool = WHITELIST_TO_TOOL.get(name)
            if tool:
                enabled_tools.add(tool)
        return [s for s in TOOL_SCHEMAS if s["function"]["name"] in enabled_tools]

    async def run(
        self,
        user_input: str,
        session_id: str,
        on_event: Callable[[dict], "asyncio.Future"],
        settings: Optional[dict] = None,
    ) -> str:
        """执行一次完整对话。on_event 为异步回调，推送 WS 事件。"""
        settings = settings or {}
        temperature = float(settings.get("temperature", 0.7))
        max_tokens = int(settings.get("maxTokens", 2048))
        tts_enabled = bool(settings.get("ttsEnabled", True))
        voice_id = settings.get("voiceId", "voicy-female")
        enabled_tools = settings.get("whitelist", [])

        # 会话历史
        history = await conversation_store.history(session_id)
        messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_input[: config.MAX_INPUT_CHARS]})
        await conversation_store.append(session_id, "user", user_input[: config.MAX_INPUT_CHARS])

        # 降级：LLM 未配置
        if not self.llm.available:
            reply = self.llm.mock_reply(user_input)
            await conversation_store.append(session_id, "assistant", reply)
            await on_event({"type": "llm_thinking"})
            await on_event({"type": "llm_chunk", "text": reply})
            if tts_enabled:
                await self._push_tts(reply, voice_id, on_event)
            await on_event({"type": "done"})
            return reply

        tools = self._filter_tools(enabled_tools)
        full_text = ""
        try:
            for _round in range(config.MAX_TOOL_ROUNDS):
                await on_event({"type": "llm_thinking"})
                tool_calls = []
                round_text = ""
                async for chunk in self.llm.stream_chat(messages, tools=tools, temperature=temperature, max_tokens=max_tokens):
                    if chunk.delta_text:
                        round_text += chunk.delta_text
                        full_text += chunk.delta_text
                        await on_event({"type": "llm_chunk", "text": chunk.delta_text})
                    if chunk.tool_calls:
                        tool_calls.extend(chunk.tool_calls)

                if not tool_calls:
                    messages.append({"role": "assistant", "content": round_text})
                    break

                # 有工具调用：记录 assistant(tool_calls) + 执行工具
                messages.append(
                    {
                        "role": "assistant",
                        "content": round_text or None,
                        "tool_calls": [
                            {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": json.dumps(tc.arguments, ensure_ascii=False)}}
                            for tc in tool_calls
                        ],
                    }
                )
                for tc in tool_calls:
                    start = time.time()
                    await on_event(
                        {
                            "type": "tool_calling",
                            "tool": tc.name,
                            "label": TOOL_LABELS.get(tc.name, tc.name),
                            "args": tc.arguments,
                        }
                    )
                    result = await amap_tools.call(tc.name, tc.arguments)
                    elapsed = round(time.time() - start, 1)
                    summary = self._summarize_result(tc.name, result)
                    event = {
                        "type": "tool_result",
                        "tool": tc.name,
                        "summary": summary,
                        "duration": f"{elapsed}s",
                        "count": result.get("count", 0),
                    }
                    if result.get("poiList"):
                        event["poiList"] = result["poiList"]
                        event["center"] = result.get("center", {})
                    await on_event(event)
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result, ensure_ascii=False)[:4000]})

            if not full_text:
                full_text = "抱歉，我没有理解您的问题，请再说一遍。"
            await conversation_store.append(session_id, "assistant", full_text)
            if tts_enabled:
                await self._push_tts(full_text, voice_id, on_event)
            await on_event({"type": "done"})
            return full_text
        except Exception as e:
            logger.exception("[orchestrator] run failed")
            await on_event({"type": "error", "code": "LLM_FAILED", "message": f"服务暂时不可用：{e}"})
            return full_text or ""

    async def _push_tts(self, text: str, voice_id: str, on_event):
        audio = await tts_client.synthesize(text, voice_id)
        if audio:
            import base64

            await on_event({"type": "tts_audio", "data": base64.b64encode(audio).decode(), "format": "mp3"})
            await on_event({"type": "tts_end"})

    def _summarize_result(self, tool: str, result: dict) -> str:
        if result.get("poiList"):
            n = len(result["poiList"])
            first = result["poiList"][0]
            return f"找到 {n} 个结果，最近的「{first.get('name', '')}」约 {first.get('distance', 0)} 米"
        if result.get("weather"):
            return f"{result.get('city')}当前{result.get('weather')}，{result.get('temperature')}℃，{result.get('winddirection')}风{result.get('windpower')}"
        if result.get("distance"):
            return f"全程约 {result['distance'] / 1000:.1f} 公里，预计 {int(result['duration'] / 60)} 分钟"
        if result.get("districts"):
            names = "、".join(d["name"] for d in result["districts"][:3])
            return f"查询到：{names}"
        return str(result)[:120]


orchestrator = LLMOrchestrator()
