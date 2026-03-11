# Swiss 说明书系统——完整设计文档

**版本**：v1.0  
**日期**：2025-06-08  
**状态**：当前系统实况记录

---

## 1. 系统目标

为亚俊氏旗下全部产品线（真空封口机、制冰机等）自动化生成多品牌、多语言、多地区的 A5 产品说明书。

- **自有品牌**（Wevac / Vesta）：HTML → PDF
- **ODM 客户**（ACT 等）：JSON → DOCX（可编辑交付）+ PDF
- **翻译人员**只改 Excel 工作簿，不碰 HTML / CSS / JSON 结构
- **审稿人**只看 PDF

---

## 2. 五层流水线

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌──────────┐     ┌──────────┐
│  ① 结构源    │────▶│  ② 翻译工作簿 │────▶│ ③ 编译 JSON │────▶│ ④ 构建    │────▶│ ⑤ 导出   │
│  (JSON)      │     │  (.xlsx)      │     │ (compiled)  │     │ (HTML)    │     │ (PDF/DOCX)│
└─────────────┘     └──────────────┘     └────────────┘     └──────────┘     └──────────┘
```

### ① 结构源（谁定义"说明书有什么内容"）

每个产品有独立的 JSON 文件树:

| 文件 | 作用 |
|------|------|
| `product.json` | 产品事实：名称、品牌矩阵、规格参数、按钮、零件、区域市场映射 |
| `images.json` | 图片注册表：语义 ID → 文件名、尺寸、用途、归属关系 |
| `content/source/manifest.json` | 章节排列顺序、目录标题、页眉引用、启用开关 |
| `content/source/chapters/*.json` | 每章一个文件，定义页面和 block 的结构树 |

**关键设计**：正文内容不写在 HTML 模板里，全部以 block 结构存在 JSON 中。

### ② 翻译工作簿（谁改译文）

每个产品 × 每种语言对应一个 `.xlsx` 文件:

```
products/<product>/i18n/workbooks/<locale>.xlsx
```

工作簿结构（`strings` 工作表）:

| 列 | 说明 |
|----|------|
| `text_id` | 唯一键，对应 JSON block 里每个可翻译字段的路径 |
| `scope` | 来源标记（content / product） |
| `context` | 上下文参考 |
| `source_text` | 中文原文 |
| `target_text` | 目标语言译文 |
| `status` | 翻译状态标记 |
| `review_note` | 审校批注 |

翻译工作流：
- 翻译人员/模型**只改** `target_text` 列
- 不增删行、不改 `text_id`、不碰其他列
- 如果 `target_text` 为空，编译时回退到 `source_text`

### ③ 编译（workbook → flat JSON）

工具：`compile-translation-workbook.js`

```bash
node tools/compile-translation-workbook.js --product products/v23 --locale en
```

做一件事：把 xlsx 的 `text_id` + `target_text` 提取成扁平 JSON:

```json
{
  "locale": "en",
  "strings": {
    "content.chapter.01-safety.page.page1.block.1.item.1": "This machine is for household use only...",
    "product.specs.eu.rows.0.label": "Voltage",
    ...
  }
}
```

输出位置：`products/<product>/i18n/compiled/<locale>.json`

### ④ 构建（compiled JSON + template → HTML）

工具：`build-variant.js`

```bash
node tools/build-variant.js --product products/v23 --region gb --brand wevac
```

做的事：
1. 读 `product.json`（产品事实）
2. 读 `compiled/<locale>.json`（所有翻译后的文字）
3. 读 `content/source/manifest.json` + `chapters/*.json`（chapter 结构）
4. 读 HTML 模板（`template/<product>-master-<lang>.html`）
5. 根据 block 类型调用对应渲染器，把 JSON block 转成 HTML
6. 替换品牌变量 `{{brand.*}}`、产品变量 `{{product.*}}`
7. 输出完整 HTML 到 `output/`

**区域-语言映射**（硬编码在 build-variant.js 里）:

| region | locale | market |
|--------|--------|--------|
| cn | zh-CN | eu |
| gb | en | eu |
| de | de | eu |
| it | it | eu |
| hk | zh-HK | eu |
| tw | zh-TW | us |
| za | en | eu |

### ⑤ 导出

| 工具 | 输入 | 输出 | 引擎 |
|------|------|------|------|
| `export-pdf.js` | HTML | PDF | Playwright 无头浏览器 |
| `export-pdf-batch.js` | 多个 HTML | 多个 PDF | 同上，批量 |
| `export-docx.js` | JSON 源 + compiled JSON | DOCX | 纯代码生成（docx 库），14 种 block 渲染器 |
| `make-booklet.py` | PDF | 骑马钉拼版 PDF | PyMuPDF |

---

## 3. 目录结构

```
swiss/
├── SYSTEM-DESIGN.md          ← 本文件（系统全景）
├── DESIGN-STANDARD.md        ← 视觉规范（A5 尺寸、色彩、字体）
├── SOP-new-product.md         ← 操作手册（新产品 12 步、维护流程、hotfix 规则）
├── WORD-BASE-TEMPLATE-CN.md   ← Word 母版基线说明
├── ARCHITECTURE-PLAN.md       ← 历史文档：从 HTML-blob 架构迁移到 JSON-source 的方案
├── README.md                  ← 快速概览
│
├── products/                  ← 产品数据（每产品一个目录）
│   ├── v23/                   ← V23 真空封口机
│   │   ├── product.json
│   │   ├── images.json
│   │   ├── images/            ← 产品图片（PNG + SVG）
│   │   ├── content/source/    ← 结构源
│   │   │   ├── manifest.json
│   │   │   └── chapters/      ← 10 个章节 JSON
│   │   └── i18n/
│   │       ├── compiled/      ← 6 个 locale JSON（编译产物）
│   │       └── workbooks/     ← 6 个 locale xlsx（翻译编辑面）
│   └── imt050/                ← IMT050 制冰机（同结构）
│
├── template/                  ← HTML 模板
│   ├── v23-master-cn.html     ← V23 中文母版
│   ├── v23-master-en.html     ← V23 英文母版
│   ├── v23-master-de.html     ← V23 德文母版
│   ├── v23-master-it.html     ← V23 意大利文母版
│   ├── imt050-master-*.html   ← IMT050 系列母版
│   └── shared/
│       ├── base/
│       │   ├── core-shell.css       ← 全局 CSS（A5 页面、分页、排版）
│       │   ├── brand-themes.json    ← 品牌主题包（色彩、边框）
│       │   ├── v23-booklet.css      ← V23 产品级样式
│       │   ├── v23-longtext.css     ← V23 长文本语言补偿
│       │   └── imt050-booklet.css   ← IMT050 产品级样式
│       ├── cn/                      ← 中文专用片段
│       ├── en/                      ← 英文专用片段
│       ├── de/                      ← 德文专用片段
│       ├── it/                      ← 意大利文专用片段
│       └── docx/
│           └── base-template-cn.docx  ← DOCX A5 Word 母版骨架
│
├── standards/                 ← 语言和品牌规范资产
│   ├── terminology-glossary.json         ← 术语表（6 语言）
│   ├── brand-language-guide.md           ← 品牌语言指南
│   ├── unit-and-measurement-policy.md    ← 单位与计量规范
│   ├── warning-language-policy.md        ← 警示语三级体系
│   ├── locale-guides.json                ← 各 locale 写作规则
│   ├── ai-translation-draft-prompt.md    ← 模型翻译生成 prompt
│   ├── ai-localization-audit-prompt.md   ← 模型翻译审计 prompt
│   └── ai-new-product-structure-prompt.md ← 模型结构生成 prompt
│
├── tools/                     ← 构建工具链
│   ├── build-variant.js                ← ④ HTML 构建器
│   ├── compile-translation-workbook.js ← ③ 工作簿编译器
│   ├── export-translation-workbook.js  ← 结构源 → xlsx 导出器
│   ├── export-pdf.js                   ← ⑤ PDF 导出（Playwright）
│   ├── export-pdf-batch.js             ← ⑤ 批量 PDF
│   ├── export-docx.js                  ← ⑤ DOCX 导出（1421 行，14 种渲染器）
│   ├── make-booklet.py                 ← 骑马钉拼版
│   ├── audit-visual.js                 ← 视觉审计（溢出/重叠/空页/残留，JSON 输出）
│   ├── migrate-json-single-source.js   ← 历史迁移工具
│   ├── migrate-source-i18n.js          ← 历史迁移工具
│   └── normalize-json-content.js       ← JSON 内容规范化
│
├── tests/                     ← 测试套件（node:test，共 24 个用例）
│   ├── build-variant-content.test.js     (9 tests)
│   ├── build-variant-includes.test.js    (2 tests)
│   ├── content-driven-templates.test.js  (6 tests)
│   ├── export-docx.test.js              (3 tests)
│   ├── imt050-alignment.test.js         (2 tests)
│   ├── shared-master-cn.test.js         (1 test)
│   └── shared-master-multilang.test.js  (1 test)
│
└── output/                    ← 构建产物（可再生，不入库全量）
```

---

## 4. 数据模型

### 4.1 product.json 核心字段

```
product
├── model_id: "v23"
├── product_name: { zh-CN: "真空封口机", en: "Vacuum Sealer", ... }
├── brands: { wevac: {...}, vesta: {...}, act: {...} }
│   └── 每个品牌: display_name, name, address, website, support_email, warranty_years
├── manufacturer: { name, address }
├── specs: { us: { rows: [...] }, eu: { rows: [...] } }
├── parts: [ { id, name_cn, name_en, ... } ]
├── buttons: [ { id, name_cn, name_en, desc_cn, desc_en, ... } ]
├── regions: { cn, gb, de, it, hk, tw, za }
│   └── 每个区域: locale, market, brand_default
└── warranty: { years }
```

### 4.2 章节 JSON 内容模型

```
chapter
├── chapter_id: "06-operation"
├── pages:
│   └── page1, page2, ...
│       └── section_title: "操作指引"
│       └── blocks: [
│           { type: "sub_title", text: "6.1 如何使用切袋刀" }
│           { type: "step_flow", body: [{ item: [...], step: {...} }] }
│           { type: "warning_box", title: "注意", text: "..." }
│           { type: "figure", image_id: "img_05", ... }
│           ...
│       ]
```

### 4.3 正式 Block 类型清单（14 种）

| 类型 | 说明 | 数据字段 |
|------|------|---------|
| `paragraph` | 纯文本段落 | text, bold? |
| `sub_title` | 节标题 | text |
| `bullet_list` | 无序列表 | items[] |
| `warning_box` | ⚠️ 警告框 | title, items[] 或 text |
| `caution_box` | ⚡ 注意框 | title, items[] 或 text |
| `notice_box` | ℹ️ 提示框 | title, items[] 或 text |
| `step_flow` | 有序步骤流 | body[].step.stepN.text |
| `figure` | 单图 | image_id |
| `figure_row` | 多图横排 | figures[] |
| `split_panel` | 图文分栏 | 左右面板 |
| `table_ref` | 表格引用 | header[], rows[][] |
| `qa_list` | 问答列表 | items[].q, items[].a |
| `contact_block` | 品牌联络信息 | 模板变量 |
| `warranty_card` | 保修卡 | fields[] |

---

## 5. 品牌风格系统

不为每个品牌复制模板，而是使用**共享母版 + 品牌主题包**：

```json
// brand-themes.json 示例
{
  "wevac": {
    "accent_color": "#E63946",
    "footer_border": "#E63946",
    "cover_accent": "#E63946"
  },
  "vesta": {
    "accent_color": "#2D6A4F",
    "footer_border": "#2D6A4F",
    "cover_accent": "#2D6A4F"
  }
}
```

模板中通过 CSS 变量注入品牌色，正文完全一致，只有封面、页脚、品牌信息不同。

---

## 6. 翻译管道详解

### 6.1 数据流

```
结构源 JSON ──[导出]──▶ workbook.xlsx ──[翻译/审核]──▶ workbook.xlsx ──[编译]──▶ compiled.json
     │                                                                           │
     └───────────────────────── content 结构 ──────────────────────────────────────┘
                                           ↓
                                    build-variant.js
                                           ↓
                                     HTML / PDF / DOCX
```

### 6.2 工具调用

| 步骤 | 命令 | 说明 |
|------|------|------|
| 导出 | `node tools/export-translation-workbook.js --product products/v23 --all` | 从 JSON 源生成 6 个 .xlsx |
| 编译 | `node tools/compile-translation-workbook.js --product products/v23 --locale en` | xlsx → compiled JSON |
| 编译全部 | `node tools/compile-translation-workbook.js --product products/v23 --all` | 一次编译所有语言 |

### 6.3 已知失败模式（来自实际审计）

| # | 失败模式 | 原因 | 影响 | 对策 |
|---|---------|------|------|------|
| 1 | **target_text 含源语言文字** | 模型翻译时上下文截断，直接抄源文 | 产出中出现中文 | 编译时加语言检测校验 |
| 2 | **翻译放错 key** | 跨页续表 key 结构相似，模型搞混 | 翻译内容对不上原文 | 审计时交叉比对 |
| 3 | **键值交换** | 相邻键的值互换 | 标题/内容错位 | 审计时逐键比对 |
| 4 | **target_text 为空** | 模型遗漏 | 回退为 source_text（中文） | 编译时 WARN |

### 6.4 当前语言矩阵

| Locale | 中文名 | 来源 |
|--------|--------|------|
| zh-CN | 简体中文 | 原始创作 |
| zh-HK | 港繁 | 独立翻译（非逐字简转繁） |
| zh-TW | 台繁 | 独立翻译 |
| en | 英文 | 模型翻译 |
| de | 德文 | 模型翻译 |
| it | 意大利文 | 模型翻译 |

---

## 7. 质量保障

### 7.1 自动化测试

```bash
node --test tests/*.test.js
```

24 个测试用例，覆盖：
- 内容驱动模板渲染（9）
- 模板 include 解析（2）
- 多语言内容模板（6）
- DOCX 导出（3）
- IMT050 对齐（2）
- 共享母版中文（1）
- 共享母版多语言（1）

### 7.2 视觉审计

```bash
node tools/audit-visual.js output/v23-wevac-eu-gb.html --json
```

自动检测：
- 每页截图（A5 比例 560×794px）
- 图片拉伸（natural ratio vs render ratio）
- 页面溢出（scrollHeight > clientHeight）

### 7.3 PDF 导出验证

```bash
node tools/export-pdf.js output/v23-wevac-eu-gb.html
```

自动报告：
- 页数
- 图片加载失败数
- 零宽图片数
- 请求失败数

### 7.4 翻译审计（手动触发）

使用 `standards/ai-localization-audit-prompt.md` 模板，对 compiled JSON 做逐条审计，检查：
- 术语一致性
- 品牌语言
- 单位格式
- 警示语级别
- 漏译/错译/直译
- 地区本地化

---

## 8. 规范资产索引

| 文件 | 管什么 |
|------|--------|
| `DESIGN-STANDARD.md` | A5 页面尺寸、边距、色彩系统、字体系统、长文本语言补偿 |
| `SOP-new-product.md` | 新产品 12 步流程、维护流程、PDF hotfix 规则、验收标准 |
| `WORD-BASE-TEMPLATE-CN.md` | Word 母版基线（A5、Arial Narrow + 宋体、不求 1:1 复刻 PDF） |
| `standards/terminology-glossary.json` | 核心术语 6 语言对照 |
| `standards/brand-language-guide.md` | 品牌语言统一原则和禁止项 |
| `standards/unit-and-measurement-policy.md` | 单位格式规范 |
| `standards/warning-language-policy.md` | 警示语三级体系 |
| `standards/locale-guides.json` | 各 locale 写作规则 |

---

## 9. 当前产品与变体矩阵

### 产品

| 产品 | model_id | 章节数 | 图片数 |
|------|---------|--------|--------|
| V23 真空封口机 | v23 | 10 | 16（含 SVG） |
| IMT050 制冰机 | imt050 | 10 | 18（全 PNG） |

### 品牌

| 品牌 | 类型 | 已支持 |
|------|------|--------|
| WEVAC | 自有 | ✅ |
| Vesta | 自有 | ✅ |
| ACT | ODM | ✅ |

### 变体矩阵（每产品）

| 区域 | 语言 | 市场 | 品牌组合 |
|------|------|------|---------|
| cn | zh-CN | eu | wevac |
| gb | en | eu | wevac, vesta |
| de | de | eu | wevac, vesta, act |
| it | it | eu | wevac, vesta, act |
| hk | zh-HK | eu | wevac |
| tw | zh-TW | us | wevac |
| za | en | eu | act |

---

## 10. 已知局限

| # | 问题 | 状态 |
|---|------|------|
| 1 | 编译工具不检测 target_text 语言是否匹配 | 待加 `--check-lang` |
| 2 | 术语表只有 5 个全局词条，需要扩充 | 可用但不完整 |
| 3 | DOCX SVG 图片需要 sharp 库做 PNG 光栅化（单次 ~1.7MB） | 已实现，但产出体积大 |
| 4 | 无自动化的 workbook ↔ compiled JSON 双向同步 | compiled JSON 手动修改后需手动回写 workbook |
| 5 | 目录页码和章节编号仍部分硬编码在模板中 | 未来可自动化 |

---

## 11. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 快速概览 | `README.md` | 一页纸看懂系统 |
| 视觉规范 | `DESIGN-STANDARD.md` | A5 版式设计标准 |
| 操作手册 | `SOP-new-product.md` | 新产品接入与维护操作指南 |
| Word 基线 | `WORD-BASE-TEMPLATE-CN.md` | DOCX 版式说明 |
| 架构迁移记录 | `ARCHITECTURE-PLAN.md` | 从 HTML-blob 到 JSON-source 的历史方案 |
