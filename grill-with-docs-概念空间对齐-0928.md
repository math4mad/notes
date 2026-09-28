# grill-with-docs = 概念空间对齐的工程实践（0928 视频对账记）

> 源件：`~/Downloads/AI 编程范式变革：从 grill-me 到领域驱动的 grill-with-docs 深度剖析 - 002 - 双语字幕.mp4`（bilibili「牛不知道」转载 Matt Pocock 原声，15:16）
> 文字稿：OCR 烧录英文字幕 → `external/grill-with-docs-视频文字稿-EN-0928.txt`（314 句 / 2873 词，与 15 分钟口速吻合；中文轨本机 Vision 模型残缺，弃）
> 园笔按：主人直觉「这就是我们的概念空间对齐问题」——**证实，且视频提供了罕见的现场标本**。

## 一、视频主干（摘）

1. grill-me 四句真言走红（每日一百封反馈），但 Matt 自感三桩不满：agent 啰嗦时他要提醒"早有术语了"；他自己啰嗦的表述**不被挑战**；好的共享语言**没落盘**，每会话重讲一遍领域。
2. 解法 = 最薄文档层：Eric Evans DDD 的 **ubiquitous language**——`CONTEXT.md` 纯词汇表（无实现细节）+ ADR 三门槛（难撤销 / 缺上下文会困惑 / 真实取舍，三者齐备才立档）。
3. **现场标本（09:14，全片命门）**：agent 在拷问中挂牌——"你说 standalone video，但词表定义是 no lesson，你的新用法混入了 no pitch——**术语冲突**，哪个算数？" 主人被迫在 A/B 框架间表态，一表态，UI 分区、删除级联、pitchId 元数据全被牵动。会话尾 CONTEXT.md 当场更新。
4. 收益三件：回复变简（token 少）、**思考轨迹也变简**（"AI 用语言对自己思考"）、说话方式=代码结构 → 可导航性。Matt 原话：*"it magically aligned with the thoughts I had before the words came out of my brain."*
5. 分工律：无代码库用 grill-me（纯决策树拷问），有代码库用 grill-with-docs；grill-me 移入 productivity（有人用它写悼词）。

## 二、对表园学（为何这就是我们的问题）

| 视频机制 | 园中对应 | 注 |
|---|---|---|
| standalone 术语冲突挂牌 | **同 token 在两个概念空间指向不同区域** | 即 MaxSim 失配的人类版；他们靠人肉察觉，我们可算法化 |
| CONTEXT.md 词汇表 | 术语碑 GLOSSARY / 冻册判据 | 共享坐标系一旦落定，通信从"描述"降为"点名" |
| ADR 三门槛 | 判据先冻后用 + LEDGER | "难撤销+反直觉+真取舍" ≈ 我们的"值得刻石"标准 |
| 挑战用户用词（grilling 的 working-if 条） | 园笔当值之责：主人用词与冻册冲突时**当场对撞** | 我们已有此律，视频证明它值钱 |
| "查事实归 AI，决策归用户" | 提醒账批复通道（☑=朱批） | 完全同构 |
| "对齐后 token 消耗降" | 义素经济学的实证外证 | 语言=压缩的概念索引；共享词表=字典训练 |

## 三、园笔进言（候圈点）

1. **grill-garden skill 自铸案**升级：grilling 轮次 × 提醒账批复 × ADR→LEDGER/PREREG 格式——视频已把算法讲透，桥接件我们全有。
2. 试刀场仍荐 **04 案判据冻册**（γ=3.0、FIFO 600、lock 阈值三处沉默假设）。
3. 研究侧彩蛋：他们的"术语冲突检测"是**人肉+提示词**；我们若用概念空间给冲突做个**可计算判据**（同 token 双空间区域重叠度），正是 Chora 理论的正牌用武之地——可挂骨架页为一列候补（08 · 对齐工程?）。
