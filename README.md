# Voice Full-Stack · 语音全栈 AI 助手（微信小程序版）

> **能听 · 能想 · 能动手 · 能开口** —— ASR + LLM + 地图工具 + TTS 全链路闭环
> 前端形态：**原生微信小程序**（游客模式，无登录）

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)
[![WeChat MiniProgram](https://img.shields.io/badge/WeChat-MiniProgram-07C160)](https://developers.weixin.qq.com/miniprogram/dev/framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

全栈 AI 语音助手：用户**按住说话** → 系统**理解**（ASR）→ LLM **思考并调用工具**（地图/天气/路线）→ **开口回答**（TTS）。

四大能力：**ASR 语音识别 · 大模型推理 · 地图工具调用 · TTS 语音合成**

核心设计：
- **游客模式**：首次启动自动生成 UUID 作为 `session_id`，无需登录即可体验完整流程
- **流式对话**：WebSocket 推送 `思考中 → 调工具 → 工具结果 → 逐字回答 → 语音` 事件流
- **Mock 降级**：未配置任何 API Key 时，ASR/TTS/LLM/地图工具全部返回模拟数据，演示流程可跑通
- **深浅主题**：CSS 变量实现深色/浅色/跟随系统三态

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 原生微信小程序（WXML / WXSS / JS）+ RecorderManager + InnerAudioContext + WebSocket + map 组件 |
| 后端 | Python 3.10+ / FastAPI / uvicorn / pydantic v2 / SQLite |
| LLM | 阿里云百炼 Qwen（主力，OpenAI 兼容协议）· Deepseek（备选） |
| 语音 | 阿里云智能语音（dashscope：paraformer 识别 + sambert 合成） |
| 工具 | 高德地图 Web 服务 REST（地理编码 / 周边搜索 / 路径规划 / 天气 / 行政区划） |
| 部署 | Docker / Nginx / 阿里云 ECS + 微信提审发布 |

## 快速开始

### 1. 环境准备

```bash
# 后端
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 配置环境变量（填入你的 API Key；不填也能以 Mock 模式跑通演示）
cp .env.example ../.env
```

### 2. 启动后端

```bash
uvicorn app.main:app --reload --port 8000
# 健康检查: http://localhost:8000/api/health
# API 文档: http://localhost:8000/docs
```

### 3. 运行小程序

1. 打开**微信开发者工具** → 导入项目 → 选择 `miniprogram/` 目录
2. 填入你的小程序 AppID（或游客模式用测试号）
3. 详情 → 本地设置 → 勾选「**不校验合法域名**」（开发期）
4. 编译运行即可开始语音对话

> 小程序后端地址在 `miniprogram/utils/config.js` 中配置，开发期指向本机 `http://localhost:8000`。

## API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 + 外部依赖状态 |
| GET | `/api/config` | 模型/音色/能力开关配置 |
| GET | `/api/tools` | 工具列表（设置页白名单） |
| POST | `/api/asr` | 录音文件上传 → 识别文本（multipart） |
| POST | `/api/tts` | 文本 → base64 mp3 语音 |
| POST | `/api/chat` | REST 同步对话（WS 不可用时的降级） |
| WS | `/ws/chat` | 流式对话主通道（事件协议见 docs/03） |
| GET/DELETE | `/api/sessions/{id}` | 会话历史查询 / 删除 |
| POST | `/api/sessions/{id}/clear` | 清空会话历史 |

## 项目结构

```
voice-fullstack/
├── miniprogram/            # 微信小程序（原生）
│   ├── app.js              # 入口（游客 session_id / 主题管理）
│   ├── pages/              # index(对话) / sessions(历史) / settings(设置) / map(全屏地图)
│   ├── components/         # mic-button / message-item / tool-card / map-card
│   ├── services/           # api / ws / storage / recorder / player
│   └── utils/              # config / format
├── backend/                # FastAPI 后端
│   └── app/
│       ├── api/            # 路由：health / config / asr / tts / chat(WS+REST) / sessions
│       ├── services/       # orchestrator（LLM 编排 LOOP）/ conversation（SQLite 存储）
│       ├── domain/         # 领域模型（Message / ToolCall / Session）
│       ├── infrastructure/ # llm / asr / tts / tools（高德）客户端，全部带 Mock 降级
│       └── common/         # 日志
├── docs/                   # 项目文档（5 份，小程序版）
├── scripts/                # 开发 / 测试脚本
└── .github/                # CI/CD
```

## 文档索引

| 文档 | 说明 |
|---|---|
| [docs/01-前置准备清单.md](docs/01-前置准备清单.md) | 平台 / API / 工具 / 部署准备（含小程序注册与备案） |
| [docs/02-需求文档.md](docs/02-需求文档.md) | 完整 PRD（小程序 + 游客模式） |
| [docs/03-系统架构.md](docs/03-系统架构.md) | 架构设计 / 数据流 / WS 事件协议（小程序版） |
| [docs/04-页面设计Prompt.md](docs/04-页面设计Prompt.md) | 页面设计提示词（v3.0，9 块独立可粘贴） |
| [docs/05-Git代码管理规范.md](docs/05-Git代码管理规范.md) | Git 工作流（含小程序提审发布链路） |

## 开发路线

- [x] v0.1 小程序骨架 + ASR + LLM 文字对话
- [x] v0.2 地图工具调用（高德 REST）+ map 组件展示
- [x] v0.3 TTS 语音输出（边说边播）+ Mock 降级体系
- [x] v0.4 会话历史 + 设置页（游客本地存储 + SQLite）
- [ ] v1.0 备案域名上线 + HTTPS + 提审发布

## License

[MIT](LICENSE)
