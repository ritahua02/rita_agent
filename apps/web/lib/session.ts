const SESSION_STORAGE_KEY = 'rita-session-id';

/**
 * 获取当前浏览器的会话 id，持久化到 localStorage。
 * 与后端 SessionStore 的 session_id 对应，用于维持会话级上下文（历史/状态/短期记忆）。
 * 如果需要开启一段全新的对话，调用 resetSessionId()。
 */
export function getSessionId(): string {
  if (typeof window === 'undefined') return '';

  const existing = window.localStorage.getItem(SESSION_STORAGE_KEY);
  if (existing) return existing;

  const created = crypto.randomUUID();
  window.localStorage.setItem(SESSION_STORAGE_KEY, created);
  return created;
}

export function resetSessionId(): string {
  const created = crypto.randomUUID();
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(SESSION_STORAGE_KEY, created);
  }
  return created;
}
