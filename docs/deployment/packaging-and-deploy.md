# Rita 打包与快速部署指南

这份文档给未来"把 Rita 从这台机器搬到别的地方"时看，目标是：不用重新理解架构，
照着步骤走就能在新环境里跑起来。

## 1. 项目结构回顾（部署相关）

```text
20260611104928/
├─ apps/
│  ├─ api/            # FastAPI 后端，运行时会读取仓库根目录下的 data/
│  └─ web/             # Next.js 前端
├─ data/               # Rita 的自我模型 / 长期记忆（*.md, *.json）—— 必须随项目一起迁移
├─ docker-compose.yml  # 一键起 api + web
├─ .env                # 真实密钥，不进 git，迁移时要手动复制
└─ .env.example        # 环境变量清单（占位）
```

**关键点**：后端不是无状态的纯代码服务，它在每次收到 `/api/chat` 请求时都会去读
`data/references/rita-source-notes/*.md`、`data/memories/processed/*.md` 等文件，
拼进 system prompt。**迁移项目时，`data/` 目录必须完整带走**，否则 Rita 会"失忆"。

## 2. 迁移前检查清单

- [ ] `.env` 里的 `LLM_API_KEY`（或 `OPENAI_API_KEY`）、`LLM_BASE_URL`、`LLM_MODEL` 是否是新环境可用的
- [ ] `data/` 目录是否完整（尤其是 `references/rita-source-notes/`、`memories/processed/`）
- [ ] `CORS_ALLOW_ORIGINS` 是否需要改成新的前端域名（不再是 `localhost:3000`）
- [ ] `NEXT_PUBLIC_API_BASE_URL` 是否需要改成新的后端域名（前端构建时写死，改了要重新构建）
- [ ] 不要把 `.env` 提交到 git 或直接贴在聊天记录里；换新环境时手动复制内容

## 3. 方式一：不用 Docker，直接跑（适合先在新机器验证）

### 后端

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 确保项目根目录有 .env（含 LLM_API_KEY）
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd apps/web
cp .env.local.example .env.local   # 按需修改 NEXT_PUBLIC_API_BASE_URL
npm install
npm run build
npm run start   # 生产模式，默认监听 3000
```

## 4. 方式二：Docker 打包（推荐用于正式部署/迁移）

已提供：

- `apps/api/Dockerfile`
- `apps/web/Dockerfile`
- `docker-compose.yml`（根目录）

### 一键启动（本机验证）

```bash
# 项目根目录
cp .env.example .env   # 填好真实的 LLM_API_KEY 等
docker compose up --build
```

- 后端：http://localhost:8000
- 前端：http://localhost:3000

### 单独构建后端镜像

```bash
# 必须在【项目根目录】执行（不是 apps/api！），因为要把 data/ 一起打进镜像
docker build -f apps/api/Dockerfile -t rita-api .
docker run --rm -p 8000:8000 --env-file .env rita-api
```

### 单独构建前端镜像

```bash
docker build -f apps/web/Dockerfile \
  --build-arg NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com \
  -t rita-web apps/web
docker run --rm -p 3000:3000 rita-web
```

### 更新人格 / 记忆内容后如何生效

- 如果用 `docker-compose.yml`：`data/` 是**只读 volume 挂载**（不是打进镜像），
  改完 `data/` 下的 md 文件后，`docker compose restart api` 即可生效，**不需要重新构建镜像**。
- 如果用 `docker build` 单独构建（没有走 volume）：`data/` 是 `COPY` 进镜像的，
  改内容后要重新 `docker build`。

## 5. 迁移到云主机 / 新服务器的典型步骤

1. 把整个项目目录（含 `data/`，不含 `node_modules`、`.next`、`__pycache__`、`.venv`）打包传过去
   ```bash
   tar -czf rita-project.tar.gz \
     --exclude='node_modules' --exclude='.next' --exclude='__pycache__' \
     --exclude='.venv' --exclude='.git' \
     -C .. 20260611104928
   ```
2. 在新服务器上装好 Docker（或者 Python 3.11+ / Node 20+，走方式一）
3. 手动创建 `.env`（不要用聊天记录/git 传密钥，用安全渠道单独传）
4. `docker compose up --build -d`
5. 如果要用域名 + HTTPS，前面加一层 nginx / Caddy 反向代理，例如：

   ```nginx
   server {
       listen 443 ssl;
       server_name rita.yourdomain.com;

       location /api/ {
           proxy_pass http://127.0.0.1:8000/api/;
           proxy_set_header Host $host;
       }

       location / {
           proxy_pass http://127.0.0.1:3000/;
           proxy_set_header Host $host;
       }
   }
   ```

6. 同步更新：
   - `.env` 里 `CORS_ALLOW_ORIGINS=https://rita.yourdomain.com`
   - 前端构建时 `NEXT_PUBLIC_API_BASE_URL=https://rita.yourdomain.com/api`（如果反代到同域名下的 `/api`）

## 6. 常见问题排查

| 现象 | 常见原因 | 排查方式 |
|---|---|---|
| 前端报"无法连接到 Rita 的后端服务" | 后端没启动 / 端口不对 / `NEXT_PUBLIC_API_BASE_URL` 配错 | `curl http://localhost:8000/health` |
| `/api/chat` 返回 500 `LLM_API_KEY ... not configured` | `.env` 没填密钥，或后端没读到 `.env` | 确认 `.env` 在**项目根目录**，不是 `apps/api/.env` |
| `/api/chat` 返回 502 `Rita LLM request failed` | 密钥有效但 `LLM_MODEL` 名称不对 / 供应商模型下线 | 直接用 Python 跑一次 `RitaAgent().chat("你好")` 看完整报错 |
| 浏览器控制台报 CORS 错误 | `CORS_ALLOW_ORIGINS` 没包含前端实际访问的域名 | 检查 `apps/api/app/config.py` 读取的 `CORS_ALLOW_ORIGINS` |
| Rita 回复内容和人格设定不符 | `data/` 目录没迁移完整，或 volume 挂载路径不对 | 看 `/api/chat` 响应里的 `debug.self_model_sources` / `debug.memory_sources` |

## 7. 安全提醒

- `.env` 永远不进 git、不贴聊天记录、不写进 Dockerfile。
- 生产环境的 `CORS_ALLOW_ORIGINS` 不要用 `*`，只填真实会访问的前端域名。
- 如果之后接数据库（`DATABASE_URL`），同样走环境变量，不要写死在代码里。
