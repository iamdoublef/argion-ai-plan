# Swiss 说明书 QA 审计规范（SOT · 双流水线共享）

**版本**：v1.3
**日期**：2026-05-17
**适用范围**：Swiss A5 booklet 产品说明书全流程质量保障 — **PDF/HTML 流水线 + DOCX 流水线**
**引用标准**：`DESIGN-STANDARD.md`（视觉 + 内容结构标准 SOT）

> ## 本文是 SOT (Single Source of Truth)
>
> 本文件定义审计**流程和方法**；审计**标准**在 `DESIGN-STANDARD.md` 中。
> Audit agent 执行审计时，必须同时读取本文件和 `DESIGN-STANDARD.md`。
>
> 两条流水线（PDF/HTML + DOCX）共享 Phase 1（pre-render）+ Phase 4（翻译质检）+ Phase 5（全变体验证）。
> Phase 2（构建）+ Phase 3（post-render 视觉）按各自流水线实现：
> - **PDF/HTML 流水线**：`build-variant.js` + `audit-visual.js`（Playwright）
> - **DOCX 流水线**：`generator.py` + `ai-qa.py` 3 轮 fix-or-escalate + anti-cheat + 人工 review
>
> 详见 §八 DOCX 流水线审计适配。

---

## 一、审计流程总览

```
Phase 1: Pre-render 静态检查（不需要构建 HTML）
  ├─ 1a. JSON 结构验证
  ├─ 1b. 翻译完整性检查
  └─ 1c. 图片资源检查

Phase 2: Build（构建 HTML）
  └─ node tools/build-variant.js → 生成 HTML

Phase 3: Post-render 视觉审计（需要 Playwright）
  ├─ 3a. 页面溢出检测
  ├─ 3b. 图片渲染检查
  ├─ 3c. 内容完整性验证
  └─ 3d. 数据残留检查

Phase 4: 翻译质检（非源语言变体）
  ├─ 4a. 源语言残留检测
  ├─ 4b. 已知失败模式检查
  └─ 4c. 术语一致性

Phase 5: 全变体验证
  └─ 对所有 region × brand 组合重复 Phase 2-4
```

### 判定标准

| 级别 | 含义 | 处理 |
|------|------|------|
| ERROR | 必须修复才能交付 | 阻断 |
| WARNING | 应修复，可带条件交付 | 标记并跟踪 |
| INFO | 建议优化 | 记录 |

---

## 二、Phase 1 — Pre-render 静态检查

### 1a. JSON 结构验证

检查所有 `content/source/chapters/*.json`：

| 检查项 | 对应标准 | 严重级别 | 检查方法 |
|--------|---------|---------|---------|
| warranty_card 字段不跨 page block | DESIGN-STANDARD §十七 C1 | ERROR | 遍历所有 page block，统计 warranty_card 出现次数，>1 则报错 |
| figure 引用指向存在的 images.json key | DESIGN-STANDARD §十 | ERROR | 解析 figure 引用，与 images.json 交叉比对 |
| text_id 唯一且有对应翻译 | — | ERROR | 收集所有 text_id，检查 compiled JSON 中是否存在 |
| object_fit 值为 contain | DESIGN-STANDARD §十七 C6 | WARNING | grep JSON 中所有 object_fit 字段值 |
| `rowspan` 配置与分组数据行数一致 | DESIGN-STANDARD §十七 C17 | ERROR | 检查结构化表格分组总行数与跨行配置是否匹配；不匹配则极易错位 |

### 1b. 翻译完整性检查

检查 `i18n/compiled/*.json`：

| 检查项 | 严重级别 | 检查方法 |
|--------|---------|---------|
| compiled JSON 中所有 text_id 均有非空值 | ERROR | 遍历 strings 对象，检查空值 |
| 模板变量 `{{}}` 语法正确 | ERROR | 正则匹配 `\{\{[^}]*\}\}`，检查变量名合法性 |

### 1c. 图片资源检查

| 检查项 | 严重级别 | 检查方法 |
|--------|---------|---------|
| images.json 中所有 file 指向真实文件 | ERROR | 逐个检查文件存在性 |
| 无未引用的孤立图片文件 | INFO | 图片目录文件 vs images.json 引用集合 |
| 同组图片存在极端尺寸差异时需人工复核承载方式 | WARNING | 对同一 `figure_row` / `split_panel` 内图片的渲染尺寸做横向比对，明显一大一小则标记 |

---

## 三、Phase 3 — Post-render 视觉审计

**工具**：`tools/audit-visual.js`（Playwright-based）

### 3a. 页面溢出检测

| 检查项 | 对应标准 | 严重级别 |
|--------|---------|---------|
| 所有元素的 scrollHeight ≤ clientHeight | §十七 C8 | ERROR |
| 所有元素的 scrollWidth ≤ clientWidth | §十七 C4/C5 | ERROR |
| 无空页面（content height < 10% page height） | — | WARNING |
| 同章连续页不得出现明显“大面积留白 + 下一页仍为同主题延续” | §十七 C15 | WARNING |
| `warranty_info + warranty_card` 若被拆页，需确认是否确因内容过长而非默认分页导致 | §十七 C16 | WARNING |
| 同一保修范围若被拆成“上页说明 + 下页空表格感”的形态，应标记为分页退化 | §十七 C16 | WARNING |

### 3b. 图片渲染检查

| 检查项 | 对应标准 | 严重级别 |
|--------|---------|---------|
| 图片右边界 ≤ page 右边界 | §十七 C5 | ERROR |
| 图片 naturalWidth/naturalHeight vs renderWidth/renderHeight 比例差 < 5% | §十 | WARNING |
| 无 0-width 或 0-height 图片 | — | ERROR |
| 同组图片承载尺寸明显不一致且无内容理由支持 | §十七 C14 | WARNING |

### 3c. 数据残留检查

在渲染后的 HTML 文本中检查：

| 检查项 | 严重级别 | 检查方法 |
|--------|---------|---------|
| 无 `{{...}}` 未替换的模板变量 | ERROR | 正则搜索 |
| 无 `undefined`、`null`、`TODO` 字面量 | ERROR | 文本搜索 |
| 无 `NaN` 字面量 | ERROR | 文本搜索 |

### 3d. 封面 absolute 元素排除

审计工具检测到 `.page` 第一页（封面）的子元素重叠时，如果重叠元素带有 `position: absolute`，应标记为 INFO 而非 ERROR（见 DESIGN-STANDARD §十七 C10）。

---

## 四、Phase 4 — 翻译质检

> 仅对非源语言（非 zh-CN）的变体执行。

### 4a. 源语言残留检测

| 目标语言 | 检查正则 | 严重级别 |
|---------|---------|---------|
| en, de, it | `[\u4e00-\u9fff]`（CJK 字符） | ERROR |
| zh-HK, zh-TW | 与 zh-CN compiled JSON 逐条对比，完全相同的条目标记 | WARNING |

**检查位置**：compiled JSON 的 strings 值 + 渲染后 HTML 的文本内容。

### 4b. 已知翻译失败模式

从本次 V23 英文版审计中总结的 3 种失败模式：

| # | 失败模式 | 表现 | 检测方法 | 严重级别 |
|---|---------|------|---------|---------|
| T1 | **Truncation（截断）** | 翻译模型在某行后停止翻译，后续行的 target_text 保持中文 | 检查 compiled JSON 中连续多条含 CJK 的 entries | ERROR |
| T2 | **Wrong key mapping（错位映射）** | A 段落的翻译出现在 B 段落的 text_id 下 | 语义比对 source_text 和 target_text（需 LLM 辅助或人工） | WARNING |
| T3 | **Key-value swap（键值交换）** | 两条 text_id 的翻译互换了位置 | 同 T2，需要语义分析 | WARNING |

> T2 和 T3 难以完全自动化检测，建议在 compile 阶段加 `--check-lang` 拦截 T1，T2/T3 依赖审计 agent 人工抽检。

### 4c. Workbook 同步状态检查

| 检查项 | 严重级别 | 检查方法 |
|--------|---------|---------|
| compiled JSON 和 workbook 的条目数一致 | WARNING | 比对 strings 对象 key 数量 vs workbook rows 数量 |
| compiled JSON 中手动修改的条目已同步回 workbook | WARNING | 比对 compiled JSON value 和 workbook target_text |

> ⚠️ **关键风险**：如果 compiled JSON 被手动修复但 workbook 未同步，重新运行 `compile-translation-workbook.js` 会**覆盖修复**。
> 工具链中应使用 `tools/sync-json-to-workbook.js` 反写 workbook，或在 QA report 中明确标注 WARNING。

### 4d. 单位一致性检查

| 检查项 | 严重级别 | 检查方法 |
|--------|---------|---------|
| 正文中的尺寸/温度/时间/重量/压力单位与规格表单位一致 | ERROR | 对照 `product.json` 的 `specs.us / specs.eu` 与 compiled JSON 正文表达抽检 |
| 同一地区版本中不得同时出现冲突的双套单位口径 | WARNING | 检查正文和规格表是否混用不同单位体系或不同写法 |
| `zh-HK` / `zh-TW` 不得回退为逐字简转繁 | WARNING | 与 zh-CN 逐条比对，完全相同条目标记并人工复核 |

---

## 五、Phase 5 — 全变体验证

### 变体矩阵

每个产品需验证所有活跃变体。当前矩阵：

| 产品 | Region | Brand | Locale | 变体文件名模式 |
|------|--------|-------|--------|--------------|
| V23 | cn | wevac | zh-CN | v23-wevac-eu-cn.html |
| V23 | gb | wevac | en | v23-wevac-eu-gb.html |
| V23 | de | wevac | de | v23-wevac-eu-de.html |
| V23 | it | wevac | it | v23-wevac-eu-it.html |
| IMT050 | cn | wevac | zh-CN | imt050-wevac-eu-cn.html |
| IMT050 | gb | wevac | en | imt050-wevac-eu-gb.html |
| ... | ... | ... | ... | ... |

> 完整矩阵由 `tools/build-all.js --product <name>` 自动枚举。

### 全变体审计流程

```bash
# 构建所有变体 + 自动审计
node tools/build-all.js --product v23

# 输出示例：
# v23-wevac-eu-cn.html  PASS (0 errors, 0 warnings)
# v23-wevac-eu-gb.html  PASS (0 errors, 1 warning)
# v23-wevac-eu-de.html  FAIL (1 error: page overflow on page 12)
```

### 同一产品线批准版派生检查

- 当某产品线已经存在批准版时，后续地区/品牌版本的审计必须先对照批准版检查：
  - 章节顺序是否一致
  - 图文组织是否一致
  - 保修页与长表分页逻辑是否退化
  - 仅允许品牌字段、主题 token、本地化文本和市场/法规必要差异发生变化
- 若发现派生版本为了解决局部问题而改动正文结构，应标记为 WARNING，并回查是否应先修中文批准版或公共规范。
- 审计时应先区分“产品特有经验”和“公共失败模式”：
  - 产品特有经验看对应产品目录 README
  - 通用失败模式和通用检查点看本文件与 `DESIGN-STANDARD.md`

---

## 六、审计工具清单

| 工具 | 路径 | 用途 | Phase |
|------|------|------|-------|
| `audit-visual.js` | `tools/audit-visual.js` | Playwright 视觉审计 | 3 |
| `build-all.js` | `tools/build-all.js` | 批量构建 + 审计 | 2+3+4+5 |
| `compile-translation-workbook.js --check-lang` | `tools/compile-translation-workbook.js` | 翻译编译 + 语言检测 | 1b |
| `sync-json-to-workbook.js` | `tools/sync-json-to-workbook.js` | compiled JSON → workbook 反写 | 4c |

---

## 七、Writer 自检流程（必须执行）

Writer agent 在提交产品 JSON 修改后，**必须**执行以下自检：

```bash
# 1. 构建目标变体
node tools/build-variant.js --product products/<name> --region <region> --brand <brand>

# 2. 运行视觉审计
node tools/audit-visual.js output/<variant>.html

# 3. 如果是翻译相关修改，运行翻译质检
node tools/compile-translation-workbook.js --product products/<name> --locale <locale> --check-lang

# 4. 全变体验证（交付前）
node tools/build-all.js --product products/<name>
```

**Writer 自检不通过的，禁止提交给 Audit agent。**

---

## 八、DOCX 流水线审计适配

> DOCX 流水线（`swiss/tools/docx-pipeline/`）共享 SOT 但实现路径不同。本节说明哪些 Phase 直接复用、哪些需要替代实现。

### 8.1 Phase 共享/替代矩阵

| Phase | PDF/HTML | DOCX | 说明 |
|------|---------|------|------|
| 1a JSON 结构 | source JSON 校验 | `strings/{lang}.md` 结构校验 | 等效：检查 key 唯一 + 表格分组对齐 |
| 1b 翻译完整性 | compiled JSON 空值 + `{{}}` 残留 | `strings/{lang}.md` 空值 + master_unpacked 中 `{{*}}` 残留 | **完全共享语义**，工具不同 |
| 1c 图片资源 | images.json 校验 | W50 母版自带，仅检查 `word/media/` 完整 | W50 锁定，新 SKU 才需校验 |
| 2 Build | `build-variant.js` | `generator.py --lang {lang}` | 各自实现 |
| 3a 页面溢出 | Playwright scrollHeight | **页数变化** + **text_ratio** 代理 + 人工抽样 | DOCX 无 Playwright；C8/C9 转 §8.2 |
| 3b 图片渲染 | Playwright 边界检查 | W50 母版固定 + LO/Word 渲染 PNG 抽样 | 同上 |
| 3c 数据残留 | HTML 文本 grep | docx 文本提取 grep | **完全共享语义** |
| 4a CJK 残留 | HTML 文本 + compiled JSON | docx 文本 + `strings/{lang}.md` | **完全共享语义** |
| 4b T1/T2/T3 翻译失败 | 同 PDF 流水线 | 同 PDF 流水线 | **完全共享语义** |
| 4c Workbook 同步 | 同 PDF 流水线 | 同 PDF 流水线 | **完全共享语义** |
| 4d 单位一致性 | 同 PDF 流水线 | 同 PDF 流水线 | **完全共享语义** |
| 5 全变体验证 | 21 个 HTML | 7 个 docx（cn/en/de/it/gb/hk/tw） | 各自实现 |

### 8.2 DOCX 专属 anti-cheat（替代 Phase 3 视觉审计的"硬底线"部分）

| 检查项 | 阈值 | 严重级别 |
|-------|------|---------|
| `wt_count` (w:t 节点数) | ≥ 300 | ERROR |
| `image_hack` (整页图片替换) | false | ERROR |
| `text_ratio` | [0.95, 1.20] | ERROR |
| `validate.py` (官方 docx skill) | 通过 | ERROR |
| MS Word COM 打开（`compare_word.py` / `docx2pdf`） | 不报错 | ERROR（W28 教训）|
| 页数 = 15 (±1) | 是 | ERROR |
| `score_candidate.py`（仅 CN 有 target PDF） | = W50 (7.21/10.13) ±0.01 | ERROR |

任何一道挂 → 拒收 patch + 回滚。Python 实现见 `.claude/skills/docx-pipeline/references/anti-cheat-impl.md`。

### 8.3 3 轮 fix-or-escalate（DOCX 替代多轮 sweep）

DOCX 流水线**不做研究式调优**（W27→W50 那套 50 轮 sweep 是研究阶段，已结束）。生产阶段规则：

```
每个非 CN 语言生成后：
  迭代 N (N=1,2,3):
    1. 跑 Phase 1+3+4 检查（按 8.1 矩阵适配 DOCX）
    2. 跑 anti-cheat 三道闸 + 页数 + Word COM（8.2）
    3. 若全通过 → 标记 PASS，下一语言
    4. 若有具体可定位错误（如 wt_count<300 / CJK 残留 / 页数 14）：
       a. 精准定位（哪页 / 哪段 / 哪个 placeholder）
       b. 单维度 fix（一轮只改一处）
       c. 写 patches/{lang}.md 日志
       d. 重跑步骤 1-3
    5. 若 N=3 仍未通过 → 停，写诊断报告，转人工
```

**禁用**：sub-cohort sweep、研究式 lever exploration、5+ 轮迭代。

### 8.4 DOCX 人工 review gate

下述节点必须**大 boss 或指定人工 reviewer** 通过才能继续：

| Gate | 触发 | 检查内容 |
|------|------|---------|
| G1 母版生成 | 阶段 1 完成 | PLACEHOLDER_MAP 命名合理、round-trip CN = W50 零误差、抽样占位符位置合理 |
| G2 翻译对齐 | 阶段 2 完成 | spot-check 关键术语跨语言一致（IMT050/Wevac/制冰机/警告/单位） |
| G3 批量生成完成 | 阶段 3 完成 | 7 个 docx 抽样人工看（LO 渲染 PNG）、ACCEPTANCE_REPORT.md review |
| G4 fix-or-escalate 升级 | 任意语言 N=3 未通过 | 诊断报告 review + 决定（人工修 / 改 strings / 砍语言交付） |

详见 `.claude/skills/docx-pipeline/SKILL.md`。

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-03-16 | 初稿创建：5 阶段审计流程、翻译质检规则（3 种失败模式）、全变体验证矩阵、工具清单 |
| v1.1 | 2026-03-12 | 回写 V23 派生审计经验：rowspan 错位、长页留白、保修分页、正文与规格表单位一致性、批准版派生检查 |
| v1.2 | 2026-03-12 | 强化共性检查点：同组图片尺寸失衡、保修同范围拆页退化、产品 README 与公共 QA 的归属边界 |
| v1.3 | 2026-05-17 | **升级为 SOT**：双流水线共享声明，新增§八 DOCX 流水线审计适配（Phase 共享矩阵、anti-cheat、3 轮 fix-or-escalate、4 个人工 review gate） |
