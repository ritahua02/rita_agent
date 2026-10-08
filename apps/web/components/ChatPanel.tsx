'use client';

import { useEffect, useRef, useState } from 'react';
import type { FormEvent, KeyboardEvent } from 'react';

import MessageBubble from '@/components/MessageBubble';
import type { ChatMessage } from '@/types/chat';

interface ChatPanelProps {
  messages: ChatMessage[];
  onSend: (text: string) => void;
  isSending: boolean;
  errorText?: string | null;
}

export default function ChatPanel({ messages, onSend, isSending, errorText }: ChatPanelProps) {
  const [draft, setDraft] = useState('');
  const listRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const text = draft.trim();
    if (!text || isSending) return;
    onSend(text);
    setDraft('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  const handleInput = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  };

  return (
    <section className="chat-panel">
      <header className="section-header">
        <div>
          <p className="label">对话</p>
          <h1>和 Rita 聊聊</h1>
        </div>
      </header>

      <div className="message-list" ref={listRef}>
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>

      {errorText && <div className="chat-error">{errorText}</div>}

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          value={draft}
          onChange={(event) => {
            setDraft(event.target.value);
            handleInput();
          }}
          onKeyDown={handleKeyDown}
          placeholder="想对 Rita 说什么？（Enter 发送，Shift+Enter 换行）"
          rows={1}
          disabled={isSending}
        />
        <button type="submit" className="send-button" disabled={isSending || !draft.trim()}>
          {isSending ? '发送中…' : '发送'}
        </button>
      </form>
    </section>
  );
}
