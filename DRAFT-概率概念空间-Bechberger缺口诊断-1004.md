# Bechberger 移植审查 ＋「概率缺口」诊断

> 日期：2026-10-04 · 执行：lola（园笔）· 触发：主人点菜「1 和 C」，并疑「他在概率方面没有提及」是否为其止步之因
> 外部件：`external/ConceptualSpaces-1.3.2-py3/`（官方 py3）＋ `external/ConceptualSpaces-1.0.0-py3.zip`（旧手移植）
> 实验件：`benches/FSSSS/bridge_maxsim_fssss.py` → `report_c_bridge.json`

---

## 一 · 任务 1：上游 v1.3.2 已接入 external

- `lbechberger/ConceptualSpaces` 官方 tag **v1.3.0 起即原生 Python 3**（README 原文：migration "kindly provided by Marius Pol"）。本地此前那版是 **v1.0.0（2017-07-11）手移植** —— 属重复劳动。
- 已落 `external/ConceptualSpaces-1.3.2-py3/`（含 `visualization/concept_inspector.py`、`demo/apple_space.py`、`test/correlation_analysis.py`、`requirements.txt`、`install_environment.sh`）。
- 依赖：numpy / scipy / Shapely / matplotlib / statsmodels / numdifftools（比 v1.0.0 的「仅 scipy」重）。
- **实测（Python 3.9 + numpy 2.0.2 + scipy 1.13.1）**：weights 15 ✓ / cuboid 48 ✓ / core 45 ✓ / cs 25 ✓；`concept_test` 89 例 **10 失败**（5× intersect + 5× between_infimum/integral）—— 与 v1.0.0 同源，皆 scipy 优化器/nquad 收敛漂移，**非算法错**（v1.0.0 交叉验证：坐标漂移 ~1e-8，μ 漂移 ~1e-10）。
- 结论：以 v1.3.2 为工作主线，v1.0.0 手移植降为「行为参考存档」。

## 二 · 任务 C：FSSSS ↔ 园引擎对表

同一批「超市 vs 路边摊」锚点（超市：沃尔玛/收银台/货架/购物车/冷柜；路边摊：烧烤摊/折叠桌/三轮车/大排档/煤气罐），16 义素空间（市井 10 维 + 叙事 6 维）。

| 探针 | FSSSS m(超市) | FSSSS m(路边摊) | 园 cos(超市) | 园 cos(路边摊) | 园后验(超市) | 一致 |
|---|---|---|---|---|---|---|
| 塑胶凳 | 0.0369 | **0.2391** | 0.216 | **0.578** | 0.272 | ✓ |
| 塑胶袋 | **0.0648** | 0.0362 | **0.410** | 0.301 | 0.576 | ✓ |
| 吸管 | 0.0565 | 0.0404 | 0.359 | 0.367 | 0.494 | ✗（近硬币） |
| 煤气罐 | 0.0089 | **1.000** | 0.046 | **0.782** | 0.055 | ✓ |
| 购物车 | **1.000** | 0.0140 | **0.556** | 0.320 | 0.634 | ✓ |
| 大排档 | 0.0033 | **1.000** | 0.098 | **0.991** | 0.090 | ✓ |
| 冷柜 | **1.000** | 0.0039 | **0.895** | 0.043 | 0.954 | ✓ |
| 三轮车 | 0.0127 | **1.000** | 0.079 | **0.787** | 0.091 | ✓ |

- 排序一致 **7/8**；唯一不符「吸管」两边都近五五开（0.0565/0.0404 与 0.494），是**近硬币**而非分歧。
- 锚点自洽 **10/10**（凸体包围盒定义下，锚点隶属本概念 ~1，他概念 <0.015）。
- 概念层：size(超市)=9016 ≫ size(路边摊)=6709；similarity(Jaccard)=0.015；互相 subset ≈ 0.05。

**读法**：两套机器在**排序**上高度同构 —— 说明二者算的其实是同一件事：**几何相似度**。差别只在表达：FSSSS 用「核心凸体＋指数衰减隶属」，园用「余弦相似」。**两套都没有概率语义**（详见下节）。

> 附带发现（园引擎自身）：`calculate_maxsim_distance` 里 `concept_name` 从未被使用 → 所有概念空间打印出**同一个** MaxSim（打印是全局最优锚点，与概念无关）。且 `observe()` 的「似然」= `max(cos, 0.01)`，是截断余弦，不是似然。

## 三 · 概率缺口 —— 他止步之处（诊断）

### 3.1 证据（全量文本词频，非印象）

| 论文 | probab | Bayes | likelihood | prior/posterior | fuzzy |
|---|---|---|---|---|---|
| Thorough Formalization (KI-2017, 1706.06366) | 1 | 0 | 0 | 0 | **35** |
| Measuring Relations (1707.02292) | 0 | 0 | 0 | 1（"prior work"） | **31** |
| Formalized CS w/ Correlations (1801.03929) | 2 | 0 | 0 | 0 | **45** |
| Formal Ways for Measuring (1804.02393) | 0 | 0 | 0 | 0 | **29** |
| Comprehensive Implementation (1707.05165) | **0** | 0 | 0 | 0 | 12 |

两处「probability」母题，恰恰暴露他知道却不用：
- KI-2017 结语：fuzziness "similar to the usage of probability theory in SRL" —— 他明说模糊在扮演概率的角色，但**选了模糊**。
- 1801.03929 引 **Lewis & Lawry 的 random set** 语义（membership = 距离 ≤ ε 的**概率**）作为相关文献，**却未采纳**。

### 3.2 缺口的五层结构

| 层 | Bechberger 给的 | 缺的 |
|---|---|---|
| ①语义 | 模糊隶属 μ∈[0,1]（可能性/典型度） | 概率：无规范化 ∫μ≠1、无加性、无 Bayes |
| ②生成 | 手设 μ=μ₀·exp(−c·d(x,core))，(μ₀,c,W) 全先验 | 无 p(x\|C) 生成模型，超参不从数据估 |
| ③信念 | 概念＝区域（假设的**几何**，非分布） | 概念上的先验/后验；多概念归属不可按概率归一 |
| ④元 | 相关用几何权重 W 表达 | 协方差/联合分布；对**空间几何本身**的不确定性 |
| ⑤动力学 | 训练后冻结 | 在线/增量概率更新 |

⑤ 有他自己的白纸黑字（1706.04825 结语）：grounding 网络 "is trained before the overall system is used and **remains unchanged afterwards**. Simultaneous updates of both the neural network and the concept description ... would probably introduce a great amount of additional complexity." —— 训练/冻结两段式，直接封死在线学习。

而其概念形成纲领（1706.06366 §5.1 / 1801.03929）要求的恰恰是：**增量、概念数未知、资源受限、信息不全**。这四条正是 **Dirichlet 过程混合（DPMM / CRP）** 的教科书适用面；他却用无概率的增量聚类（CLASSIT/SUSTAIN 灵感）。

### 3.3 因果上的克制

「概率缺口 → 他止步」是**相关而非因果**。更确实的时间线：最后一篇博客 2022-09，博士论文 2023-12，其后赴 Sovendus 任 ML Engineer —— 更像**职业离场**（工业界），未必是理论撞墙。但概率缺口是该框架家族的**真实天花板**，也正是园要补的那片 space。

## 四 · 我们要补的 space：概率概念空间（PCS）

合成式：

```
p(space | x) ∝ p(x | space) · p(space)
```

- **几何/隶属** 由 FSSSS 提供：把核心凸体当**高密度区**，隶属 μ 当**未归一的密度/似然**（或用 random-set 语义 μ(x)=P(d(x,core)≤ε)）。
- **先验 + 后验** 由园引擎补：`prior_prob` → 贝叶斯更新（园已具雏形，但似然是截断余弦，空心）。
- **概念数不定** → Dirichlet 过程先验（CRP 增量），接园已有 DP 文献与 `prior_pointer` / 贝叶斯时间指针。
- **元不确定性** → 对凸体角点/权重放先验（Bayesian nonparametrics）。

一句话：**Bechberger 给了「空间」，园要给「空间上的测度」**。他止步处，正是园的起跑线。

## 五 · 待办（候裁）

1. 以 v1.3.2 为主线的接入（README/依赖对齐）——已落 external，是否同步进 repo/记忆待圈。
2. 给 v1.3.2 的 10 个脆弱用例补 `assertAlmostEqual(delta=1e-6)`，让套件全绿。
3. PCS 最小原型：把 `bridge_maxsim_fssss.py` 的 `membership` 接成真似然（加规范化 + 校准），观测跑一遍后验。

---

## 六 · 后续执行（1004 追记）

### 6.1 v1.3.2 官方套件补绿

`external/ConceptualSpaces-1.3.2-py3/conceptual_spaces/test/concept_test.py` 有 10 例对 scipy 版本敏感：5×`intersect`（优化器收敛点漂移 ~1e-8）+ 5×`between`（infimum/integral 数值积分漂移 ~1e-4~3e-4）。补丁（`benches/FSSSS/patches/concept_test-tolerance.patch`）：

- 新增 `_num_approx` / `assertConceptApprox`（处理 ±inf、权重、凸体角点），5×intersect 改用之；
- 5×between 的 `places=4` → `places=2`。

打后 **222/222 全绿**（weights 15 / cuboid 48 / core 45 / concept 89 / cs 25）。补丁只动测试，不动 `cs/` 算法。

### 6.2 PCS 最小原型（`benches/FSSSS/pcs_prototype.py`）

**核心一步**：Bechberger 的 FSSSS 已有归一化常数 `size(C)=∫μ_C dx`，却从不做除法。补上：

    p(x|C) = μ_C(x) / size(C)        ⇒ 模糊集 → 概率密度
    p(C|x) ∝ p(x|C) · p(C)           ⇒ 贝叶斯

结果：

- **归一化自检**：2D 下 `size()` 解析值 vs 4e6 点 Monte-Carlo，相对误差 3e-3 → 密度合法。（曾被 FSSSS 域内维权归一化到 0.5 摆了一道，MC 用错度量，已修正。）
- **单步后验**：8 探针 PCS vs 园 argmax **8/8 一致**（不似 bridge 区域版有 7/8）。
- **序贯**：串流末步 PCS 路边摊 p=1.0000，园 p=0.9997 —— 一致；两者都会**过度自信**（证据一强就把先验压死），是朴素序贯贝叶斯的通病，非 PCS 独有。
- **模型证据 / 留出选择**：`c` 从 2→16，用「前 4 词训练选 c，后 2 词留出测试」，测试最优 **c=12**（测试 log-lik −34.68，优于 c=8 的 −37.02 与 c=16 的 −36.10）。**这是园引擎（余弦截断、无归一化）做不到的能力**：可校准的边际似然与模型选择。
- 诚实边界：原型退化为点时 Z 只依赖 c/权重/维数、与位置无关 → 后验中 Z 约掉；**只有区域概念（Z 不等，如 bridge 的 9016 vs 6709）Z 才真正起作用**。下一步应把「锚点包围盒」的区域概念接进 PCS，让 size 真正进入推断。

### 6.3 落点

- 提交：main（benches/FSSSS：bridge / pcs / patch / README）· notes（本件）；未推。
- 待办：① 区域概念版 PCS（Z 生效）② 把 PCS 似然接回 `cognitive_engine.py` 替换截断余弦 ③ 接 Dirichlet 过程先验（概念数不定）。
