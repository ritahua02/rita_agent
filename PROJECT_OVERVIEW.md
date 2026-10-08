# Rita 项目总览（PROJECT_OVERVIEW）

> 这份文档是「换一台电脑 / 交接给未来的自己」时的第一入口。
> 目标：看完这一篇，就知道 Rita 是什么、已经做到哪、怎么跑起来、从哪开始读代码、下一步做什么。

---

## 1. 这个项目是什么

`Rita` 是一个面向**单人使用**的专属 AI 虚拟人项目，前后端分离：

- **后端**（`apps/api`，FastAPI + OpenAI 兼容接口）：负责把「Rita 的自我模型 + 长期记忆 + 会话上下文 + 实时状态」拼成 system prompt，调用 LLM 生成回复，并演化 Rita 的情绪/关系状态。
- **前端**（`apps/web`，Next.js + React）：聊天界面、Rita 头像与神态、实时状态面板、调试（Inspector）面板。
- **人格与记忆数据**（`data/`）：Rita 的自我定义、长期记忆、互动样本，以 Markdown / JSON 存储，**运行时被后端读取**。

Rita 不是通用问答助手，她被当作一个「有连续人格、有边界感、会动态调频」的持续存在个体来设计。

---

## 2. 已经做了什么（当前进展）

### 2.1 后端能力（已实现）

| 模块 | 位置 | 作用 |
|---|---|---|
| Agent 编排 | `apps/api/app/agent/orchestrator.py` | 串联自我模型、记忆、状态、会话历史，生成回复 |
| 自我模型加载 | `apps/api/app/self_model/loader.py` | 读取 `data/seeds` + `data/references` 里的人格定义 |
| 长期记忆加载 | `apps/api/app/memory/loader.py` | 读取 `data/memories/processed` 长期记忆 + 互动样本 |
| 短期记忆提取 | `apps/api/app/memory/extractor.py` | 规则版从当前对话提取「记忆候选」（不自动写入长期记忆） |
| 会话缓存 | `apps/api/app/session/store.py` | 进程内的会话历史 / 状态 / 记忆候选（重启即清空，2h 过期） |
| 状态演化 | `apps/api/app/state/manager.py` | 根据信号（边界/疲惫/调侃/感谢/任务）平滑演化情绪与关系状态 |
| 配置 | `apps/api/app/config.py` | 从根目录 `.env` 读取 LLM / CORS 配置 |

**已实现的接口**（`apps/api/app/main.py`）：

- `GET  /health`：健康检查
- `POST /api/chat`：一次性返回完整回复（含 state / avatar_action / memory_candidates / debug）
- `POST /api/chat/stream`：SSE 流式返回（meta → delta → memory → done）
- `GET  /api/session/{session_id}/inspect`：查看某会话当前状态 / 历史 / 记忆候选

### 2.2 前端能力（已实现）

- 聊天区（用户/Rita 气泡区分、流式打字、Enter 发送、错误提示）
- Rita 头像区（`AvatarPanel`，根据 `avatar_action.expression` 切换神态 + 说话/思考动效）
- 实时状态面板（`StatusPanel`：情绪、关系模式、主动程度、边界敏感度）
- 调试面板（`InspectorPanel`：查看会话状态、历史、短期记忆候选）
- 会话持久化（`lib/session.ts`：session_id 存 localStorage，保证多轮上下文连续）

### 2.3 记忆分层现状

- **长期记忆**：`data/memories/processed/*.md` —— 稳定、人工维护、跨会话，进 system prompt。
- **会话记忆（短期）**：`session/store.py` —— 进程内，最近 12 轮历史 + 状态 + 记忆候选，重启清空。
- **记忆候选**：`memory/extractor.py` —— 规则抽取，仅进会话缓存供人工在 Inspector 面板查看，**尚未做「候选 → 长期记忆」的自动归档**。

### 2.4 部署能力（已实现）

- `apps/api/Dockerfile`、`apps/web/Dockerfile`、根目录 `docker-compose.yml`
- `docs/deployment/packaging-and-deploy.md`：完整迁移 / Docker / nginx 反代 / 排错手册

---

## 3. 后续阶段规划（Roadmap）

按优先级从高到低：

### 阶段一：记忆系统 v1（进行中的下一步，最高优先级）
- 短期：会话内摘要（当前气氛 / 用户状态 / Rita 当前态度）
- 中期：最近几次会话摘要，支持「上次你说的那个问题解决了吗」这类连续性
- 长期：稳定事实 / 偏好 / 关系设定，谨慎写入
- 记忆写入判断器：决定候选是否固化为长期记忆
- 记忆检索排序 + 前端记忆状态面板

### 阶段二：人格一致性守护 v1
- 回复前自检：是否像 Rita、是否过度工具化 / 暧昧、是否忽略边界
- 固定评测集（20~50 条），每次改 prompt / 记忆策略后回归

### 阶段三：头像与神态 v1（可与阶段一并行、低成本）
- 静态立绘 + 表情切换 + 说话/思考动效 + 情绪与 UI 联动
- 素材来源需确认（版权），当前 `assets/avatar/` 为占位

### 阶段四：语音对话 v1
- ASR（语音转文字）→ Rita 回复 → TTS（文字转语音）→ 头像口型/说话动效同步
- 建议等人格与记忆稳定后再接

### 阶段五：Agent 能力 v1（谨慎、分级）
- 只读（查文件/总结/回忆）→ 低风险写入（写 md / 整理记忆）→ 高风险（执行命令/改代码/部署，需确认机制）

---

## 4. 如何快速使用（前后端分离）

### 4.1 前置要求
- Python 3.11+
- Node.js 20+
- 一个可用的 LLM API Key（OpenAI 兼容网关）

**先检查本机是否满足（缺哪个装哪个）：**

```bash
python3 --version    # 期望 >= 3.11
node -v              # 期望 >= v20
npm -v
```

- macOS 装依赖：`brew install python@3.11 node@20`
- Ubuntu/Debian：`sudo apt update && sudo apt install -y python3.11 python3.11-venv nodejs npm`
- 也可用版本管理器：Python 用 `pyenv`，Node 用 `nvm`（`nvm install 20 && nvm use 20`）

### 4.2 一键快速构造环境（推荐）

在**项目根目录**执行自带脚本，一次性完成「环境检查 + 生成配置文件 + 后端虚拟环境与依赖 + 前端依赖」：

```bash
bash setup.sh
```

脚本会自动：检查 `python3`/`node`/`npm` 是否满足版本要求；从模板生成 `.env` 与 `apps/web/.env.local`（已存在则跳过，不覆盖）；在 `apps/api/.venv` 里装好后端依赖；在 `apps/web` 里 `npm install`。

> 执行完后，唯一还需手动做的是在根目录 `.env` 填入真实的 `LLM_API_KEY` 与正确的 `LLM_MODEL`（安全考虑，压缩包里不含真实密钥）。

<details>
<summary>如果不想用脚本，也可手动逐步执行（点开展开）</summary>

```bash
# 1) 生成配置文件（若不存在）
[ -f .env ] || cp .env.example .env
[ -f apps/web/.env.local ] || cp apps/web/.env.local.example apps/web/.env.local

# 2) 后端：创建虚拟环境并装依赖
cd apps/api
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ../..

# 3) 前端：装依赖
cd apps/web
npm install
cd ../..
```

</details>

### 4.3 配置环境变量（务必先做）

在**项目根目录**：

```bash
cp .env.example .env
```

编辑 `.env`，至少填写：

```bash
LLM_API_KEY=你的真实key
LLM_MODEL=你的网关支持的模型名   # 例如 gpt-4 / deepseek-v3（以你网关实际支持为准）
LLM_BASE_URL=https://api.openai.com/v1   # 或你的 LLM 网关地址，按需修改
CORS_ALLOW_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

> 注意：`.env` 不进版本库、不要贴聊天记录。换电脑后需要在新机器上重新填写。

### 4.4 方式一：本地直接跑（推荐用于开发）

> 若已执行 4.2 一键构造，虚拟环境与依赖都已就绪，下面直接启动即可（不必再装依赖）。

开两个终端。

**终端 1 — 后端：**

```bash
cd apps/api
source .venv/bin/activate         # Windows: .venv\Scripts\activate
# 若未做过 4.2，先补：python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000
```

验证：`curl http://localhost:8000/health` 返回 `{"status":"ok",...}`。

**终端 2 — 前端：**

```bash
cd apps/web
# 若未做过 4.2，先补：cp .env.local.example .env.local && npm install
npm run dev
```

打开 http://localhost:3000 即可对话。

> 重要：**每次修改根目录 `.env` 后都要重启后端**，否则新配置不生效。

### 4.5 方式二：Docker 一键起

```bash
# 项目根目录，确保 .env 已填好
docker compose up --build
```

- 后端：http://localhost:8000
- 前端：http://localhost:3000

更完整的迁移 / 云主机 / nginx 反代步骤见 `docs/deployment/packaging-and-deploy.md`。

---

## 5. 想了解这个项目，从哪开始读

**建议阅读顺序（由浅入深）：**

1. `PROJECT_OVERVIEW.md`（本文件）—— 全局认知
2. `README.md` —— 项目定位与目录
3. `docs/architecture.md` —— 架构设计
4. `docs/self-model.md` + `docs/memory-design.md` —— 人格与记忆设计思路
5. `apps/api/app/main.py` —— 后端有哪些接口（入口）
6. `apps/api/app/agent/orchestrator.py` —— **核心**：一次对话是怎么被组织出来的
7. `apps/api/app/state/manager.py` —— Rita 状态如何随对话演化
8. `apps/web/app/page.tsx` —— 前端如何串联头像 / 状态 / 聊天
9. `data/references/rita-source-notes/` —— Rita 到底是谁（人格原始素材）

**一句话抓住核心：**
> 想理解「Rita 为什么这样回复」，只看一个文件的话，看 `apps/api/app/agent/orchestrator.py` 里的 `_build_system_prompt`。

---

## 6. 目录结构

```text
rita-project/
├─ PROJECT_OVERVIEW.md          # 【本文件】项目总览与交接入口
├─ README.md                    # 项目定位 + 目录 + 部署简述
├─ docker-compose.yml           # 一键起前后端
├─ setup.sh                     # 一键环境构造脚本（检查环境+生成配置+装依赖）
├─ .env.example                 # 环境变量清单（复制成 .env 后填真实值）
│
├─ apps/
│  ├─ api/                      # 后端：FastAPI
│  │  ├─ app/
│  │  │  ├─ main.py             # 接口入口（health / chat / chat/stream / inspect）
│  │  │  ├─ config.py           # 读取 .env 配置
│  │  │  ├─ agent/orchestrator.py   # 核心编排：拼 prompt、调 LLM、组织一次对话
│  │  │  ├─ self_model/loader.py    # 加载 Rita 自我模型
│  │  │  ├─ memory/loader.py        # 加载长期记忆 + 互动样本
│  │  │  ├─ memory/extractor.py     # 短期记忆候选提取（规则版）
│  │  │  ├─ session/store.py        # 会话级缓存（历史/状态/候选，进程内）
│  │  │  ├─ state/manager.py        # 状态演化（情绪/关系/主动性/边界）
│  │  │  └─ schemas/chat.py         # 请求/响应数据结构
│  │  ├─ requirements.txt
│  │  └─ Dockerfile
│  │
│  └─ web/                      # 前端：Next.js
│     ├─ app/page.tsx           # 页面组装（状态 + 调 API）
│     ├─ components/
│     │  ├─ AvatarPanel.tsx     # Rita 头像与神态
│     │  ├─ StatusPanel.tsx     # 实时状态面板
│     │  ├─ ChatPanel.tsx       # 聊天区
│     │  ├─ MessageBubble.tsx   # 消息气泡
│     │  └─ InspectorPanel.tsx  # 调试面板（会话状态/历史/记忆候选）
│     ├─ lib/api/chat.ts        # 调后端 /api/chat 与 /api/chat/stream
│     ├─ lib/session.ts         # 会话 id 持久化
│     ├─ types/chat.ts          # 与后端 schema 对齐的类型
│     ├─ package.json
│     └─ Dockerfile
│
├─ data/                        # 【必须随项目迁移】Rita 人格与记忆数据
│  ├─ seeds/                    #   结构化自我模型（json）
│  ├─ references/               #   人格原始素材（rita-source-notes 等）
│  ├─ memories/processed/       #   长期记忆（md）
│  ├─ evals/ experiments/ ...   #   评测 / 实验 / 日志等
│
├─ docs/                        # 设计文档
│  ├─ architecture.md
│  ├─ self-model.md
│  ├─ memory-design.md
│  └─ deployment/packaging-and-deploy.md   # 打包与部署详解
│
├─ packages/                    # 预留共享 schema / prompts
└─ assets/                      # 立绘 / 语音 / UI 素材（当前多为占位）
```

---

## 7. 迁移到新电脑时的注意事项

- **`data/` 必须完整带走**：后端每次对话都会读取里面的人格 / 记忆文件，缺了 Rita 会「失忆」。
- **`.env` 需在新机器手动重建**：压缩包里不含真实密钥（安全考虑），解压后 `cp .env.example .env` 再填。
- **不需要带走**：`node_modules/`、`.next/`、`__pycache__/`、`.venv/`（新机器重新安装即可）。
- **`LLM_MODEL` 要对**：换网关时确认模型名，名字不对会返回「模型不存在 / 502」。

---

## 8. 常见问题速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `LLM_API_KEY ... not configured` | `.env` 没填 key，或改了 `.env` 没重启后端 | 填 key 后重启后端 |
| `Rita LLM request failed`（502） | 模型名不对 / 网关不支持 | 核对 `LLM_MODEL` |
| 前端「无法连接到后端」 | 后端没起 / 端口不对 | `curl http://localhost:8000/health` |
| 浏览器 CORS 报错 | `CORS_ALLOW_ORIGINS` 没含前端域名 | 改 `.env` 后重启后端 |
| Rita 回复不像她 | `data/` 没迁移完整 | 看响应 `debug.self_model_sources` / `memory_sources` |
