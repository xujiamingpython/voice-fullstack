"""腾讯混元最小连通性测试：1) 纯对话（无工具） 2) 带工具定义 3) 工具调用格式验证"""
import asyncio
import json
import sys

sys.path.insert(0, ".")

from app.infrastructure.llm_client import LLMClient, LLMChunk
from app.domain.message import Message, ToolCall


async def main():
    client = LLMClient(provider="tencent")
    print(f"provider={client.provider} model={client.model} base_url={client.base_url}")
    print(f"api_key={'set' if client.api_key else 'EMPTY'}\n")

    # 1) 纯对话
    print("=== 1. 纯对话（无工具） ===")
    try:
        msgs = [{"role": "user", "content": "你好，请用一句话介绍你自己"}]
        text = await client.chat(msgs)
        print("OK:", text[:200])
    except Exception as e:
        print("FAIL:", str(e)[:400])

    # 2) 带工具定义
    print("\n=== 2. 带工具定义（get_weather） ===")
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名"}},
                "required": ["city"],
            },
        },
    }]
    try:
        msgs = [
            {"role": "system", "content": "你是天气助手。需要查天气时调用 get_weather 工具。"},
            {"role": "user", "content": "北京今天天气怎么样？"},
        ]
        chunks = []
        async for ch in client.stream_chat(msgs, tools=tools):
            chunks.append(ch)
        for ch in chunks:
            if ch.tool_calls:
                tc = ch.tool_calls[0]
                print(f"tool_call: name={tc.name} args={tc.arguments!r}")
                # 验证 arguments 是否为合法 JSON
                try:
                    if isinstance(tc.arguments, str):
                        json.loads(tc.arguments)
                        print("  args is valid JSON string ✓")
                    else:
                        json.dumps(tc.arguments)
                        print("  args is dict ✓")
                except Exception as je:
                    print(f"  args INVALID: {je}")
            if ch.delta_text:
                print("text:", ch.delta_text[:100])
    except Exception as e:
        print("FAIL:", str(e)[:500])

    # 3) 带 tool_calls 历史消息（模拟第二轮）
    print("\n=== 3. 历史含 tool_calls 消息（第二轮） ===")
    try:
        history = [
            {"role": "user", "content": "北京今天天气怎么样？"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "id": "call_abc123",
                    "type": "function",
                    "function": {"name": "get_weather", "arguments": json.dumps({"city": "北京"})},
                }],
            },
            {"role": "tool", "tool_call_id": "call_abc123", "content": json.dumps({"weather": "晴", "temp": 29}, ensure_ascii=False)},
        ]
        text = await client.chat(history)
        print("OK:", text[:200])
    except Exception as e:
        print("FAIL:", str(e)[:500])


asyncio.run(main())
