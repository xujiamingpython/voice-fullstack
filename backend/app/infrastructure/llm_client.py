"""LLM 客户端：OpenAI 兼容协议（阿里云百炼 / Deepseek），支持流式 + Function Calling。"""
import json
import logging
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional

from openai import AsyncOpenAI

from app import config
from app.domain.message import ToolCall

logger = logging.getLogger(__name__)


@dataclass
class LLMChunk:
    """流式返回的一个分片。"""

    delta_text: Optional[str] = None
    tool_calls: list = field(default_factory=list)  # [ToolCall]
    finish_reason: Optional[str] = None


class LLMClient:
    def __init__(self, provider: str = None):
        provider = provider or config.LLM_PROVIDER
        self.provider = provider
        if provider == "deepseek":
            self.api_key = config.DEEPSEEK_API_KEY
            self.base_url = config.DEEPSEEK_BASE_URL
            self.model = config.DEEPSEEK_MODEL
        else:
            self.api_key = config.ALIYUN_BAILIAN_API_KEY
            self.base_url = config.LLM_BASE_URL
            self.model = config.LLM_MODEL
        self._client: Optional[AsyncOpenAI] = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url, timeout=config.REQUEST_TIMEOUT)
        return self._client

    async def stream_chat(
        self,
        messages: list,
        tools: Optional[list] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[LLMChunk]:
        """流式调用，产出文本增量与工具调用。"""
        kwargs = dict(model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens, stream=True)
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        stream = await self._get_client().chat.completions.create(**kwargs)
        pending_calls: dict[int, dict] = {}
        async for part in stream:
            if not part.choices:
                continue
            choice = part.choices[0]
            delta = choice.delta
            chunk = LLMChunk(finish_reason=choice.finish_reason)

            if delta and delta.content:
                chunk.delta_text = delta.content

            if delta and delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in pending_calls:
                        pending_calls[idx] = {"id": tc.id or "", "name": "", "arguments": ""}
                    if tc.id:
                        pending_calls[idx]["id"] = tc.id
                    if tc.function and tc.function.name:
                        pending_calls[idx]["name"] += tc.function.name
                    if tc.function and tc.function.arguments:
                        pending_calls[idx]["arguments"] += tc.function.arguments

            if chunk.delta_text or chunk.finish_reason:
                yield chunk

        # 流结束后收集工具调用
        for idx, pc in pending_calls.items():
            args = {}
            try:
                args = json.loads(pc["arguments"] or "{}")
            except json.JSONDecodeError:
                logger.warning("[llm] tool args parse fail: %s", pc["arguments"])
            yield LLMChunk(
                tool_calls=[ToolCall(id=pc["id"] or f"call_{idx}", name=pc["name"], arguments=args)],
                finish_reason="tool_calls",
            )

    async def chat(self, messages: list, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """一次性同步对话（无流式）。"""
        resp = await self._get_client().chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    def mock_reply(self, user_input: str) -> str:
        """降级模式：无 API Key 时的模拟回复。"""
        text = user_input.lower()
        if "天气" in text or "weather" in text:
            return f"{config.DEFAULT_CITY}今天晴，气温 22~31℃，东南风 2 级，空气质量优，适合出行。（演示模式，未配置 LLM Key）"
        if "咖啡" in text or "附近" in text or "找" in text:
            return "为您找到 5 家咖啡馆，最近的是星巴克，约 320 米。已在地图中标注。（演示模式，未配置 LLM Key）"
        if "怎么走" in text or "导航" in text or "路线" in text:
            return "路线已规划完成，全程约 28 公里，预计 45 分钟。已生成地图卡片。（演示模式，未配置 LLM Key）"
        return f"你好，我是知行。我听到你说：{user_input}。当前为演示模式，配置 LLM API Key 后即可获得智能回答。"
