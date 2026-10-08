# Rita Architecture

## 当前阶段目标

先完成一条最小闭环：

1. 前端发送消息
2. 后端接收并编排上下文
3. 注入 `self_model`
4. 返回 `Rita` 回复
5. 写入 `messages` 与 `memory candidates`

## 当前模块

- `apps/web`: 聊天 UI、状态面板、头像区
- `apps/api`: FastAPI、Agent 编排入口
- `packages/prompts`: 系统提示词模板
- `data/seeds`: 初始人格和种子数据

## 后续补充

- `memory service`
- `state manager`
- `reflection runner`
- `voice pipeline`
- `avatar bridge`
