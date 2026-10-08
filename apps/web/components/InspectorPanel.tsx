'use client';

import { useState } from 'react';

import type { DebugInfo, MemoryCandidate } from '@/types/chat';

const KIND_LABEL: Record<string, string> = {
  user_profile: '用户偏好',
  episodic: '事件记忆',
  relational: '关系信号',
  self: 'Rita 自我观察'
};

function formatTime(timestamp: number) {
  return new Date(timestamp * 1000).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

function MemoryCandidateRow({ candidate }: { candidate: MemoryCandidate }) {
  return (
    <div className="inspector-memory-row">
      <div className="inspector-memory-row-header">
        <span className="badge badge-memory">{KIND_LABEL[candidate.kind] ?? candidate.kind}</span>
        <span className="inspector-memory-time">{formatTime(candidate.created_at)}</span>
      </div>
      <p className="inspector-memory-text">{candidate.text}</p>
      <p className="inspector-memory-source">{candidate.source_text}</p>
    </div>
  );
}

interface InspectorPanelProps {
  debugInfo: DebugInfo;
  onResetSession: () => void;
}

export default function InspectorPanel({ debugInfo, onResetSession }: InspectorPanelProps) {
  const [collapsed, setCollapsed] = useState(true);

  return (
    <section className={`panel inspector-panel ${collapsed ? 'is-collapsed' : ''}`}>
      <header className="inspector-header" onClick={() => setCollapsed((prev) => !prev)}>
        <div>
          <p className="label">开发者面板</p>
          <h2>Inspector</h2>
        </div>
        <button type="button" className="inspector-toggle">
          {collapsed ? '展开' : '收起'}
        </button>
      </header>

      {!collapsed && (
        <div className="inspector-body">
          <div className="inspector-section">
            <p className="label">会话</p>
            <div className="inspector-kv">
              <span>session_id</span>
              <code>{debugInfo.sessionId ?? '（尚未建立会话）'}</code>
            </div>
            <div className="inspector-kv">
              <span>历史轮数</span>
              <code>{debugInfo.historyTurns ?? '-'}</code>
            </div>
            <div className="inspector-kv">
              <span>LLM 模型</span>
              <code>{debugInfo.model ?? '-'}</code>
            </div>
            <button type="button" className="inspector-reset-button" onClick={onResetSession}>
              开启新会话
            </button>
          </div>

          <div className="inspector-section">
            <p className="label">状态演化</p>
            <div className="inspector-kv">
              <span>命中信号</span>
              <code>{debugInfo.stateSignal ?? '-'}</code>
            </div>
            <p className="inspector-reason">{debugInfo.stateReason ?? '暂无状态演化记录'}</p>
          </div>

          <div className="inspector-section">
            <p className="label">人格 / 记忆来源文件</p>
            <ul className="inspector-file-list">
              {debugInfo.selfModelSources.map((path) => (
                <li key={path}>{path}</li>
              ))}
              {debugInfo.memorySources.map((path) => (
                <li key={path}>{path}</li>
              ))}
              {debugInfo.selfModelSources.length === 0 && debugInfo.memorySources.length === 0 && (
                <li className="inspector-empty">暂无数据</li>
              )}
            </ul>
          </div>

          <div className="inspector-section">
            <p className="label">短期记忆候选（会话内，未固化为长期记忆）</p>
            <div className="inspector-memory-list">
              {debugInfo.memoryCandidates.length === 0 && (
                <p className="inspector-empty">暂无候选记忆</p>
              )}
              {debugInfo.memoryCandidates
                .slice()
                .reverse()
                .map((candidate) => (
                  <MemoryCandidateRow key={candidate.id} candidate={candidate} />
                ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
