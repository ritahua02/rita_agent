'use client';

import type { AvatarAction, RitaState } from '@/types/chat';

const EXPRESSION_EMOJI: Record<string, string> = {
  soft_smile: '🙂',
  gentle_tease: '😏',
  warm: '😊',
  curious: '🤔',
  shy: '😳',
  concerned: '😟',
  calm: '😌'
};

interface AvatarPanelProps {
  state: RitaState;
  avatarAction: AvatarAction;
  isThinking: boolean;
}

export default function AvatarPanel({ state, avatarAction, isThinking }: AvatarPanelProps) {
  const emoji = EXPRESSION_EMOJI[avatarAction.expression] ?? '🙂';

  return (
    <div className="avatar-panel">
      <div
        className={[
          'avatar-orb',
          avatarAction.speaking ? 'is-speaking' : '',
          isThinking ? 'is-thinking' : ''
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <span className="avatar-orb-emoji">{emoji}</span>
        <span className="avatar-orb-ring" />
        <span className="avatar-orb-ring avatar-orb-ring-delay" />
      </div>

      <div className="avatar-name-block">
        <h2>Rita</h2>
        <p className="avatar-expression-label">{avatarAction.expression.replaceAll('_', ' ')}</p>
      </div>

      <div className="avatar-hint">
        <p className="label">当前动作</p>
        <p>
          {isThinking
            ? '正在思考要怎么回应你…'
            : avatarAction.speaking
              ? '正在对你说话'
              : avatarAction.motion
                ? avatarAction.motion
                : '安静地看着你，等你开口'}
        </p>
      </div>
    </div>
  );
}
