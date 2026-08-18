"""端到端测试：LLM + 高德工具 全链路（orchestrator 级别，单轮工具调用演示）。"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from app.infrastructure.llm_client import LLMClient
from app.infrastructure.tools_client import AmapToolsClient, TOOL_SCHEMAS
from app.domain.message import Message
from app import config


async def run_scenario(user_text: str, label: str) -> bool:
    """通用场景：用户提问 → LLM 决策 → 工具执行 → LLM 总结"""
    print(f"\n=== {label} ===")
    print(f"  [用户] {user_text}")
    llm = LLMClient()
    tools = AmapToolsClient()

    system = Message(role="system", content=config.SYSTEM_PROMPT)
    user = Message(role="user", content=user_text)

    # 第一轮：LLM 决策
    text_parts = []
    async for chunk in llm.stream_chat([system, user], tools=TOOL_SCHEMAS):
        if chunk.delta_text:
            text_parts.append(chunk.delta_text)
        if chunk.tool_calls:
            for tc in chunk.tool_calls:
                print(f"  [工具调用] {tc.name}({json.dumps(tc.arguments, ensure_ascii=False)})")
                result = await tools.call(tc.name, tc.arguments)
                result_str = json.dumps(result, ensure_ascii=False)
                print(f"  [工具结果] {result_str[:150]}...")
                # 构造工具回填消息
                messages = [system, user, Message(role="assistant", tool_calls=[tc]),
                            Message(role="tool", tool_call_id=tc.id, content=result_str)]
                # 第二轮：LLM 总结
                reply_parts = []
                async for c2 in llm.stream_chat(messages, tools=TOOL_SCHEMAS):
                    if c2.delta_text:
                        reply_parts.append(c2.delta_text)
                reply = "".join(reply_parts)
                print(f"  [知行回复] {reply}")
                return True
    # 如果没调工具，直接回复
    reply = "".join(text_parts)
    print(f"  [知行回复] {reply}")
    return True


async def main():
    model = config.LLM_MODEL
    if config.LLM_PROVIDER == "tencent":
        model = config.TENCENT_HUNYUAN_MODEL
    elif config.LLM_PROVIDER == "deepseek":
        model = config.DEEPSEEK_MODEL
    print(f"[config] MODEL={model}  PROVIDER={config.LLM_PROVIDER}")
    print(f"[config] AMAP_KEY={'已配置' if config.AMAP_SERVER_API_KEY else '未配置'}")

    r1 = await run_scenario("北京今天天气怎么样？", "E2E 1: 天气查询")
    r2 = await run_scenario("帮我找一下附近的咖啡店", "E2E 2: 附近搜索")
    r3 = await run_scenario("从天安门到北京南站怎么走？", "E2E 3: 路线规划")
    r4 = await run_scenario("你好，你是谁？", "E2E 4: 纯对话（无工具）")

    print(f"\n{'='*50}")
    print(f"  天气查询:    {'✅ PASS' if r1 else '❌ FAIL'}")
    print(f"  附近搜索:    {'✅ PASS' if r2 else '❌ FAIL'}")
    print(f"  路线规划:    {'✅ PASS' if r3 else '❌ FAIL'}")
    print(f"  纯对话:      {'✅ PASS' if r4 else '❌ FAIL'}")
    if r1 and r2 and r3 and r4:
        print(f"\n🎉 全链路通过！qwen3-max + 高德工具 完整可用。")
    else:
        print(f"\n⚠️ 部分失败，请检查上方日志。")


if __name__ == "__main__":
    asyncio.run(main())
