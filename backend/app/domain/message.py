"""领域模型：消息与工具调用。"""
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ToolCall:
    """LLM 发起的工具调用。"""

    id: str
    name: str
    arguments: dict = field(default_factory=dict)


@dataclass
class Message:
    """对话消息（与 LLM 协议的 role/content 对齐）。"""

    role: str  # system | user | assistant | tool
    content: str = ""
    tool_call_id: Optional[str] = None
    tool_calls: list = field(default_factory=list)  # [ToolCall]

    def to_dict(self) -> dict:
        d = {"role": self.role, "content": self.content}
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            # OpenAI 格式：arguments 必须是 JSON 字符串
            import json
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": json.dumps(tc.arguments, ensure_ascii=False)},
                }
                for tc in self.tool_calls
            ]
            # assistant 消息有 tool_calls 时 content 可以为空
            if not self.content:
                d["content"] = None
        return d
