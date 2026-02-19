# 研究过程日志 — yjs-mfg-ai

> 项目：制造业AI应用场景研究
> 委托方：亚俊氏（Argion Technology，新三板874106）
> 研究周期：2026-02-17
> 记录目的：过程复盘 + 失败教训（失败比成功更重要）

---

## 阶段0：项目初始化

**完成内容**
- 建立 `research/yjs-mfg-ai/` 目录结构
- 创建 INDEX.md（阶段索引）

**耗时**：快速完成，无障碍。

---

## 阶段0.5：需求画像

**完成内容**
- 采集委托方背景：亚俊氏年营收2.92亿、350人、3个生产基地、两条核心业务线
- 确定研究聚焦：业务线A（Wevac真空袋，24条线）+ 业务线B（ODM设备代工，25条线）
- 确定10个AI场景（每条业务线5个）
- 产出：`data/d0-research-brief.md`

**用户确认**：已确认，进入阶段1。

---

## 阶段1：方法论

**决策**：跳过独立方法论调研阶段，直接进入数据采集。

**理由**：委托方需求清晰（10个具体场景已定义），分析维度已在 d0-research-brief.md 中明确（痛点/技术路径/成熟度/投入/ROI/案例/前置条件）。

**教训**：对于需求已高度明确的研究，可以合并阶段1和阶段2，节省时间。

---

## 阶段2：数据采集（v1）

**完成内容**
- 10个场景数据文件全部产出（a1-a5, b1-b5）
- commit: 7a97eb0

**已知问题（事后审计发现）**
- A线：8个ERROR（URL编造、案例空白、ROI跨方案混合）
- B线：14个ERROR（URL编造、ROI计算错误、数据来源薄弱）
- 对比报告：2个ERROR

**根因分析**
1. **URL编造**：Agent在无法访问真实URL时，倾向于"合理推测"URL格式，而非诚实标注"URL未验证"。A3场景URL失效率高达53%。
2. **ROI跨方案混合**：B4（智能报价）和A2（吹膜优化）将不同投入规模的ROI混在一起计算，导致数字自相矛盾。
3. **案例空白**：A1（薄膜质检）缺乏具体企业案例，用行业通用描述填充，可信度低。

---

## 阶段3：横向对比（v1）

**完成内容**
- 10场景优先级矩阵：P0(A5+B5) / P1(B2+A3+B1) / P2(其余5个)
- commit: cc35c7f

**问题**：v1数据质量差，对比报告的结论可信度受影响。

---

## 阶段4：审计（v1）→ 发现严重质量问题

**审计结果**
- A线：C级（8 ERROR）
- B线：C级（14 ERROR）
- 对比报告：B级（2 ERROR）
- 合计：24个ERROR

**决策**：v1全部推倒重来，进行v2重新采集。

**教训**：审计必须在阶段2完成后立即执行，不能等到阶段3之后才审计。v1的对比报告建立在有缺陷的数据上，导致阶段3的工作也需要重做。

---

## 阶段2-4（v2）：重新采集 + 对比 + 审计

### v2改进措施

1. **URL验证前置**：每个场景数据文件写完后，立即用curl批量验证所有URL，不可达的标注实测状态。
2. **ROI分方案独立计算**：每个投入规模（国产/进口/SaaS/自研等）单独列一行，不混合计算。
3. **数据不足诚实声明**：A3（排产优化）找不到精确ROI数据，直接写"数据不足，暂无法得出结论"，用Panasonic案例（工时-75%）作为参考锚点。

### v2审计结果

| 审计对象 | v1评级 | v2评级 | ERROR变化 |
|---------|--------|--------|-----------|
| A线（5场景） | C级（8 ERROR） | A级（2 ERROR→修复后0） | -8 |
| B线（5场景） | C级（14 ERROR） | A级（0 ERROR） | -14 |
| 横向对比 | B级（2 ERROR） | A级（0 ERROR） | -2 |

> 注：A线v2审计初次发现2个新ERROR（A2回收期计算），当场修复，最终0 ERROR。

**v2 commit**: 4e437bf

---

## 阶段5：归档

**完成内容**
- 本文件（research-log.md）
- INDEX.md 指针全部锚定为 `git:4e437bf:` 格式

---

## 核心教训汇总

| # | 教训 | 对策 |
|---|------|------|
| 1 | Agent编造URL（A3失效率53%） | 每个文件写完立即curl验证，不可达标注实测状态 |
| 2 | ROI跨方案混合导致数字矛盾 | 每个投入路径独立一行，禁止混合计算 |
| 3 | 案例空白用通用描述填充 | 找不到案例时明确写"暂无直接案例，以下为行业数据" |
| 4 | 阶段3建立在未审计的v1数据上 | 审计必须在阶段2完成后、阶段3开始前执行 |
| 5 | 数据不足时倾向于估算而非声明 | 数据不足时直接写"数据不足，暂无法得出结论" |

---

## 最终产出清单

| 文件 | 类型 | 状态 |
|------|------|------|
| data/d0-research-brief.md | 需求画像 | ✓ commit 7a97eb0 |
| data/a1-film-inspection.md | A1场景数据 | ✓ commit 4e437bf |
| data/a2-blown-film-optimization.md | A2场景数据 | ✓ commit 4e437bf |
| data/a3-production-scheduling.md | A3场景数据 | ✓ commit 4e437bf |
| data/a4-biodegradable-formulation.md | A4场景数据 | ✓ commit 4e437bf |
| data/a5-fba-demand-forecast.md | A5场景数据 | ✓ commit 4e437bf |
| data/b1-injection-inspection.md | B1场景数据 | ✓ commit 4e437bf |
| data/b2-injection-process-optimization.md | B2场景数据 | ✓ commit 4e437bf |
| data/b3-predictive-maintenance.md | B3场景数据 | ✓ commit 4e437bf |
| data/b4-smart-quoting.md | B4场景数据 | ✓ commit 4e437bf |
| data/b5-ai-design.md | B5场景数据 | ✓ commit 4e437bf |
| analysis/scenarios-comparison.md | 横向对比v2 | ✓ commit 4e437bf |
| analysis/audit-a-line.md | A线审计v2 | ✓ commit 4e437bf |
| analysis/audit-b-line.md | B线审计v2 | ✓ commit 4e437bf |
| analysis/audit-comparison.md | 对比报告审计v2 | ✓ commit 4e437bf |

---

## 下游消费

本研究产出供 `research/yjs-boss-pitch` 使用，重点参考：
- `analysis/scenarios-comparison.md` — 优先级矩阵（P0/P1/P2）
- 各场景数据文件中的"亚俊氏适用性评估"章节
