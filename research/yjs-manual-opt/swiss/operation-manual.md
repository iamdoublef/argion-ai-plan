# Swiss 说明书系统操作手册

**版本**：v1.0
**日期**：2026-03-12
**适用范围**：`research/yjs-manual-opt/swiss/` 下的 A5 共享母版说明书体系

---

## 一、系统概览

Swiss 说明书系统是一套 **JSON 单源驱动、多变体输出** 的产品说明书生产线。

### 核心特征

- **一份内容，多种输出**：同一套 JSON 内容源 + 译文 → HTML/PDF（自有品牌） + DOCX/PDF（ODM 客户）
- **A5 竖版**：148mm × 210mm
- **变体矩阵**：7 地区 × 3 品牌 = 最多 21 种组合
- **共享母版**：所有产品共用一套 CSS + 模板骨架，差异仅落在内容 JSON 和产品图片

### 当前产品

| 产品 | 目录 | 状态 |
|------|------|------|
| V23（真空封口机） | `products/v23/` | 已完成 |
| IMT050（制冰机） | `products/imt050/` | 已完成 |

### 输出双轨

| 交付线 | 格式 | 用途 |
|--------|------|------|
| 自有品牌 | HTML + PDF | Wevac / Vesta / ACT 品牌包装内说明书 |
| ODM 客户 | DOCX + PDF | 客户可编辑、替换品牌后使用 |

---

## 二、目录结构

```
swiss/
├── DESIGN-STANDARD.md        ← 唯一视觉标准
├── QA-RULES.md                ← 审计流程与规则
├── SOP-new-product.md         ← 新产品接入 + 维护流程
├── WORD-BASE-TEMPLATE-CN.md   ← Word 母版规范
├── standards/                 ← 规范资产（术语、品牌语言、单位、警示语、AI prompt）
├── products/
│   ├── v23/
│   │   ├── product.json       ← 产品事实（规格、品牌矩阵、区域矩阵）
│   │   ├── images.json        ← 语义图片 ID → 文件映射
│   │   ├── images/            ← 产品图片
│   │   ├── content/source/
│   │   │   ├── manifest.json  ← 章节顺序、目录标题
│   │   │   └── chapters/      ← 各章 block 结构
│   │   └── i18n/
│   │       ├── compiled/      ← 正式译文 JSON（构建器读取）
│   │       └── workbooks/     ← 翻译工作簿 Excel（人工编辑面）
│   └── imt050/                ← 同上结构
├── template/
│   ├── v23-master-cn.html     ← V23 中文母版模板
│   ├── v23-master-en.html     ← V23 英文母版模板
│   ├── v23-master-de.html     ← V23 德文母版模板
│   ├── v23-master-it.html     ← V23 意大利文母版模板
│   ├── imt050-master-*.html   ← IMT050 各语言母版
│   └── shared/
│       ├── base/              ← 共享 CSS + 品牌主题
│       └── docx/              ← Word 基础母版
├── tools/                     ← 构建、导出、审计工具链
├── output/                    ← 生成的 HTML / PDF / DOCX
├── skills/                    ← AI skill 定义
│   ├── swiss-manual-a5/       ← 主技能
│   └── swiss-issue-fix/       ← 问题修复技能
└── 00_discussions/            ← 讨论记录
```

---

## 三、角色定义与职责

### 角色 1：内容管理员（人工）

**你是谁**：负责产品内容事实准确性的人。

**你要做的事**：
- 准备新产品的源稿（Word/PDF 原文、产品图片、参数规格表）
- 确认 AI 生成的结构草稿中的事实是否正确（章节划分、步骤、参数、零件名）
- 审核保修年限、品牌法律名称、制造商地址等法律信息
- 最终签字确认每个变体的关键页

**你不需要做的事**：
- 不改 HTML / CSS / 模板
- 不改构建脚本
- 不操作命令行工具

**验收检查页**：封面、目录、安全须知第一页、结构/控制面板页、操作页、保修页、保修卡续页

---

### 角色 2：翻译人员（人工）

**你是谁**：负责多语言译文质量的人。

**你要做的事**：
- 编辑 `i18n/workbooks/<locale>.xlsx` 工作簿中的译文
- 参照 `standards/` 下的术语表、品牌语言指南、单位规范、警示语规范
- 确保 `zh-HK` 和 `zh-TW` 是独立翻译，不是简转繁

**你不需要做的事**：
- 不改 HTML / CSS / 模板
- 不改章节结构 JSON
- 不改图片绑定

**关键参考文件**：
| 文件 | 用途 |
|------|------|
| `standards/terminology-glossary.json` | 术语统一 |
| `standards/brand-language-guide.md` | 品牌语言规范 |
| `standards/unit-and-measurement-policy.md` | 单位格式 |
| `standards/warning-language-policy.md` | 警示语措辞 |
| `standards/locale-guides.json` | 各语言本地化指南 |

---

### 角色 3：AI 模型操作员

**你是谁**：使用 AI 工具（Claude Code / VS Code Copilot Chat）完成说明书生成、修复、审计等工作的人。

**你要做的事**：
- 用正确的 agent 和 skill 指令驱动 AI 完成任务
- 运行构建和审计命令
- 将 AI 产出提交给内容管理员确认

**详细操作见下方 §四（AI 操作指南）。**

---

### 角色 4：开发人员

**你是谁**：维护构建工具链、模板骨架和 CSS 系统的人。

**你要做的事**：
- 维护 `tools/` 下的 Node.js 工具链
- 维护 `template/shared/base/` 下的共享 CSS
- 维护 `DESIGN-STANDARD.md`、`QA-RULES.md` 等规范文件
- 处理新 block 类型的开发需求
- 处理 Word/DOCX 导出引擎的问题

**关键文件**：
| 文件 | 职责 |
|------|------|
| `tools/build-variant.js` | 单变体 HTML 构建 |
| `tools/build-all.js` | 批量构建 + 自动审计 |
| `tools/export-pdf.js` | 单文件 PDF 导出 |
| `tools/export-pdf-batch.js` | 批量 PDF 导出 |
| `tools/export-docx.js` | DOCX 导出（14+ block 渲染器） |
| `tools/audit-visual.js` | Playwright 视觉审计 |
| `tools/export-translation-workbook.js` | 从 JSON 导出翻译工作簿 |
| `tools/compile-translation-workbook.js` | 从工作簿编译回 JSON |
| `tools/sync-json-to-workbook.js` | compiled JSON → 工作簿反写 |

---

## 四、AI 操作指南（核心章节）

本节教你如何用对的 AI agent/skill 完成不同任务。

### 4.1 系统中可用的 AI Agent（4 个）

| Agent 名称 | 用途 | 何时使用 |
|------------|------|---------|
| `swiss-manual-writer` | 生成 / 重构 / 修复说明书 | 新产品首版、修结构、修翻译、修排版 |
| `swiss-content-auditor` | 内容与版式审计 | 构建完成后质检、交付前全面审计 |

### 4.2 系统中可用的 AI Skill（2 个）

| Skill 名称 | 用途 |
|------------|------|
| `swiss-manual-a5` | 主技能：定义整个 Swiss 体系的输入契约、输出规格、block 类型、硬规则 |
| `swiss-issue-fix` | 问题修复技能：6 种决策树（溢出/图片/翻译/分页/DOCX/构建失败） |

### 4.3 规范资产中的 AI Prompt（3 个）

| Prompt 文件 | 用途 | 位置 |
|-------------|------|------|
| `ai-new-product-structure-prompt.md` | 从源稿生成结构化 JSON 草稿 | `standards/` |
| `ai-translation-draft-prompt.md` | 生成译文初稿 | `standards/` |
| `ai-localization-audit-prompt.md` | 译文本地化质检 | `standards/` |

---

### 4.4 任务类型 → 操作方法速查表

#### A. 新产品首版接入

**场景**：拿到一个新产品的 Word 原稿，要生成完整的多语言、多品牌说明书。

**操作步骤**：

1. **准备资料**：把 Word 原稿、产品图片、参数规格表放到 `products/<新产品>/` 目录

2. **告诉 AI 生成结构草稿**：
   ```
   使用 swiss-manual-writer agent。
   任务：新产品首版接入。
   产品目录：products/<新产品>/
   源稿：[附上 Word 文本或文件路径]
   请按 SOP-new-product.md Step 2 生成结构草稿。
   ```

3. **人工确认结构事实**（内容管理员）：
   - 检查章节划分是否合理
   - 检查步骤与图片对应关系
   - 检查参数、按钮、零件名是否正确
   - 检查品牌和保修信息

4. **告诉 AI 建立正式结构源**：
   ```
   已确认结构草稿。请建立正式结构源：
   - product.json
   - images.json
   - content/source/manifest.json
   - content/source/chapters/*.json
   ```

5. **导出翻译工作簿**：
   ```powershell
   cd D:\work\private\yjsplan\research\yjs-manual-opt\swiss
   node tools/export-translation-workbook.js --product products/<新产品> --all
   ```

6. **翻译人员审核工作簿**（翻译人员）：
   - 编辑 `i18n/workbooks/<locale>.xlsx`

7. **编译译文**：
   ```powershell
   node tools/compile-translation-workbook.js --product products/<新产品> --all
   ```

8. **构建 HTML**：
   ```powershell
   node tools/build-variant.js --product products/<新产品> --region cn
   ```

9. **导出 PDF / DOCX**：
   ```powershell
   node tools/export-pdf.js output/<产品>-<品牌>-<市场>-<地区>.html
   node tools/export-docx.js --product products/<新产品> --region cn
   ```

10. **审计**：
    ```powershell
    node tools/audit-visual.js output/<产品>-<品牌>-<市场>-<地区>.html
    ```
    或告诉 AI：
    ```
    使用 swiss-content-auditor agent。
    请对 output/<文件名>.html 做全面审计。
    ```

11. **人工抽检关键页**（内容管理员）

12. **批量生成全矩阵**：
    ```powershell
    node tools/build-all.js --product <新产品>
    node tools/export-pdf-batch.js
    ```

---

#### B. 修改现有产品内容

**场景**：产品参数变更、文字勘误、图片更新。

**操作步骤**：

1. **定位要改的文件**：
   - 事实/参数 → `product.json`
   - 章节结构 → `content/source/chapters/*.json`
   - 图片 → `images.json` + `images/` 目录
   - 译文 → `i18n/workbooks/<locale>.xlsx`

2. **告诉 AI 修复**：
   ```
   使用 swiss-manual-writer agent。
   产品：v23
   问题：[描述具体问题]
   请修改对应的结构源文件。
   ```

3. **如涉及译文，编译**：
   ```powershell
   node tools/compile-translation-workbook.js --product products/v23 --all
   ```

4. **重建 + 重导 + 审计**：
   ```powershell
   node tools/build-variant.js --product products/v23 --region cn
   node tools/export-pdf.js output/v23-wevac-eu-cn.html
   node tools/audit-visual.js output/v23-wevac-eu-cn.html
   ```

---

#### C. 修复排版/溢出/图片问题

**场景**：审计发现页面溢出、图片变形、分页异常等。

**操作步骤**：

1. **告诉 AI 使用问题修复技能**：
   ```
   使用 swiss-manual-writer agent 和 swiss-issue-fix skill。
   产品：v23
   问题类型：[溢出 / 图片 / 翻译 / 分页 / DOCX / 构建失败]
   具体表现：[描述问题，附截图或审计报告]
   ```

2. **AI 会按决策树定位和修复**（6 种决策树）：
   - **A：页面溢出** → 检查内容量 → 拆页/续页/compact 类
   - **B：图片问题** → 检查 images.json → 检查 CSS 承载尺寸
   - **C：翻译/本地化** → 检查 compiled JSON → 检查工作簿同步
   - **D：分页/布局** → 检查 manifest → 检查页面序列
   - **E：DOCX 特有** → 检查 Word 母版 → 检查导出器
   - **F：构建失败** → 检查 JSON 结构 → 检查工具链依赖

3. **修复后重新审计确认**

---

#### D. 翻译更新流程

**场景**：翻译人员改完工作簿，需要重新编译和构建。

**操作步骤**：

```powershell
cd D:\work\private\yjsplan\research\yjs-manual-opt\swiss

# 1. 编译工作簿到 compiled JSON
node tools/compile-translation-workbook.js --product products/v23 --locale en

# 2. 重建目标变体
node tools/build-variant.js --product products/v23 --region gb

# 3. 导出 PDF
node tools/export-pdf.js output/v23-wevac-eu-gb.html

# 4. 审计
node tools/audit-visual.js output/v23-wevac-eu-gb.html
```

**⚠️ 关键风险**：如果 compiled JSON 被手动修过但工作簿未同步，重新编译会覆盖修复。此时用：
```powershell
node tools/sync-json-to-workbook.js --product products/v23 --locale en
```

---

#### E. 全面审计（交付前）

**场景**：准备交付给品牌方或 ODM 客户前的全面质检。

**告诉 AI**：
```
使用 swiss-content-auditor agent。
产品：v23
请按 QA-RULES.md 执行全 5 阶段审计：
Phase 1: JSON 结构验证 + 翻译完整性 + 图片资源
Phase 2: 构建 HTML
Phase 3: Playwright 视觉审计（溢出/图片/残留）
Phase 4: 翻译质检
Phase 5: 全变体验证
```

或直接批量构建 + 自动审计：
```powershell
node tools/build-all.js --product v23
```

---

#### F. 生成 AI 翻译初稿

**场景**：新语言版本需要 AI 辅助翻译。

**操作步骤**：

1. **导出翻译工作簿**：
   ```powershell
   node tools/export-translation-workbook.js --product products/v23 --locale de
   ```

2. **告诉 AI 生成翻译草稿**：
   ```
   使用 swiss-manual-writer agent。
   参照 standards/ai-translation-draft-prompt.md 的规则。
   产品：v23
   源语言：zh-CN
   目标语言：de
   请生成德语翻译初稿。
   ```

3. **翻译人员审核修正**
4. **编译 + 构建 + 审计**

---

## 五、工具命令速查

所有命令在 `D:\work\private\yjsplan\research\yjs-manual-opt\swiss` 目录下执行。

### 构建

```powershell
# 构建单个变体
node tools/build-variant.js --product products/v23 --region cn
node tools/build-variant.js --product products/v23 --region cn --brand wevac

# 构建全矩阵（含自动审计）
node tools/build-all.js --product v23
```

### PDF 导出

```powershell
# 单文件
node tools/export-pdf.js output/v23-wevac-eu-cn.html

# 批量
node tools/export-pdf-batch.js
```

### DOCX 导出

```powershell
# 单地区
node tools/export-docx.js --product products/v23 --region cn

# 全地区
node tools/export-docx.js --product products/v23 --all
```

### 翻译工具

```powershell
# 导出翻译工作簿（从 JSON → Excel）
node tools/export-translation-workbook.js --product products/v23 --all
node tools/export-translation-workbook.js --product products/v23 --locale en

# 编译翻译工作簿（从 Excel → JSON）
node tools/compile-translation-workbook.js --product products/v23 --all
node tools/compile-translation-workbook.js --product products/v23 --locale en

# 反写 compiled JSON 到工作簿
node tools/sync-json-to-workbook.js --product products/v23 --locale en
```

### 审计

```powershell
# 单文件视觉审计
node tools/audit-visual.js output/v23-wevac-eu-cn.html

# 带 JSON 输出
node tools/audit-visual.js output/v23-wevac-eu-cn.html --json

# 批量审计
$files = Get-ChildItem output/v23-*.html | Where-Object { $_.Name -notmatch 'booklet' }
foreach ($f in $files) {
  $out = node tools/audit-visual.js $f.FullName --json 2>&1 | Out-String
  if ($out -match 'ALL CHECKS PASSED') { Write-Host "[PASS] $($f.Name)" }
  else { Write-Host "[FAIL] $($f.Name)"; $out }
}
```

---

## 六、常见问题 FAQ

### Q1：AI 说 "我不知道怎么处理 Swiss 说明书"

**A**：确保在对话开始时明确指定使用 `swiss-manual-writer` 或 `swiss-content-auditor` agent。不要使用 `manual-writer` 或 `manual-auditor`（这是旧 A4 链路）。

### Q2：DOCX 输出很丑 / 格式混乱

**A**：当前 DOCX 由 `export-docx.js`（JS 引擎）生成，已知视觉效果有限。中文版请确认使用了 `base-template-cn.docx` 母版。长期方案已规划使用 poi-tl（Java）替代。

### Q3：德语/意大利语版本页面溢出

**A**：DE/IT 文本比中文长 20-30%，需要：
1. 应用语言补偿 CSS（§三 of DESIGN-STANDARD.md）
2. 使用 `.compact-ops`、`.compact-table` 等 compact 类
3. 优先拆页/续页，不优先压缩

### Q4：翻译编译后之前的修复被覆盖了

**A**：`compile-translation-workbook.js` 以工作簿为准覆盖 compiled JSON。如果 compiled JSON 被手动修过，先运行：
```powershell
node tools/sync-json-to-workbook.js --product products/v23 --locale <locale>
```
把修改同步回工作簿，再编译。

### Q5：`zh-HK` / `zh-TW` 版本跟 `zh-CN` 完全一样

**A**：这三个是独立的 locale catalog，不再做运行时简转繁。如果内容完全一样，说明翻译人员还没审核。目前种子译文仍需人工审核。

### Q6：构建出来的 HTML 里有 `{{...}}` 残留

**A**：说明模板变量未被正确替换。检查：
1. `product.json` 中对应字段是否存在
2. `compiled/<locale>.json` 中对应 `text_id` 是否有值
3. 模板中变量名拼写是否正确

### Q7：审计脚本退出码非零但实际通过了

**A**：`audit-visual.js` 的退出码不可靠（Playwright stderr 可能触发非零），判定 PASS/FAIL 必须检查 stdout 中是否包含 `ALL CHECKS PASSED`。

---

## 七、硬规则汇总（所有角色必知）

1. **内容只认 JSON**：`product.json` + `images.json` + `manifest.json` + `chapters/*.json`
2. **译文只认工作簿 + compiled JSON**：翻人员改工作簿，构建器读 compiled JSON
3. **不允许在模板/HTML 里写正文**：正文必须来自结构 JSON
4. **不允许 `html_fragment` block**：遇到报错处理
5. **图片不允许变形/裁切/横向顶出**：必须 `object-fit: contain`
6. **三级警示体系不可缩减**：WARNING（人身伤害）、CAUTION（产品损坏）、NOTICE（使用提示）
7. **`zh-HK`/`zh-TW` 不用简转繁**：独立 locale catalog
8. **PDF hotfix 必须回写源头**：禁止 PDF 一套、JSON 一套、工作簿又一套
9. **长语种溢出优先拆页**：不优先压缩
10. **封面图不用 `width:100%`**：用 `max-width` 防止拉伸

---

## 八、规范文件索引

| 文件 | 职责 | 何时读 |
|------|------|--------|
| `DESIGN-STANDARD.md` | 唯一视觉标准（色彩、字体、布局、组件样式） | 创建/修改模板时 |
| `QA-RULES.md` | 审计的 5 阶段流程和判定标准 | 审计时 |
| `SOP-new-product.md` | 新产品接入和现有产品维护的完整流程 | 新产品接入 / 内容变更时 |
| `WORD-BASE-TEMPLATE-CN.md` | 中文 Word 母版规范 | DOCX 相关任务时 |
| `skills/swiss-manual-a5/SKILL.md` | AI 主技能定义（输入契约、输出规格、block 类型） | AI 操作员每次发起任务前 |
| `skills/swiss-issue-fix/SKILL.md` | AI 问题修复技能（6 种决策树） | 修复问题时 |
| `standards/brand-language-guide.md` | 品牌语言规范 | 翻译 / 品牌校对 |
| `standards/terminology-glossary.json` | 术语表 | 翻译 / 审计 |
| `standards/unit-and-measurement-policy.md` | 单位格式规范 | 翻译 / 审计 |
| `standards/warning-language-policy.md` | 警示语规范 | 翻译 / 审计 |
| `standards/locale-guides.json` | 各语言本地化指南 | 翻译 |
| `standards/ai-new-product-structure-prompt.md` | AI 结构草稿 prompt | 新产品接入 |
| `standards/ai-translation-draft-prompt.md` | AI 翻译草稿 prompt | 翻译初稿 |
| `standards/ai-localization-audit-prompt.md` | AI 本地化审计 prompt | 翻译质检 |

---

## 附录 A：变体命名规则

产出文件命名格式：`<产品>-<品牌>-<市场>-<地区>.html`

示例：
- `v23-wevac-eu-cn.html` — V23，Wevac 品牌，EU 市场，中国地区
- `v23-vesta-us-gb.html` — V23，Vesta 品牌，US 市场，英国地区
- `imt050-wevac-eu-de.html` — IMT050，Wevac 品牌，EU 市场，德国地区

市场决定规格参数（US/EU），地区决定语言和法规。

## 附录 B：block 类型一览

所有正式内容只允许以下 block 类型（禁止 `html_fragment`）：

| Block 类型 | 用途 |
|-----------|------|
| `paragraph` | 普通段落 |
| `bullet_list` | 项目符号列表 |
| `warning_box` | WARNING 警告框（人身伤害风险） |
| `caution_box` | CAUTION 注意框（产品损坏风险） |
| `notice_box` | NOTICE 提示框（使用提示） |
| `sub_title` | 二级标题 |
| `figure` | 单图 |
| `figure_row` | 多图并排 |
| `step_flow` | 步骤列表 |
| `table_ref` | 表格 |
| `split_panel` | 左右分栏 |
| `custom_table` | 自定义表格 |
| `qa_list` | Q&A 问答列表 |
| `contact_block` | 联系信息块 |
| `warranty_card` | 保修卡 |
