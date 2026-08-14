#!/usr/bin/env bash
# 本地一键启动：后端 + 前端
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# 检查 .env
if [ ! -f .env ]; then
  echo "⚠️ 未找到 .env，正在从 .env.example 复制…"
  cp .env.example .env
  echo "请编辑 .env 填入你的 API Key 后重新运行"
  exit 1
fi

echo "🚀 启动后端 (FastAPI)…"
(cd backend && source .venv/bin/activate 2>/dev/null && uvicorn app.main:app --reload --port 8000) &
BACKEND_PID=$!

echo "🚀 启动前端 (静态服务器)…"
(cd frontend && python3 -m http.server 8080) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

echo ""
echo "✅ 后端:  http://localhost:8000/api/health"
echo "✅ 前端:  http://localhost:8080"
echo "按 Ctrl+C 停止"

wait
