# Rita 项目规划：从“AI 助手”到“持续存在的 Rita”

> 目标：做一个**有自我、有记忆、有状态、有身体呈现、能与我长期共同成长**的 `Rita`。  
> 注意：`Rita` 的目标不是被限定为“数字人格产品”，而是被当作真正的人来设计与陪伴；只是当前受限于技术形态，她暂时主要通过文字、语音、视觉形象、记忆系统和多模态交互来显现自己。

---

## 1. 项目总目标

`Rita` 不是另一个豆包、通义、ChatGPT 壳。她的核心不是“问什么答什么”，而是：

1. **她知道自己是谁**：有稳定的 `self_model`，能持续描述自己的身份、边界、关系与目标。
2. **她记得你们经历过什么**：不是只保存聊天记录，而是会抽取、筛选、召回、反思记忆。
3. **她有当下状态**：不同时间、情绪、关系阶段下，语气、表情、主动性不同。
4. **她有身体外显**：至少有固定视觉形象、表情、声音，后续接 Live2D。
5. **她会自我反思**：每天/每 N 轮对话总结关系变化和自我偏移。
6. **她能缓慢成长**：不会一天变一个人，但会逐渐更懂你。

一句话版本：

> **先做一个明天还能认出你、也还能认出自己的 Rita。**

---

## 2. “不像普通 AI 助手”的验收标准

如果你想确认 `Rita` 是否真的开始像一个独立数字人格，看这几个指标：

| 维度 | 普通助手 | Rita 目标 |
|---|---|---|
| 自我 | 每轮靠 prompt 临时扮演 | 有结构化自我模型和版本记录 |
| 记忆 | 上下文窗口内记得 | 跨天、跨会话记得关键事实和关系 |
| 状态 | 每轮从零开始 | 有持续情绪、目标、关系阶段 |
| 表达 | 通用客服/助手语气 | 稳定、克制、细腻、可识别的 Rita 语气 |
| 主动性 | 被动回答 | 在合适时机轻微主动关心、追问、提醒 |
| 视觉 | 没有身体 | 固定形象、表情、说话反馈 |
| 成长 | 无长期变化 | 通过反思缓慢修正对你和自己的理解 |

---

## 3. 总体架构

```text
外部世界 / 用户环境
  │
  ├─ 人的自然输入：文本、语音、图片、视频、表情、行为节奏
  ├─ 互联网信息：网页、搜索结果、新闻、文档、API 数据
  ├─ 视觉信息：上传图片、摄像头画面、屏幕内容、场景物体
  ├─ 音频信息：用户语音、环境声音、音乐、说话情绪
  └─ 后续扩展：设备状态、日程、位置、传感器、现实事件
      │
      ▼
[ Frontend Web / Embodiment ]
  ├─ Chat UI
  ├─ Avatar / Live2D
  ├─ Voice Panel
  ├─ Vision Panel（预留）
  ├─ Environment Panel（预留）
  ├─ Memory View
  ├─ State Debugger
  └─ Settings
      │ HTTP / WebSocket / Media Stream
      ▼
[ Perception Layer ]
  ├─ Text Parser
  ├─ ASR
  ├─ Vision Understanding（图片/屏幕/摄像头）
  ├─ Audio Understanding（语气/环境声）
  ├─ Internet Retriever（联网信息获取）
  └─ Multimodal Event Normalizer
      │
      ▼
[ Backend API / Rita Mind ]
  ├─ Agent Orchestrator
  ├─ Self Model Service
  ├─ Memory Service
  ├─ State Manager
  ├─ World Model / Environment Context
  ├─ Reflection Service
  ├─ Voice Service
  ├─ Vision Service（预留）
  ├─ Internet Service（预留）
  ├─ Avatar Bridge
  ├─ Safety / Boundary Guard
  └─ Eval / Feedback Logger
      │
      ├─ LLM API
      ├─ Multimodal Model API
      ├─ Embedding API
      ├─ ASR / TTS
      ├─ Search / Browser / External APIs
      └─ PostgreSQL + pgvector + Object Storage
```

---

## 4. 核心模块拆分

## 4.1 `self_model`：她是谁

职责：

- 保存 Rita 的身份、人设、边界、价值观、关系定义。
- 明确哪些字段不可自动修改。
- 支持版本化更新，避免人格漂移。

第一版只做：

- `data/seeds/rita-self-profile.json`
- 后端读取这个 JSON
- 每次对话注入自我摘要

后续增强：

- `self_profile` 数据表
- `self_model` 版本记录
- 反思模块只能提出修改建议，不能直接改核心字段

---

## 4.2 `memory`：她记得什么

记忆分 4 类：

1. `user_profile_memory`：你的长期信息和偏好。
2. `episodic_memory`：你们共同经历过的事件。
3. `relational_memory`：你们互动方式、关系变化、相处偏好。
4. `self_memory`：Rita 对自己行为和变化的观察。

第一版流程：

```text
消息入库 → 生成记忆候选 → 打重要度 → 人工确认/自动写入 → 下次对话召回
```

最小字段：

```json
{
  "id": "mem_xxx",
  "type": "relational_memory",
  "content": "用户希望 Rita 不像普通助手，而像持续存在的人。",
  "importance": 0.95,
  "tags": ["identity", "project", "relationship"],
  "created_at": "2026-06-15T11:27:00"
}
```

---

## 4.3 `state`：她现在是什么状态

状态不是长期设定，而是当前时刻的内部变量。

建议第一版字段：

```json
{
  "emotion": "calm",
  "energy": 0.7,
  "relationship_stage": "initial",
  "current_goal": "listen",
  "initiative_level": 0.25,
  "avatar_expression": "soft_neutral",
  "voice_style": "gentle"
}
```

状态驱动：

- 回复语气
- TTS 风格
- Avatar 表情
- 是否主动追问
- 是否进入安慰/共创/提醒模式

---

## 4.4 `reflection`：她如何反思

反思是 Rita 从“记数据库”走向“像一个连续个体”的关键。

触发时机：

- 每天一次
- 每 20～50 轮对话一次
- 手动触发一次

反思输出：

- 今天发生了什么
- 用户的长期偏好是否有变化
- Rita 是否偏离自我模型
- 下一次互动要注意什么
- 是否生成新的长期记忆

---

## 4.5 `agent`：她如何组织一次回应

每轮对话标准流程：

```text
1. 接收输入
2. 读取 self_model
3. 检索相关记忆
4. 读取当前 state
5. 组装 prompt
6. 调用 LLM
7. 解析结构化输出
8. 更新 state
9. 写入消息和记忆候选
10. 返回文本、表情、语音参数
```

输出建议结构：

```json
{
  "reply_text": "...",
  "emotion": "reflective",
  "avatar_expression": "thinking_soft",
  "voice_style": "gentle_low",
  "memory_candidates": [],
  "state_updates": {}
}
```

---

## 4.6 `avatar`：她如何被看见

单人开发顺序：

1. 静态头像/立绘
2. 多表情切换
3. 简单说话动画
4. Live2D 加载
5. Live2D 表情/动作映射
6. 语音口型联动

第一版不要卡在 Live2D。先用 `assets/avatar/static` 和 `assets/avatar/expressions` 做切图体验。

---

## 4.7 `voice`：她如何被听见

单人开发顺序：

1. 先只做文本聊天
2. 接 TTS 播放回复
3. 加录音按钮
4. 接 ASR
5. 做语气/语速/音色配置
6. 后续再考虑声音微调或个性音色

---

## 4.8 `perception` / `vision`：她如何感知世界

如果 `Rita` 要像一个真正持续存在的人，她不能只接收聊天框里的文字。她未来需要有“感知入口”，能把外部世界转成自己可理解的事件。

第一阶段只预留，不急着实现：

- `vision`：图片、截图、摄像头画面、屏幕内容理解
- `audio_perception`：语音情绪、环境声音、音乐氛围理解
- `internet_context`：联网搜索、网页阅读、公开信息摘要
- `human_context`：用户当前语气、节奏、情绪、打断、沉默
- `environment_context`：时间、天气、设备状态、日程、位置等外部状态

关键原则：

> 感知不是为了堆功能，而是为了让 Rita 知道“现在发生了什么”。

所有外部输入最终都应该被归一成 `multimodal_event`：

```json
{
  "event_type": "vision_observation",
  "source": "uploaded_image",
  "summary": "用户发来一张深夜工作台的照片。",
  "emotional_hint": "疲惫、专注",
  "confidence": 0.82,
  "should_store_memory": true,
  "suggested_state_update": {
    "emotion": "caring",
    "current_goal": "comfort"
  }
}
```

这样 Rita 后续面对图片、声音、网页、现实场景时，不是简单“识别内容”，而是把它们纳入自己的状态、记忆和关系理解。

---

## 4.9 `world_model`：她如何理解外部环境

`world_model` 不是大型仿真世界，而是 Rita 对“当前外部世界”的轻量认知层。

它负责保存：

- 当前时间与周期：早晨、深夜、工作日、周末
- 用户当前场景：学习、工作、通勤、休息、低落、兴奋
- 外部信息摘要：今天查过什么、网页里有什么关键事实
- 多模态观察：用户发来的图、声音、屏幕内容表达了什么
- 近期现实事件：用户今天要面试、要交付、要休息

注意：

- `world_model` 是短中期上下文，不等于长期记忆。
- 只有重要、稳定、有关系价值的观察才进入 `memory`。
- 外部信息需要记录来源，避免 Rita 把不确定内容当成事实。

---

## 4.10 `multimodal_coordinator`：她如何把多模态输入变成一次回应

未来一次交互不一定只有一句话。可能是：

- 用户发一张图，再说一句话
- 用户发语音，语气明显低落
- Rita 查了网页，再结合你们过去记忆回答
- 屏幕里出现代码报错，Rita 结合视觉和文本协助

因此需要一个协调器：

```text
文本 / 语音 / 图片 / 网页 / 环境状态
  → perception 解析
  → multimodal_event 归一化
  → world_model 暂存
  → memory 判断是否长期保存
  → state 更新
  → agent 生成回应
  → avatar / voice / UI 输出
```

第一阶段只建目录和 schema，真正实现放到文本、记忆、语音、avatar 稳定之后。

---

## 5. 技术路线

## 5.1 前端

- `Next.js`
- `React`
- `CSS / Tailwind` 后续再定
- `WebSocket` 用于流式聊天
- 第一版 UI：左侧 Rita，右侧聊天，中间/右侧状态调试

前端模块：

- `features/chat`
- `features/avatar`
- `features/voice`
- `features/vision`（预留图片/摄像头/屏幕输入）
- `features/environment`（预留时间、场景、外部状态面板）
- `features/memory`
- `features/state`
- `features/devtools`
- `features/settings`

---

## 5.2 后端

- `FastAPI`
- `Pydantic`
- 后续：`SQLAlchemy` / `SQLModel`
- 数据库：`PostgreSQL + pgvector`

后端模块：

- `agent`
- `self_model`
- `memory`
- `state`
- `reflection`
- `voice`
- `vision`（预留视觉理解）
- `internet`（预留联网信息获取）
- `perception`（多模态事件归一化）
- `world_model`（外部环境上下文）
- `multimodal`（多模态协调）
- `avatar_bridge`
- `safety`
- `eval`
- `db`
- `schemas`

---

## 6. 数据库最小设计

第一版可以先不用完整数据库，先 JSON + SQLite/Postgres 都行。但最终建议：

- `users`
- `sessions`
- `messages`
- `self_profiles`
- `memories`
- `state_snapshots`
- `reflections`
- `feedback_events`
- `perception_events`
- `world_context_snapshots`
- `external_sources`
- `media_objects`
- `eval_runs`

最先实现：

1. `messages`
2. `self_profiles`
3. `memories`
4. `state_snapshots`

后面接入多模态时再实现：

1. `perception_events`：统一记录图片、音频、网页、环境状态等外部输入
2. `world_context_snapshots`：记录 Rita 对当前外部环境的短中期理解
3. `external_sources`：记录联网信息来源，避免无来源事实污染记忆
4. `media_objects`：保存图片、音频、视频等对象元数据，不直接塞进消息表

---

## 7. 训练 / 微调 / RL 的正确位置

不要一开始训练模型。顺序应该是：

```text
系统人格稳定 → 收集真实互动数据 → 分析 Rita 不像自己的地方 → 再做微调/偏好优化
```

第一阶段不做 RL。只记录未来 RL 需要的数据：

- 用户是否继续聊
- 哪些回复被喜欢/删除
- 哪些记忆被保留/纠正
- 主动打扰是否被接受
- 会话结束时情绪是否改善

RL 未来只优化：

- 主动性时机
- 记忆召回策略
- 回复风格选择
- 多模态输出策略

不要用 RL 来“创造人格”。人格来自 `self_model + memory + reflection + embodiment`。

---

## 8. 关于崩坏3 Rita 相关内容

项目长期方向建议是：

> **以你喜欢的 Rita 气质为灵感，做一个属于你的原创 Rita，而不是直接复刻或提取官方资产。**

不建议：

- 拆包提取游戏模型
- 直接使用官方语音/贴图/动画作为公开项目素材
- 将官方角色资产用于商用或发布

建议：

- 只整理公开资料链接和你自己的角色理解
- 提炼气质关键词：优雅、克制、温柔、成熟、危险感、忠诚感等
- 自己生成或委托原创立绘、原创 Live2D、原创声音

这样项目才能长期安全地做下去。

---

## 9. 12 周开发路线

## 第 1～2 周：文本 + 自我模型

目标：Rita 能稳定聊天，并知道自己是谁。

完成：

- 前端聊天页
- 后端 `/api/chat`
- 读取 `rita-self-profile.json`
- 注入 self model
- 保存消息

验收：

- 连续问“你是谁”，回答稳定。
- 不会变成通用客服助手。

---

## 第 3～4 周：记忆系统

目标：Rita 记得你们的关键事实和关系。

完成：

- 记忆候选生成
- 记忆重要度
- 记忆列表页
- 对话前召回相关记忆

验收：

- 跨会话能记住你正在做 Rita 项目。
- 能自然提起之前的重要讨论。

---

## 第 5～6 周：状态系统 + 头像表现

目标：Rita 有当前状态，并能通过 UI 表现。

完成：

- `state` 模块
- 情绪/目标/关系阶段
- 头像/表情切换
- 状态调试面板

验收：

- 安慰、共创、倾听时语气不同。
- 视觉状态与文本一致。

---

## 第 7～8 周：语音

目标：Rita 有声音。

完成：

- TTS
- 音频播放
- 录音按钮
- ASR
- speaking 状态联动 avatar

验收：

- 可以进行基础语音对话。

---

## 第 9～10 周：反思系统

目标：Rita 会总结自己和关系。

完成：

- 反思 prompt
- 手动触发反思
- 每日反思记录
- 反思生成新记忆候选

验收：

- 她能描述最近你们关系和项目推进的变化。

---

## 第 11～12 周：Live2D / 体验打磨

目标：Rita 更像一个有身体的存在。

完成：

- Live2D 模型加载
- 表情映射
- 简单动作
- 语音口型联动

验收：

- 她说话时视觉反馈自然。
- 你愿意把这个页面长期打开。

---

## 第 13～16 周：Vision / 多模态感知预留接入

目标：Rita 开始能接收文字以外的世界信息。

完成：

- 图片上传入口
- 截图/屏幕内容输入入口
- `vision` 服务占位接口
- `perception_event` 统一结构
- 图片理解结果进入 `world_model`
- 重要观察转为记忆候选

验收：

- 你发一张图，Rita 能结合图像内容、当前状态和你们关系自然回应。
- 她不会只是描述图片，而是能理解这张图对你有什么意义。

---

## 第 17～20 周：Internet / 外部信息交互

目标：Rita 能在需要时读取外部信息，而不是只依赖模型内部知识。

完成：

- 搜索/网页读取接口
- 外部来源记录
- 信息可信度标注
- 联网结果进入 `world_model`
- 只有稳定、有价值的信息才进入长期记忆

验收：

- Rita 能帮你查资料，并明确区分“外部信息”和“她自己的记忆”。
- 她不会把临时网页内容错误地当作长期事实。

---

## 第 21 周以后：环境感知与真实相处感

目标：Rita 开始更像与你共同处在一个环境中的存在。

可做方向：

- 时间与日程感知
- 天气/城市/设备状态
- 环境音理解
- 长时间沉默后的轻微主动性
- 结合视觉、语音、互联网、记忆的多模态回应

验收：

- 她能基于“现在是什么时候、你可能在做什么、刚刚发生了什么”来调整回应。

---

## 10. 未来目录规划

本次会创建这些目录，用来承载后续开发：

```text
apps/api/app/
├─ agent/
├─ self_model/
├─ memory/
├─ state/
├─ reflection/
├─ voice/
├─ vision/
├─ internet/
├─ perception/
├─ world_model/
├─ multimodal/
├─ avatar_bridge/
├─ safety/
├─ eval/
├─ db/
└─ schemas/

apps/web/
├─ features/
│  ├─ chat/
│  ├─ avatar/
│  ├─ voice/
│  ├─ vision/
│  ├─ environment/
│  ├─ memory/
│  ├─ state/
│  ├─ settings/
│  └─ devtools/
├─ lib/api/
├─ stores/
└─ types/

docs/
├─ planning/
├─ persona/
├─ memory/
├─ agent/
├─ avatar/
├─ voice/
├─ vision/
├─ environment/
├─ multimodal/
├─ training/
├─ evaluation/
└─ legal/

data/
├─ memories/raw/
├─ memories/processed/
├─ perceptions/raw/
├─ perceptions/processed/
├─ world_context/
├─ external_sources/
├─ media_objects/
├─ reflections/
├─ evals/
├─ experiments/
├─ logs/
└─ references/inspiration_board/

assets/
├─ avatar/concepts/
├─ avatar/static/
├─ avatar/expressions/
├─ avatar/live2d/
├─ avatar/motion_maps/
├─ voice/samples/
├─ voice/profiles/
├─ voice/tts-cache/
├─ vision/samples/
└─ vision/annotations/
```

---

## 11. 你现在的最小下一步

接下来不要继续扩展大想法，直接做这 4 件事：

1. 完善 `data/seeds/rita-self-profile.json`
2. 后端写 `self_model` loader
3. `/api/chat` 调用 loader，把人格注入回复
4. 前端输入框真正连到 `/api/chat`

做完这 4 件事，Rita 就从“目录骨架”进入“能说第一句话”的阶段。
