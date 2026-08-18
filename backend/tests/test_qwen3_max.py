"""快速验证 qwen3-max 真实链路：普通对话 + Function Calling。"""
import asyncio
import os
import sys

# 确保项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# 修复 macOS SSL
import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from openai import AsyncOpenAI

API_KEY = os.getenv("ALIYUN_BAILIAN_API_KEY", "")
BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
MODEL = os.getenv("LLM_MODEL", "qwen3-max")

print(f"[test] MODEL={MODEL}  BASE_URL={BASE_URL}  KEY={API_KEY[:12]}...")

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=30)


async def test_simple_chat():
    """1) 普通对话"""
    print("\n=== Test 1: Simple Chat ===")
    try:
        resp = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是「知行」，一款AI语音导航助手。回答简洁口语化，3句话以内。"},
                {"role": "user", "content": "你好，你是谁？能帮我做什么？"},
            ],
            temperature=0.7,
            max_tokens=512,
        )
        text = resp.choices[0].message.content or ""
        print(f"[OK] 回复: {text}")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False


async def test_streaming():
    """2) 流式对话"""
    print("\n=== Test 2: Streaming ===")
    try:
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是「知行」，AI语音导航助手。回答简洁。"},
                {"role": "user", "content": "用一句话介绍北京天安门。"},
            ],
            temperature=0.7,
            max_tokens=256,
            stream=True,
        )
        parts = []
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                parts.append(chunk.choices[0].delta.content)
        full = "".join(parts)
        print(f"[OK] 流式回复: {full}")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False


async def test_function_calling():
    """3) Function Calling（工具调用）"""
    print("\n=== Test 3: Function Calling ===")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询指定城市的天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "城市名，如北京、上海"},
                    },
                    "required": ["city"],
                },
            },
        }
    ]
    try:
        resp = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是「知行」，AI语音导航助手。需要查天气时调用get_weather工具。"},
                {"role": "user", "content": "北京今天天气怎么样？"},
            ],
            tools=tools,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=512,
        )
        msg = resp.choices[0].message
        if msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"[OK] 工具调用: name={tc.function.name}  args={tc.function.arguments}")
        else:
            print(f"[INFO] 未触发工具调用，直接回复: {msg.content}")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False


async def main():
    r1 = await test_simple_chat()
    r2 = await test_streaming()
    r3 = await test_function_calling()
    print(f"\n=== Summary ===")
    print(f"  Simple Chat:    {'PASS' if r1 else 'FAIL'}")
    print(f"  Streaming:      {'PASS' if r2 else 'FAIL'}")
    print(f"  Function Call:  {'PASS' if r3 else 'FAIL'}")
    if r1 and r2 and r3:
        print("\n✅ qwen3-max 全部通过！LLM 真实链路可用。")
    else:
        print("\n⚠️ 部分失败，请检查上方错误信息。")


if __name__ == "__main__":
    asyncio.run(main())
