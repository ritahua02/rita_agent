# API App

这里是 `Rita` 的后端服务。

## 当前职责

- 接收聊天请求
- 注入 `self_model`
- 预留记忆、状态、反思模块入口

## 启动方式

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000
```
