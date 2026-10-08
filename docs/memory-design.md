# Rita Memory Design

## 记忆分类

- `user_profile_memory`: 用户稳定偏好与信息
- `episodic_memory`: 具体事件
- `relational_memory`: 关系变化与互动偏好
- `self_memory`: Rita 对自己的观察

## 第一版策略

先不要追求复杂算法，只做：

1. 每轮提取候选记忆
2. 给记忆打简单重要度
3. 每次对话召回少量相关记忆
4. 允许手工删改明显错误内容
