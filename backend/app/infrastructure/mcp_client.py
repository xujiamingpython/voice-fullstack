"""高德地图 MCP 客户端（骨架：预留 SSE 连接实现）。

参考工具（实际以 MCP server 返回为准）：
  - maps_geocode         地址 → 坐标
  - maps_search_around   周边搜索（keyword, location, radius）
  - maps_direction       路径规划
  - maps_weather         天气查询
"""
import json
import logging

from app import config

logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self):
        self.endpoint = config.AMAP_MCP_ENDPOINT
        self.token = config.AMAP_MCP_TOKEN
        self._tools: list | None = None

    async def list_tools(self) -> list:
        """返回 LLM 可用的工具定义（OpenAI function calling 格式）。"""
        if self._tools is None:
            self._tools = await self._fetch_tools()
        return self._tools

    async def call(self, name: str, args: dict) -> dict:
        """调用 MCP 工具。"""
        # TODO(v0.2):
        #   1. 建立 SSE 连接（sse.js: /sse + /messages）
        #   2. initialize 握手（协议版本 + capabilities + client info）
        #   3. tools/call 发送 {name, arguments: args}
        #   4. 读取工具结果返回
        raise NotImplementedError("MCP 客户端待实现：接入高德 MCP SSE 服务")

    async def _fetch_tools(self) -> list:
        """获取工具定义（骨架）。"""
        logger.info("MCP endpoint=%s", self.endpoint)
        return [
            {
                "type": "function",
                "function": {
                    "name": "maps_search_around",
                    "description": "搜索指定位置周边的 POI（如咖啡馆、餐厅）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {"type": "string", "description": "搜索关键词"},
                            "location": {"type": "string", "description": "经纬度，如 116.397428,39.90923"},
                            "radius": {"type": "integer", "description": "搜索半径（米）"},
                        },
                        "required": ["keyword", "location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "maps_geocode",
                    "description": "将地址转换为经纬度坐标",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "maps_direction",
                    "description": "路径规划（驾车 / 步行 / 公交）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {"type": "string", "description": "起点经纬度"},
                            "destination": {"type": "string", "description": "终点经纬度"},
                            "mode": {"type": "string", "enum": ["driving", "walking", "transit"]},
                        },
                        "required": ["origin", "destination"],
                    },
                },
            },
        ]
