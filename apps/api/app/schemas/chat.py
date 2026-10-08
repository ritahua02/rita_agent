from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1)
    session_id: str | None = None


class RitaState(BaseModel):
    emotion: str = "calm"
    relationship_mode: str = "boundary_aware"
    current_goal: str = "respond"
    initiative_level: float = 0.3
    boundary_sensitivity: float = 0.8


class AvatarAction(BaseModel):
    expression: str = "soft_smile"
    motion: str | None = None
    speaking: bool = False


class MemoryCandidateOut(BaseModel):
    id: str
    kind: str
    text: str
    source_text: str
    created_at: float


class ChatResponse(BaseModel):
    session_id: str
    reply_text: str
    state: RitaState
    avatar_action: AvatarAction
    memory_candidates: list[MemoryCandidateOut] = Field(default_factory=list)
    debug: dict | None = None
