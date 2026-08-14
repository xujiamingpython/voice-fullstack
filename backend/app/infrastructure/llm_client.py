"""LLM 客户端：兼容 OpenAI 协议（百炼 Qwen / Deepseek 通用）。

- 阿里云百炼: base_url=https://dashscope.aliyuncs.com/compatible-mode/v1
- Deepseek:   base_url=https://api.deepseek.com/v1
"""
import logging
from typing import AsyncIterator

from openai import AsyncOpenAI

from app import config

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        if config.LLM_PROVIDER == "deepseek":
            self.client = AsyncOpenAI(api_key=config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
            self.model = config.DEEPSEEK_MODEL
        else:
            self.client = AsyncOpenAI(api_key=config.ALIYUN_BAILIAN_API_KEY, base_url=config.LLM_BASE_URL)
            self.model = config.LLM_MODEL

    async def stream(self, messages: list, tools: list | None = None, system: str = "") -> AsyncIterator[dict]:
        """流式返回 chunk：{"text": str} 或 {"tool_call": {"id","name","args"}}。"""
        payload = [{"role": "system", "content": system}] if system else []
        payload.extend(messages)

        kwargs = {"model": self.model, "messages": payload, "stream": True}
        if tools:
            kwargs["tools"] = tools

        stream = await self.client.chat.completions.create(**kwargs)
        tool_calls: dict[int, dict] = {}

        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta is None:
                continue
            if getattr(delta, "content", None):
                yield {"text": delta.content}
            if getattr(delta, "tool_calls", None):
                for tc in delta.tool_calls:
                    slot = tool_calls.setdefault(tc.index, {"id": "", "name": "", "arguments": ""})
                    if tc.id:
                        slot["id"] = tc.id
                    if tc.function and tc.function.name:
                        slot["name"] += tc.function.name
                    if tc.function and tc.function.arguments:
                        slot["arguments"] += tc.function.arguments

        # 收尾：完整工具调用
        for slot in tool_calls.values():
            if slot["name"]:
                import json
                try:
                    args = json.loads(slot["arguments"] or "{}")
                except json.JSONDecodeError:
                    args = {}
                yield {"tool_call": {"id": slot["id"], "name": slot["name"], "args": args}}
