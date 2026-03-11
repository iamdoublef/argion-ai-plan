# Swiss Manual Content System — 架构重构方案

**版本**：v1.0
**日期**：2026-03-10
**状态**：待评审
**作者**：架构评估（基于实际代码分析）

---

## 一、现状诊断

### 1.1 现有架构

```
master template (58行 shell)
  + content.{lang}.json (CONTENT_BODY = ~1300行 HTML 字符串)
  + config.json (品牌/产品/参数变量)
  ↓ build-variant.js
  完整 HTML (1370行)
```

### 1.2 数据驱动比例

| 类别 | 驱动方式 | 比例 |
|------|---------|------|
| 品牌变量（`{{brand.*}}`） | config.json | ~2% |
| 产品变量（`{{product.*}}`） | config.json | ~2% |
| 零件表（`{{#PARTS_TABLE_ROWS}}`） | config.json | ~2% |
| 按键表（`{{#BUTTONS_TABLE_ROWS}}`） | config.json | ~2% |
| 技术参数（`{{#SPECS_TABLE_ROWS}}`） | config.json | ~1% |
| 品牌/制造商信息 | config.json | ~1% |
| **正文全部章节内容** | **HTML 硬编码** | **~90%** |

### 1.3 V23-CN 内容块统计（19页）

| Block 类型 | 数量 |
|-----------|------|
| page div | 19 |
| section-title（章节标题）| 16 |
| sub-title（节标题）| 17 |
| ol.steps（有序步骤）| 12 |
| table（表格）| 9 |
| bullet-list（无序列表）| 7 |
| img（图片）| 15 |
| note-box | 8 |
| caution-box | 3 |
| warning-box | 1 |
| flex 图文并排布局 | 10 |
| inline-style 段落 | 10 |

### 1.4 核心问题

1. **~90% 内容是 HTML 字符串**：全部操作步骤、安全须知、故障排除、维护保养、真空特性科普 — 都写在 JSON 的 `CONTENT_BODY` 字段里
2. **页码硬编码**：目录页数字、每页 page-footer 里的页码都是手写数字
3. **目录不能自动生成**：章节名和页码都是硬写的 HTML
4. **图片路径硬写在 HTML 中**：没有图片-步骤的显式绑定关系
5. **新产品需复制整个 HTML blob**：无法按章节级别复用

---

## 二、目标架构

### 2.1 架构总图

```
products/{model}/
  config.json          ← 品牌/产品/参数变量（已有，保留）
  content/
    {lang}/
      ch01-safety.json       ← 每章一个文件
      ch02-usage-tips.json
      ch03-structure.json
      ...
      ch10-warranty.json

template/
  {model}-master-{lang}.html  ← 缩减为 shell（head + cover + TOC slot + body slot）
  shared/                     ← CSS 不动

tools/
  build-variant.js            ← 增强：章节渲染器 + 自动 TOC + 自动页码
  renderers/                  ← 新增：11 种 block renderer
    paragraph.js
    warning-box.js
    steps.js
    figure-steps.js
    table.js
    ...
```

### 2.2 三层分离（加强版）

| 层 | 文件 | 职责 | 谁可以改 |
|----|------|------|---------|
| **数据层** | `config.json` + `content/{lang}/ch*.json` | 产品参数 + 全部正文内容 | 只需懂 JSON 基础 |
| **模板层** | `template/*-master-*.html` | 页面 shell（head、封面、共享片段） | 极少改动 |
| **样式层** | `template/shared/base/*.css` | 字号、颜色、间距、分页 | 极少改动 |
| **渲染层** | `tools/build-variant.js` + `renderers/` | block→HTML 转换、分页、TOC、页码 | 仅开发者 |

---

## 三、内容数据模型（Schema）

### 3.1 章节文件结构

```json
{
  "chapter_num": "06",
  "title": "操作指引",
  "header_ref": "CH.06 — OPERATION",
  "compact_class": "compact-ops",
  "blocks": [
    { "type": "...", ... },
    { "type": "...", ... }
  ]
}
```

### 3.2 Block 类型定义

#### 1. `paragraph` — 纯文本段落

```json
{
  "type": "paragraph",
  "text": "真空包装是通过去除密封容器中的大部分空气来延长食品的寿命...",
  "bold": false
}
```

#### 2. `labeled-paragraph` — 带加粗前缀的段落

```json
{
  "type": "labeled-paragraph",
  "label": "从卷袋中制作袋子并密封：",
  "text": ""
}
```

#### 3. `warning-box` — 警告框

```json
{
  "type": "warning-box",
  "title": "警告 WARNING",
  "icon": "image3.png",
  "items": [
    "本机仅供家庭使用，请勿用于其他非设计用途。",
    "请勿让儿童玩耍本机或电源线。..."
  ]
}
```

#### 4. `caution-box` — 注意框

```json
{
  "type": "caution-box",
  "title": "注意 CAUTION",
  "items": [
    "请妥善保管本手册。",
    "本机无需添加任何润滑剂..."
  ]
}
```

也支持单条文本模式：

```json
{
  "type": "caution-box",
  "title": "注意",
  "text": "启用 Extend Seal Time 功能时，将暂时禁用智能密封调节功能..."
}
```

#### 5. `note-box` — 提示框

```json
{
  "type": "note-box",
  "title": "提示 NOTICE",
  "items": ["...", "..."]
}
```

或单条：

```json
{
  "type": "note-box",
  "text": "在手动真空过程中，长按按键抽气..."
}
```

#### 6. `steps` — 有序操作步骤

```json
{
  "type": "steps",
  "steps": [
    "打开面盖。",
    "打开切袋刀架。",
    "从卷袋上拉扯出所需长度的袋子。",
    "将切袋刀移至最左或最右边，再使刀架下压着袋子。",
    "将切袋刀下压滑动划过袋子，以进行整齐的切割。"
  ]
}
```

#### 7. `figure-steps` — 步骤 + 侧图并排

```json
{
  "type": "figure-steps",
  "steps": [
    "打开面盖。",
    "打开切袋刀架。",
    "..."
  ],
  "image": "image12.svg",
  "image_width": "34mm",
  "image_alt": "切袋刀操作"
}
```

多图并排：

```json
{
  "type": "figure-steps",
  "steps": ["..."],
  "images": [
    { "src": "image20.svg", "alt": "Mason Jar Connection", "width": "28mm" },
    { "src": "image22.svg", "alt": "Mason Jar Operation", "width": "28mm" }
  ]
}
```

#### 8. `figure-bullets` — 列表 + 侧图并排

```json
{
  "type": "figure-bullets",
  "items": [
    "对梅森罐适配器和带阀门拉链袋抽真空时...",
    "对真空罐和瓶塞抽真空时..."
  ],
  "image": "image18.svg",
  "image_width": "30mm"
}
```

#### 9. `bullet-list` — 无序列表

```json
{
  "type": "bullet-list",
  "items": [
    "确保使用机器的工作台平整、干净、干燥。",
    "在不使用机器时请不要将机器锁扣锁上..."
  ]
}
```

#### 10. `table` — 通用表格

```json
{
  "type": "table",
  "headers": ["故障现象", "可能原因", "解决方案"],
  "col_widths": ["22%", "40%", "38%"],
  "rows": [
    { "cells": ["**不能开机**", "电源线未正确插入电源插座", "确保电源线已正确插入。"], "rowspan_first": 3 },
    { "cells": [null, "电源线破裂或损坏", "断电检查电源线..."] },
    { "cells": [null, "控制板或面板排线端子松脱", "请咨询专业人员进行维修。"] }
  ]
}
```

#### 11. `figure` — 独立图片

```json
{
  "type": "figure",
  "image": "image5.svg",
  "max_height": "46mm",
  "caption": "图 1 — 产品结构",
  "alt": "产品结构图"
}
```

#### 12. `sub-section` — 节标题 + 内含 blocks

```json
{
  "type": "sub-section",
  "title": "6.1 如何使用切袋刀",
  "blocks": [
    { "type": "figure-steps", "..." },
    { "type": "note-box", "..." }
  ]
}
```

#### 13. `figure-stack` — 垂直图片堆叠

```json
{
  "type": "figure-stack",
  "images": [
    { "src": "image28.svg", "alt": "单卷袋放置" },
    { "src": "image30.svg", "alt": "双卷袋放置" }
  ],
  "max_width": "78mm"
}
```

### 3.3 文本标记约定

正文文本中支持以下内联标记：

| 标记 | 渲染为 | 示例 |
|------|--------|------|
| `[ButtonName]` | `<span class="btn-name">ButtonName</span>` | `点击 [Seal] 按键` |
| `**text**` | `<b>text</b>` | `**Normal** 模式` |
| 图片名（无路径） | 自动拼接 `./{{images_dir}}/` | `image12.svg` |

---

## 四、渲染引擎改造

### 4.1 新增模块

```
tools/
  build-variant.js          ← 入口，增加 chapter 加载和渲染流程
  renderers/
    index.js                ← renderer 注册表
    paragraph.js
    warning-box.js
    caution-box.js
    note-box.js
    steps.js
    figure-steps.js
    figure-bullets.js
    bullet-list.js
    table.js
    figure.js
    figure-stack.js
    sub-section.js
    labeled-paragraph.js
    utils/
      inline-markup.js      ← [Button] / **bold** 替换
      page-layout.js        ← 自动分页逻辑
      toc-generator.js      ← 自动目录生成
      page-numbering.js     ← 自动页码
```

### 4.2 渲染流程

```
1. 读取 config.json + 所有 chapter JSON
2. 按 chapter_num 排序
3. 初始化页面计数器（cover=1, toc=2, content从3起）
4. 逐章渲染：
   a. 开一个 <div class="page {compact_class}">
   b. 渲染 header-strip
   c. 渲染 section-title
   d. 遍历 blocks → 调用 renderer
   e. 累计内容高度预估
   f. 接近 A5 可用高度时：关闭当前 page，开新 page（续页标题）
   g. 记录章节起始页码
5. 回填 TOC（章节名 + 实际页码）
6. 回填所有 page-footer 页码
7. 变量替换（brand/product/specs）
8. 输出完整 HTML
```

### 4.3 自动分页策略

**A5 可用内容高度估算**：

```
页面高度：210mm
上下 padding：10mm × 2 = 20mm
header-strip：约 10mm
page-footer：约 8mm
可用正文区域：≈ 172mm
```

**block 高度预估规则**（保守值，单位 mm）：

| Block 类型 | 预估公式 |
|-----------|---------|
| section-title | 12 |
| sub-title | 10 |
| paragraph | 行数 × 4.5 |
| steps | 步骤数 × 5 |
| figure-steps | max(步骤数 × 5, image_height) + 8 |
| bullet-list | 条目数 × 5 |
| table | (行数 + 1) × 6 |
| warning/caution/note-box | (条目数 × 5) + 12 |
| figure | max_height + caption 6mm |

**分页规则**：
- 累计高度 > 可用高度 × 0.85 时，尝试在当前 block 之前分页
- 如果单个 block 超过可用高度（如大表格），拆分 block
- 分页后自动添加续页标题：`<h2 class="section-title">06 操作指引（续）</h2>`

---

## 五、保留不变的部分

| 文件/系统 | 状态 |
|----------|------|
| `DESIGN-STANDARD.md` | 不变 |
| `core-shell.css` | 不变 |
| `v23-booklet.css` / `imt050-booklet.css` | 不变 |
| `config.json` 结构 | 保留，可能补字段 |
| `export-pdf.js` | 不变 |
| `export-pdf-batch.js` | 不变 |
| `make-booklet.py` | 不变 |
| `_audit-visual.js` | 不变（后续增强） |
| master template shell 部分 | 小改（TOC 改为 slot） |

---

## 六、分阶段落地

### Phase 0：Schema 验证（2天）

**目标**：用一章证明数据→HTML 渲染可行

- [ ] 定义 JSON Schema（可用 ajv 校验）
- [ ] 编写 `ch01-safety.json`（从现有 HTML 提取）
- [ ] 实现 `warning-box`、`caution-box`、`note-box` 三个 renderer
- [ ] 构建后对比输出 HTML 与现有版本一致

**交付标准**：ch01 渲染输出与现有输出逐像素对比，无视觉差异

### Phase 1：核心渲染器（3-4天）

**目标**：实现全部 13 种 block renderer + 自动 TOC + 自动页码

- [ ] 实现全部 renderer
- [ ] 实现 inline markup 解析（`[Button]`、`**bold**`）
- [ ] 实现 TOC 自动生成
- [ ] 实现页码自动编排
- [ ] 单元测试覆盖每种 renderer

### Phase 2：V23-CN 全量迁移（2天）

**目标**：V23 中文版 10章全部迁移为 JSON

- [ ] 提取 ch01~ch10 的 JSON
- [ ] 构建并对比输出（应与现有完全一致）
- [ ] 删除旧 `content.cn.json` 的 CONTENT_BODY

### Phase 3：多语言 + IMT050（3天）

- [ ] V23 EN/DE/IT 迁移
- [ ] IMT050 CN/EN/DE/IT 迁移
- [ ] 全量构建 42 个变体，PDF 对比

### Phase 4：自动分页（2-3天）

- [ ] 实现高度预估逻辑
- [ ] 实现自动续页
- [ ] Playwright 渲染后溢出二次检测
- [ ] 对比验证

### Phase 5：内容审计增强（2天）

- [ ] 源稿文本 ↔ JSON 内容比对工具
- [ ] 多语言文本长度差异自动检测
- [ ] 图片引用完整性检查

---

## 七、验收标准

Phase 2 完成时，以下条件全部满足：

1. V23-CN 21个变体构建输出 PDF 与重构前无视觉差异
2. 修改一句操作步骤 → 只需改 JSON 中一个字符串
3. TOC 页码随内容增减自动正确
4. 新增/删除一页内容后，后续页码自动更新
5. JSON 文件中零 HTML 标签（除 `[ButtonName]` 标记外）
6. JSON Schema 校验通过（`ajv validate`）

---

## 八、风险评估

| 风险 | 概率 | 影响 | 对策 |
|------|------|------|------|
| 自动分页不准确 | 高 | 中 | 预估 + Playwright 二次校正；Phase 4 专项处理 |
| 表格跨页拆分复杂 | 中 | 中 | 大表格优先保持不拆，溢出时缩字号 |
| 迁移后视觉微差异 | 中 | 低 | Playwright 截图逐页对比 |
| JSON 编辑门槛仍高 | 低 | 低 | 可后续加 YAML 转 JSON 或简单 Web 表单 |

---

## 附录：现有 content.cn.json 的 HTML 标记统计

从 CONTENT_BODY 中提取的标记清单（用于迁移对照）：

- `@CONTENT:safety:start/end`
- `@CONTENT:usage_tips:start/end`
- `@CONTENT:operations:start/end`
- `@CONTENT:troubleshooting:start/end`
- `@CONTENT:maintenance:start/end`
- `@CONTENT:vacuum_features:start/end`

这些注释标记说明原作者已有章节分离的意图，但未实现为数据结构。
本方案正式将这些意图落实为结构化数据。
