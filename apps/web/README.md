# Web App

这里是 `Rita` 的前端界面。

## 当前进展

第一版聊天 UI 已完成：

- 左侧：Rita 头像区（呼吸/说话动效）+ 实时状态面板（情绪、关系模式、当前目标、主动程度、边界敏感度）
- 右侧：聊天区，气泡样式区分用户/Rita，支持打字中动画、错误提示、Enter 发送
- 通过 `lib/api/chat.ts` 直连后端 `/api/chat` 接口

## 启动方式

1. 先启动后端（见 `apps/api/README.md`），默认监听 `http://localhost:8000`
2. 配置前端环境变量：

```bash
cd apps/web
cp .env.local.example .env.local
```

3. 安装依赖并启动：

```bash
npm install
npm run dev
```

4. 打开 http://localhost:3000 即可和 Rita 对话。

## 目录说明

- `app/page.tsx`：页面组装（状态管理 + 调用 API）
- `components/AvatarPanel.tsx`：头像与动作展示
- `components/StatusPanel.tsx`：Rita 实时状态面板
- `components/ChatPanel.tsx` / `MessageBubble.tsx`：聊天消息列表与输入框
- `lib/api/chat.ts`：调用后端 `/api/chat` 的封装
- `types/chat.ts`：与后端 `schemas/chat.py` 对齐的类型定义
