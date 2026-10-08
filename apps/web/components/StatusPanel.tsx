'use client';

import type { RitaState } from '@/types/chat';

const RELATIONSHIP_LABEL: Record<string, string> = {
  boundary_aware: '边界感知',
  warming_up: '逐渐熟悉',
  close: '亲密',
  playful: '轻松调侃'
};

function MeterRow({ label, value }: { label: string; value: number }) {
  const percent = Math.round(Math.min(Math.max(value, 0), 1) * 100);
  return (
    <div className="meter-row">
      <div className="meter-row-header">
        <span>{label}</span>
        <span className="meter-value">{percent}%</span>
      </div>
      <div className="meter-track">
        <div className="meter-fill" style={{ width: `${percent}%` }} />
      </div>
    </div>
  );
}

interface StatusPanelProps {
  state: RitaState;
}

export default function StatusPanel({ state }: StatusPanelProps) {
  return (
    <div className="status-card">
      <p className="label">当前状态</p>

      <div className="status-badges">
        <span className="badge badge-emotion">{state.emotion}</span>
        <span className="badge badge-relation">
          {RELATIONSHIP_LABEL[state.relationship_mode] ?? state.relationship_mode}
        </span>
      </div>

      <p className="status-goal">
        <span className="label-inline">当前目标</span>
        {state.current_goal}
      </p>

      <MeterRow label="主动程度" value={state.initiative_level} />
      <MeterRow label="边界敏感度" value={state.boundary_sensitivity} />
    </div>
  );
}
