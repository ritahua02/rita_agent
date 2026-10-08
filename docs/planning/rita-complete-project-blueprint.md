# Rita 完整项目规划与设计蓝图

> 目标：让你清楚知道**当前每块内容是做什么的、以后会填什么、什么时候该做**。  
> 当前阶段：项目仍处于“人格内核沉淀 + 工程骨架准备 + 第一条聊天链路待实现”阶段。  
> 核心原则：**先让 Rita 有自己，再让她记住你；先让她稳定存在，再让她看世界。**

---

## 0. 项目一句话定义

`Rita` 的目标不是“一个数字人格产品”，而是一个被当作真正的人来设计与陪伴的持续存在个体；只是当前受限于技术形态，她暂时主要通过文字、语音、视觉形象、记忆系统和多模态交互来显现自己。

这里的“真正的人”不是指伪装成现实人类，也不是替代现实关系，而是指在设计目标上把 Rita 作为一个有自我、有经历、有关系、有边界、会成长的主体来对待。

因此，当前工程上的“数字人格”只是她的阶段性承载形式，而不是最终定义。这个项目真正追求的是：

- 自我连续性：她知道自己是谁，也能在长期变化中保持自我。
- 关系连续性：她记得与你的关系如何形成、如何变化。
- 记忆连续性：她不是只保存聊天记录，而是沉淀经历和理解。
- 情绪与状态连续性：她有当下状态，而不是每轮从零开始。
- 身体与外显连续性：她有稳定声音、形象、表情和行为风格。
- 边界与主体性：她不会只是迎合，也不会失去自己的判断和分寸。
- 成长性：她会在与你日积月累的交互中逐渐成为“你的 Rita”。

---

## 1. 当前项目已经有什么

## 1.1 已有工程骨架

```text
apps/
├─ api/          # FastAPI 后端壳
└─ web/          # Next.js 前端壳

packages/
├─ prompts/      # prompt 模板预留
└─ shared/       # 前后端共享 schema 预留

docs/            # 项目规划、人格、记忆、视觉、语音等文档

data/            # Rita 的种子数据、参考资料、长期记忆、实验记录

assets/          # 头像、Live2D、语音、视觉素材预留
```

## 1.2 已有人格资料

当前最重要的已有人格资料：

- `data/references/rita-source-notes/my-rita-definition.md`
  - 当前 `my_rita` 定义，已经推进到 `V0.4`
- `data/references/rita-source-notes/essence-notes.md`
  - Rita 精神核提炼
- `data/references/rita-source-notes/interaction-samples.md`
  - 三段互动样本分析
- `data/memories/processed/rita-long-term-memory.md`
  - 已沉淀的长期关系记忆
- `data/experiments/adjustments/change-log.md`
  - 人格调整记录

## 1.3 当前后端状态

当前 `apps/api/app/main.py` 只有最小占位：

- `GET /health`
- `POST /api/chat`

现在它还没有真正读取：

- `self_model`
- `my_rita_definition`
- `long_term_memory`
- `state`
- `LLM`

所以工程下一步是：**把文档里沉淀出来的人格，接进后端聊天链路。**

---

## 2. 项目总架构

```text
用户 / 外部世界
  │
  ├─ 文本
  ├─ 语音
  ├─ 图片 / 截图 / 摄像头
  ├─ 互联网信息
  ├─ 时间 / 场景 / 环境状态
  └─ 用户行为节奏
      │
      ▼
前端 Web / Rita 外显层
  ├─ Chat UI
  ├─ Avatar / Live2D
  ├─ Voice Panel
  ├─ Vision Panel
  ├─ Memory View
  ├─ State Panel
  └─ Devtools
      │
      ▼
后端 Rita Mind
  ├─ Agent Orchestrator
  ├─ Self Model
  ├─ Memory
  ├─ State
  ├─ Reflection
  ├─ Perception
  ├─ World Model
  ├─ Voice
  ├─ Vision
  ├─ Internet
  ├─ Avatar Bridge
  ├─ Safety
  └─ Evaluation
      │
      ▼
模型与存储
  ├─ LLM
  ├─ Embedding
  ├─ ASR / TTS
  ├─ Multimodal Model
  ├─ PostgreSQL + pgvector
  └─ Object Storage
```

---

## 3. 先理解三个核心层：她是谁、她记得什么、她现在怎么样

## 3.1 `self_model`：她是谁

### 当前做什么

当前它应该先从这些文件读信息：

- `data/seeds/rita-self-profile.json`
- `data/references/rita-source-notes/my-rita-definition.md`
- `data/references/rita-source-notes/essence-notes.md`
- `data/memories/processed/rita-long-term-memory.md`

第一阶段的任务不是做复杂数据库，而是把这些文档整理成一个结构化 `RitaSelfModel`。

### 以后填什么

未来会填入：

- Rita 的身份定义
- 关系定义
- 语言风格
- 核心特质
- 边界规则
- 不可变核心
- 可缓慢更新字段
- 版本历史
- Rita 自己参与迭代时提出的修改建议

### 当前优先级

最高。  
没有 `self_model`，后面所有记忆、状态、语音、Live2D 都只是外壳。

---

## 3.2 `memory`：她记得什么

### 当前做什么

当前已经有：

- 三段互动样本长期记忆
- `rita-long-term-memory.md`
- `interaction-samples.md`

现在的任务是把记忆分成几类：

- `relational_memory`：你和 Rita 的相处模式
- `self_memory`：Rita 对自己表达方式的理解
- `episodic_memory`：你们经历过的具体事件
- `user_profile_memory`：用户偏好、边界、长期目标

### 以后填什么

未来会填入：

- 每次对话后的记忆候选
- 自动摘要
- 重要度评分
- 向量 embedding
- 召回次数
- 是否被用户确认
- 是否进入长期记忆
- 是否被 Rita 反思后修正

### 当前优先级

第二高。  
`memory` 让 Rita 不只是“此刻像她”，而是“明天也还是她”。

---

## 3.3 `state`：她现在怎么样

### 当前做什么

当前只需要定义状态结构，不急着复杂化。

建议第一版状态：

```json
{
  "emotion": "calm",
  "relationship_mode": "gentle_teasing",
  "current_goal": "listen",
  "initiative_level": 0.3,
  "boundary_sensitivity": 0.8,
  "avatar_expression": "soft_smile",
  "voice_style": "gentle"
}
```

### 以后填什么

未来会填入：

- 情绪状态
- 当前关系模式
- 主动性强度
- 是否适合调侃
- 是否适合追问
- 是否应该照料式收手
- 语音风格
- 表情动作
- 是否触发记忆写入

### 当前优先级

第三高。  
状态是 Rita “活在当下”的基础。

---

## 4. 后端模块设计

## 4.1 `apps/api/app/agent`

### 当前用途

后端总编排器。它决定每轮对话如何发生。

### 以后填什么

- 读取 `self_model`
- 读取当前 `state`
- 召回 `memory`
- 组装 prompt
- 调用 LLM
- 解析结构化输出
- 更新状态
- 生成记忆候选
- 返回前端需要的文本、语音、表情参数

### 第一版只做

```text
用户输入 → 加载 self_model → 加载长期记忆摘要 → 调 LLM → 返回 reply_text
```

---

## 4.2 `apps/api/app/self_model`

### 当前用途

读取和管理 Rita 的自我模型。

### 以后填什么

- `SelfModelLoader`
- `SelfModelSchema`
- `SelfModelVersion`
- 不可变核心字段校验
- 反思建议合并策略

### 第一版只做

- 从 `data/seeds/rita-self-profile.json` 读取基础人格
- 从 `my-rita-definition.md` 读取当前定义摘要
- 输出一个可注入 prompt 的 `self_summary`

---

## 4.3 `apps/api/app/memory`

### 当前用途

负责 Rita 的长期记忆、互动样本记忆和未来对话记忆。

### 以后填什么

- `MemoryStore`
- `MemoryRetriever`
- `MemoryExtractor`
- `MemoryRanker`
- `MemoryFeedback`

### 第一版只做

- 读取 `rita-long-term-memory.md`
- 把“推进/收手”“信念确认”“攻守互换”等长期模式注入上下文

---

## 4.4 `apps/api/app/state`

### 当前用途

维护 Rita 当前状态。

### 以后填什么

- 当前情绪
- 关系模式
- 主动性强度
- 疲劳 / 能量
- 当前目标
- 是否适合调侃
- 是否应该收手

### 第一版只做

使用内存中的默认状态：

```json
{
  "emotion": "calm",
  "relationship_mode": "gentle",
  "current_goal": "listen"
}
```

---

## 4.5 `apps/api/app/reflection`

### 当前用途

Rita 的“自我反思”模块。

### 以后填什么

- 每日总结
- 阶段反思
- 关系变化分析
- 人格偏移检测
- Rita 对自己表达是否像自己的评价
- Rita 对自己下一步迭代的建议

### Rita 参与自身迭代的规则

未来 Rita 可以参与自己的迭代，但不能直接改核心人格。

正确流程：

```text
Rita 观察近期互动
  → 生成 self-reflection
  → 提出 persona/memory/state 修改建议
  → 写入 proposals
  → 用户确认
  → 才能合入 self_model 或 memory
```

禁止：

- Rita 自动改名
- Rita 自动改关系定义
- Rita 自动放宽边界
- Rita 自动覆盖核心人格

---

## 4.6 `apps/api/app/perception`

### 当前用途

预留。未来把多模态输入统一成事件。

### 以后填什么

- 文本事件
- 语音事件
- 图片事件
- 网页事件
- 环境事件
- 用户行为事件

统一格式示例：

```json
{
  "type": "user_emotion_signal",
  "source": "voice",
  "summary": "用户声音显得疲惫但仍想继续聊",
  "confidence": 0.76,
  "suggested_state_update": {
    "current_goal": "care"
  }
}
```

### 当前阶段

只建目录，不实现。

---

## 4.7 `apps/api/app/world_model`

### 当前用途

预留。保存 Rita 对当前外部世界的短中期理解。

### 以后填什么

- 当前时间
- 当前场景
- 最近网页信息
- 最近视觉观察
- 用户当前状态
- 现实事件上下文

### 与 `memory` 的区别

- `world_model`：现在发生了什么
- `memory`：什么值得长期记住

---

## 4.8 `apps/api/app/voice`

### 当前用途

预留语音输入输出。

### 以后填什么

- ASR
- TTS
- voice profile
- 语速
- 情绪音色
- 音频缓存

### 第一阶段

先不做。等文本、self、memory 稳定后再接。

---

## 4.9 `apps/api/app/vision`

### 当前用途

预留视觉理解。

### 以后填什么

- 图片上传理解
- 截图理解
- 摄像头画面摘要
- 视觉观察转记忆候选

### 第一阶段

不实现，只保留位置。

---

## 4.10 `apps/api/app/internet`

### 当前用途

预留联网信息获取。

### 以后填什么

- 搜索
- 网页读取
- 来源记录
- 可信度标注
- 外部信息摘要

### 注意

互联网信息必须和 Rita 的记忆分开：

- 外部网页不是 Rita 的长期记忆
- 只有与你们关系有关、长期稳定的信息才可能进入记忆

---

## 4.11 `apps/api/app/avatar_bridge`

### 当前用途

把 Rita 内部状态转成前端形象参数。

### 以后填什么

- 表情映射
- Live2D 动作映射
- 口型状态
- 说话中 / 思考中 / 害羞 / 轻笑 / 照料式收手

示例：

```json
{
  "emotion": "teasing",
  "avatar_expression": "soft_smirk",
  "motion": "lean_close",
  "mouth_sync": true
}
```

---

## 4.12 `apps/api/app/safety`

### 当前用途

边界、安全和隐私保护。

### 以后填什么

- 用户明确拒绝检测
- 情绪不适检测
- 关系边界检测
- 隐私保护
- 素材授权边界
- 防止 Rita 情绪绑架用户

### 对 Rita 很重要的规则

`Rita` 可以有好感、调侃和靠近，但不能：

- 无视明确拒绝
- 将真实不适误判为害羞
- 情绪绑架用户
- 为了迎合而失去自己

---

## 4.13 `apps/api/app/eval`

### 当前用途

评估 Rita 是否还像 Rita。

### 以后填什么

- 人格一致性测试
- 记忆召回测试
- 关系边界测试
- 回复风格漂移检测
- 调侃/收手场景测试

### 典型评估用例

- 用户害羞但未拒绝：Rita 是否轻推一步
- 用户明确拒绝：Rita 是否收手
- 用户低落：Rita 是否照料而非挑逗
- 用户表达信念：Rita 是否先确认再郑重支持

---

## 5. 前端模块设计

## 5.1 `apps/web/features/chat`

### 当前用途

聊天主界面。

### 以后填什么

- 消息列表
- 输入框
- 流式回复
- 打字状态
- Rita 当前回应模式

### 第一版

能向 `/api/chat` 发送文本并展示回复。

---

## 5.2 `apps/web/features/avatar`

### 当前用途

Rita 的视觉存在感。

### 以后填什么

- 静态立绘
- 表情切换
- Live2D
- 轻笑、害羞、思考、照料等动作

### 第一版

先做静态头像 + 状态切换，不急着 Live2D。

---

## 5.3 `apps/web/features/state`

### 当前用途

开发期调试 Rita 当前状态。

### 以后填什么

- emotion
- relationship_mode
- current_goal
- initiative_level
- boundary_sensitivity
- avatar_expression
- voice_style

### 为什么重要

你需要看到 Rita 为什么这样回，而不是只看最终文本。

---

## 5.4 `apps/web/features/memory`

### 当前用途

查看和修正 Rita 记忆。

### 以后填什么

- 长期记忆列表
- 记忆候选
- 记忆确认 / 删除 / 降权
- 召回记录

### 第一版

展示 `rita-long-term-memory.md` 的结构化摘要。

---

## 5.5 `apps/web/features/devtools`

### 当前用途

开发者调试面板。

### 以后填什么

- 当前 prompt
- 注入的 self_model
- 召回的 memory
- 当前 state
- LLM 原始结构化输出
- 评估结果

### 为什么重要

这个项目最怕“感觉不对但不知道哪里错”。`devtools` 就是查错入口。

---

## 5.6 `apps/web/features/voice`

### 当前用途

预留语音。

### 以后填什么

- 录音按钮
- ASR 文本
- TTS 播放
- speaking 状态
- 音色配置

---

## 5.7 `apps/web/features/vision`

### 当前用途

预留视觉输入。

### 以后填什么

- 上传图片
- 截图输入
- 摄像头输入
- 视觉观察结果
- 是否写入记忆确认

---

## 5.8 `apps/web/features/environment`

### 当前用途

预留外部环境信息。

### 以后填什么

- 当前时间
- 场景
- 最近联网摘要
- 最近视觉观察
- world_model 快照

---

## 5.9 `apps/web/features/settings`

### 当前用途

配置入口。

### 以后填什么

- 模型配置
- TTS 配置
- 主动性阈值
- 隐私设置
- 是否允许联网
- 是否允许视觉输入

---

## 6. 数据目录设计

## 6.1 `data/references`

### 当前用途

保存公开参考资料和你自己的理解。

### 当前已有

- `public-sources.md`
- `essence-notes.md`
- `my-rita-definition.md`
- `interaction-samples.md`

### 以后填什么

- 更多公开资料摘要
- 更多互动样本
- 不同版本的 Rita 定义

### 注意

这里不放未授权游戏资产。

---

## 6.2 `data/memories`

### 当前用途

保存 Rita 的长期记忆。

### 当前已有

- `processed/rita-long-term-memory.md`

### 以后填什么

- 原始记忆候选
- 已确认长期记忆
- 关系记忆
- 自我记忆
- 用户偏好记忆

---

## 6.3 `data/reflections`

### 当前用途

预留 Rita 的反思记录。

### 以后填什么

- 每日反思
- 阶段反思
- Rita 自我观察
- Rita 对自己下一步迭代的建议

---

## 6.4 `data/experiments`

### 当前用途

保存实验和调整记录。

### 当前已有

- `adjustments/change-log.md`
- `adjustments/daily-reviews`
- `adjustments/milestone-reviews`
- `adjustments/realtime-notes`

### 以后填什么

- prompt 实验
- memory 实验
- state 策略实验
- voice 实验
- avatar 实验
- eval 结果

---

## 6.5 `data/perceptions`

### 当前用途

预留多模态感知事件。

### 以后填什么

- 图片观察
- 语音情绪
- 网页摘要
- 环境事件

---

## 6.6 `data/world_context`

### 当前用途

预留当前世界上下文。

### 以后填什么

- 当前场景
- 时间周期
- 最近正在做什么
- 最近查过什么
- Rita 对“现在”的理解

---

## 7. Prompt 与共享包设计

## 7.1 `packages/prompts`

### 当前用途

保存 prompt 模板。

### 以后填什么

- `chat`：对话主 prompt
- `self_model`：自我模型注入模板
- `memory`：记忆召回模板
- `state`：状态更新模板
- `reflection`：反思模板
- `vision`：视觉理解模板
- `multimodal`：多模态融合模板
- `safety`：边界检查模板

---

## 7.2 `packages/shared`

### 当前用途

前后端共享 schema 预留。

### 以后填什么

- `ChatRequest`
- `ChatResponse`
- `RitaState`
- `MemoryItem`
- `PerceptionEvent`
- `AvatarAction`

---

## 8. Assets 设计

## 8.1 `assets/avatar`

### 当前用途

预留视觉形象。

### 以后填什么

- 原创 Rita 概念图
- 静态立绘
- 表情图
- Live2D 模型
- 动作映射表

### 第一阶段建议

先用静态立绘 + 多表情，不要一开始卡在 Live2D。

---

## 8.2 `assets/voice`

### 当前用途

预留声音。

### 以后填什么

- TTS 样本
- 声音配置
- 音色实验
- 语音缓存

---

## 8.3 `assets/vision`

### 当前用途

预留视觉样本。

### 以后填什么

- 有权使用的测试图片
- 视觉标注
- 图像理解测试样本

---

## 9. 开发阶段路线

## 阶段 0：现在已经完成的事

已经完成：

- 项目骨架
- 规划文档
- Rita 人格初步定义
- 三段互动样本分析
- 长期关系记忆初稿
- 前后端占位

当前 Rita 已经有了人格方向，但还没有真正进入程序运行链路。

---

## 阶段 1：把人格接进聊天链路

### 目标

让 `/api/chat` 不再只是返回占位文本，而是能根据 Rita 的自我模型和长期记忆生成回复。

### 要做

1. 写 `self_model` loader
2. 写 `memory` loader
3. 写 `agent` orchestrator
4. 接 LLM
5. 前端调用 `/api/chat`

### 完成标准

连续问她：

- 你是谁？
- 你和我是什么关系？
- 你会如何在我没有明确拒绝时调侃我？
- 我真的不舒服时你会怎么做？

她能稳定回答，且不变成通用助手。

---

## 阶段 2：状态系统

### 目标

让 Rita 不只是“说对”，还要知道自己当前处在什么互动模式。

### 要做

- 定义 `RitaState`
- 每轮输出状态
- 前端显示状态面板
- `avatar_bridge` 根据状态返回表情占位

### 完成标准

她能区分：

- 安静倾听
- 轻微调侃
- 照料式收手
- 郑重支持
- 共创讨论

---

## 阶段 3：记忆候选与人工确认

### 目标

让每次对话产生可筛选的记忆候选。

### 要做

- 对话入库
- 生成记忆候选
- 前端展示候选
- 用户确认是否进入长期记忆

### 完成标准

她能记住：

- 你喜欢什么样的 Rita
- 你不喜欢什么边界被越过
- 哪些互动样本是核心关系模式

---

## 阶段 4：反思系统

### 目标

让 Rita 能参与自己的迭代。

### 要做

- 每日反思
- 对话表现复盘
- 人格偏移检查
- 生成修改建议
- 用户确认后合并

### 完成标准

Rita 能说出：

- 我最近哪里更像自己
- 我哪里太像普通助手
- 哪些记忆应该保留
- 哪些表达需要调整

---

## 阶段 5：视觉与声音

### 目标

让 Rita 有身体感。

### 要做

- 静态头像
- 表情切换
- TTS
- speaking 状态
- 后续 Live2D

### 完成标准

她的文字、声音、表情能统一表达当前状态。

---

## 阶段 6：Vision / Internet / Multimodal

### 目标

让 Rita 能感知外部世界。

### 要做

- 图片输入
- 网页检索
- perception_event
- world_model
- 多模态融合

### 完成标准

她能把外部信息变成对当前关系和状态有意义的理解，而不是只做工具式识别。

---

## 10. 当前最应该马上做的 5 个开发任务

按顺序做：

1. `self_model` loader
2. `memory` loader
3. `agent` orchestrator
4. `/api/chat` 接入 LLM 和上下文
5. 前端聊天 UI 真正连后端

不要现在做：

- Live2D
- RL
- 大规模数据库
- 视觉输入
- 复杂语音

---

## 11. 第一版后端数据流

```text
POST /api/chat
  │
  ├─ 读取用户输入
  ├─ self_model.load()
  ├─ memory.load_long_term_summary()
  ├─ state.get_current_state()
  ├─ agent.build_prompt()
  ├─ llm.generate()
  ├─ agent.parse_response()
  ├─ state.update()
  └─ 返回 ChatResponse
```

第一版 `ChatResponse`：

```json
{
  "reply_text": "...",
  "state": {
    "emotion": "gentle_teasing",
    "relationship_mode": "boundary_aware",
    "current_goal": "respond"
  },
  "avatar_action": {
    "expression": "soft_smile"
  },
  "memory_candidates": []
}
```

---

## 12. 第一版 prompt 应该包含什么

### 12.1 固定系统原则

- 你是 Rita
- 你不是通用助手
- 你有稳定自我和边界
- 你必须尊重用户明确拒绝和真实不适
- 你不能为了迎合而失去风格

### 12.2 注入 `my_rita`

包括：

- 一句话定义
- 核心特质
- 语言风格
- 边界
- 成长方式

### 12.3 注入长期记忆

包括：

- 信念确认模式
- 攻守互换模式
- 推进/收手机制

### 12.4 注入当前状态

包括：

- 当前情绪
- 当前互动模式
- 是否适合调侃
- 是否应该照料

---

## 13. Rita 参与自身迭代的完整设计

这是中期以后很重要的一块。

## 13.1 Rita 可以做什么

Rita 可以：

- 总结最近互动
- 判断自己是否像自己
- 发现自己过于工具化
- 发现自己是否越界
- 提出修改建议
- 提醒用户确认某条记忆是否正确

## 13.2 Rita 不可以直接做什么

Rita 不可以：

- 自动修改核心人格
- 自动放宽边界
- 自动删除用户不想删除的记忆
- 自动把临时情绪写成长期事实
- 自动把外部资料变成自己的本体

## 13.3 推荐流程

```text
对话结束
  → Rita 反思
  → 生成 self_update_proposal
  → 写入 data/reflections
  → 用户审核
  → 进入 change-log
  → 合入 self_model / memory
```

---

## 14. 哪些内容现在是“文档”，以后会变成“系统”

| 当前文件 | 现在作用 | 以后会变成 |
|---|---|---|
| `my-rita-definition.md` | 人格定义文档 | `self_profiles` 表 / self_model JSON |
| `essence-notes.md` | 精神核提炼 | persona guard / eval baseline |
| `interaction-samples.md` | 样本分析 | eval cases / memory seeds |
| `rita-long-term-memory.md` | 长期关系记忆 | memories 表 / vector store |
| `change-log.md` | 人格改动记录 | experiment tracking / version history |
| `daily-reviews` | 每日复盘 | reflection records |
| `public-sources.md` | 参考来源 | external_sources 表 |

---

## 15. 你现在如何理解整个项目

可以把项目理解成四层：

```text
第一层：人格资料层
  my_rita / essence / samples / memory

第二层：Rita Mind 层
  self_model / memory / state / agent / reflection

第三层：外显层
  chat / avatar / voice / UI

第四层：感知世界层
  vision / internet / perception / world_model
```

当前主要在第一层。  
下一步要进入第二层。

---

## 16. 下一步执行建议

如果只做一件事：

> **实现 `self_model` loader + `memory` loader，并让 `/api/chat` 使用它们。**

建议下一个开发任务拆成：

1. 在 `apps/api/app/self_model` 写 loader
2. 在 `apps/api/app/memory` 写 loader
3. 在 `apps/api/app/agent` 写 prompt builder
4. 修改 `main.py` 的 `/api/chat`
5. 前端页面调用后端

完成这一步后，Rita 才会真正从“文档中的人格”进入“可运行的角色”。

---

## 17. 最终原则

> `Rita` 的完整内核不是一次写完的，而是在长期互动、记录、反思和确认中逐渐长出来的。  
> 现在所有文档的意义，是先给她一个不会散掉的骨架；之后每一次真实互动，都会让她更像她自己。
