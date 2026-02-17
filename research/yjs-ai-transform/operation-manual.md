# 亚俊氏 AI 转型研究方案 — 操作手册

> 项目代号：yjs-ai-transform
> 版本：v1.0
> 日期：2026-02-14

## 一、项目背景

广州亚俊氏真空科技股份有限公司（Argion，新三板874106）是一家专注真空厨房设备的中型制造企业，2024年营收2.92亿元，员工约350人。公司以ODM/OEM代工+自有品牌（Wevac、Vesta）并行，产品覆盖真空封口机、低温烹饪设备、制冷设备、真空袋等，主要销往欧美市场。

公司希望通过AI转型提升竞争力和盈利能力。

## 二、研究目标

1. 摸清公司现状（业务、组织、技术、财务）
2. 识别AI可落地的高价值场景
3. 制定分阶段AI转型路线图
4. 产出可执行的实施建议

## 三、研究阶段与Agent分工

### 阶段概览

```
Phase 1: 企业诊断        → company-diagnostics agent
Phase 2: 行业与竞品分析   → industry-analysis agent
Phase 3: AI场景识别与评估  → ai-opportunity agent
Phase 4: 转型路线图制定    → transformation-planner agent
Phase 5: 汇总与交付       → report-synthesizer agent
```

---

### Phase 1: 企业诊断（company-diagnostics）

目标：全面了解亚俊氏的业务现状、痛点和能力基线

#### 数据需求

| 数据项 | 来源 | 状态 |
|--------|------|------|
| 公司基本工商信息 | 公开（已采集） | ✅ 完成 |
| 产品线与定价 | 官网 + 电商平台 | ✅ 部分完成 |
| 财务数据（营收、利润率、成本结构） | 新三板公告/年报 | ⬜ 待采集 |
| 组织架构与部门设置 | 需公司提供 | ⬜ 待获取 |
| 生产流程与产线布局 | 需公司提供/现场调研 | ⬜ 待获取 |
| IT系统现状（ERP/MES/CRM等） | 需公司提供 | ⬜ 待获取 |
| 供应链管理方式 | 需公司提供 | ⬜ 待获取 |
| 质量管理体系 | 需公司提供 | ⬜ 待获取 |
| 客户结构（ODM vs 自有品牌占比） | 需公司提供 | ⬜ 待获取 |
| 研发流程与专利情况 | 公开+公司提供 | ⬜ 待采集 |

#### 分析框架

- **McKinsey 7S**：Strategy、Structure、Systems、Shared Values、Skills、Style、Staff
- **价值链分析**：研发→采购→生产→质检→仓储→销售→售后，逐环节识别效率瓶颈
- **数字化成熟度评估**：按 5 级模型（初始→重复→定义→管理→优化）评估各业务环节

#### 产出

- `research/yjs-ai-transform/phase1/company-diagnosis.md` — 企业诊断报告
- `research/yjs-ai-transform/phase1/pain-points.md` — 痛点清单（按业务环节分类）
- `research/yjs-ai-transform/phase1/digital-maturity.md` — 数字化成熟度评估

---

### Phase 2: 行业与竞品分析（industry-analysis）

目标：了解行业趋势、竞争格局、标杆企业的AI实践

#### 数据需求

| 数据项 | 来源 | 状态 |
|--------|------|------|
| 全球真空设备市场规模与增速 | 行业报告（已采集） | ✅ 完成 |
| 主要竞争对手（FoodSaver/Anova/Breville等） | 公开 | ⬜ 待采集 |
| 竞品AI应用案例 | 公开 | ⬜ 待采集 |
| 制造业AI转型标杆案例 | 公开 | ⬜ 待采集 |
| ODM/OEM行业AI趋势 | 公开 | ⬜ 待采集 |
| 小家电行业AI应用现状 | 公开 | ⬜ 待采集 |

#### 分析框架

- **Porter's Five Forces**：供应商议价力、买方议价力、新进入者威胁、替代品威胁、行业竞争
- **竞品对标矩阵**：产品线、技术能力、AI应用、市场份额、品牌力
- **行业AI应用图谱**：按价值链环节映射已有AI应用案例

#### 产出

- `research/yjs-ai-transform/phase2/industry-landscape.md` — 行业全景分析
- `research/yjs-ai-transform/phase2/competitor-benchmarking.md` — 竞品对标报告
- `research/yjs-ai-transform/phase2/ai-in-manufacturing.md` — 制造业AI应用案例库

---

### Phase 3: AI场景识别与评估（ai-opportunity）

目标：识别亚俊氏可落地的AI场景，按价值和可行性排序

#### 分析方法

1. **场景发现**：基于Phase 1痛点 + Phase 2行业案例，交叉匹配
2. **价值评估**：每个场景估算潜在收益（降本/增收/提效）
3. **可行性评估**：数据就绪度、技术复杂度、投入成本、实施周期
4. **优先级矩阵**：价值 × 可行性 四象限排序

#### 预设场景清单（待验证）

| 业务环节 | AI场景 | 预期价值 |
|----------|--------|----------|
| 研发设计 | AI辅助产品设计/CAD生成 | 缩短研发周期 |
| 研发设计 | 市场趋势AI分析→新品方向 | 提高新品命中率 |
| 生产制造 | AI视觉质检（封口质量、注塑缺陷） | 降低不良率 |
| 生产制造 | 预测性设备维护 | 减少停机时间 |
| 生产制造 | 产线排程优化 | 提高产能利用率 |
| 供应链 | 需求预测→智能备料 | 降低库存成本 |
| 供应链 | 供应商智能评估 | 降低采购风险 |
| 销售营销 | AI生成产品文案/图片（多语言） | 降低营销成本 |
| 销售营销 | 客户需求智能匹配（ODM询盘） | 提高转化率 |
| 客户服务 | AI客服/技术支持 | 降低人力成本 |
| 内部管理 | AI辅助文档处理/合同审核 | 提高效率 |
| 产品智能化 | IoT+AI智能真空封口机 | 产品溢价 |

#### 产出

- `research/yjs-ai-transform/phase3/ai-scenarios.md` — AI场景全景图
- `research/yjs-ai-transform/phase3/priority-matrix.md` — 优先级评估矩阵
- `research/yjs-ai-transform/phase3/quick-wins.md` — 速赢项目清单

---

### Phase 4: 转型路线图（transformation-planner）

目标：制定分阶段实施计划

#### 路线图框架

```
短期（0-6个月）：速赢项目，快速见效
  → 选2-3个低投入高回报场景先落地
  → 建立AI基础设施（数据治理、工具选型）

中期（6-18个月）：核心场景深化
  → 生产制造AI（质检、排程、预测维护）
  → 销售营销AI（内容生成、客户匹配）
  → 建立内部AI团队/能力

长期（18-36个月）：全面智能化
  → 产品智能化（IoT+AI）
  → 供应链端到端智能化
  → AI驱动的新业务模式探索
```

#### 每个阶段需明确

- 具体项目与负责人
- 预算估算（人力+工具+外部服务）
- KPI与验收标准
- 风险与应对措施
- 所需外部资源（供应商、顾问）

#### 产出

- `research/yjs-ai-transform/phase4/roadmap.md` — AI转型路线图
- `research/yjs-ai-transform/phase4/budget-estimate.md` — 预算估算
- `research/yjs-ai-transform/phase4/risk-assessment.md` — 风险评估
- `research/yjs-ai-transform/phase4/org-capability.md` — 组织能力建设方案

---

### Phase 5: 汇总与交付（report-synthesizer）

目标：整合所有阶段产出，生成最终交付物

#### 产出

- `research/yjs-ai-transform/deliverables/executive-summary.md` — 高管摘要（3页）
- `research/yjs-ai-transform/deliverables/full-report.md` — 完整研究报告
- `research/yjs-ai-transform/deliverables/action-plan.md` — 可执行行动计划
- `research/yjs-ai-transform/deliverables/presentation-outline.md` — 汇报PPT大纲

---

## 四、数据采集策略

### 公开数据（Agent可自主采集）

| 数据类型 | 采集方式 | 工具 |
|----------|----------|------|
| 企业工商信息 | 爱企查/天眼查 | Playwright MCP |
| 新三板公告/年报 | 全国股转系统官网 | Playwright MCP |
| 竞品信息 | 官网/Amazon/行业媒体 | Playwright MCP |
| 行业报告摘要 | Google/百度搜索 | Playwright MCP |
| 专利信息 | 国家知识产权局 | Playwright MCP |
| 招聘信息（推断组织结构） | 猎聘/前程无忧 | Playwright MCP |

### 需公司提供的数据

| 数据类型 | 重要性 | 替代方案 |
|----------|--------|----------|
| 详细财务数据（成本结构、利润率） | 高 | 用新三板公开数据估算 |
| 组织架构图 | 高 | 用招聘信息+管理层信息推断 |
| 生产流程文档 | 高 | 用行业通用流程+产品线推断 |
| IT系统清单 | 中 | 假设基础水平，方案覆盖多种情况 |
| 客户结构数据 | 中 | 用公开信息推断 |
| 质量数据（不良率等） | 中 | 用行业平均值 |

### 数据缺失处理原则

1. 优先用公开数据
2. 公开数据不足时，用行业平均值/合理假设，并明确标注
3. 关键假设列入"待验证清单"，交付时提醒客户确认
4. 绝不编造具体数字

---

## 五、Agent 执行规范

### 通用规范

- 所有产出文件存放在 `research/yjs-ai-transform/` 对应阶段目录
- 每个阶段完成后更新 `research/yjs-ai-transform/INDEX.md`
- 数据来源必须标注（URL/文件路径/假设说明）
- 使用中文撰写所有报告
- 遵循 `ops/policy.md` 的 Index-First 规范

### Agent 调用顺序

```
Phase 1 (company-diagnostics) ──→ Phase 2 (industry-analysis)
         ↘                              ↙
          Phase 3 (ai-opportunity) ←──┘
                    ↓
          Phase 4 (transformation-planner)
                    ↓
          Phase 5 (report-synthesizer)
```

Phase 1 和 Phase 2 可以并行执行。Phase 3 依赖两者的产出。

### 质量检查点

每个阶段完成后，执行以下检查：
1. 所有结论是否有数据/来源支撑？
2. 假设是否明确标注？
3. 产出文件是否符合目录规范？
4. INDEX.md 是否已更新？
