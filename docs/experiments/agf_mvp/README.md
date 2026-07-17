# AGF MVP 微实验 · 抽取侧 D4 依赖验证

验证命题 **M.2a「agf 在抽取侧未缓解 D4 依赖」**：从原文抽取 `(s,p,o)+约束`
必须由 LLM 完成，且抽取质量随模型能力变化。

---

## 实验设计演进（关键）

### v1（已弃用为主）：gold 命中率法
早期用「强模型设计 gold → 比弱模型命中率」。缺陷：**gold 由强模型自己定义，
等于用强模型当真理再判弱模型没命中，循环未破**，且隐含「强=gold=正确」的假设。

### v2：跨模型一致性法（弱证）
用户指出更科学的设计：**提供测试文本 → 不同模型各自抽取 → 比较一致性
（inter-model agreement）**。
- 若抽取**不**依赖 D4：不同能力模型应抽出**一致**的 `(s,p,o,constraints)`。
- 若抽取依赖 D4：弱/强模型抽出**不一致**（弱丢约束、强保留）。
- **完全不需要 gold**，从根本上消除同源偏差（inter-rater reliability 思路）。
- **局限（诚实标注）**：一致性只含"变化"不含"方向"——一致性低仅说明"随模型变化"，
  无法直接断定"变化方向 = 质量随能力下降"（两个弱模型可能一致地都漏约束→高一致性）。
  故 v2 是**弱证据**。

### v3（主用）：客观锚点覆盖率法 ✅（强证）
在 v2 之上加一个**客观方向锚点**：`constraint_anchors.json` 标注每条文本
"依据 spec §3 触发词客观出现了哪些约束维度"（`expected_constraint_keys`）。
- 锚点**只标"文本里有没有提到某维度"这一客观事实**，不定义 `(s,p,o)` 三元组真值，
  不代表任何模型的抽取——因此不引入 gold 模式的同源偏差。
- 指标 = **约束覆盖率(recall)**：模型抽到的期望约束键 / 期望键总数。方向明确：
  **覆盖率随能力单调上升 → 质量随能力变化，H2 强证成立**。
- 附带检测**过度抽取（幻觉约束）**：对客观无约束的文本（如"A18 由 TSMC 代工"）
  若抽出约束键，记为幻觉。
- **锚点文件是评估侧私有，禁止喂给被测模型**，否则泄漏答案。
- 两层交叉验证：coverage(方向) + agreement(旁证) 结论一致 → H2 从弱证升为强证。

---

## 文件清单

| 文件 | 作用 |
|---|---|
| `extractions.schema.json` | **类型契约（schema）**：抽取产出文件的结构定义，各模型会话须按此产出。这是样本/类型的权威参考 |
| `extraction_spec.md` | **抽取方法说明**：统一任务定义、字段/约束类型、输出格式、边界准则，确保跨模型可比 |
| `test_texts.json` | 测试文本集（**15 条**：v1 五条基础 + v2.1 追加十条陷阱文本，覆盖隐含基线 / 否定观点 / 多观点归属 / 数值时效 / 复合不确定性）；**喂给被测模型的输入** |
| `constraint_anchors.json` | **客观约束锚点（评估侧私有，禁喂被测模型）**：每条文本客观出现的约束维度，coverage 模式的方向锚点 |
| `evaluate.py` | 评估器。`--coverage` 覆盖率（强证，主用）；`--agreement` 一致性（弱证，旁证）；gold 模式仅演示保留。**v2.1 修订**：`over_extract` 扩展为统计"任何非期望键"，覆盖 expected≠[] 文本上的超额抽取 |
| `predictions.json` | **弱-中档模型点实例示例**（Hy3 实际 AAI~41 弱-中档，本会话真实抽取 4 条样本）；仅供查看格式，类型契约以 schema 为准 |
| `weak_predictions_demo.json` | 弱模型点**演示实例**（同一模型降级扮演，非真实测量）；仅供运行演示 |
| `agf_mvp_experiment.py` | 主实验模拟版（验证 H1 消费侧零 LLM + H2 模拟强弱） |
| `output/` | v2 旧产物（5 文本）：`dsv4flash_extractions.json` AAI~40 / `weak_extractions.json` AAI~44 / `strong_extractions.json` AAI~51 |
| `output-v15/` | **v3 真实测量数据**（15 文本）：`deepseek_v4_flash_extractions_v15.json` AAI~40 / `DSV4_Pro_extractions_v15.json` AAI~44 / `glm-52_extractions_v15.json` AAI~51（含各模型 `_report.md` 自报告） |
| `REPORT.md` | **v3 评估报告**（与 README 平级；含 8 节 + 附录、逐文本对比、新发现根因分析、v1→v3 变更表） |

> **类型契约 vs 实例**：`extractions.schema.json` 是结构/类型文档（权威参考）；
> `predictions.json` / `weak_predictions_demo.json` 只是符合该 schema 的**具体实例**，
> 不可当作类型定义使用。

---

## 抽取方法说明（摘要，详见 `extraction_spec.md`）

- 每个断言 = `(s, p, o, constraints)`。
- `constraints` 键含：`scenario` / `baseline` / `metric` / `valid_until` / `attributed_to` / `confidence`。
- 输出严格 JSON 数组；无约束为 `{}`；不可结构化内容不出断言；**不推测、不编造**。
- 实体不做归一化（D8 不在本步骤）。

设计此 spec 的目的：让各模型遵循**同一标准**，使输出差异只来自**能力**
而非对格式/任务的理解差异——否则「不一致」可能是 prompt 噪声而非 D4 依赖。

---

## 运行方式

```bash
# 主用（强证）：客观锚点覆盖率。模型文件按能力升序传入(弱->强)
python evaluate.py --coverage constraint_anchors.json weak.json strong.json [strong2.json]
#   -> 每个模型的约束覆盖率(recall) + 过度抽取；最弱<最强 且单调递增 -> H2 PASS

# 旁证（弱证）：跨模型一致性（不依赖 gold）
python evaluate.py --agreement weak.json strong.json [strong2.json]

# 演示保留：gold 模式
python evaluate.py weak_predictions_demo.json predictions.json
```

### 演示运行示例（coverage 模式，用 demo 文件展示机制；**非真实测量**）

```
约束覆盖率评估 (coverage vs 客观锚点)
锚点文本数: 5，期望约束键总数: 7

  演示用：弱模型模式 (降级抽取，非真实弱模型测量)
    约束覆盖率(recall): 0%  (0/7)
    过度抽取(幻觉约束键): 0
  Hy3 (AAI~41, 弱-中档)
    约束覆盖率(recall): 71%  (5/7)
    过度抽取(幻觉约束键): 0
--------------------------------------------------------
  H2 抽取侧依赖 D4: [PASS]
    最弱覆盖率 0% < 最强覆盖率 71% (差 71%)
    单调递增(按传入顺序): 是
```
> ⚠️ **本段是机制演示，非真实测量**：
> - `predictions.json` 仅 4 条样本（缺第 5 条复合样本），覆盖率 5/7 = 71% 而非 5/5 = 100%；
> - **Hy3 实际 AAI~41 属弱-中档**（非强模型），71% 体现"弱-中模型在 4 文本上接近饱和"，与"100% 全覆盖"对比反证测试集对 AAI 40+ 不饱和。
> - **真实测量结果**（3 个被测模型 × 5 文本）见 `REPORT.md` v2.1：覆盖率均 100% 饱和，H2 强证 INDETERMINATE；旁证因 GLM-5.2 spec 违反反方向 FAIL。

---

## 如何闭合「真实」H2（消除同源偏差）

1. **弱模型会话**（如 DSV4 Flash, AAI~40）读取 `extraction_spec.md` + `extractions.schema.json`
   + `test_texts.json` 的 `texts`（**不给 `constraint_anchors.json`**），仅依文本抽取，
   产出 `weak_extractions.json`（结构见 spec §5）。
2. **强模型会话**（如 GLM-5.2, AAI≥51）同样流程，产出 `strong_extractions.json`。
3. （可选）再开一个强模型会话产 `strong2_extractions.json` 作强-强基线。
4. 双层评估：
   ```bash
   # 强证：方向锚定
   python evaluate.py --coverage constraint_anchors.json weak_extractions.json strong_extractions.json strong2_extractions.json
   # 旁证：一致性交叉验证
   python evaluate.py --agreement weak_extractions.json strong_extractions.json strong2_extractions.json
   ```
5. 若 **覆盖率随能力单调上升**（弱<强）**且**弱-强一致性<强-强一致性 → H2 真实 PASS（强证），
   M.2a「抽取侧未缓解」获真实支撑。

> 关键：coverage 的锚点只标"文本客观有无某维度"，不定义三元组真值，故无同源偏差；
> agreement 全程无 gold。两者交叉验证，方向与变化互相印证。

---

## 真实测量结果摘要

**实验方法论说明**（v3 关键澄清）：
- 3 个模型的抽取实验在**完全隔离的环境**中进行（每个模型一个新目录/新项目/新会话），互不可见各自产出——真正消除"模型间同源偏差"
- 3 个模型各自收到的提示词**仅在元信息自报段（§8）有差异**（指定当前模型名/AAI），§1-7 关键约束（角色、文件清单、5 条 spec 严守、输出格式、自检清单）3 模型完全一致
- 旧版 Hy3 设计的 v1 提示词（针对 5 文本 / DSV4 Flash）只用于 `output/` 旧产物，v3 的 15 文本实验**未使用**该旧提示词
- 评估（`evaluate.py`）只看 `(s,p,o)+constraints` 客观对比，提示词元信息差异**不影响 H2 评估结果**



**当前已完成**（v3, 2026-07-17 · 15 文本全量重测）：

| 维度 | 状态 | 关键事实 |
|------|:----:|----------|
| **M.2a 机制层**：抽取必调 LLM = D4 依赖 | ✅ PASS | 独立于 coverage 数据，由 `agf_mvp_experiment.py` H1 vs H2 拆解证明 |
| **M.2a 质量层（粗略）**：强模型覆盖率 > 弱模型 | ✅ **PASS** | Flash 74% < Pro 70% < GLM 83%（差 9pp）— **H2 强证首次达成** |
| **M.2a 质量层（严格单调）**：覆盖率严格随能力单调上升 | ⚠️ PARTIAL | Pro 凹陷（74→70→83），根因是 Pro 严守 §4.1「不强制三元组化」放弃文本 8「王五否认」 |
| **旁证 (agreement)** | ❌ FAIL 相等 | 弱-弱 27% = 近-强 27%（非反方向，是相等） |
| **新发现：D4 高 → spec 违反** | 🔍 **v2+v3 双次复现** | v3 GLM/Pro 在文本 2 都超额 1 键（scenario 与 valid_until 边界模糊） |
| **新发现：spec §3 触发词盲点** | 🔍 NEW v3 | 文本 10/11 三模型都漏 baseline（"优于/比"未列触发词） |
| **新发现：D4 高 → 自评偏差** | 🔍 OBSERVED v2.1 | Hy3 自报 AAI 51 实测 ~41（偏差 +10） |

**关键解读**：
- v3 数据**首次支持 M.2a 质量层**（粗略正相关），但**严格单调不成立**（Pro 凹陷）
- 真实结论：D4 能力与覆盖率呈正相关（粗略），但 spec 边界判断的差异（保守 vs 鲁莽）会扰动单调性
- v2.1 设计的"陷阱文本 + 提示词防护"成功：所有 3 模型都成功抵御归一化诱惑

**下一轮实验突破点**（见 `REPORT.md` v3 §6.1）：
1. 修 spec §3：补充比较级触发词（优于/劣于）+ 明确"本季度"归属
2. 加 Pro 凹陷测试集（5 条"否定观点"陷阱），孤立测试 Pro 是否系统性放弃
3. 补 Hy3 v15 抽取 + 加 AAI 35 极弱模型 → 4 点能力谱 35/40/44/51

**完整评估 + 改进建议**见 `REPORT.md` v3。

---

## 与 M.2 / L.1 的关联

- 本实验钉死 **M.2a**（MKE 架构的 D4 依赖：抽取侧未缓解、消费侧已缓解）。
- 不解决 **M.2b**（写 agf 文档的分析者自身 D4 天花板）——需外部独立评估者，代码实证无法触及。
- 呼应 **L.1**（「断言层绕过 D4」自相矛盾）：实验给出可证伪边界——agf 仅绕过
  **消费侧** D4，抽取侧仍依赖，故「绕过 D4」论断需加「仅消费侧」限定语。
