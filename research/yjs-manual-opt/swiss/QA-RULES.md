# Swiss 说明书 QA 审计规范

**版本**：v1.0  
**日期**：2026-03-16  
**适用范围**：Swiss A5 booklet 产品说明书全流程质量保障  
**引用标准**：`DESIGN-STANDARD.md`（视觉 + 内容结构标准）

> 本文件定义审计**流程和方法**。审计**标准**在 DESIGN-STANDARD.md 中。
> Audit agent 执行审计时，必须同时读取本文件和 DESIGN-STANDARD.md。

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

---

## 三、Phase 3 — Post-render 视觉审计

**工具**：`tools/audit-visual.js`（Playwright-based）

### 3a. 页面溢出检测

| 检查项 | 对应标准 | 严重级别 |
|--------|---------|---------|
| 所有元素的 scrollHeight ≤ clientHeight | §十七 C8 | ERROR |
| 所有元素的 scrollWidth ≤ clientWidth | §十七 C4/C5 | ERROR |
| 无空页面（content height < 10% page height） | — | WARNING |

### 3b. 图片渲染检查

| 检查项 | 对应标准 | 严重级别 |
|--------|---------|---------|
| 图片右边界 ≤ page 右边界 | §十七 C5 | ERROR |
| 图片 naturalWidth/naturalHeight vs renderWidth/renderHeight 比例差 < 5% | §十 | WARNING |
| 无 0-width 或 0-height 图片 | — | ERROR |

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

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-03-16 | 初稿创建：5 阶段审计流程、翻译质检规则（3 种失败模式）、全变体验证矩阵、工具清单 |
