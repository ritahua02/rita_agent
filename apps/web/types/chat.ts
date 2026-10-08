export interface RitaState {
  emotion: string;
  relationship_mode: string;
  current_goal: string;
  initiative_level: number;
  boundary_sensitivity: number;
}

export interface AvatarAction {
  expression: string;
  motion: string | null;
  speaking: boolean;
}

export interface MemoryCandidate {
  id: string;
  kind: string;
  text: string;
  source_text: string;
  created_at: number;
}

export interface ChatResponse {
  session_id: string;
  reply_text: string;
  state: RitaState;
  avatar_action: AvatarAction;
  memory_candidates: MemoryCandidate[];
  debug: Record<string, unknown> | null;
}

export interface StreamMetaEvent {
  type: 'meta';
  session_id: string;
  state: RitaState;
  state_reason: string;
  state_signal: string;
  avatar_action: AvatarAction;
}

export interface StreamDeltaEvent {
  type: 'delta';
  text: string;
}

export interface StreamMemoryEvent {
  type: 'memory';
  memory_candidates: MemoryCandidate[];
}

export interface StreamDoneEvent {
  type: 'done';
  session_id: string;
  reply_text: string;
  memory_candidates: MemoryCandidate[];
  debug: Record<string, unknown> | null;
}

export interface StreamErrorEvent {
  type: 'error';
  message: string;
}

export type ChatStreamEvent =
  | StreamMetaEvent
  | StreamDeltaEvent
  | StreamMemoryEvent
  | StreamDoneEvent
  | StreamErrorEvent;

export type MessageRole = 'user' | 'rita' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  text: string;
  timestamp: number;
  pending?: boolean;
  error?: boolean;
}

export interface DebugInfo {
  sessionId: string | null;
  stateReason: string | null;
  stateSignal: string | null;
  historyTurns: number | null;
  model: string | null;
  selfModelSources: string[];
  memorySources: string[];
  memoryCandidates: MemoryCandidate[];
}
