# 05 · 语音全栈应用 · Git 代码管理规范（微信小程序版）

> **目标**：用一套清晰的 Git 流程管理从开发、测试、部署到回滚的完整链路。
> **适用规模**：个人 / 小团队（1-5 人）
> **核心原则**：主分支稳定 · 提交原子化 · 流程可追溯
> **说明**：小程序代码与后端代码在同一仓库管理（monorepo），`miniprogram/` 目录为微信小程序源码。

---

## 1. 仓库初始化

### 1.1 在 GitHub 创建仓库

```bash
# 1. 在 GitHub 网页端创建仓库
#    - 名称：voice-fullstack
#    - 描述：Voice Full-Stack AI Assistant (WeChat Mini Program) · ASR + LLM + MCP + TTS
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
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# 粘贴到 GitHub → Settings → SSH and GPG keys → New SSH key
ssh -T git@github.com
```

---

## 2. 仓库目录结构

```
voice-fullstack/
├── miniprogram/                  # 微信小程序（原生）
│   ├── app.js / app.json / app.wxss
│   ├── project.config.json       # 开发者工具配置（可提交）
│   ├── sitemap.json
│   ├── pages/                    # index / settings / sessions
│   ├── components/               # mic-button / tool-card / map-card / message-item
│   ├── services/                 # api / ws / recorder / player / storage
│   └── utils/
├── backend/                      # FastAPI 后端
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── docs/                         # 5 份项目文档（含本文档）
├── scripts/
│   ├── dev.sh                    # 本地一键启动后端
│   └── test.sh                   # 后端测试
├── .github/workflows/            # test.yml / deploy.yml
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── .env.example
├── README.md
├── CHANGELOG.md
└── LICENSE
```

> ⚠️ **不要提交**：`project.private.config.json`（开发者工具本地私有配置，含个人设置）、`miniprogram_npm/`（若使用 npm 构建产物）。

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
| `feature/*` | 新功能 | `feature/miniprogram-voice-input` | `develop` | `develop` |
| `fix/*` | Bug 修复 | `fix/asr-timeout` | `main` 或 `develop` | 自身 + `develop` |
| `hotfix/*` | 紧急修复生产 | `hotfix/api-down` | `main` | `main` + `develop` |
| `release/*` | 发布准备 | `release/v1.0.0` | `develop` | `main` + `develop` |
| `docs/*` | 文档变更 | `docs/update-prd` | `develop` | `develop` |
| `chore/*` | 杂项（依赖/配置） | `chore/bump-fastapi` | `develop` | `develop` |

### 3.3 scope 建议

- 前端：`miniprogram`（统一用这一个 scope，下面可再细分模块）
- 后端：`backend` 或模块名 `asr` / `tts` / `llm` / `mcp` / `orchestrator` / `ws`
- 其他：`docs` / `ci` / `deps`

---

## 4. Commit 规范（Conventional Commits）

格式：`<type>(<scope>): <subject>`

| type | 含义 | 示例 |
|---|---|---|
| `feat` | 新功能 | `feat(miniprogram): add long-press mic recording` |
| `fix` | 修复 Bug | `fix(asr): handle empty audio input` |
| `docs` | 仅文档 | `docs: update api reference` |
| `style` | 代码格式 | `style(miniprogram): format wxml` |
| `refactor` | 重构 | `refactor: split orchestrator` |
| `perf` | 性能优化 | `perf: cache mcp tool list` |
| `test` | 测试 | `test: add asr unit tests` |
| `chore` | 构建/工具/依赖 | `chore: bump fastapi to 0.110` |
| `revert` | 回退 | `revert: feat(miniprogram) add tts` |

> subject 不超过 50 字，动词开头，结尾不加句号。前端统一 `miniprogram` scope。

### 优秀示例

```bash
feat(miniprogram): add long-press to start recording

- Implement RecorderManager wrapper
- Add 200ms threshold to avoid accidental trigger
- Show real-time audio waveform via canvas
- Add permission denied guidance

Closes: #12

fix(orchestrator): prevent infinite tool call loop

Add max iteration limit (5 rounds) to LLM orchestrator to
prevent runaway agents in case of tool failures.
```

---

## 5. .gitignore 配置（Python + 小程序 + 项目特定）

```gitignore
# ============ Python ============
__pycache__/
*.py[cod]
*.so
venv/
env/
.venv/
*.egg-info/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# ============ Node ============
node_modules/
dist/
build/
.npm/

# ============ 微信小程序 ============
miniprogram/project.private.config.json   # 开发者工具私有配置
miniprogram/miniprogram_npm/              # npm 构建产物
miniprogram/__pycache__/
.DS_Store
# 注：project.config.json（公共配置）建议提交

# ============ 环境变量 / 密钥 ============
.env
.env.local
.env.*.local
*.pem
secrets/

# ============ 媒体 / 上传 ============
*.mp3
*.wav
*.pcm
*.aac
uploads/
recordings/

# ============ IDE ============
.vscode/
.idea/
*.swp
*~
.DS_Store
Thumbs.db

# ============ 系统 / 日志 ============
*.log
logs/
*.pid

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

## 6. Tag 与版本管理（SemVer）

```
v<MAJOR>.<MINOR>.<PATCH>
```

- v0.1.0 → v0.2.0：新增 ASR（minor）
- v0.2.0 → v0.2.1：修复 ASR Bug（patch）
- v0.2.1 → v1.0.0：首个提审发布版本（major）

```bash
git tag -a v1.0.0 -m "Release v1.0.0: 完整语音助手"
git push origin v1.0.0
```

---

## 7. 小程序专属发布流程（重要）

小程序发布与普通 Web 不同，**代码合入 main 后还需微信侧提审**：

### 7.1 小程序发布链路

```
Git develop → feature 分支 → PR 合并 → main
        ↓
1. 微信开发者工具：上传代码（填写版本号 + 备注）
2. 微信公众平台 → 版本管理 → 开发版本 → 提交审核
3. 审核通过 → 发布（全量/灰度）
4. （可选）Git tag v1.0.0 记录发布版本
```

### 7.2 版本与 Git 的对应关系

| 微信侧 | Git 侧 |
|---|---|
| 开发版本（开发工具上传） | develop 最新 |
| 体验版（审核前内测） | release/v1.0.0 |
| 正式版（线上） | main + tag v1.0.0 |

### 7.3 发布 Checklist（小程序）

```bash
# 1. 准备发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. 测试
./scripts/test.sh

# 3. 更新 CHANGELOG.md + README 版本号
git add CHANGELOG.md README.md
git commit -m "docs: bump version to v1.0.0"

# 4. 合并 main + 打 tag
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"

# 5. 合并回 develop + 推送
git checkout develop
git merge --no-ff release/v1.0.0
git push origin main develop --tags

# 6. 微信侧：开发者工具上传 → 提审 → 发布（见 7.1）
```

---

## 8. CI/CD（GitHub Actions）

### 8.1 自动化测试（`.github/workflows/test.yml`）

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

  miniprogram-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: |
          cd miniprogram
          # 小程序 JS 语法检查（不依赖微信开发者工具）
          for f in $(find . -name "*.js" -not -path "./miniprogram_npm/*"); do
            node --check "$f"
          done
```

> 小程序 UI 的完整编译验证需微信开发者工具 CLI（`miniprogram-ci`），可后续按需接入（需上传密钥，注意密钥安全性）。

### 8.2 自动化部署（`.github/workflows/deploy.yml`）

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
      - name: Deploy backend to server
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
            curl -f https://api.yourdomain.com/api/health || exit 1
```

> 后端随 tag 自动部署；小程序代码由微信侧分发，部署到微信服务器（提审发布），后端 API 保持兼容即可。

---

## 9. Pull Request 规范

### 9.1 PR 标题

```
[模块名] 简短描述

[backend] 接入阿里云 ASR SDK
[miniprogram] 实现录音可视化
[docs] 更新架构文档
[fix] 修复 TTS 音频播放卡顿
```

### 9.2 PR 描述模板（`.github/PULL_REQUEST_TEMPLATE.md`）

```markdown
## 变更类型
- [ ] ✨ 新功能 (feat)
- [ ] 🐛 Bug 修复 (fix)
- [ ] 📝 文档 (docs)
- [ ] ♻️ 重构 (refactor)
- [ ] ✅ 测试 (test)
- [ ] 🔧 工具 (chore)

## 变更描述
<!-- 详细描述本次改动的目的、思路、影响范围 -->

## 截图 / 录屏
<!-- UI 改动必填（小程序可用开发者工具截图 / 真机预览截图） -->

## 测试
- [ ] 已通过本地测试（pytest / 微信开发者工具）
- [ ] 已补充单测
- [ ] 已手动验证（iOS + Android 真机）

## Checklist
- [ ] 代码已格式化
- [ ] 通过 lint / 语法检查
- [ ] 文档已更新（如需要）
- [ ] Commit 符合规范
```

### 9.3 Code Review 要点

- ✅ 命名清晰、注释到位
- ✅ 无 API Key / 密钥泄漏（**尤其检查小程序端**）
- ✅ 错误处理完善（录音失败 / 网络断开 / 后端 5xx）
- ✅ 微信兼容性（iOS aac / Android mp3、基础库版本）
- ✅ 单元测试覆盖

---

## 10. 紧急修复流程（Hotfix）

线上小程序故障时：

```bash
# 1. 从 main 拉 hotfix
git checkout main
git pull origin main
git checkout -b hotfix/prod-down

# 2. 最小修复 + 提交
git commit -m "fix: rollback tts due to upstream issue"

# 3. 合并 main + 打 tag
git checkout main
git merge --no-ff hotfix/prod-down
git tag -a v0.1.1 -m "hotfix"

# 4. 同步 develop
git checkout develop
git merge --no-ff hotfix/prod-down

# 5. 后端立即部署
./scripts/deploy.sh production

# 6. 小程序：开发者工具上传修复版 → 加急提审（微信审核不可绕，但可选择"加急"通道）
# 7. 清理分支
```

> ⚠️ 小程序 hotfix 受**微信审核周期**约束（常规 1-2 天，可申请加急），后端可即时修复，前端修复需预留审核时间——**关键逻辑尽量放后端**。

---

## 11. 仓库初始 Checklist

- [ ] GitHub 仓库已创建
- [ ] SSH Key 已配置
- [ ] `.gitignore` 已就位（含小程序配置）
- [ ] `README.md` 写好（含本地启动 + 微信开发者工具导入步骤）
- [ ] `LICENSE` 已选（推荐 MIT）
- [ ] 分支保护规则已设置（main / develop）
- [ ] PR / Issue 模板已添加
- [ ] CI workflow 已配置
- [ ] 第一次 commit + push 验证通过
- [ ] 微信开发者工具能成功导入 `miniprogram/` 并编译运行

---

> 🎉 完成！至此，从 **0 准备 → 需求 → 架构 → 设计 → Git 管理** 的全流程文档（小程序版）已就绪。
> 下一步：用 GitHub 仓库开始你的第一个 commit 🚀
