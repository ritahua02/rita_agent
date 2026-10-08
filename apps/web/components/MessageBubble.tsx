'use client';

import type { ChatMessage } from '@/types/chat';

function formatTime(timestamp: number) {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  });
}

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  if (message.role === 'system') {
    return (
      <div className="message message-system">
        <p>{message.text}</p>
      </div>
    );
  }

  const isUser = message.role === 'user';

  return (
    <div className={`message-row ${isUser ? 'message-row-user' : 'message-row-rita'}`}>
      {!isUser && <div className="message-avatar">R</div>}

      <div
        className={[
          'bubble',
          isUser ? 'bubble-user' : 'bubble-rita',
          message.error ? 'bubble-error' : ''
        ]
          .filter(Boolean)
          .join(' ')}
      >
        {message.pending && !message.text ? (
          <span className="typing-dots">
            <span />
            <span />
            <span />
          </span>
        ) : (
          <p>
            {message.text}
            {message.pending && <span className="stream-cursor" />}
          </p>
        )}
        {!message.pending && <span className="bubble-time">{formatTime(message.timestamp)}</span>}
      </div>
    </div>
  );
}
