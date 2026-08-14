# Voice Full-Stack · 语音全栈 AI 助手（微信小程序版）

> **能听 · 能想 · 能动手 · 能开口** —— ASR + LLM + MCP + TTS 全链路闭环
> 前端形态：**原生微信小程序**（游客模式，无登录）

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)
[![WeChat MiniProgram](https://img.shields.io/badge/WeChat-MiniProgram-07C160)](https://developers.weixin.qq.com/miniprogram/dev/framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

Day-02 课程项目：从纯前端升级到前后端打通的全栈 AI 应用，前端运行在**微信小程序**内。
用户**按住说话** → 系统**理解**（ASR）→ LLM **思考并调用工具**（MCP）→ **开口回答**（TTS）。

四大能力：**ASR 语音识别 · 大模型推理 · MCP 工具调用 · TTS 语音合成**

> 📌 **当前状态**：需求文档与 UI 设计**评审中**（docs/ 已更新为小程序版），业务代码待确认后开发。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 原生微信小程序（WXML / WXSS / JS）+ RecorderManager + InnerAudioContext + WebSocket |
| 后端 | Python 3.10+ / FastAPI / uvicorn / pydantic v2 |
| LLM | 阿里云百炼 Qwen（主力）· Deepseek（备选） |
| 语音 | 阿里云智能语音 ASR / TTS |
| 工具 | 高德地图 MCP + 小程序 map 组件 |
| 部署 | Docker / Nginx / 阿里云 ECS + 微信提审发布 |

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

### 3. 运行小程序

1. 打开**微信开发者工具** → 导入项目 → 选择 `miniprogram/` 目录
2. 填入你的小程序 AppID（或游客模式用测试号）
3. 详情 → 本地设置 → 勾选「**不校验合法域名**」（开发期）
4. 编译运行即可看到骨架页面

### 一键启动（开发）

```bash
./scripts/dev.sh   # 仅启动后端；小程序侧用微信开发者工具
```

## 项目结构

```
voice-fullstack/
├── miniprogram/      # 微信小程序（原生）
│   ├── app.js        # 入口（游客 session_id 初始化）
│   ├── pages/        # index(主聊天) / settings(设置)
│   ├── components/   # 自定义组件（待开发）
│   ├── services/     # API / WS / 录音 / 播放 封装（待开发）
│   └── utils/        # 工具
├── backend/          # FastAPI 后端（当前为基础骨架）
│   └── app/
│       ├── api/          # API 层（当前仅 health）
│       ├── services/     # 业务编排（待开发）
│       ├── domain/       # 领域模型
│       ├── infrastructure/ # 外部客户端（待开发）
│       └── common/       # 日志 / 配置
├── docs/             # 项目文档（5 份，小程序版）
├── scripts/          # 开发 / 测试脚本
└── .github/          # CI/CD
```

## 文档索引

| 文档 | 说明 |
|---|---|
| [docs/01-前置准备清单.md](docs/01-前置准备清单.md) | 平台 / API / 工具 / 部署准备（含小程序注册与备案） |
| [docs/02-需求文档.md](docs/02-需求文档.md) | 完整 PRD（小程序 + 游客模式） |
| [docs/03-系统架构.md](docs/03-系统架构.md) | 架构设计 / 数据流 / 协议（小程序版） |
| [docs/04-页面设计Prompt.md](docs/04-页面设计Prompt.md) | 页面设计提示词（750rpx 设计稿） |
| [docs/05-Git代码管理规范.md](docs/05-Git代码管理规范.md) | Git 工作流（含小程序提审发布链路） |

## 开发路线

- [ ] v0.1 小程序骨架 + ASR + LLM 文字对话
- [ ] v0.2 MCP 工具调用（地图）+ map 组件展示
- [ ] v0.3 TTS 语音输出（边说边播）
- [ ] v0.4 会话历史 + 设置页（游客本地存储）
- [ ] v1.0 备案域名上线 + 提审发布

## License

[MIT](LICENSE)
