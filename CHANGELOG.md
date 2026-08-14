# 更新日志

本项目的所有重要变更都会记录在此文件中。
格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### ✨ 新增（规划中，待文档评审后开发）
- ASR 语音识别（阿里云智能语音，微信 RecorderManager 录音上传）
- LLM 对话（阿里云百炼 Qwen / Deepseek）
- MCP 工具调用（高德地图）+ 小程序 map 组件展示
- TTS 语音输出（InnerAudioContext 边说边播）
- 流式响应（WebSocket）
- 会话历史（游客模式本地存储）
- 设置页

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
