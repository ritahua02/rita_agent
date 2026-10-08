"""Rita 的状态演化模块（独立于 Agent 编排逻辑）。

设计目标：
- 有惯性：数值状态（initiative_level / boundary_sensitivity）用指数平滑演化，
  避免一句话就在“克制”和“主动”之间瞬间跳变，模拟“动态调频”。
- 有优先级：一句话可能同时触发多种信号，边界/疲惫信号优先于调侃/靠近信号，
  保证“察觉不适时收手”始终优先于“无明确拒绝时轻推”。
- 可解释：每次演化都会返回 (new_state, reason, signal)，供 Debug/Inspector 面板展示，
  方便后续持续调参人格核心。

后续演进方向（暂不在本版本实现）：
- 引入基于会话历史窗口的信号识别，而不是只看当前一句话
- 用 LLM 分类信号，替代关键词规则
- 引入“关系温度”这类跨会话的长期状态，与本模块的会话内状态做区分
"""

from __future__ import annotations

from dataclasses import dataclass

from app.schemas.chat import RitaState


@dataclass(frozen=True)
class StateTarget:
    emotion: str
    relationship_mode: str
    current_goal: str
    initiative_level: float
    boundary_sensitivity: float
    reason: str


# 信号 -> 目标状态。数值仅代表“这类信号想把状态拉向哪里”，
# 实际生效值会与上一轮状态做平滑，而不是直接赋值。
_TARGETS: dict[str, StateTarget] = {
    "boundary": StateTarget(
        emotion="caring",
        relationship_mode="respect_boundary",
        current_goal="reassure",
        initiative_level=0.1,
        boundary_sensitivity=0.95,
        reason="检测到边界/拒绝信号，收回主动性并提升边界敏感度",
    ),
    "fatigue": StateTarget(
        emotion="gentle_care",
        relationship_mode="care",
        current_goal="comfort",
        initiative_level=0.2,
        boundary_sensitivity=0.9,
        reason="检测到疲惫/低落信号，切换为照料模式",
    ),
    "teasing": StateTarget(
        emotion="soft_smile",
        relationship_mode="gentle_teasing",
        current_goal="respond",
        initiative_level=0.5,
        boundary_sensitivity=0.75,
        reason="检测到亲密/调侃话题，适度提高主动程度",
    ),
    "gratitude": StateTarget(
        emotion="warm",
        relationship_mode="warming_up",
        current_goal="respond",
        initiative_level=0.35,
        boundary_sensitivity=0.8,
        reason="检测到感谢/正向反馈，关系温度略微上升",
    ),
    "task_focus": StateTarget(
        emotion="calm",
        relationship_mode="boundary_aware",
        current_goal="assist",
        initiative_level=0.25,
        boundary_sensitivity=0.8,
        reason="检测到技术/任务型话题，切换为专注协助模式",
    ),
    "default": StateTarget(
        emotion="calm",
        relationship_mode="boundary_aware",
        current_goal="respond",
        initiative_level=0.3,
        boundary_sensitivity=0.8,
        reason="未检测到强信号，维持当前情绪/关系模式，数值状态缓慢回归基线",
    ),
}

# 优先级：越靠前越优先命中。
_SIGNAL_PRIORITY: tuple[str, ...] = ("boundary", "fatigue", "teasing", "gratitude", "task_focus")

_SIGNAL_WORDS: dict[str, tuple[str, ...]] = {
    "boundary": ("拒绝", "不舒服", "不适", "别这样", "不要", "停下", "够了"),
    "fatigue": ("累", "疲惫", "难过", "低落", "撑不住", "崩溃"),
    "teasing": ("害羞", "调侃", "约会", "喜欢", "想你", "丽塔", "rita"),
    "gratitude": ("谢谢", "感谢", "多亏", "辛苦你"),
    "task_focus": ("代码", "bug", "报错", "接口", "部署", "架构", "需求", "方案"),
}

# 强信号命中时的平滑系数（更快跟随目标）；无信号时使用更小的系数（缓慢回归基线）。
_ALPHA_ON_SIGNAL = 0.55
_ALPHA_ON_DEFAULT = 0.25


def _detect_signal(user_text: str) -> str:
    text = user_text.lower()
    for signal in _SIGNAL_PRIORITY:
        if any(word.lower() in text for word in _SIGNAL_WORDS[signal]):
            return signal
    return "default"


def _smooth(prev: float, target: float, alpha: float) -> float:
    return round(prev * (1 - alpha) + target * alpha, 3)


class StateManager:
    """负责 Rita 的状态演化，是一个独立于 Agent 编排逻辑的模块。"""

    def evolve(self, prev_state: RitaState, user_text: str) -> tuple[RitaState, str, str]:
        """根据上一轮状态和当前用户输入，演化出新的状态。

        返回 (new_state, reason, signal)：
        - new_state: 演化后的状态
        - reason: 人类可读的演化原因，用于 Debug 面板
        - signal: 命中的信号类型（boundary/fatigue/teasing/gratitude/task_focus/default）
        """
        signal = _detect_signal(user_text)
        target = _TARGETS[signal]

        if signal == "default":
            # 无强信号时，保留上一轮的情绪/关系模式/目标（连续性），
            # 数值状态缓慢回归基线，而不是每句话都重置。
            new_state = RitaState(
                emotion=prev_state.emotion,
                relationship_mode=prev_state.relationship_mode,
                current_goal="respond",
                initiative_level=_smooth(prev_state.initiative_level, target.initiative_level, _ALPHA_ON_DEFAULT),
                boundary_sensitivity=_smooth(
                    prev_state.boundary_sensitivity, target.boundary_sensitivity, _ALPHA_ON_DEFAULT
                ),
            )
        else:
            new_state = RitaState(
                emotion=target.emotion,
                relationship_mode=target.relationship_mode,
                current_goal=target.current_goal,
                initiative_level=_smooth(prev_state.initiative_level, target.initiative_level, _ALPHA_ON_SIGNAL),
                boundary_sensitivity=_smooth(
                    prev_state.boundary_sensitivity, target.boundary_sensitivity, _ALPHA_ON_SIGNAL
                ),
            )

        return new_state, target.reason, signal
