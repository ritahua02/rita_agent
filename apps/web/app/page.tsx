'use client';

import { useEffect, useState } from 'react';

import AvatarPanel from '@/components/AvatarPanel';
import ChatPanel from '@/components/ChatPanel';
import InspectorPanel from '@/components/InspectorPanel';
import StatusPanel from '@/components/StatusPanel';
import { ChatRequestError, streamChatMessage } from '@/lib/api/chat';
import { getSessionId, resetSessionId } from '@/lib/session';
import type { AvatarAction, ChatMessage, DebugInfo, RitaState } from '@/types/chat';

const DEFAULT_STATE: RitaState = {
  emotion: 'calm',
  relationship_mode: 'boundary_aware',
  current_goal: 'respond',
  initiative_level: 0.3,
  boundary_sensitivity: 0.8
};

const DEFAULT_AVATAR_ACTION: AvatarAction = {
  expression: 'soft_smile',
  motion: null,
  speaking: false
};

let messageIdSeed = 0;
function createMessageId() {
  messageIdSeed += 1;
  return `msg-${Date.now()}-${messageIdSeed}`;
}

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: createMessageId(),
      role: 'system',
      text: '你现在连接的是 Rita 的真实后端，她会读取自己的自我模型和长期记忆来回应你。',
      timestamp: Date.now()
    }
  ]);
  const [ritaState, setRitaState] = useState<RitaState>(DEFAULT_STATE);
  const [avatarAction, setAvatarAction] = useState<AvatarAction>(DEFAULT_AVATAR_ACTION);
  const [isSending, setIsSending] = useState(false);
  const [errorText, setErrorText] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string>('');
  const [debugInfo, setDebugInfo] = useState<DebugInfo>({
    sessionId: null,
    stateReason: null,
    stateSignal: null,
    historyTurns: null,
    model: null,
    selfModelSources: [],
    memorySources: [],
    memoryCandidates: []
  });

  useEffect(() => {
    setSessionId(getSessionId());
  }, []);

  const handleResetSession = () => {
    const nextId = resetSessionId();
    setSessionId(nextId);
    setRitaState(DEFAULT_STATE);
    setAvatarAction(DEFAULT_AVATAR_ACTION);
    setDebugInfo({
      sessionId: nextId,
      stateReason: null,
      stateSignal: null,
      historyTurns: null,
      model: null,
      selfModelSources: [],
      memorySources: [],
      memoryCandidates: []
    });
    setMessages([
      {
        id: createMessageId(),
        role: 'system',
        text: '已开启新的会话，Rita 不会再带着上一段对话的上下文。',
        timestamp: Date.now()
      }
    ]);
  };

  const handleSend = async (text: string) => {
    const userMessage: ChatMessage = {
      id: createMessageId(),
      role: 'user',
      text,
      timestamp: Date.now()
    };
    const pendingId = createMessageId();
    const pendingMessage: ChatMessage = {
      id: pendingId,
      role: 'rita',
      text: '',
      timestamp: Date.now(),
      pending: true
    };

    setMessages((prev) => [...prev, userMessage, pendingMessage]);
    setErrorText(null);
    setIsSending(true);

    let streamStarted = false;
    let streamFailed = false;

    try {
      await streamChatMessage(
        text,
        (event) => {
          switch (event.type) {
            case 'meta':
              setRitaState(event.state);
              setAvatarAction(event.avatar_action);
              setSessionId(event.session_id);
              setDebugInfo((prev) => ({
                ...prev,
                sessionId: event.session_id,
                stateReason: event.state_reason,
                stateSignal: event.state_signal
              }));
              break;
            case 'delta':
              streamStarted = true;
              setMessages((prev) =>
                prev.map((message) =>
                  message.id === pendingId
                    ? { ...message, text: message.text + event.text, pending: false }
                    : message
                )
              );
              break;
            case 'memory':
              setDebugInfo((prev) => ({
                ...prev,
                memoryCandidates: [...prev.memoryCandidates, ...event.memory_candidates]
              }));
              break;
            case 'done':
              setMessages((prev) =>
                prev.map((message) =>
                  message.id === pendingId
                    ? { ...message, text: event.reply_text || message.text, pending: false, timestamp: Date.now() }
                    : message
                )
              );
              setAvatarAction((prev) => ({ ...prev, speaking: false }));
              setDebugInfo((prev) => ({
                ...prev,
                sessionId: event.session_id,
                model: (event.debug?.model as string) ?? prev.model,
                historyTurns: (event.debug?.history_turns as number) ?? prev.historyTurns,
                selfModelSources: (event.debug?.self_model_sources as string[]) ?? prev.selfModelSources,
                memorySources: (event.debug?.memory_sources as string[]) ?? prev.memorySources,
                stateReason: (event.debug?.state_reason as string) ?? prev.stateReason,
                stateSignal: (event.debug?.state_signal as string) ?? prev.stateSignal
              }));
              break;
            case 'error':
              streamFailed = true;
              setErrorText(event.message || 'Rita 暂时没有回应，请稍后再试。');
              setMessages((prev) =>
                prev.map((item) =>
                  item.id === pendingId
                    ? {
                        ...item,
                        text: streamStarted ? item.text : '（这句话好像没有传到 Rita 那里……）',
                        pending: false,
                        error: !streamStarted
                      }
                    : item
                )
              );
              setAvatarAction((prev) => ({ ...prev, speaking: false }));
              break;
          }
        },
        sessionId
      );
    } catch (error) {
      if (!streamFailed) {
        const message = error instanceof ChatRequestError ? error.message : 'Rita 暂时没有回应，请稍后再试。';
        setErrorText(message);
        setMessages((prev) =>
          prev.map((item) =>
            item.id === pendingId
              ? {
                  ...item,
                  text: streamStarted ? item.text : '（这句话好像没有传到 Rita 那里……）',
                  pending: false,
                  error: !streamStarted
                }
              : item
          )
        );
        setAvatarAction((prev) => ({ ...prev, speaking: false }));
      }
    } finally {
      setIsSending(false);
    }
  };

  return (
    <main className="page">
      <section className="panel avatar-column">
        <AvatarPanel state={ritaState} avatarAction={avatarAction} isThinking={isSending} />
        <StatusPanel state={ritaState} />
      </section>

      <section className="panel chat-column">
        <ChatPanel messages={messages} onSend={handleSend} isSending={isSending} errorText={errorText} />
      </section>

      <InspectorPanel debugInfo={debugInfo} onResetSession={handleResetSession} />
    </main>
  );
}
