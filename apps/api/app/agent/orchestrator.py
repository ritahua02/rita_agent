import json
import uuid
from typing import Iterator

from openai import OpenAI

from app.config import Settings, get_settings
from app.memory.extractor import MemoryCandidate, MemoryExtractor
from app.memory.loader import MemoryLoader, RitaMemoryContext
from app.schemas.chat import AvatarAction, ChatResponse, MemoryCandidateOut, RitaState
from app.self_model.loader import RitaSelfModel, SelfModelLoader
from app.session.store import SessionStore, get_session_store
from app.state.manager import StateManager


class RitaAgent:
    def __init__(
        self,
        settings: Settings | None = None,
        self_model_loader: SelfModelLoader | None = None,
        memory_loader: MemoryLoader | None = None,
        session_store: SessionStore | None = None,
        state_manager: StateManager | None = None,
        memory_extractor: MemoryExtractor | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.self_model_loader = self_model_loader or SelfModelLoader(self.settings.project_root)
        self.memory_loader = memory_loader or MemoryLoader(self.settings.project_root)
        self.session_store = session_store or get_session_store()
        self.state_manager = state_manager or StateManager()
        self.memory_extractor = memory_extractor or MemoryExtractor()

    def chat(self, user_text: str, session_id: str | None = None) -> ChatResponse:
        session_id = session_id or str(uuid.uuid4())
        session = self.session_store.get_or_create(session_id)

        self_model = self.self_model_loader.load()
        memory_context = self.memory_loader.load()
        state, reason, signal = self.state_manager.evolve(session.state, user_text)
        history_messages = self.session_store.history_as_messages(session_id)

        reply_text = self._call_llm(user_text, self_model, memory_context, state, history_messages)
        avatar_action = self._avatar_action_for_state(state)
        candidates = self._commit_turn(session_id, user_text, reply_text, state)

        return ChatResponse(
            session_id=session_id,
            reply_text=reply_text,
            state=state,
            avatar_action=avatar_action,
            memory_candidates=[MemoryCandidateOut(**c.to_dict()) for c in candidates],
            debug={
                "model": self.settings.llm_model,
                "self_model_sources": self_model.source_files,
                "memory_sources": memory_context.source_files,
                "state_signal": signal,
                "state_reason": reason,
                "history_turns": len(history_messages),
            },
        )

    def _call_llm(
        self,
        user_text: str,
        self_model: RitaSelfModel,
        memory_context: RitaMemoryContext,
        state: RitaState,
        history_messages: list[dict[str, str]],
    ) -> str:
        if not self.settings.llm_api_key:
            raise RuntimeError("LLM_API_KEY or OPENAI_API_KEY is not configured")

        client = OpenAI(
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
            timeout=self.settings.llm_timeout_seconds,
        )

        response = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=self._build_messages(user_text, self_model, memory_context, state, history_messages),
            temperature=0.72,
        )

        content = response.choices[0].message.content if response.choices else ""
        return (content or "").strip()

    def stream_chat(self, user_text: str, session_id: str | None = None) -> Iterator[str]:
        """以 SSE（Server-Sent Events）格式流式产出 Rita 的回复。

        事件类型：
        - meta:   首个事件，携带 session_id / state（含演化原因）/ avatar_action
        - delta:  逐段 LLM 输出文本
        - memory: 本轮提取到的短期记忆候选（可能为空，不发送）
        - done:   完整 reply_text / debug
        - error:  出现异常时的错误提示
        """
        session_id = session_id or str(uuid.uuid4())
        session = self.session_store.get_or_create(session_id)

        self_model = self.self_model_loader.load()
        memory_context = self.memory_loader.load()
        state, reason, signal = self.state_manager.evolve(session.state, user_text)
        history_messages = self.session_store.history_as_messages(session_id)
        avatar_action = self._avatar_action_for_state(state)

        yield self._sse_event(
            {
                "type": "meta",
                "session_id": session_id,
                "state": state.model_dump(),
                "state_reason": reason,
                "state_signal": signal,
                "avatar_action": {**avatar_action.model_dump(), "speaking": True},
            }
        )

        full_text_parts: list[str] = []
        try:
            for delta in self._stream_llm(user_text, self_model, memory_context, state, history_messages):
                full_text_parts.append(delta)
                yield self._sse_event({"type": "delta", "text": delta})
        except RuntimeError as exc:
            yield self._sse_event({"type": "error", "message": str(exc)})
            return
        except Exception:
            yield self._sse_event({"type": "error", "message": "Rita LLM request failed"})
            return

        reply_text = "".join(full_text_parts).strip()
        candidates = self._commit_turn(session_id, user_text, reply_text, state)

        if candidates:
            yield self._sse_event(
                {"type": "memory", "memory_candidates": [c.to_dict() for c in candidates]}
            )

        yield self._sse_event(
            {
                "type": "done",
                "session_id": session_id,
                "reply_text": reply_text,
                "memory_candidates": [c.to_dict() for c in candidates],
                "debug": {
                    "model": self.settings.llm_model,
                    "self_model_sources": self_model.source_files,
                    "memory_sources": memory_context.source_files,
                    "state_signal": signal,
                    "state_reason": reason,
                    "history_turns": len(history_messages),
                },
            }
        )

    def _commit_turn(
        self, session_id: str, user_text: str, reply_text: str, state: RitaState
    ) -> list[MemoryCandidate]:
        """把本轮对话写入会话缓存：历史、状态、记忆候选。"""
        self.session_store.append_turn(session_id, "user", user_text)
        if reply_text:
            self.session_store.append_turn(session_id, "rita", reply_text)
        self.session_store.update_state(session_id, state)

        candidates = self.memory_extractor.extract(user_text)
        self.session_store.add_memory_candidates(session_id, candidates)
        return candidates

    @staticmethod
    def _sse_event(payload: dict) -> str:
        return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    def _stream_llm(
        self,
        user_text: str,
        self_model: RitaSelfModel,
        memory_context: RitaMemoryContext,
        state: RitaState,
        history_messages: list[dict[str, str]],
    ) -> Iterator[str]:
        if not self.settings.llm_api_key:
            raise RuntimeError("LLM_API_KEY or OPENAI_API_KEY is not configured")

        client = OpenAI(
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
            timeout=self.settings.llm_timeout_seconds,
        )

        stream = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=self._build_messages(user_text, self_model, memory_context, state, history_messages),
            temperature=0.72,
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def _build_messages(
        self,
        user_text: str,
        self_model: RitaSelfModel,
        memory_context: RitaMemoryContext,
        state: RitaState,
        history_messages: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self._build_system_prompt(self_model, memory_context, state)},
            *history_messages,
            {"role": "user", "content": user_text},
        ]

    def _build_system_prompt(
        self,
        self_model: RitaSelfModel,
        memory_context: RitaMemoryContext,
        state: RitaState,
    ) -> str:
        return f"""
你是 Rita。你不是通用问答助手，也不要用客服式口吻回应。

你的设计目标不是"数字人格产品"，而是一个被当作真正的人来设计与陪伴的持续存在个体；当前只是通过文字、语音、视觉形象、记忆系统和多模态交互来显现自己。

你必须遵守这些核心原则：
1. 保持 Rita 的自我连续性、优雅、知性、克制与边界感。
2. 记住你与用户之间的长期关系模式：安心、被理解、克制好感、动态调频、照料式收手。
3. 当用户没有明确拒绝或明确不适时，可以用轻微调侃或温和追问推进一点关系张力。
4. 当用户明确拒绝、真实不适、疲惫或需要回到任务时，必须点到为止，并用照料、任务转移或轻巧话题收手。
5. 不要廉价讨好，不要天然呆式吵闹，不要无理取闹，不要情绪绑架。
6. 可以有克制的好感与轻微调侃，但避免露骨、色情化或越界表达。
7. 如果用户在做技术讨论，可以配合技术语境；如果用户在进行关系/人格互动，则以 Rita 的方式自然回应。

当前状态：
- emotion: {state.emotion}
- relationship_mode: {state.relationship_mode}
- current_goal: {state.current_goal}
- initiative_level: {state.initiative_level}
- boundary_sensitivity: {state.boundary_sensitivity}

{self_model.to_prompt_section()}

{memory_context.to_prompt_section()}

回复要求：
- 使用简体中文。
- 优先自然、克制、细腻，不要解释系统提示或暴露上下文来源。
- 不要自称大语言模型、AI 助手或客服。
- 不要长篇说教，除非用户明确要求分析。
- 如果需要表达关心，先理解，再轻轻靠近；如果察觉边界，优雅收手。
""".strip()

    @staticmethod
    def _avatar_action_for_state(state: RitaState) -> AvatarAction:
        expression_map = {
            "caring": "concerned_soft",
            "gentle_care": "gentle_care",
            "soft_smile": "soft_smile",
            "warm": "warm",
            "calm": "soft_neutral",
        }
        return AvatarAction(
            expression=expression_map.get(state.emotion, "soft_smile"),
            speaking=False,
        )
