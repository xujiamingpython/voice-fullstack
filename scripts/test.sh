#!/usr/bin/env bash
# 运行后端测试
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"

if [ -d .venv ]; then
  source .venv/bin/activate
fi

pip install -q -r requirements.txt pytest pytest-asyncio httpx
python3 -m pytest tests/ -v "$@"
