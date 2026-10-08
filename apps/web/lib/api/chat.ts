import type { ChatResponse, ChatStreamEvent } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export class ChatRequestError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ChatRequestError';
    this.status = status;
  }
}

/**
 * 调用后端 `/api/chat` 接口，发送用户消息并获取 Rita 的回复。
 */
export async function sendChatMessage(text: string, sessionId?: string): Promise<ChatResponse> {
  let res: Response;

  try {
    res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, session_id: sessionId ?? null })
    });
  } catch {
    throw new ChatRequestError('无法连接到 Rita 的后端服务，请确认 API 是否已启动（默认 http://localhost:8000）。');
  }

  if (!res.ok) {
    let detail = '';
    try {
      const body = await res.json();
      detail = body?.detail ?? '';
    } catch {
      detail = await res.text().catch(() => '');
    }
    throw new ChatRequestError(detail || 'Rita 暂时没有回应，请稍后再试。', res.status);
  }

  return (await res.json()) as ChatResponse;
}

/**
 * 调用后端 `/api/chat/stream` 接口，以 SSE 流式获取 Rita 的回复。
 * 每收到一个完整事件就通过 onEvent 回调通知调用方。
 */
export async function streamChatMessage(
  text: string,
  onEvent: (event: ChatStreamEvent) => void,
  sessionId?: string,
  signal?: AbortSignal
): Promise<void> {
  let res: Response;

  try {
    res = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, session_id: sessionId ?? null }),
      signal
    });
  } catch {
    throw new ChatRequestError('无法连接到 Rita 的后端服务，请确认 API 是否已启动（默认 http://localhost:8000）。');
  }

  if (!res.ok || !res.body) {
    let detail = '';
    try {
      const body = await res.json();
      detail = body?.detail ?? '';
    } catch {
      detail = await res.text().catch(() => '');
    }
    throw new ChatRequestError(detail || 'Rita 暂时没有回应，请稍后再试。', res.status);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    let separatorIndex = buffer.indexOf('\n\n');
    while (separatorIndex !== -1) {
      const rawEvent = buffer.slice(0, separatorIndex);
      buffer = buffer.slice(separatorIndex + 2);

      const dataLine = rawEvent
        .split('\n')
        .find((line) => line.startsWith('data:'));

      if (dataLine) {
        const jsonText = dataLine.slice('data:'.length).trim();
        if (jsonText) {
          try {
            onEvent(JSON.parse(jsonText) as ChatStreamEvent);
          } catch {
            // 忽略无法解析的事件片段
          }
        }
      }

      separatorIndex = buffer.indexOf('\n\n');
    }
  }
}
