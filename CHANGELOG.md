# 更新日志

本项目的所有重要变更都会记录在此文件中。
格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### ✨ v0.3.0 前后端全链路打通
- **前端（miniprogram/）**：4 页 + 4 组件 + 6 服务全部实现
  - index 主对话页：语音/文字双模式、录音流程（权限→录音→ASR→发送）、WS 流式渲染、工具/地图卡片、REST 降级
  - sessions 历史页：会话卡片、左滑删除、长按菜单
  - settings 设置页：模型/语音/工具/数据四组，音色试听、主题切换
  - map 全屏地图页：markers + POI 列表 + 导航
  - 组件：mic-button（6 状态 + 音量柱）、message-item（4 类气泡）、tool-card（3 态）、map-card
- **后端（backend/）**：FastAPI 全链路
  - `/ws/chat` WebSocket 流式（事件协议：llm_thinking/tool_calling/tool_result/llm_chunk/tts_audio/done/error）
  - REST：`/api/chat`（降级）、`/api/asr`、`/api/tts`、`/api/config`、`/api/tools`、`/api/sessions/*`
  - LLM 编排 LOOP（思考→调工具→回填→再思考，Function Calling，MAX_TOOL_ROUNDS）
  - 高德 5 工具（地理编码/周边搜索/路径规划/天气/行政区划）+ SQLite 会话存储
  - **Mock 降级体系**：未配置任何 Key 时 ASR/TTS/LLM/工具全部返回模拟数据，演示可跑通
- 依赖：dashscope>=1.9.1（阿里云镜像同步上限，API 兼容）
- CI：backend pytest（2 passed）+ miniprogram JS 语法检查（16 files）

### 🔄 技术栈调整（v0.2.0）
- **前端：Web → 原生微信小程序**（miniprogram/，游客模式无登录）
- 5 份项目文档全面更新为小程序版（docs/）
- 后端收敛为基础骨架（仅 health），业务路由待评审后开发
- CI：frontend-check → miniprogram-check（JS 语法检查）

### 🏗️ 项目脚手架（v0.1.0 初始提交）
- FastAPI 后端骨架
- 微信小程序骨架（app 入口 + 游客 session_id + 页面占位）
- Docker + Nginx 部署配置（API 反代 + WSS）
- GitHub Actions CI
- 5 份项目文档
