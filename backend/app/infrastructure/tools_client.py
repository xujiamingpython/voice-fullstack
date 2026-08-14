"""高德地图工具客户端（Web 服务 REST）。
封装 5 个工具：地理编码 / 周边搜索 / 路径规划 / 天气 / 行政区划。
未配置 AMAP_SERVER_API_KEY 时返回模拟数据（mock=True），保证演示流程可跑通。
"""
import asyncio
import logging
from typing import Optional

import httpx

from app import config

logger = logging.getLogger(__name__)

# ---------- LLM Function Calling 工具定义 ----------
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "maps_geocode",
            "description": "将地址/地名转换为经纬度坐标，返回格式化的完整地址。",
            "parameters": {
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "要查询的地址或地名，如：天安门、北京南站"},
                },
                "required": ["address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "maps_search_around",
            "description": "在指定位置周边搜索 POI（餐饮、咖啡馆、酒店、景点等），返回名称/地址/距离/评分列表。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "搜索关键词，如：咖啡、餐厅、加油站"},
                    "location": {"type": "string", "description": "中心点经纬度 'lng,lat'，省略时用用户当前城市中心"},
                    "radius": {"type": "integer", "description": "搜索半径（米），默认 3000"},
                    "city": {"type": "string", "description": "城市名，如：北京"},
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "maps_direction",
            "description": "规划两个地点之间的驾车路线，返回距离、耗时与步行/驾车步骤。",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "起点（地址或 'lng,lat'）"},
                    "destination": {"type": "string", "description": "终点（地址或 'lng,lat'）"},
                    "mode": {"type": "string", "enum": ["driving", "walking"], "description": "出行方式，默认 driving"},
                },
                "required": ["origin", "destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市实时天气与未来几小时预报。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如：北京、上海、深圳"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "maps_district",
            "description": "查询行政区划信息（省份/城市/区县列表）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {"type": "string", "description": "区划名称关键词，如：北京、朝阳"},
                },
                "required": ["keywords"],
            },
        },
    },
]

# 工具显示名映射（前端卡片）
TOOL_LABELS = {
    "maps_geocode": "地理编码",
    "maps_search_around": "附近搜索",
    "maps_direction": "路径规划",
    "get_weather": "天气",
    "maps_district": "行政区划",
}


class AmapToolsClient:
    def __init__(self):
        self.api_key = config.AMAP_SERVER_API_KEY
        self._http: Optional[httpx.AsyncClient] = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def _get_http(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=config.REQUEST_TIMEOUT)
        return self._http

    async def call(self, name: str, args: dict) -> dict:
        """统一入口：按工具名分派。"""
        handlers = {
            "maps_geocode": self._geocode,
            "maps_search_around": self._search_around,
            "maps_direction": self._direction,
            "get_weather": self._weather,
            "maps_district": self._district,
        }
        handler = handlers.get(name)
        if not handler:
            return {"error": f"unknown tool: {name}", "mock": True}
        try:
            return await handler(args or {})
        except Exception as e:
            logger.error("[amap] %s failed: %s", name, e)
            return {"error": str(e), "mock": not self.available}

    async def _geocode(self, args: dict) -> dict:
        address = args.get("address", "")
        if not self.available:
            return self._mock_geocode(address)
        http = await self._get_http()
        r = await http.get(
            f"{config.AMAP_BASE_URL}/geocode/geo",
            params={"key": self.api_key, "address": address},
        )
        data = r.json()
        if data.get("status") != "1" or not data.get("geocodes"):
            raise RuntimeError(data.get("info", "geocode failed"))
        g = data["geocodes"][0]
        lng, lat = g["location"].split(",")
        return {
            "location": {"longitude": float(lng), "latitude": float(lat)},
            "formatted_address": g.get("formatted_address", address),
            "level": g.get("level", ""),
        }

    async def _search_around(self, args: dict) -> dict:
        keyword = args.get("keyword", "")
        location = args.get("location")
        radius = args.get("radius", 3000)
        city = args.get("city", "")
        if not self.available:
            return self._mock_search(keyword, city)
        http = await self._get_http()
        params = {"key": self.api_key, "keywords": keyword, "radius": radius, "offset": 10, "page": 1}
        if location:
            params["location"] = location
        if city:
            params["city"] = city
        r = await http.get(f"{config.AMAP_BASE_URL}/place/around", params=params)
        data = r.json()
        if data.get("status") != "1":
            raise RuntimeError(data.get("info", "search failed"))
        pois = []
        for p in data.get("pois", [])[:10]:
            try:
                lng, lat = p["location"].split(",")
                pois.append(
                    {
                        "id": p.get("id", ""),
                        "name": p.get("name", ""),
                        "address": p.get("address", "") or p.get("pname", ""),
                        "latitude": float(lat),
                        "longitude": float(lng),
                        "distance": int(float(p.get("distance", 0))),
                        "rating": float(p.get("biz_ext", {}).get("rating", 0) or 0) if p.get("biz_ext") else 0,
                        "type": p.get("type", ""),
                    }
                )
            except (ValueError, KeyError):
                continue
        center = {}
        if pois:
            center = {"latitude": pois[0]["latitude"], "longitude": pois[0]["longitude"]}
        return {"keyword": keyword, "poiList": pois, "center": center, "count": len(pois)}

    async def _direction(self, args: dict) -> dict:
        origin = args.get("origin", "")
        destination = args.get("destination", "")
        mode = args.get("mode", "driving")
        if not self.available:
            return self._mock_direction(origin, destination)
        http = await self._get_http()
        # 地址需先转坐标
        origin_loc = await self._resolve_loc(origin)
        dest_loc = await self._resolve_loc(destination)
        url = f"{config.AMAP_BASE_URL}/direction/driving" if mode == "driving" else f"{config.AMAP_BASE_URL}/direction/walking"
        r = await http.get(
            url,
            params={"key": self.api_key, "origin": origin_loc, "destination": dest_loc, "extensions": "base"},
        )
        data = r.json()
        if data.get("status") != "1" or not data.get("route"):
            raise RuntimeError(data.get("info", "direction failed"))
        path = data["route"]["paths"][0]
        steps = [s.get("instruction", "") for s in path.get("steps", [])[:5]]
        return {
            "distance": int(path.get("distance", 0)),
            "duration": int(path.get("duration", 0)),
            "steps": steps,
            "mode": mode,
        }

    async def _resolve_loc(self, text: str) -> str:
        if "," in text:
            return text.strip()
        g = await self._geocode({"address": text})
        loc = g["location"]
        return f"{loc['longitude']},{loc['latitude']}"

    async def _weather(self, args: dict) -> dict:
        city = args.get("city", config.DEFAULT_CITY)
        if not self.available:
            return self._mock_weather(city)
        http = await self._get_http()
        r = await http.get(
            f"{config.AMAP_BASE_URL}/weather/weatherInfo",
            params={"key": self.api_key, "city": city, "extensions": "base"},
        )
        data = r.json()
        if data.get("status") != "1" or not data.get("lives"):
            raise RuntimeError(data.get("info", "weather failed"))
        w = data["lives"][0]
        return {
            "city": w.get("city", city),
            "weather": w.get("weather", ""),
            "temperature": w.get("temperature", ""),
            "winddirection": w.get("winddirection", ""),
            "windpower": w.get("windpower", ""),
            "humidity": w.get("humidity", ""),
            "reporttime": w.get("reporttime", ""),
        }

    async def _district(self, args: dict) -> dict:
        keywords = args.get("keywords", "")
        if not self.available:
            return {"districts": [{"name": keywords or "北京", "adcode": "110000", "level": "city"}], "mock": True}
        http = await self._get_http()
        r = await http.get(
            f"{config.AMAP_BASE_URL}/config/district",
            params={"key": self.api_key, "keywords": keywords, "subdistrict": 0},
        )
        data = r.json()
        if data.get("status") != "1":
            raise RuntimeError(data.get("info", "district failed"))
        districts = [
            {"name": d.get("name", ""), "adcode": d.get("adcode", ""), "level": d.get("level", "")}
            for d in data.get("districts", [])
        ]
        return {"districts": districts}

    # ---------- 降级 mock ----------
    def _mock_geocode(self, address: str) -> dict:
        return {
            "location": {"longitude": 116.397428, "latitude": 39.90923},
            "formatted_address": address or "北京",
            "level": "poi",
            "mock": True,
        }

    def _mock_search(self, keyword: str, city: str = "") -> dict:
        name = keyword or "咖啡"
        pois = [
            {"id": "1", "name": f"星巴克（{city or '北京'}店）", "address": "建国路88号", "latitude": 39.90923, "longitude": 116.397428, "distance": 320, "rating": 4.6, "type": "餐饮服务;咖啡厅"},
            {"id": "2", "name": "瑞幸咖啡", "address": "朝阳门外大街18号", "latitude": 39.9112, "longitude": 116.4015, "distance": 850, "rating": 4.4, "type": "餐饮服务;咖啡厅"},
            {"id": "3", "name": "Manner Coffee", "address": "三里屯路19号", "latitude": 39.9151, "longitude": 116.4042, "distance": 1200, "rating": 4.5, "type": "餐饮服务;咖啡厅"},
            {"id": "4", "name": "M Stand", "address": "工体北路4号", "latitude": 39.9170, "longitude": 116.4080, "distance": 1800, "rating": 4.3, "type": "餐饮服务;咖啡厅"},
            {"id": "5", "name": "库迪咖啡", "address": "东三环中路39号", "latitude": 39.9205, "longitude": 116.4112, "distance": 2400, "rating": 4.2, "type": "餐饮服务;咖啡厅"},
        ]
        center = {"latitude": 39.90923, "longitude": 116.397428}
        return {"keyword": keyword, "poiList": pois, "center": center, "count": len(pois), "mock": True}

    def _mock_direction(self, origin: str, destination: str) -> dict:
        return {
            "distance": 28000,
            "duration": 2700,
            "steps": [f"从{origin or '起点'}出发", "沿主路直行", f"到达{destination or '终点'}"],
            "mode": "driving",
            "mock": True,
        }

    def _mock_weather(self, city: str) -> dict:
        return {
            "city": city or config.DEFAULT_CITY,
            "weather": "晴",
            "temperature": "26",
            "winddirection": "东南",
            "windpower": "2级",
            "humidity": "40%",
            "reporttime": "2026-08-14 15:00:00",
            "mock": True,
        }


amap_tools = AmapToolsClient()
