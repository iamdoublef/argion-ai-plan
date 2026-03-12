# Swiss Template Design Standard (A5 Booklet)

**版本**：v1.2  
**日期**：2026-03-09  
**基准来源**：V23 模版 CSS + `data/d5-manual-standard.md` v2.0  
**适用范围**：所有 Swiss A5 booklet 产品说明书模版（`swiss/template/*-master-*.html`）

> 本文件是 Swiss A5 模版**唯一设计基准**。模版创建、审计、修正均以此为标准。
> 与 d5 冲突时，以本文件为准（本文件已考虑 A5 适配）。

### 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-03-08 | 初稿创建，从V23模版提取设计规范 |
| v1.1 | 2026-03-08 | IMT050全部4语言模板已对齐V23；新增compact-ops sub-title规范；确认三级警告系统box-title规则 |
| v1.2 | 2026-03-09 | 同步文档数值至 core-shell.css 实际值（字号、间距、边距等16处修正）；修复V23封面 width:100% 问题 |
| v1.3 | 2026-03-16 | 新增§十七内容结构约束（10条规则，含[结构]/[渲染]分类标签）；figure-row 多图 CSS 修复；IMT050 保修卡分页修复 |

---

## 一、页面布局

| 项目 | 规范值 | 说明 |
|------|--------|------|
| 页面尺寸 | A5 (148×210 mm) | `@page { size: 148mm 210mm; margin: 0; }` |
| 页边距 | 10mm | `--page-margin: 10mm` |
| 页面容器 | 固定宽高 | `.page { width: 148mm; height: 210mm; }` |
| 页面溢出 | `overflow: hidden` | 内容必须在设计时确保不溢出（见§十一） |
| 分页 | `page-break-after: always` | 每个 `.page` 独立成页 |
| 背景 | `#FFF` | 打印友好，无灰色背景 |

> **注意**：d5 §8.4 禁止 `height + overflow: hidden`（针对 A4 `min-height` 布局）。
> Swiss A5 因需要精确的 booklet 拼版，**必须使用固定 height**。
> 但 overflow:hidden 只是安全网，设计时**必须确保内容不溢出**，由审计脚本检测。

---

## 二、色彩系统

从 V23 模版继承，所有产品统一。

| 用途 | 变量 | 色值 | 说明 |
|------|------|------|------|
| 主黑 | `--swiss-black` | `#000000` | V23 用 #000000 |
| 强调红 | `--swiss-red` | `#E63946` | V23 品牌红 |
| 灰底 | `--swiss-gray-bg` | `#F2F2F7` | V23 灰底 |
| 灰字 | `--swiss-gray-text` | `#8E8E93` | 页眉/页脚文字 |
| 正文 | — | `var(--swiss-black)` | 同主黑 |

**禁止**：
- ❌ 使用 `#E30613` 或其他非标准红色
- ❌ 使用 `#1A1A1A` 替代 `#000000`（正文可接受，但变量必须定义为 #000000）
- ❌ 使用 `#F5F5F5` 替代 `#F2F2F7`

---

## 三、字体系统

### 字体栈

```css
body { font-family: 'Helvetica Neue', 'Inter', Arial, sans-serif; }
```

- CN 模版可追加 CJK 字体：`'PingFang SC', 'Microsoft YaHei'`（放在 Arial 之后）
- 等宽场景（header-ref, page-footer）：`'Courier New', monospace`

### 字号对照表（V23 A4 → Swiss A5 适配）

| 用途 | V23 (A4) | Swiss (A5) | 缩放比 |
|------|----------|------------|--------|
| body line-height | 1.65 | 1.55 | — |
| 一级标题 `.section-title` | 26px | 18px | 0.69 |
| 二级标题 `.sub-title` | 14px | 10px | 0.71 |
| 正文 `p` | 13px | 10px | 0.77 |
| 步骤文字 `.step-text` | 13px | 10px | 0.77 |
| 列表项 `.bullet-list li` | 13px | 10px | 0.77 |
| 表格正文 `td` | 12px | 9px | 0.75 |
| 表格表头 `th` | 11px | 8px | 0.73 |
| 警告框 | 12px | 9.4px | 0.78 |
| 页眉品牌 `.header-brand` | 13px | 9px | 0.69 |
| 页眉章节 `.header-ref` | 10px | 7.5px | 0.75 |
| 页脚 `.page-footer` | — | 7px | — |
| 目录项 `.toc-item` | 13px | 10px | 0.77 |

### 长文本语言补偿（DE/IT）

德语和意大利语文本比中文/英文长 20-30%，需全局补偿：

| 属性 | CN/EN 标准值 | DE/IT 补偿值 |
|------|-------------|-------------|
| body line-height | 1.55 | 1.45 |
| .step-text font-size | 10px | 9.5px |
| .step-text line-height | 1.5 | 1.42 |
| .bullet-list li font-size | 10px | 9.5px |
| .bullet-list li margin-bottom | 6px | 4px |

---

## 四、页面头部 `.header-strip`

```css
.header-strip {
  border-top: 4px solid var(--swiss-black);
  padding-top: 6px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 12px;
}
.header-brand {
  font-weight: 900;
  letter-spacing: 1.4px;
  font-size: 9px;        /* A5 适配，V23 A4 为 13px */
  text-transform: uppercase;
}
.header-ref {
  font-family: 'Courier New', monospace;  /* 必须 monospace */
  font-size: 7.5px;
  color: var(--swiss-gray-text);
}
```

---

## 五、标题系统

### 一级标题 `.section-title`

**必须保持 V23 设计语言：左侧竖线**

```css
.section-title {
  font-size: 18px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.3px;
  margin: 0 0 10px;
  border-left: 4px solid var(--swiss-black);  /* V23 核心特征 */
  padding-left: 8px;
}
.section-title .chapter-num {
  color: var(--swiss-red);
  margin-right: 6px;
}
```

**禁止**：
- ❌ 使用 `border-bottom` 替代 `border-left`
- ❌ 省略 `.chapter-num` 的红色编号

### 二级标题 `.sub-title`

**必须保持 V23 设计语言：底部黑线 + uppercase**

```css
.sub-title {
  font-size: 10px;
  font-weight: 700;
  border-bottom: 1.5px solid var(--swiss-black);
  padding-bottom: 3px;
  margin: 12px 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.35px;
}
```

**禁止**：
- ❌ 省略 `border-bottom`
- ❌ 省略 `text-transform: uppercase`

---

## 六、表格系统

### 标准表格

**必须保持 V23 设计语言：黑底白字表头 + 交替行色**

```css
table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0;
  font-size: 9px;
  table-layout: fixed;
}
th {
  background: var(--swiss-black);
  color: #FFF;
  padding: 5px 6px;
  text-align: left;
  font-size: 8px;
  text-transform: uppercase;
  letter-spacing: 0.35px;
}
td {
  border: 1px solid #CCC;
  padding: 5px 6px;
  color: #1A1A1A;
  vertical-align: top;
}
tr:nth-child(even) td {
  background: var(--swiss-gray-bg);
}
```

**禁止**：
- ❌ 灰底表头（`background: #F5F5F5` 等）
- ❌ 省略交替行色
- ❌ 使用 `border: 1px solid #DDD`（应为 `#CCC`）

---

## 七、警示体系（三级，从 d5 继承）

**必须使用 d5 三级体系，不得缩减**

### CSS 类名和样式

```css
/* WARNING — 人身伤害风险 */
.warning-box {
  border: 2px solid var(--swiss-red);
  padding: 8px 10px;
  margin: 10px 0;
}
.warning-box .box-title {
  font-size: 8.5px;
  font-weight: 900;
  color: var(--swiss-red);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* CAUTION — 产品损坏风险 */
.caution-box {
  border: 2px solid #000;
  padding: 8px 10px;
  margin: 10px 0;
}
.caution-box .box-title {
  font-size: 8.5px;
  font-weight: 900;
  color: #000;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* NOTICE — 使用提示 */
.note-box {
  background: var(--swiss-gray-bg);
  padding: 8px 10px;
  margin: 10px 0;
  border-left: 3px solid var(--swiss-gray-text);
  font-size: 9px;
  color: #444;
}
.note-box .box-title {
  font-weight: 900;
  color: #333;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-size: 8.5px;
  letter-spacing: 0.35px;
}

/* 列表 */
.box-list {
  list-style: none;
  padding: 0;
}
.box-list li {
  padding: 1px 0 1px 12px;
  position: relative;
  font-size: 9.4px;
  line-height: 1.45;
}
.box-list li::before {
  content: "\2022";
  position: absolute;
  left: 0;
  top: 0.32em;
  color: var(--swiss-red);
  font-weight: 900;
  font-size: 7px;
  line-height: 1;
}
```

**禁止**：
- ❌ 使用 `.warn-box` / `.info-box` 等非标准类名
- ❌ 只用两级（warn + info），必须实现三级
- ❌ 使用 emoji（⚠/⚡/📝）替代文字标题

### HTML 模版

```html
<div class="warning-box">
  <div class="box-title">WARNING</div>
  <ul class="box-list"><li>内容</li></ul>
</div>
<!-- CN 版标题用: 警告 WARNING / 注意 CAUTION / 提示 NOTICE -->
```

---

## 八、步骤列表

### HTML 语义结构

```html
<ol class="steps">
  <li><span class="step-num">1</span>打开面盖。</li>
  <li><span class="step-num">2</span>...</li>
</ol>
```

### CSS

```css
.steps {
  list-style: none;
  padding: 0;
  margin: 8px 0;
}
.steps li {
  position: relative;
  display: block;
  padding-left: 28px;
  margin-bottom: 6px;
  font-size: 10px;
  line-height: 1.5;
}
.step-num {
  position: absolute;
  left: 0;
  top: 1px;
  width: 18px;
  height: 18px;
  background: var(--swiss-black);
  color: #FFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 900;
}
```

**也接受** `div.step-row` + `div.step-text` 结构（视觉等价），但 `<ol class="steps">` 是首选。

---

## 九、普通列表 `.bullet-list`

```css
.bullet-list {
  list-style: none;
  padding: 0;
  margin: 6px 0;
}
.bullet-list li {
  padding: 2px 0 2px 12px;
  position: relative;
  font-size: 10px;
  line-height: 1.5;
}
.bullet-list li::before {
  content: "\2022";
  position: absolute;
  left: 0;
  top: 0.3em;
  color: var(--swiss-red);
  font-weight: 900;
  font-size: 8px;
  line-height: 1;
}
```

---

## 十、图片规范

```css
.fig-wrap {
  text-align: center;
  margin: 8px 0;
}
.fig-wrap img {
  width: auto;
  max-width: 100%;
  max-height: 54mm;
  object-fit: contain;
  display: inline-block;
}
.fig-caption {
  font-size: 7.5px;
  color: var(--swiss-gray-text);
  margin-top: 3px;
  text-align: center;
  font-family: 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
```

**与 V23 差异**：max-height 从 70mm 缩到 54mm（A5 页面更矮）。

### 步骤图并排布局

操作步骤配图使用 flex 行并排时：

```html
<div style="display:flex;gap:3mm;justify-content:center;align-items:flex-start;margin:4px 0 6px;">
  <img src="./{{images_dir}}/imageXX.png" alt="..." style="max-height:28mm;max-width:30%;object-fit:contain;">
  <img src="./{{images_dir}}/imageYY.png" alt="..." style="max-height:28mm;max-width:30%;object-fit:contain;">
</div>
```

**关键**：`align-items:flex-start` 是强制的。不加此属性，不同长宽比的图片会被 flex 拉伸到等高（见陷阱 #17）。

| 场景 | max-height | max-width |
|------|-----------|-----------|
| 3 图并排（操作步骤） | 28mm | 30% |
| 2 图并排（操作步骤） | 32mm | 35% |
| 2 图并排（控制面板+指示灯） | 28mm | 35%/55% |
| 2 图并排（排水/维护） | 26mm | 48%/28% |
| 行内指示灯图标（ICE FULL 等） | 14px | — |
| 控制面板详图 | 20mm | — |

---

## 十一、Compact 类系统（溢出管理）

A5 页面空间有限，长文本语言（DE/IT）和大表格可能溢出。用 compact 类管理：

| 类名 | 用途 | 应用页面 |
|------|------|---------|
| `.compact-ops` | 操作步骤、清洁等步骤密集页 | 操作、清洁 |
| `.compact-table` | 中等表格页（规格、零件） | 规格 |
| `.compact-ts` | 故障排除表（EN/DE/IT） | 故障排除 |
| `.compact-warranty` | 保修信息页 | 保修 |

### 规则

1. CN 模版优先不用 compact（中文短，空间够）
2. 如果 CN 也溢出，用 `.compact-table`
3. DE/IT 必须使用语言补偿（§三）
4. 每个 compact 类的具体参数记录在模版内 CSS，不在本标准中规定具体数值
5. **审计脚本必须检测 overflow**，compact 类的目标是让所有页面 content ≤ page height
6. `.compact-ops .sub-title` 必须缩小 `padding-bottom` 以补偿 V23 sub-title 新增的 `border-bottom`，否则易溢出

---

## 十二、页脚 `.page-footer`

```css
.page-footer {
  position: absolute;
  bottom: 4mm;
  left: var(--page-margin);
  right: var(--page-margin);
  border-top: 1px solid #EEE;
  padding-top: 4px;
  display: flex;
  justify-content: space-between;
  font-size: 7px;
  color: var(--swiss-gray-text);
  font-family: 'Courier New', monospace;
}
```

格式：`<品牌> <型号> <文档类型> | <页码>`

---

## 十三、内容结构（从 d5 §二 继承，A5 适配）

### 标准页面序列

| 页码 | 内容 | 说明 |
|------|------|------|
| 1 | 封面 | 产品图 + 品牌 + 型号 |
| 2 | 目录 | TOC |
| 3 | 安全须知 | WARNING + CAUTION + NOTICE（三级体系） |
| 4+ | 使用前准备 | 开箱、安装 |
| ... | 产品结构 | 结构图 + 零件表 |
| ... | 控制面板 | 按键功能 |
| ... | 产品参数 | 规格表（按市场分版） |
| ... | 操作指引 | 步骤 + 配图 |
| ... | 清洁保养 | 清洁方法 + 存储 |
| ... | 故障排除 | 问题-原因-解决 三列表 |
| 末页 | 保修信息 | 品牌+制造商+保修条款+保修卡 |

A5 因页面小，总页数一般 11-14 页。奇数页需在 booklet 拼版时补空白页。

---

## 十四、已知陷阱与经验教训

### 从 d5 继承

| # | 陷阱 | 对策 |
|---|------|------|
| 1 | Word docx 中 SVG+PNG 重复 | MD5 检测，SVG 优先 |
| 2 | 非标准警示框 | 归入三级体系 |
| 3 | EN版遗漏制造商表格 | 所有版本必须有 |
| 4 | overflow:hidden 截断内容 | 审计脚本检测实际 content height |
| 5 | 颜色不一致 | 严格使用 CSS 变量 |

### 本轮新增（IMT050 验证）

| # | 陷阱 | 后果 | 对策 |
|---|------|------|------|
| 6 | config.json 字段名不匹配 build 脚本 | 输出 `undefined` | 新产品必须用 `name`/`address` 字段名 |
| 7 | 制造商地址不完整 | 法规要求完整地址 | 核对 V23 config，复用已验证的地址 |
| 8 | 保修年限从 Word 提取错误 | 误标 1 年实为 2 年 | 交叉核对 Word 原文 |
| 9 | 品牌法律名称不一致 | 法律风险 | 统一从 V23 config 继承品牌数据 |
| 10 | ACT 品牌邮箱/地址 TODO 占位 | 输出含 TODO | 建新产品前先确认所有品牌数据完整 |
| 11 | 规格参数遗漏 | 信息不完整 | 与 Word 原文逐行对照，不得遗漏 |
| 12 | 封面图 `width:100%` 拉伸 | 图片变形 | 始终用 `max-width` 不用 `width` |
| 13 | export-pdf.js 写死 A4 | PDF 尺寸错 | 用 `preferCSSPageSize: true` |
| 14 | make-booklet.py 写死 A4 | booklet 尺寸错 | 动态检测源 PDF 页面尺寸 |
| 15 | DE/IT 文本溢出 A5 | 内容被截断 | 语言补偿 CSS + compact 类 |
| 16 | 模版 CSS 偏离 V23 设计语言 | 视觉不统一 | **严格按本标准创建** |
| 17 | Flex 容器内混合比例图片拉伸 | 窄长图被拉伸至最高邻居等高 | `display:flex` 容器**必须**加 `align-items:flex-start`；单独 `object-fit:contain` 不够 |
| 18 | 多语言模板正则匹配硬编码 | DE/IT 模板提取失败（如 notice box-title HINWEIS/AVVISO ≠ NOTICE） | 正则用 `[^<]+` 匹配，不硬编码语言文本 |
| 19 | 插入新页面后批量页码更新误伤新页 | 新页面页码也被 +1 | 用占位符标记新页码，更新旧页码后再替换占位符 |
| 20 | 旧 `_audit-visual.js` 已废弃 | 请用新版 | 使用 `audit-visual.js`，输出结构化 JSON，可程序化读取 |
| 21 | `make-booklet.py --all --filter` 无法匹配 | 0 个文件处理 | 用 PowerShell 循环单文件模式：`Get-ChildItem *.pdf \| Where -notmatch booklet \| % { python make-booklet.py $_.FullName }` |

---

## 十五、审计检查清单

新产品模版创建后、交付前，必须通过以下检查：

### A. 设计一致性（对照本标准）
- [ ] CSS 变量色值与 §二 一致
- [ ] `.section-title` 使用左侧竖线（非底部线）
- [ ] `.sub-title` 有 `border-bottom` + `text-transform: uppercase`
- [ ] 表格表头黑底白字 + 交替行色
- [ ] 警示体系使用三级（warning-box/caution-box/note-box）
- [ ] 图片有 `max-width` + `max-height` + `object-fit: contain`
- [ ] 页眉 `.header-ref` 使用 monospace 字体

### B. 数据完整性
- [ ] 所有 `{{}}` 占位符在 build 后已替换（0 个残留）
- [ ] 无 `undefined` / `TODO` / `null` 出现
- [ ] 品牌名/地址/邮箱与 config.json 一致
- [ ] 规格参数与 Word 原文逐行对照无遗漏
- [ ] 保修年限与 Word 原文一致

### C. 页面溢出（Playwright 审计脚本）
- [ ] 所有页面 content height ≤ page height
- [ ] 所有 4 语言版本均通过
- [ ] DE/IT 已应用语言补偿

### D. 图片
- [ ] 所有 `<img>` 的 src 指向真实文件
- [ ] natural aspect ratio ≈ render aspect ratio（差异 < 2%）
- [ ] 无拉伸、无裁切

### E. 多语言一致性
- [ ] 4 语言版本章节数量和顺序一致
- [ ] 数值/数量/按键名在所有版本中一致
- [ ] 品牌信息 + 制造商信息在所有版本中存在

### F. 产出完整性
- [ ] 21 个 HTML 无警告
- [ ] 21 个 PDF 导出成功（A5 尺寸）
- [ ] 21 个 booklet 生成成功（landscape A4）

---

## 十六、审计工具

- `swiss/tools/audit-visual.js` — Playwright 视觉审计（溢出/重叠/空页/残留检测，输出结构化 JSON）
- 运行：`node tools/audit-visual.js output/<file>.html [--json] [--locale en]`
- 预期输出：`ALL CHECKS PASSED`
- **注意**：退出码不可靠（Playwright stderr 可能触发非零退出码），判定 PASS/FAIL 必须检查 stdout 文本（见陷阱 #20）

### 批量审计脚本

```powershell
$files = Get-ChildItem output/imt050-*.html | Where-Object { $_.Name -notmatch 'booklet' }
foreach ($f in $files) {
  $out = node tools/audit-visual.js $f.FullName --json 2>&1 | Out-String
  if ($out -match 'ALL CHECKS PASSED') { Write-Host "[PASS] $($f.Name)" }
  else { Write-Host "[FAIL] $($f.Name)"; $out }
}
```

---

## 附录：CONFIG.JSON 字段规范

品牌对象必须包含以下字段（build 脚本 `buildBrandInfoRows()` 使用）：

```json
{
  "display_name": "品牌显示名",
  "name": "法律全称",
  "address": "完整注册地址",
  "website": "www.example.com",
  "support_email": "support@example.com"
}
```

制造商对象必须包含：

```json
{
  "name_cn": "中文公司名",
  "name_en": "English Company Name",
  "address_cn": "完整中文地址",
  "address_en": "Full English address",
  "website": "www.example.com"
}
```

**禁止**使用 `legal_name` / `address_cn` / `address_en` 替代 `name` / `address`（品牌对象）。

---

## 十七、内容结构约束

> 本节规则以 `[结构]` 或 `[渲染]` 标签分类：
> - **[结构]**：Writer 在编写 JSON 时即可遵守，无需渲染验证
> - **[渲染]**：必须构建 HTML 后通过审计工具验证，Writer 无法仅凭 JSON 判断

### 分页完整性

| # | 规则 | 标签 | 说明 |
|---|------|------|------|
| C1 | `warranty_card` block 的全部 fields 必须在**同一个 page block** 中 | [结构] | 保修卡跨页切断用户体验极差，应合并到一页 |
| C2 | `structured_table` 超过 15 行时建议拆分到独立 page block | [结构] | 过长表格在 A5 页面必然溢出 |
| C3 | `step_flow` 的单个 step（文字+配图）不得跨页 | [渲染] | 需 Playwright 检查每个 step 是否被 page boundary 切断 |

### 图片与容器

| # | 规则 | 标签 | 说明 |
|---|------|------|------|
| C4 | `figure_row` 包含多张图时，所有子图必须共享容器宽度 | [渲染] | CSS 已通过 `.figure-row img { flex:1 1 0; min-width:0 }` 保障，但新增 figure 类型时需验证 |
| C5 | 所有 `<img>` 的渲染右边界不得超出 `.page` 右边界 | [渲染] | 审计工具检查项 |
| C6 | 图片的 `object-fit` 必须为 `contain`，禁止 `cover` 或 `fill` | [结构] | JSON 中 figure 定义可检查 |
| C7 | `split_panel` 中配图宽度不得超过容器 50% | [结构] | 在 JSON 中通过 `figure_width` 或 `max_width` 控制 |

### 文本与溢出

| # | 规则 | 标签 | 说明 |
|---|------|------|------|
| C8 | 每页可视内容的实际高度不得超过页面内容区高度（190mm） | [渲染] | 审计工具核心检查项 |
| C9 | 德语/意大利语文本比中文/英文长 30-60%，compact 类页面必须验证所有语言 | [渲染] | 仅测试一种语言不充分 |
| C10 | `cover-bottom` 使用 `position:absolute` 定位时，与内容区的 box 重叠是设计行为，不算排版错误 | [渲染] | 审计工具应排除此类 false positive |
| C11 | 产品结构图 (Ch.03) 中的零件编号标注必须在 PDF 中肉眼可辨，不得因缩图导致编号重叠或模糊不清 | [渲染] | 验证方式：PDF 100% 缩放下，所有编号数字可独立辨认。当前参考值——V23: 68mm, IMT050: 72mm |
| C12 | 控制面板/功能面板图 (Ch.04) 中的按键文字和标注必须在 PDF 中清晰可读 | [渲染] | 验证方式：PDF 100% 缩放下，按键名称和编号无需放大即可读取。当前参考值——V23: 40mm, IMT050: 36mm+30mm |
| C13 | 调整图片尺寸后必须验证**不增加页数**——结构图和面板图应与对应表格共处同一页 | [渲染] | 每次修改后用 export-pdf 确认总页数不变 |
