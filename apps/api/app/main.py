from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.agent.orchestrator import RitaAgent
from app.config import get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.session.store import get_session_store


settings = get_settings()
app = FastAPI(title="Rita API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

agent = RitaAgent()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "rita-api"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        return agent.chat(payload.text, payload.session_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Rita LLM request failed") from exc


@app.post("/api/chat/stream")
def chat_stream(payload: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        agent.stream_chat(payload.text, payload.session_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # 避免反向代理（如 nginx）缓冲 SSE 响应
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/session/{session_id}/inspect")
def inspect_session(session_id: str) -> dict:
    """供 Debug/Inspector 面板使用：查看某个会话当前的状态、历史长度、记忆候选。"""
    session = get_session_store().snapshot(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    return {
        "session_id": session.session_id,
        "state": session.state.model_dump(),
        "history": [
            {"role": turn.role, "text": turn.text, "timestamp": turn.timestamp} for turn in session.history
        ],
        "memory_candidates": [c.to_dict() for c in session.memory_candidates],
        "last_active_at": session.last_active_at,
    }
