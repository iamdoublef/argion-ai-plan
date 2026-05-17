# DOCX 多语言流水线设计

> **日期**：2026-05-17
> **状态**：设计中，等大 boss review
> **作者**：管理之神（AI）+ 大 boss
> **产品**：IMT050 自动制冰机说明书 · 7 个语言版本（cn/de/en/it/gb/hk/tw）

---

## 一、背景

### 1.1 起点
- 历时 50+ 轮 OOXML 优化得到 **W50 docx**：评分 7.21/10.13（最优单 SKU 单语言版本）
- 现有 PDF 流水线 `swiss/tools/export-pdf.js` + `build-variant.js` 已能产出 7 语言 PDF
- 现有 `swiss/tools/export-docx.js` 能产出多语言 docx 但**视觉差 4.5 分**（11.74 vs W50 7.21）

### 1.2 矛盾
- W50 视觉最好但**未模板化**（200+ OOXML 微调与具体中文文本耦合）
- export-docx.js 模板化但视觉差（与 W50 lever 没融合）

### 1.3 目标
**做 docx 流水线 = PDF 流水线的等效物**：
- 输入翻译字典 → 输出多语言 docx
- 保留 W50 视觉质量
- 模型参与质量保证（AI QA + 自修复）
- 母版一致（master 永远只有一份）
- 产品术语跨语言一致

---

## 二、架构选型

### 2.1 路径选择
**A 路径**：W50 母版 + placeholder 替换 → 走官方 docx skill (unpack/pack/validate)

否决了：
- B 路径（docx-js）：放弃 W50 视觉到 11.74，与 boss "docx skill 硬约束" 冲突
- C 路径（A + 后处理 backport 到 export-docx.js）：长期可维护但短期工程量大

### 2.2 实施架构
**架构 2**：静态 placeholder 母版 + AI QA + AI 自修复 loop

否决了：
- 架构 1（仅 QA 不修复）：部分语言因 wrap 失败时质量参差
- 架构 3（AI 全流水线含翻译）：产品术语风险大，与 PDF 流水线人工翻译体系脱节

---

## 三、架构与组件

### 3.1 目录结构

```
swiss/tools/docx-pipeline/
├── master_template.docx          ← W50 + placeholder 化（永远一份）
├── master_unpacked/              ← unpacked XML 含 {{key}} 占位符
├── strings/
│   ├── cn.md  (复用 swiss/template/cn/ 内容)
│   ├── en.md  (复用 swiss/template/en/)
│   ├── de.md, it.md, gb.md, hk.md, tw.md
├── patches/                       ← AI 自修复产物（MD 格式可审计）
│   ├── en.md (英文版 OOXML 修复日志)
│   ├── de.md, it.md, ...
├── docs/
│   ├── PLACEHOLDER_MAP.md         ← 阶段 1 人工 review 产物
│   ├── ACCEPTANCE_REPORT.md       ← 验收报告
│   └── PIPELINE_README.md         ← 客户使用文档
├── generator.py                   ← 占位符替换 + pack（Python 确定性）
├── ai-qa.py                       ← AI QA + 自修复（调用 agent）
└── pipeline.py                    ← 全流水线入口

swiss/output/
├── imt050-wevac-eu-cn.docx       ← 生成结果（评分 = W50）
├── imt050-wevac-eu-en.docx
├── imt050-wevac-eu-de.docx
├── imt050-wevac-eu-it.docx
├── imt050-wevac-eu-gb.docx
├── imt050-wevac-eu-hk.docx
└── imt050-wevac-eu-tw.docx
```

### 3.2 4 大组件

#### 1. `master_template.docx` — 母版

- 来源：`final/imt050-wevac-eu-cn.docx`（W50）
- 处理：所有中文字符串 → `{{key}}` 占位符
- 数量：约 200-400 个 placeholder
- **唯一**，保证视觉一致

#### 2. `strings/{lang}.md` — 翻译字典（MD 表格格式）

- 复用 PDF 流水线现有翻译（`swiss/template/{lang}/`）
- 人类编辑友好，模型读取友好
- 每个语言一份，相同 key 跨语言对齐

#### 3. `generator.py` — 占位符替换器

确定性 Python 脚本（不让 AI 做）：
```
1. unpack master_template.docx → unpacked/
2. 读 strings/{lang}.md → 构建 {{key}} → 译文 字典
3. 遍历 unpacked/word/*.xml → 替换 {{key}}
4. apply patches/{lang}.md（如存在）→ 改 OOXML
5. pack → output/imt050-wevac-eu-{lang}.docx
6. validate
```

#### 4. `ai-qa.py` — AI QA + 自修复 loop

AI agent 主控：
```
1. 跑 score_candidate.py（仅 CN 版有目标 PDF 可评分）
2. 跑 compare_word.py（Word COM 必须可打开）
3. anti-cheat 检查
4. 若劣化 → AI 选 lever（参照 METHODOLOGY.md）→ 写入 patches/{lang}.md
5. 重跑 generator.py 重新生成
6. 最多 5 轮自修复
7. 输出 ACCEPTANCE_REPORT.md
```

---

## 四、端到端数据流

### 阶段 1：母版生成 + 人工确认 ⚠️

```
W50 docx
   │
   ▼
[AI agent] 提取中文 → master_template.docx + cn.md
   │
   ▼
自动 round-trip 验证：
   generator.py --lang cn
   → 用 master + cn.md 重新生成 CN docx
   → 评分必须 = W50 (7.21/10.13，零误差)
   │
   ▼
AI 输出 PLACEHOLDER_MAP.md：
  - 每个 {{key}} 对应中文原文
  - 文档中位置（page / section）
  - 提取规则说明
   │
   ▼
⚠️ 大 boss 人工 review gate ⚠️
   1. 看 PLACEHOLDER_MAP.md 确认 key 命名 + 提取范围
   2. 看 round-trip CN docx 确认视觉 = W50
   3. 抽样看 master_unpacked/word/document.xml 确认占位符位置合理
   │
通过 → 进入阶段 2
不通过 → AI 修正提取逻辑，重做阶段 1
```

### 阶段 2：翻译字典对齐（人工 + AI 协作）

```
swiss/template/{en, de, it, gb, hk, tw}/  (PDF 流水线已有)
   │
   ▼
[AI agent] 把 PDF 翻译映射到 docx placeholder key
   │
   └→ strings/{en, de, it, gb, hk, tw}.md
   │
⚠️ 人工 review 翻译对齐（spot check 关键术语）
```

### 阶段 3：流水线生成 + AI 自修复（核心循环）

```
for lang in [cn, en, de, it, gb, hk, tw]:
  generator.py --lang {lang}
    → output/imt050-wevac-eu-{lang}.docx
  ai-qa.py --lang {lang} --max-iter 5
    → 验证 + 自修复 + 写 patches/{lang}.md
```

### 阶段 4：批量交付

```
output/
├── imt050-wevac-eu-{cn, en, de, it, gb, hk, tw}.docx  (7 个)

docs/
├── PLACEHOLDER_MAP.md
├── ACCEPTANCE_REPORT.md
└── patches/{lang}.md × 6
```

---

## 五、关键文件 Schema

### 5.1 `strings/cn.md` 格式

```markdown
# IMT050 中文翻译字典

> 这是 master_template.docx 占位符的中文映射。
> 人工 review 这份 → 模型读这份替换 {{key}} → 生成 imt050-wevac-eu-cn.docx
> 评分必须 = W50 (7.21/10.13)

## 封面

| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| cover_brand | 威富可 | p1 顶部 | 品牌名 |
| cover_model | IMT050 | p1 中央 | 型号 |
...

## 第 1 章 安全注意事项 (p3-p4)

| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| safety_warning_1 | 本产品仅供家庭使用 | p3 警告框第 1 条 | |
...
```

### 5.2 `patches/{lang}.md` 格式

```markdown
# {lang} 版 OOXML 修复日志

> 每条修复 = 1 个 AI agent iter
> 人工可随时 review + 决定是否回滚某条

## 修复 1 — p3 char-spacing tighten

- **状态**: ✅ Applied (iter-1)
- **触发**: English 版生成后，p3 diff = 14.2 (vs CN W50 11.86)
- **原因**: 英文文本占宽 1.5x 中文，p3 wrap 多了一行
- **方法论**: rPr w:spacing tighten（METHODOLOGY § 2.2 小字号 DOWN 方向）
- **具体改动**:
  - selector: `sz=14 BLACK runs in p3 paragraphs`
  - before: `w:spacing w:val="10"`
  - after: `w:spacing w:val="8"`
  - sites: 14
- **效果**: p3 diff 14.2 → 12.8 (-1.4)，无其他页回退
- **commit**: `<sha>`
```

### 5.3 命令行接口

```bash
# 生成单语言
python generator.py --lang en
python generator.py --lang de

# 全部 7 语言
python generator.py --all

# QA + 自修复
python ai-qa.py --lang en --max-iter 5

# 全流水线
python pipeline.py --all
```

---

## 六、模型主控（AI agent）

### 6.1 AI agent prompt 模板（自修复用）

```
任务：{lang} docx 视觉劣化，修复 OOXML。

基线：output/imt050-wevac-eu-cn.docx（W50, 7.21/10.13）
劣化：output/imt050-wevac-eu-{lang}.docx
per-page diff: [...]

步骤：
1. 读 METHODOLOGY.md (所有 lever + 坑)
2. 读 patches/{lang}.md (已应用 patch)
3. 选 1 个未试 lever（sub-cohort 二次 sweep 优先）
4. 写入新 patch 条目到 patches/{lang}.md（详细 selector + before/after）
5. 调 generator.py --lang {lang} 重新生成
6. 验证：
   - score_candidate.py
   - compare_word.py
   - anti-cheat
7. 若改善 → 标记 ✅ Applied
   若劣化 → 标记 ❌ Rejected + rollback
8. 若超过 5 轮仍未达标 → 停止，输出诊断报告
```

### 6.2 边界

- **AI 只做决策**（选 lever / 判断接受 / 写日志）
- **Python helper 做确定性操作**（XML 替换、pack、validate、scoring）
- **人工审查点**：阶段 1 master + 阶段 2 翻译对齐 + 随时审 patches/{lang}.md

---

## 七、错误处理

| 错误类型 | 检测点 | 处理 |
|---------|--------|------|
| 占位符漏字段 | 阶段 1 round-trip CN ≠ W50 | AI diff → 补占位符 → 重做。人工 review gate 必须发现 |
| validate 失败 | 每次 pack 后 | AI 看错误 → 修 XML (METHODOLOGY § 3.1) → 重 pack |
| Word COM 打开失败 | compare_word.py | 立即拒绝 patch（W28 教训），回滚 + 换 lever |
| anti-cheat 失败 | wt_count<300 / image_hack / text_ratio | 立即拒绝 → 报告人工 |
| 视觉劣化但 validate pass | score > baseline + 容差 | AI sub-cohort sweep 修复（≤5 轮）|
| AI 自修复死循环 | iter > 5 仍未达标 | 自动停止 + 诊断报告 |
| patches 累积破坏 | wt_count 突降 / 页数变 | 自动 rollback 最后 patch + flag incompatible |

---

## 八、验收标准

### 8.1 强制项（不通过则拒绝交付）

| 检查项 | CN 版 | 其他语言 |
|--------|------|---------|
| validate.py 通过 | ✅ | ✅ |
| Word COM 可打开 | ✅ | ✅ |
| anti-cheat: wt_count ≥ 300 | ✅ | ✅ |
| anti-cheat: image_hack = false | ✅ | ✅ |
| anti-cheat: text_ratio ∈ [0.95, 1.20] | ✅ | ✅ |
| editable_pct = 100% | ✅ | ✅ |
| 页数 = 15 (±1) | ✅ | ✅ |

### 8.2 视觉项

| 检查项 | CN 版 | 其他语言 |
|--------|------|---------|
| score_candidate.py | **7.21/10.13 零误差** | 无目标 PDF，仅 wt_count + 页数 + Word 渲染 |
| per-page diff | 与 W50 完全一致 | LO 渲染 PNG 抽样人工 review |

### 8.3 文字一致性项

- 翻译来源复用 PDF 流水线（不重新翻译）
- 产品术语跨语言一致（IMT050/Wevac/Argion 等不可变）
- placeholder 命名跨语言相同 key 对应相同含义

---

## 九、复用价值

### 9.1 短期

7 个 IMT050 多语言 docx 交付，每个语言保留 W50 视觉。

### 9.2 长期

- **加新语言**（如西班牙文 es）：复制 strings/en.md → 翻译 → 跑 pipeline。约 1 小时。
- **加新 SKU**（如 IMT060）：需重做 master_template（若页面结构变），或复用（若仅文字变）。约 1-3 天。
- **替换品牌**（Argion/Vesta/Act）：改 strings 里 brand 字段即可。约 10 分钟。

---

## 十、实施工程量

| 阶段 | 工作 | 工程量 |
|------|------|--------|
| 阶段 1 | W50 → master + cn.md + round-trip 验证 + 人工 review | 半天 |
| 阶段 2 | 6 个语言翻译对齐（en/de/it/gb/hk/tw）| 半天 |
| 阶段 3 | pipeline + ai-qa.py + 自修复 loop 跑通 7 语言 | 1 天 |
| 阶段 4 | 验收 + 文档 + 交付 | 半天 |

**合计**：约 **2-3 个工作日**

---

## 十一、未尽事项 / 后续讨论

- [ ] V23/Vesta/Act 多 SKU 何时纳入（需评估页面结构差异）
- [ ] 是否集成到 `swiss/tools/build-all.js`（与 PDF 流水线统一入口）
- [ ] AI agent 模型选择（Sonnet 还是 Opus，成本 vs 效果）
- [ ] 翻译变更触发重新生成的机制（watch 文件改动 / 手动触发）

---

## 附录 A：参考文档

- `research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/METHODOLOGY.md` — 50 轮优化方法论 + 25+ 个坑
- `research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/SCORES.md` — 进展线
- `research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/final/imt050-wevac-eu-cn.docx` — W50 母版来源
- `swiss/tools/export-pdf.js` — 现有 PDF 流水线参考
- `swiss/tools/export-docx.js` — 现有 docx 流水线（视觉差，作为反例）
