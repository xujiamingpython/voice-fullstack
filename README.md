# Voice Full-Stack · 语音全栈 AI 助手

> **能听 · 能想 · 能动手 · 能开口** —— ASR + LLM + MCP + TTS 全链路闭环

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

Day-02 课程项目：从纯前端升级到前后端打通的全栈 AI 应用。
用户**说话** → 系统**理解**（ASR）→ LLM **思考并调用工具**（MCP）→ **开口回答**（TTS）。

四大能力：**ASR 语音识别 · 大模型推理 · MCP 工具调用 · TTS 语音合成**

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 原生 HTML / CSS / JS + MediaRecorder + WebSocket |
| 后端 | Python 3.10+ / FastAPI / uvicorn / pydantic v2 |
| LLM | 阿里云百炼 Qwen（主力）· Deepseek（备选） |
| 语音 | 阿里云智能语音 ASR / TTS |
| 工具 | 高德地图 MCP |
| 部署 | Docker / Nginx / 阿里云 ECS |

## 快速开始

### 1. 环境准备

```bash
# 后端
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example ../.env   # 填入你的 API Key
```

### 2. 启动后端

```bash
uvicorn app.main:app --reload --port 8000
# 健康检查: http://localhost:8000/api/health
# API 文档: http://localhost:8000/docs
```

### 3. 启动前端

```bash
cd frontend
python3 -m http.server 8080
# 打开: http://localhost:8080
```

### 一键启动（开发）

```bash
./scripts/dev.sh
```

## 项目结构

```
voice-fullstack/
├── backend/          # FastAPI 后端
│   └── app/
│       ├── api/          # API 层（WebSocket / REST）
│       ├── services/     # 业务编排（LLM Orchestrator）
│       ├── domain/       # 领域模型
│       ├── infrastructure/ # 外部服务客户端（ASR/LLM/MCP/TTS）
│       └── common/       # 日志 / 配置 / 异常
├── frontend/         # 原生前端
│   ├── css/          # 样式
│   └── js/           # 录音 / 播放 / 聊天 / WebSocket
├── docs/             # 项目文档（5 份）
├── scripts/          # 开发 / 部署脚本
└── .github/          # CI/CD
```

## 文档索引

| 文档 | 说明 |
|---|---|
| [docs/01-前置准备清单.md](docs/01-前置准备清单.md) | 平台 / API / 工具 / 部署准备 |
| [docs/02-需求文档.md](docs/02-需求文档.md) | 完整 PRD |
| [docs/03-系统架构.md](docs/03-系统架构.md) | 架构设计 / 数据流 / 协议 |
| [docs/04-页面设计Prompt.md](docs/04-页面设计Prompt.md) | 页面设计提示词 |
| [docs/05-Git代码管理规范.md](docs/05-Git代码管理规范.md) | Git 工作流 |

## 开发路线

- [ ] v0.1 ASR + LLM 文字对话
- [ ] v0.2 MCP 工具调用（地图）
- [ ] v0.3 TTS 语音输出
- [ ] v0.4 会话历史 + 设置面板
- [ ] v1.0 部署上线

## License

[MIT](LICENSE)
