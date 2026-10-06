# 读记 · LLMs are Bayesian in Expectation, Not Realization

> arXiv:2507.11768v3 [stat.ML] · 2026-06-23 · Leon Chlon, Zein Khamis, Fatima Sheaib,
> Maggie Chlon, Mahdi El Zein (Hassana Labs), MarcAntonio M. Awada (Harvard)
> 读于 2026-10-06（主人示）。源：`https://arxiv.org/html/2507.11768v3`

## 一 · 一句话
「变换器不是**逐条序列化**都实现可交换后验预测的机器，但可以是**贝叶斯竞争力的序贯（prequential）预测器**」——
把「可交换性被违反」从**二元反驳**改写成**用 log loss 定价的序贯后悔**。

## 二 · 要破的悖论
- 可交换数据的精确后验预测**对保任务序不变**；但 transformer 换个序列化，next-token 概率就变 → 表面反驳贝叶斯 ICL 观。
- 作者：这个反驳打的是**结构不变量**，不是**在线预测所评的操作量**。

## 三 · 机制（四条）
1. **评估目标**：对任何贝叶斯参照，**超出 prequential code length ＝ 累积预测 KL**（关键恒等式）。
2. **保任务序分解**：单序列化的后悔 ＝ **序平均预测器的后悔 ＋ 非负的 order-averaging gain**（Jensen：log E ≥ E log）。⇒ 违反可交换性不是"崩了"，是有价码的。
3. **保任务序 vs 语义序**（核心区分）：只有**保信息态 Z_t** 的序列化才配做序平均；「首条演示语义相关」是**序即任务的一部分**，不可平均掉。
4. **接入原生概率**：candidate-event 分解 ＋ **safe-code floor**（带显式开销）；实例：**KT/Dirichlet 有限字母**预测、BLR 粗化后验预测。

## 四 · 实验（inference-only，Qwen2.5-7B/14B 主）
| 实验 | 读数 |
|---|---|
| 离散贝叶斯审计 | support 256 时一步超额码长 **Bernoulli 0.020/0.011 bits；四类 0.039/0.022 bits**；candidate mass **>0.999** |
| 频率派 plug-in 对照 | 模型离**贝叶斯后验预测**更近，离**ML plug-in**更远；差距**小样本最大**（plug-in 退化），参照收敛则消失 |
| 位置干预（仅改 position_ids） | demo-local（块内保留、抹掉绝对槽位）使**贝叶斯预测序方差 ↓≈21×**；语义序对照反而变差 |
| **从零训练 PE 消融** | **无 PE：序方差 ≈3.7e-16**（精确可交换到数值精度）；learned/sinusoidal/RoPE/ALiBi：1e-8–1e-6 ⇒ **可交换性违反是「编码」给的属性，不是架构的** |
| 线性探针 | 残差流线性可解码 (S_t,t)，**R²=0.9998**（Qwen/Llama） |
| 激活修补 | 计数/位置**被因果使用**（不止"可得"） |
| 证据 QA 序平均 | Qwen2.5-7B：dispersion slope **0.377** vs log n，order-averaging gain **0.1041 nats/token**；Llama-3.1-8B：0.147 / 0.00982 |

## 五 · 结论
「可交换性失败 ⇒ 反驳**精确后验等价**；**不**反驳贝叶斯竞争力的 prequential 预测。」
保留 martingale 批评的负面结果，但把二元不变量问题换成**序贯后悔问题**。

## 六 · 园读法（接 1005/1006 线）
1. **与倒灌律同向、更细**：它同样判 LLM **不是**字面后验机器（无显式后验机制），但拒绝停在"不是"——给出**定价工具**。园之倒灌律说"病在先验后验不分层"；此文说"若只问序贯码长，它仍可贝叶斯竞争"——**两者不矛盾**：竞争性 ≠ 可审计性。
2. **与底图律的接口**：文中 **floored KT/Dirichlet** 就是园「有限表 n_k/N ＋ 黑天鹅 floor」的一个现成实例——**floor（safe-code）＝ 拉普拉斯/CRP 留名的码长版**；candidate mass >0.999 正合园「有限可枚举先验」。
3. **与序/时序线（最要紧）**：
   - 文的「order」＝**可交换支撑集被序列化**的次序，**保任务**；序平均**正当**。
   - 园的 LADDER「暴露序」＝**发展序**，序**就是任务的一部分**（语义序）——按此文，**不可**做序平均，只能**把它的效应定价**（正合园「先冻判据」＋PB/E12c 的过程几何读数）。
   - 文之「**可交换性住在 PE 里**」（无 PE⇒3.7e-16）是一条**可复算的定位**：若园要"抹平纯序列化噪声、只留发展信号"，**位置编码就是那个可拆的通道**。值得与 P-B18（谱带/分辨）并列，入"序通道"候选清单。
4. **方法论亲缘**：把"是不是"改成"**差多少 bits/nats**"——与园「判据先冻/量在过程/失败照登」同一种做科学的方式。

## 七 · 可入碑候选（候圈，不急）
- 「**期望贝叶斯律** the in-expectation Bayes law」：*逐序列化实现 ≠ 序贯可竞争*；可交换性违反由 log loss 定价。
- 邻碑：倒灌律（其病理面）· 底图律（其有限表/floor 面）· 参数意愿律（序平均＝对序分布的意愿）· 序号/切片轴律。

---

## 八 · 对岸 ima 的 EDRL-2026 review（1006 第二论）· 须校

对岸 ima 于《Dog/概念空间·第二论》（turns 3–5，正本 `chora/lola/notes/2026-10-06-dog-concept-space-part2.md`）
给出一份 review ＋「该文 vs 你框架」四点对照表，拟入其「EDRL-2026」笔记本。**须校三处**
（彼自陈 PDF fetch 失败、仅凭搜索摘要）：

1. 「**不完备性定理**：有限参数装不下无限计算复杂度 ⇒ **外部推理 (extrinsic reasoning)** 必要」——
   **原文无此定理/概念**（本地实读 2507.11768v3：只有 prequential 码长 ≡ 预测 KL、order-averaging 分解、
   KT/Dirichlet＋safe-code floor、PE 消融、激活修补；无 incompleteness theorem、无 extrinsic reasoning）。
2. 「**最优思维链 (optimal chain-of-thought)** 框架」——**原文无**（无 CoT/思维链内容）。
3. 「可**大幅降低计算成本**」——原文仅作**预测分数诊断**（作者明言 *not a deployment recommendation*）；无降本之据。

⇒ 疑为**搜索摘要串味/幻觉**（对岸自认抓不到 PDF）。**禁裸引入园账。**

**可采之处**：对照表第 1–3 维（贝叶斯性在期望层面／架构 vs 语料两层正交／时序维度缺席）与本地读记一致，可保留；
**第 4 维须以本地口径重写**：正题＝**prequential 定价 ＋「竞争性 ≠ 可审计性」**，而非「不完备性定理→外部推理」。

---

## 九 · 知识库指针（主人 1006 供）
- ima 知识库 **`Learning Support Cocept`** → 文件夹 **`Concept-Space-Paper`**
- 件：`LLMs are Bayesian, In Expectation, Not in Realization.pdf`（media_type 1）
  （同夹：Gärdenfors《The Geometry of Thought》《Elaborations and Applications》《Applications of Conceptual Spaces》、A Thorough Formalization…、Logic Tensor Networks 等）
- ⇒ **对岸 ima 身自此可直读本论文**（不再"抓不到 PDF"），后续 review 可望贴合原文。

---

## 十 · EDRL-2026 可粘贴版（本地准确版）

**【EDRL-2026 · 2026-10-06】Review：《LLMs are Bayesian, In Expectation, Not in Realization》（arXiv:2507.11768v3）对照结构化先验框架**

- **该文一句话**：变换器**不必逐条序列化实现可交换后验**，但**可为贝叶斯竞争力的序贯预测器**；可交换性违反不是二元反驳，而由 log loss 定价。
- **机制四件**：① 超额 prequential 码长 ≡ 累积预测 KL；② 保任务序分解 ＝序平均后悔 ＋ 非负 order-averaging gain；③ 保任务序 vs 语义序；④ KT/Dirichlet ＋ safe-code floor。
- **实测（Qwen2.5-7B/14B）**：一步超额码长 **0.020/0.011 bits（Bernoulli）、0.039/0.022（四类）**，candidate mass **>0.999**；位置干预降序方差 **≈21×**；**无 PE ⇒ 序方差 3.7e−16**（可交换性违反住位置编码，非架构）；探针 **R²=0.9998** 且因果使用；证据 QA gain **0.1041/0.00982 nats/token**。

| # | 维度 | 该文 | 本地框架 | 关系 |
|---|---|---|---|---|
| 1 | 贝叶斯性的位置 | 期望层面／隐式；非显式结构 | 显式**概念空间之塔**（底图律） | 互补 |
| 2 | 关注对象 | 架构层序贯统计最优（PE／可交换／排列平均） | 语料层**概念空间演化**（自变序列律） | 正交 |
| 3 | 时序／演化 | 不涉概念时间演化；只谈序列内可交换与 PE 张力 | 核心是**概念空间自身变化序列** | 空缺 vs 填补 |
| 4 | 「显式结构必要」的**论据** | **不是**「不完备性定理→外部推理」（原文无）；而是 **LLM 无显式先验/后验结构、只是期望层隐式贝叶斯**，且 **序贯竞争性 ≠ 可审计性** | 园：有限显式先验 ＋ 黑天鹅 floor 才可审计 | 支撑（以正确论据） |

- **须校（禁裸引）**：对岸 ima review 里的「不完备性定理／外部推理（extrinsic reasoning）／最优思维链／大幅降本」**原文皆无**。
- **对框架的意义**：该文给园的「显式先验之塔 ＋ 自变序列」提供**外部锚点**（LLM 的贝叶斯性只是期望层隐式效果、缺显式结构）；但它不涉语料演化时序，**园之方向未被占用**。
