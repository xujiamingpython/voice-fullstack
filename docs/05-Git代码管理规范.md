# 05 · 语音全栈应用 · Git 代码管理规范

> **目标**：用一套清晰的 Git 流程管理从开发、测试、部署到回滚的完整链路。  
> **适用规模**：个人 / 小团队（1-5 人）  
> **核心原则**：主分支稳定 · 提交原子化 · 流程可追溯

---

## 1. 仓库初始化

### 1.1 在 GitHub 创建仓库

```bash
# 1. 在 GitHub 网页端创建仓库
#    - 名称：voice-fullstack
#    - 描述：Voice Full-Stack AI Assistant · ASR + LLM + MCP + TTS
#    - 可见性：Private（学习项目）/ Public（开源）
#    - 初始化：勾选 Add README + .gitignore(Python) + MIT License

# 2. 本地关联远程仓库
cd /Users/ming/Desktop/娱乐/17-AI项目/Voice_Full_Stack
git init   # 如果 GitHub 初始化过了，这步可跳过
git remote add origin git@github.com:<your-username>/voice-fullstack.git
git branch -M main
```

### 1.2 SSH Key 配置（避免每次输密码）

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 粘贴到 GitHub → Settings → SSH and GPG keys → New SSH key
# 测试
ssh -T git@github.com
```

---

## 2. 仓库目录结构

```
voice-fullstack/
├── .github/                      # GitHub 配置
│   ├── workflows/                # CI/CD
│   │   ├── test.yml
│   │   └── deploy.yml
│   ├── ISSUE_TEMPLATE/           # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/                      # FastAPI 后端
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/                     # 前端
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── docs/                         # 项目文档
│   ├── 01-前置准备清单.md
│   ├── 02-需求文档.md
│   ├── 03-系统架构.md
│   ├── 04-页面设计Prompt.md
│   └── 05-Git代码管理规范.md
├── scripts/                      # 工具脚本
│   ├── dev.sh                    # 本地一键启动
│   ├── deploy.sh                 # 部署脚本
│   └── init_db.sh
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── .env.example
├── .editorconfig
├── .prettierrc
├── .eslintrc.json
├── pyproject.toml
├── README.md
├── CHANGELOG.md
└── LICENSE
```

---

## 3. 分支策略（Git Flow 轻量版）

### 3.1 长期分支

| 分支 | 作用 | 保护 | 命名 |
|---|---|---|---|
| `main` | 生产环境代码，**始终可发布** | 受保护 | `main` |
| `develop` | 集成开发分支 | 受保护 | `develop` |

### 3.2 临时分支

| 类型 | 作用 | 命名规范 | 从哪拉 | 合并到 |
|---|---|---|---|---|
| `feature/*` | 新功能 | `feature/voice-input` | `develop` | `develop` |
| `fix/*` | Bug 修复 | `fix/asr-timeout` | `main` 或 `develop` | 自身 + `develop` |
| `hotfix/*` | 紧急修复生产 | `hotfix/api-down` | `main` | `main` + `develop` |
| `release/*` | 发布准备 | `release/v1.0.0` | `develop` | `main` + `develop` |
| `docs/*` | 文档变更 | `docs/update-prd` | `develop` | `develop` |
| `chore/*` | 杂项（依赖/配置） | `chore/bump-fastapi` | `develop` | `develop` |

### 3.3 实战流程图

```
main ─────●─────────────●─────────────●────► (生产版本)
          ↑             ↑             ↑
          │             │   hotfix/*  │
          │             │             │
develop ──●───●───●─────┼───●───●───●─●────► (开发主线)
                ↑       │       ↑
                │       │       │
            feature/*   │   feature/*
                        │
                    release/*
```

---

## 4. 日常开发流程

### 4.1 开始一个新功能

```bash
# 1. 同步最新 develop
git checkout develop
git pull origin develop

# 2. 拉新分支
git checkout -b feature/voice-input

# 3. 开发（多次提交）
git add .
git commit -m "feat(frontend): add MediaRecorder wrapper"

# 4. 推送到远程
git push -u origin feature/voice-input

# 5. 在 GitHub 创建 PR：feature/voice-input → develop
# 6. 通过 Review 后合并（推荐 Squash Merge）
# 7. 删除远程分支
```

### 4.2 修复 Bug

```bash
# 从 main 拉 hotfix
git checkout main
git pull origin main
git checkout -b hotfix/asr-timeout

# 修复 + 测试
git commit -m "fix(backend): increase asr timeout to 10s"

# 合并到 main（修复线上）
git checkout main
git merge --no-ff hotfix/asr-timeout
git tag -a v0.1.1 -m "hotfix: asr timeout"

# 同步到 develop
git checkout develop
git merge --no-ff hotfix/asr-timeout

# 删除分支
git branch -d hotfix/asr-timeout
```

---

## 5. Commit 规范

### 5.1 Conventional Commits（强推）

格式：`<type>(<scope>): <subject>`

#### type 类型
| type | 含义 | 示例 |
|---|---|---|
| `feat` | 新功能 | `feat(frontend): add voice button` |
| `fix` | 修复 Bug | `fix(asr): handle audio decode error` |
| `docs` | 仅文档 | `docs: update api reference` |
| `style` | 代码格式（无逻辑变更） | `style: format with prettier` |
| `refactor` | 重构（无新功能、无修复） | `refactor: split orchestrator` |
| `perf` | 性能优化 | `perf: cache mcp tool list` |
| `test` | 测试 | `test: add asr unit tests` |
| `chore` | 构建/工具/依赖 | `chore: bump fastapi to 0.110` |
| `revert` | 回退 | `revert: feat(voice) add tts` |

#### scope 范围（可自定义）
- `frontend` / `backend` / `docs` / `ci` / `deps`
- 模块名：`asr` / `tts` / `llm` / `mcp` / `orchestrator` / `ws`

#### subject 主题
- 中文 / 英文均可（团队统一）
- **不超过 50 字**
- 首字母小写，结尾不加句号
- 用动词开头："add" / "fix" / "update"

### 5.2 Commit Message 模板

新建文件 `.gitmessage`：

```bash
# <type>(<scope>): <subject>
# |<---- 50 个字符以内 ---->|

# <body> 详细描述（72 字符换行）

# <footer> 关联 Issue / Breaking Change

# Refs: #123
# Closes: #456
# BREAKING CHANGE: 说明
```

配置 Git 使用：
```bash
git config --global commit.template ~/.gitmessage
```

### 5.3 优秀 Commit 示例

```bash
feat(voice-input): add long-press to start recording

- Implement MediaRecorder wrapper
- Add 200ms threshold to avoid accidental trigger
- Show real-time audio waveform
- Add error handling for permission denied

Closes: #12

fix(orchestrator): prevent infinite tool call loop

Add max iteration limit (5 rounds) to LLM orchestrator to
prevent runaway agents in case of tool failures.

Refs: #34
```

### 5.4 ❌ 反面示例

```bash
# ❌ 不要这样
git commit -m "fix"
git commit -m "update"
git commit -m "代码改动"
git commit -m "WIP"

# ✅ 应该这样
git commit -m "fix(asr): handle empty audio input"
git commit -m "feat(chat): add message copy button"
```

---

## 6. .gitignore 配置

完整 `.gitignore`（Python + Node + 项目特定）：

```gitignore
# ============ Python ============
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/
ENV/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# ============ Node ============
node_modules/
dist/
build/
.parcel-cache/
.vite/
.npm/
.eslintcache

# ============ 环境变量 / 密钥 ============
.env
.env.local
.env.*.local
*.pem
secrets/
config/local.json

# ============ 媒体 / 上传 ============
*.mp3
*.wav
*.pcm
*.opus
*.webm
uploads/
recordings/

# ============ IDE ============
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# ============ 系统 ============
*.log
logs/
*.pid
*.seed
*.pid.lock

# ============ 数据库 / 缓存 ============
*.db
*.sqlite
*.sqlite3
redis_data/

# ============ 部署 ============
docker-compose.override.yml
.deploy/

# ============ 临时文件 ============
tmp/
temp/
*.tmp
*.bak
```

---

## 7. Tag 与版本管理

### 7.1 语义化版本（SemVer）

```
v<MAJOR>.<MINOR>.<PATCH>
     ↑       ↑       ↑
   不兼容   新功能   Bug 修复
```

- v0.1.0 → v0.2.0：新增 ASR（minor）
- v0.2.0 → v0.2.1：修复 ASR Bug（patch）
- v0.2.1 → v1.0.0：首个生产版本（major）

### 7.2 打 Tag 流程

```bash
# 创建带注释的 Tag
git tag -a v1.0.0 -m "Release v1.0.0: 完整语音助手"

# 推送 Tag
git push origin v1.0.0

# 推送所有 Tag
git push origin --tags

# 列出所有 Tag
git tag -l

# 删除 Tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### 7.3 在 GitHub 创建 Release

```
GitHub → Releases → Draft a new release
- Choose tag: v1.0.0
- Release title: "v1.0.0 · 完整语音助手首发"
- Description: 复制 CHANGELOG.md 内容
- 勾选 "Set as the latest release"
- 附加编译产物（如 dist.zip）
```

---

## 8. CHANGELOG 维护

`CHANGELOG.md` 模板：

```markdown
# 更新日志

## [Unreleased]

## [1.0.0] - 2026-08-20

### ✨ 新增
- 语音输入（ASR）支持
- LLM 对话（百炼 + Deepseek）
- 高德 MCP 工具调用（地图 / 天气）
- 语音输出（TTS）
- 流式响应
- 会话历史持久化

### 🐛 修复
- 修复 ASR 超时未处理 (#34)
- 修复移动端键盘弹起遮挡 (#28)

### 🔧 优化
- 优化首字延迟从 2.1s → 1.3s

### 📝 文档
- 完成 5 份核心文档

### ⚠️ 破坏性变更
- WebSocket 协议 v2（不兼容 v1）

[Unreleased]: https://github.com/xxx/voice-fullstack/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/xxx/voice-fullstack/releases/tag/v1.0.0
```

---

## 9. Pull Request 规范

### 9.1 PR 标题

```
[模块名] 简短描述

示例：
[backend] 接入阿里云 ASR SDK
[frontend] 实现录音可视化
[docs] 更新架构文档
[fix] 修复 TTS 音频播放卡顿
```

### 9.2 PR 描述模板（`.github/PULL_REQUEST_TEMPLATE.md`）

```markdown
## 变更类型
- [ ] ✨ 新功能 (feat)
- [ ] 🐛 Bug 修复 (fix)
- [ ] 📝 文档 (docs)
- [ ] 🎨 样式 (style)
- [ ] ♻️ 重构 (refactor)
- [ ] ⚡ 性能 (perf)
- [ ] ✅ 测试 (test)
- [ ] 🔧 工具 (chore)

## 变更描述
<!-- 详细描述本次改动的目的、思路、影响范围 -->

## 截图 / 录屏
<!-- UI 改动必填 -->

## 测试
- [ ] 已通过本地测试
- [ ] 已补充单测
- [ ] 已手动验证

## Checklist
- [ ] 代码已格式化（black / prettier）
- [ ] 通过 lint
- [ ] 文档已更新（如需要）
- [ ] Commit 符合规范

## 关联 Issue
Closes #xxx
Refs #yyy
```

### 9.3 Code Review 要点

- ✅ 命名清晰、注释到位
- ✅ 函数 / 类单一职责
- ✅ 无明显性能问题
- ✅ 错误处理完善
- ✅ 单元测试覆盖
- ✅ 无 API Key / 密钥泄漏
- ✅ 文档同步更新

---

## 10. 协作与权限

### 10.1 仓库权限（GitHub）

| 角色 | 权限 | 适用 |
|---|---|---|
| Owner | 全部 | 仓库创建者 |
| Maintainer | 合并 PR、管理 Issue | 核心开发者 |
| Developer | Push 分支、提 PR | 一般开发者 |
| Contributor | Fork + 提 PR | 外部贡献者 |

### 10.2 分支保护规则（GitHub Settings → Branches）

对 `main` 和 `develop` 设置：
- ✅ Require pull request reviews before merging（≥ 1 人）
- ✅ Require status checks to pass before merging（CI 通过）
- ✅ Require conversation resolution before merging
- ✅ Include administrators（管理员也遵守）
- ❌ Allow force pushes（禁止）
- ❌ Allow deletions（禁止）

---

## 11. 紧急修复流程（Hotfix）

线上故障时，**5 分钟内**启动：

```bash
# 1. 从 main 拉 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/prod-down

# 2. 修复（最小改动）
# ... 改代码 ...
git add .
git commit -m "fix: rollback tts due to upstream issue"

# 3. 合并到 main
git checkout main
git merge --no-ff hotfix/prod-down
git tag -a v0.1.1 -m "hotfix"

# 4. 同步到 develop
git checkout develop
git merge --no-ff hotfix/prod-down

# 5. 立即部署
./scripts/deploy.sh production

# 6. 删除分支
git branch -d hotfix/prod-down
git push origin --delete hotfix/prod-down
```

---

## 12. 发布部署流程

### 12.1 完整发布 Checklist

```bash
# 1. 准备发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. 测试 + Bug 修复
./scripts/test.sh
# ... 修 bug ...

# 3. 同步文档
# - 更新 CHANGELOG.md
# - 更新 README.md 版本号
# - 提交
git add CHANGELOG.md README.md
git commit -m "docs: bump version to v1.0.0"

# 4. 合并到 main
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"

# 5. 合并回 develop
git checkout develop
git merge --no-ff release/v1.0.0

# 6. 推送
git push origin main develop --tags

# 7. GitHub 端：创建 Release、附上 changelog

# 8. 部署
ssh user@server "cd /opt/voice-fullstack && git pull && ./scripts/deploy.sh"

# 9. 冒烟测试
curl https://yourdomain.com/api/health

# 10. 删除发布分支
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### 12.2 一键发布脚本（`scripts/release.sh`）

```bash
#!/usr/bin/env bash
set -euo pipefail

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./scripts/release.sh v1.0.0"
  exit 1
fi

echo "🚀 Releasing $VERSION ..."
git checkout develop
git pull origin develop
git checkout -b release/$VERSION
./scripts/test.sh

git checkout main
git merge --no-ff release/$VERSION
git tag -a $VERSION -m "Release $VERSION"
git checkout develop
git merge --no-ff release/$VERSION

git push origin main develop --tags
git push origin --delete release/$VERSION || true

echo "✅ Released $VERSION"
```

---

## 13. CI/CD（GitHub Actions）

### 13.1 自动化测试（`.github/workflows/test.yml`）

```yaml
name: Test

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx
      - run: |
          cd backend
          pytest tests/ -v

  frontend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: |
          cd frontend
          npm install
          npm run lint
```

### 13.2 自动化部署（`.github/workflows/deploy.yml`）

```yaml
name: Deploy

on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/voice-fullstack
            git pull
            git checkout ${{ github.ref_name }}
            ./scripts/deploy.sh
            curl -f https://yourdomain.com/api/health || exit 1
```

---

## 14. 常用 Git 命令速查

```bash
# 撤销
git checkout -- <file>              # 撤销工作区修改
git reset HEAD <file>               # 撤销暂存
git reset --soft HEAD~1             # 撤销最近 commit（保留改动）
git reset --hard HEAD~1             # 撤销最近 commit（丢弃改动）⚠️
git revert <commit>                 # 创建一个新的 revert commit

# 查日志
git log --oneline --graph -20       # 图形化日志
git log --author="ming"             # 按作者
git log --grep="fix"                # 按关键字

# 暂存
git stash                           # 暂存当前修改
git stash pop                       # 恢复
git stash list                      # 列出

# 改写历史
git commit --amend                  # 修改最后一次 commit
git rebase -i HEAD~3                # 交互式 rebase（合并 / 重排 commit）

# 远程
git fetch --all --prune             # 同步远程 + 删除已不存在的远程分支
git remote -v                       # 查看远程地址
git remote set-url origin <url>     # 修改远程地址
```

---

## 15. 仓库初始 Checklist

- [ ] GitHub 仓库已创建
- [ ] SSH Key 已配置
- [ ] `.gitignore` 已就位
- [ ] `README.md` 写好（含 Logo / 简介 / 启动步骤）
- [ ] `LICENSE` 已选（推荐 MIT）
- [ ] 分支保护规则已设置（main / develop）
- [ ] PR / Issue 模板已添加
- [ ] CI workflow 已配置
- [ ] 第一次 commit + push 验证通过

---

> 🎉 完成！至此，从 **0 准备 → 需求 → 架构 → 设计 → Git 管理** 的全流程文档已就绪。
> 下一步：用 GitHub 仓库开始你的第一个 commit 🚀
