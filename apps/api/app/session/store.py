"""会话级临时上下文缓存（中短期实时记忆）。

设计取舍：
- 纯进程内内存缓存，不落库、不跨进程共享。重启服务即清空，这是有意为之——
  它承载的是"这次对话里正在发生什么"，不是需要长期保留的人格记忆。
- 与 `data/memories/processed/` 的长期记忆是两个层次：
    长期记忆（loader.py）  -> 稳定的、经过筛选的、跨会话的 Rita 记忆
    会话记忆（本模块）      -> 当前会话内的对话历史 + 状态 + 待筛选的记忆候选
- 未来如果要做“会话结束后，把重要的会话记忆固化为长期记忆”，
  应该在这个模块之上加一层归档逻辑，而不是把两者混在一起。
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

from app.memory.extractor import MemoryCandidate
from app.schemas.chat import RitaState

MAX_HISTORY_TURNS = 12
MAX_MEMORY_CANDIDATES = 30
SESSION_TTL_SECONDS = 60 * 60 * 2  # 2 小时未活动则视为过期，惰性清理


@dataclass
class HistoryTurn:
    role: str  # "user" | "rita"
    text: str
    timestamp: float


@dataclass
class SessionData:
    session_id: str
    history: list[HistoryTurn] = field(default_factory=list)
    state: RitaState = field(default_factory=RitaState)
    memory_candidates: list[MemoryCandidate] = field(default_factory=list)
    last_active_at: float = field(default_factory=time.time)


class SessionStore:
    """线程安全的会话级缓存，供多个请求并发访问同一 session_id 时使用。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, SessionData] = {}

    def get_or_create(self, session_id: str) -> SessionData:
        with self._lock:
            self._evict_expired_locked()
            session = self._sessions.get(session_id)
            if session is None:
                session = SessionData(session_id=session_id)
                self._sessions[session_id] = session
            session.last_active_at = time.time()
            return session

    def append_turn(self, session_id: str, role: str, text: str) -> None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return
            session.history.append(HistoryTurn(role=role, text=text, timestamp=time.time()))
            if len(session.history) > MAX_HISTORY_TURNS:
                session.history = session.history[-MAX_HISTORY_TURNS:]
            session.last_active_at = time.time()

    def update_state(self, session_id: str, state: RitaState) -> None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return
            session.state = state

    def add_memory_candidates(self, session_id: str, candidates: list[MemoryCandidate]) -> None:
        if not candidates:
            return
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return
            session.memory_candidates.extend(candidates)
            if len(session.memory_candidates) > MAX_MEMORY_CANDIDATES:
                session.memory_candidates = session.memory_candidates[-MAX_MEMORY_CANDIDATES:]

    def history_as_messages(self, session_id: str) -> list[dict[str, str]]:
        """转换为 OpenAI messages 格式，role 映射为 user/assistant。"""
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return []
            return [
                {"role": "user" if turn.role == "user" else "assistant", "content": turn.text}
                for turn in session.history
            ]

    def snapshot(self, session_id: str) -> SessionData | None:
        with self._lock:
            return self._sessions.get(session_id)

    def _evict_expired_locked(self) -> None:
        now = time.time()
        expired = [
            sid for sid, session in self._sessions.items() if now - session.last_active_at > SESSION_TTL_SECONDS
        ]
        for sid in expired:
            del self._sessions[sid]


_default_store = SessionStore()


def get_session_store() -> SessionStore:
    return _default_store
