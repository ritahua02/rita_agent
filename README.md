# Rita Project

`Rita` 是一个面向**单人开发**的专属 AI 虚拟人项目骨架。

> 仓库地址：https://github.com/ritahua02/rita_agent ｜ 开源协议：MIT
>
> 本仓库是**去敏感化后的公开骨架**：不含任何真实密钥，也不含作者与 Rita 的私人互动/记忆数据。
> `data/` 下的人格、记忆、互动样本文件均为**占位模板**，使用时请根据自己的需求填入。
> 首次使用请先读 [`PROJECT_OVERVIEW.md`](./PROJECT_OVERVIEW.md)，再执行 `bash setup.sh` 一键构造环境。

## 项目目标

第一阶段只做这些事情：

- 让 `Rita` 能稳定地和你聊天
- 让 `Rita` 有结构化自我模型
- 让 `Rita` 拥有长期记忆与关系连续性
- 为后续语音、Live2D、反思系统预留清晰目录

## 目录结构

```text
rita-project/
├─ apps/
│  ├─ web/               # 前端：Next.js UI 壳
│  └─ api/               # 后端：FastAPI 服务
├─ packages/
│  ├─ shared/            # 共享 schema / 类型约定
│  └─ prompts/           # prompt 模板与系统设定
├─ docs/                 # 架构、人格、记忆、第一周任务文档
├─ data/
│  ├─ seeds/             # 初始自我模型、默认配置
│  ├─ references/        # 公开参考资料索引
│  └─ exports/           # 导出日志与调试产物
└─ assets/
   ├─ avatar/            # 立绘 / Live2D 素材占位
   ├─ voice/             # 语音缓存与样本占位
   └─ ui/                # UI 资源占位
```

## 现在建议你先做什么

1. 先阅读 `docs/self-model.md`
2. 再改 `data/seeds/rita-self-profile.json`
3. 然后启动 `apps/api`
4. 最后开始补 `apps/web`

## 后续推荐顺序

- `self_model`
- `chat`
- `memory`
- `state`
- `voice`
- `avatar`
- `reflection`

## 打包与部署

已提供 `docker-compose.yml` + `apps/api/Dockerfile` + `apps/web/Dockerfile`，
一键启动：

```bash
cp .env.example .env   # 填好真实的 LLM_API_KEY
docker compose up --build
```

迁移到其他服务器 / 云主机的完整步骤见 `docs/deployment/packaging-and-deploy.md`。
