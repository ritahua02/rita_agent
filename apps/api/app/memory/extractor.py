"""短期记忆候选提取器（会话内实时记忆，对应 docs/memory-design.md 的分类）。

第一版策略（对齐 docs/memory-design.md「第一版策略」）：
- 不额外调用 LLM，用规则从当前这一轮对话中提取候选记忆，保证低延迟、零额外成本。
- 只做“候选”，不做“写入”：候选记忆只进入会话级 SessionStore，
  由人工在 Debug 面板里查看，后续需要时再决定是否固化进
  data/memories/processed/ 的长期记忆文件。
- 分类对齐长期记忆的四类，方便未来做“会话记忆 -> 长期记忆”的归档：
    user_profile_memory / episodic_memory / relational_memory / self_memory

后续演进方向：
- 换成 LLM 抽取，输出结构化 JSON，替换本文件的规则实现，
  但 MemoryCandidate 的数据结构和调用方（orchestrator/session store）不需要变。
- 增加重要度打分与去重（例如同一偏好反复出现时合并而不是不断新增候选）。
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

MemoryKind = str  # "user_profile" | "episodic" | "relational" | "self"

_PROFILE_PATTERNS: tuple[str, ...] = ("我喜欢", "我不喜欢", "我讨厌", "我叫", "我的名字", "我是")
_RELATIONAL_PATTERNS: tuple[str, ...] = ("谢谢", "别这样", "不要", "喜欢你", "想你", "陪着我")
_EPISODIC_PATTERNS: tuple[str, ...] = ("今天", "刚才", "昨天", "刚刚", "上次")


@dataclass
class MemoryCandidate:
    id: str
    kind: MemoryKind
    text: str
    source_text: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind,
            "text": self.text,
            "source_text": self.source_text,
            "created_at": self.created_at,
        }


class MemoryExtractor:
    """从单轮用户输入中提取候选记忆，规则版实现。"""

    def extract(self, user_text: str) -> list[MemoryCandidate]:
        text = user_text.strip()
        if not text:
            return []

        candidates: list[MemoryCandidate] = []

        for pattern in _PROFILE_PATTERNS:
            if pattern in text:
                candidates.append(self._make(kind="user_profile", text=text, pattern=pattern))
                break

        for pattern in _RELATIONAL_PATTERNS:
            if pattern in text:
                candidates.append(self._make(kind="relational", text=text, pattern=pattern))
                break

        for pattern in _EPISODIC_PATTERNS:
            if pattern in text:
                candidates.append(self._make(kind="episodic", text=text, pattern=pattern))
                break

        return candidates

    @staticmethod
    def _make(kind: MemoryKind, text: str, pattern: str) -> MemoryCandidate:
        return MemoryCandidate(
            id=str(uuid.uuid4()),
            kind=kind,
            text=text,
            source_text=f"命中规则「{pattern}」",
        )
