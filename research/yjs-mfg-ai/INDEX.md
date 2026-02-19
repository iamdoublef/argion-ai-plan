# 制造业AI应用场景研究 — 阶段索引

> 项目目的：系统研究制造业AI应用场景，拓宽boss-pitch的数据支撑面
> 委托方：亚俊氏（真空封口设备制造商，60+SKU，3个生产基地，24条真空袋线+25条设备线）
> 产出形式：深度研究报告（含真实落地案例和效果数据）
> 下游消费者：research/yjs-boss-pitch（老板汇报材料）
> 聚焦：两条核心赚钱业务线（Wevac真空袋 + ODM设备代工）

### 2026-02-17 项目初始化 + 需求画像 + 10个AI场景数据采集完成
commit: 7a97eb0
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/d0-research-brief.md` — 研究需求画像（2条业务线×5场景=10个AI场景）

**业务线A：Wevac真空袋产线（佛山+新加坡，24条线）**

- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/a1-film-inspection.md` — A1 薄膜视觉质检（成熟度4/5，投入550-1270万⚠️，ROI 12-18月回收）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/a2-blown-film-optimization.md` — A2 吹膜工艺AI优化（成熟度3.5/5，废品率降30-50%⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/a3-production-scheduling.md` — A3 24条线排产优化（成熟度4/5，投入60-150万⚠️，年化收益100-260万⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/a4-biodegradable-formulation.md` — A4 可降解材料配方AI（成熟度3.5/5，投入95-220万⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/a5-fba-demand-forecast.md` — A5 Amazon FBA需求预测（成熟度4.5/5，SaaS工具$200-2000/月）

**业务线B：ODM设备代工（广州基地，10组装+15注塑线）**

- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/b1-injection-inspection.md` — B1 注塑件视觉质检（成熟度4/5，投入150-600万⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/b2-injection-process-optimization.md` — B2 注塑工艺AI优化（成熟度3-4/5，投入120-450万⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/b3-predictive-maintenance.md` — B3 注塑机预测性维护（成熟度4/5，投入27.5-190万⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/b4-smart-quoting.md` — B4 ODM智能报价系统（综合成熟度3.3/5，报价周期从3-7天→数小时⚠️）
- ptr: `git:7a97eb0:research/yjs-mfg-ai/data/b5-ai-design.md` — B5 AI辅助产品设计（成熟度2-4/5，概念设计提速50-70%⚠️）

### 2026-02-17 阶段3：10场景横向对比汇总报告
commit: cc35c7f
- ptr: `git:cc35c7f:research/yjs-mfg-ai/analysis/scenarios-comparison.md` — 横向对比v1（P0: A5+B5 / P1: B2+A3+B1 / P2: 其余5个）

### 2026-02-17 阶段4：v1审计（发现严重质量问题）
commit: uncommitted (v1审计已被v2覆盖)
- v1审计结果：A线C级（8 ERROR）、B线C级（14 ERROR）、对比报告B级（2 ERROR）
- 主要问题：URL编造（A3失效率53%）、案例空白（A1）、ROI跨方案混合（B4/A2）

### 2026-02-17 v2重新采集：10场景数据+横向对比+审计
commit: 4e437bf

v2改进：v1的24个ERROR全部修复，所有URL经curl验证，ROI分方案独立计算。

**v2数据文件（10场景全部重写）：**

业务线A：Wevac真空袋产线
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/a1-film-inspection.md` — A1 薄膜视觉质检（成熟度4/5，投入550-1270万⚠️，回收期0.7-4.4年⚠️）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/a2-blown-film-optimization.md` — A2 吹膜工艺优化（成熟度3.5/5，先导100-250万⚠️，回收期1.2-8.3年⚠️）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/a3-production-scheduling.md` — A3 排产优化（成熟度4/5，投入/ROI数据不足，Panasonic案例：工时-75%）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/a4-biodegradable-formulation.md` — A4 配方优化（成熟度3.5/5，投入95-220万⚠️，回收期6-18月⚠️）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/a5-fba-demand-forecast.md` — A5 FBA需求预测（成熟度4.5/5，SaaS $3-6K/年，ROI 12-59x⚠️）

业务线B：ODM设备代工
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/b1-injection-inspection.md` — B1 注塑件质检（成熟度4/5，投入150-500万⚠️，回收期1-3年⚠️）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/b2-injection-process-optimization.md` — B2 注塑工艺优化（成熟度3-4/5，路径A 45-120万⚠️，ROI分3路径独立计算）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/b3-predictive-maintenance.md` — B3 预测性维护（成熟度4/5，Augury Forrester TEI 310% ROI）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/b4-smart-quoting.md` — B4 智能报价（成熟度3.3/5，方案A 30-50万⚠️，回收期0.7-1.1年⚠️）
- ptr: `git:4e437bf:research/yjs-mfg-ai/data/b5-ai-design.md` — B5 AI辅助设计（成熟度2-4/5，投入5-12万⚠️，回收期6-12月⚠️）

**v2横向对比：**
- ptr: `git:4e437bf:research/yjs-mfg-ai/analysis/scenarios-comparison.md` — 横向对比v2（P0: A5+B5 / P1: B2路径A+B1+B4 / P2: 其余，ROI分16行独立列示）

**v2审计：**
- ptr: `git:4e437bf:research/yjs-mfg-ai/analysis/audit-a-line.md` — A线审计v2（A2回收期ERROR已修复，其余A/B级）
- ptr: `git:4e437bf:research/yjs-mfg-ai/analysis/audit-b-line.md` — B线审计v2（A级：0 ERROR，9 WARNING）
- ptr: `git:4e437bf:research/yjs-mfg-ai/analysis/audit-comparison.md` — 对比报告审计v2（A级：0 ERROR，5 WARNING）

### 2026-02-19 阶段5：归档
commit: uncommitted
- ptr: `file:research/yjs-mfg-ai/research-log.md` — 研究过程日志（含5条核心教训，v1→v2全过程复盘）
