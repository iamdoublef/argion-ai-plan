# Swiss 说明书模板系统 — 操作手册

基于 V23 Swiss 风格说明书（已审计 PASS）的模板化生产系统。

**当前产品**：V23（真空封口机）、IMT050（制冰机）  
**品牌**：WEVAC、Vesta、ACT  
**语言**：中文（CN/HK/TW）、英文（GB/ZA）、德语（DE）、意大利语（IT）  
**每产品变体数**：7 地区 × 3 品牌 = 21 个 HTML / PDF / Booklet

---

## 一、目录结构

```
swiss/
├── DESIGN-STANDARD.md          ← 唯一设计基准（CSS数值、色彩、字号）
├── SOP-new-product.md          ← 新产品冷启动 SOP（12步）
├── README.md                   ← 本文件
│
├── template/                   ← 母版 HTML（含 {{占位符}} + @CONTENT 区域）
│   ├── v23-master-cn.html      ← V23 中文母版
│   ├── v23-master-en.html      ← V23 英文母版
│   ├── v23-master-de.html      ← V23 德语母版
│   ├── v23-master-it.html      ← V23 意大利语母版
│   ├── imt050-master-cn.html   ← IMT050 中文母版
│   ├── imt050-master-en.html   ← IMT050 英文母版
│   ├── imt050-master-de.html   ← IMT050 德语母版
│   ├── imt050-master-it.html   ← IMT050 意大利语母版
│   └── shared/                 ← 共享样式
│       ├── base/
│       │   ├── core-shell.css       ← 全局基础样式（A5 页面）
│       │   ├── v23-booklet.css      ← V23 产品级 compact 补丁
│       │   └── imt050-booklet.css   ← IMT050 产品级 compact 补丁
│       ├── cn/                      ← 中文共享片段
│       ├── en/                      ← 英文共享片段
│       ├── de/                      ← 德语共享片段
│       └── it/                      ← 意大利语共享片段
│
├── products/                   ← 产品配置 + 图片
│   ├── v23/
│   │   ├── config.json         ← V23 产品数据
│   │   └── images/             ← V23 图片
│   └── imt050/
│       ├── config.json         ← IMT050 产品数据
│       └── images/             ← IMT050 图片
│
├── tools/                      ← 构建工具链
│   ├── build-variant.js        ← 模板引擎（占位符替换 + 繁体转换）
│   ├── export-pdf.js           ← Playwright PDF 导出（A5）
│   ├── export-pdf-batch.js     ← 批量 PDF 导出
│   ├── make-booklet.py         ← A5 → A4 booklet 拼版
│   └── _audit-visual.js        ← Playwright 视觉审计（overflow + 图片变形）
│
├── output/                     ← 构建输出
│   ├── *.html                  ← 构建后的完整 HTML
│   ├── *.pdf                   ← A5 单页 PDF
│   ├── *-booklet-A4.pdf        ← A4 booklet（装订版）
│   └── _audit/                 ← 审计截图
│
├── audits/                     ← 审计报告
├── skills/                     ← Agent skill 定义
└── tests/                      ← 测试文件
```

---

## 二、核心概念

### 三层分离

| 层 | 文件 | 职责 | 谁可以改 |
|----|------|------|---------|
| **数据层** | `products/*/config.json` | 产品参数、品牌信息、零件、按键 | 懂 JSON 基础的人 |
| **模板层** | `template/*-master-*.html` | 页面结构、章节内容、图文排布 | 需要 HTML 知识 |
| **样式层** | `template/shared/base/*.css` | 字号、颜色、间距、分页 | 需要 CSS 知识 |

### 构建链

```
母版 HTML + config.json
        │
        ▼  build-variant.js (替换占位符 + 繁体转换)
  完整 HTML (21个变体)
        │
        ▼  export-pdf.js (Playwright)
     A5 PDF (21个)
        │
        ▼  make-booklet.py (PyMuPDF)
  A4 Booklet (21个)
        │
        ▼  _audit-visual.js (Playwright)
     审计报告 (overflow + 图片检测)
```

---

## 三、常用操作

### 3.1 全量构建（所有变体）

```powershell
cd d:\work\private\yjsplan\research\yjs-manual-opt\swiss

# V23 全量
node tools/build-variant.js --product products/v23 --all

# IMT050 全量
node tools/build-variant.js --product products/imt050 --all
```

### 3.2 单个变体构建

```powershell
# 指定产品 + 地区 + 品牌
node tools/build-variant.js --product products/v23 --region cn --brand wevac
node tools/build-variant.js --product products/imt050 --region de --brand vesta
```

### 3.3 导出 PDF

```powershell
# 单个
node tools/export-pdf.js output/v23-wevac-eu-cn.html

# 某产品全部
node tools/export-pdf-batch.js

# 或用通配符
node tools/export-pdf.js output/imt050-*.html
```

### 3.4 生成 Booklet

```powershell
# 单个
python tools/make-booklet.py output/v23-wevac-eu-cn.pdf

# 全部
python tools/make-booklet.py --all output/
```

### 3.5 运行审计

```powershell
# 单个 HTML 审计（检查 overflow + 图片变形）
node tools/_audit-visual.js output/imt050-wevac-eu-cn.html

# 期望输出：ALL CHECKS PASSED
```

---

## 四、使用场景

### 场景 A：修改产品数据（参数/品牌信息/保修年限）

**不需要改 HTML 或 CSS，只改 config.json。**

```powershell
# 1. 编辑 config.json
# 例：改保修年限 → "warranty": { "years": 3 }
# 例：改品牌邮箱 → "brands.wevac.support_email": "new@wevac.com"

# 2. 重新构建
node tools/build-variant.js --product products/v23 --all

# 3. 重新导出 PDF + Booklet
node tools/export-pdf-batch.js
python tools/make-booklet.py --all output/

# 4. 快速审计
node tools/_audit-visual.js output/v23-wevac-eu-cn.html
```

### 场景 B：修改内容文字（安全条目/操作步骤/清洁方法）

**需要改 HTML 模板中的 `@CONTENT` 区域。**

```powershell
# 1. 编辑 template/{product}-master-{lang}.html
#    找到 <!-- @CONTENT:safety:start --> 等标记
#    修改其中的文字内容
#    注意：需要同时修改 4 个语言文件（cn/en/de/it）

# 2. 重新构建 + 导出 + 审计（同场景 A 步骤 2-4）
```

### 场景 C：切换品牌/地区（无需改任何文件）

```powershell
# 切品牌
node tools/build-variant.js --product products/v23 --brand vesta

# 切地区（欧标→美标）
node tools/build-variant.js --product products/v23 --region tw

# 组合
node tools/build-variant.js --product products/v23 --brand act --region tw

# 导出
node tools/export-pdf.js output/v23-act-us-tw.html
python tools/make-booklet.py output/v23-act-us-tw.pdf
```

### 场景 D：新产品冷启动

详见 `SOP-new-product.md`（12 步完整流程，预计 2 天）。

核心步骤：
1. Word 原稿 → 提取文本 + 图片
2. 创建 `products/{新型号}/config.json`
3. 创建 `template/{新型号}-master-*.html`（4 语言）
4. 全量构建 → 导出 → 审计 → 修复 → 发布

### 场景 E：全局样式调整（字号/颜色/间距）

```powershell
# 1. 修改 template/shared/base/core-shell.css
# 2. 同步更新 DESIGN-STANDARD.md（数值必须一致！）
# 3. 重新构建所有产品所有变体
node tools/build-variant.js --product products/v23 --all
node tools/build-variant.js --product products/imt050 --all
# 4. 重新导出所有 PDF + Booklet + 审计
```

---

## 五、模板占位符说明

### 自动替换占位符（build-variant.js 处理）

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `{{brand.display_name}}` | config → brands.{brand}.display_name | 品牌显示名（WEVAC / Vesta / ACT） |
| `{{brand.name}}` | config → brands.{brand}.name | 品牌法律全称 |
| `{{brand.address}}` | config → brands.{brand}.address | 品牌注册地址 |
| `{{brand.website}}` | config → brands.{brand}.website | 品牌网址 |
| `{{brand.support_email}}` | config → brands.{brand}.support_email | 客服邮箱 |
| `{{product.model}}` | config → product.model | 产品型号（V23 / IMT050） |
| `{{product.name_cn}}` | config → product.name_cn | 中文产品名 |
| `{{product.name_en}}` | config → product.name_en | 英文产品名 |
| `{{warranty.years}}` | config → warranty.years | 保修年限 |
| `{{images_dir}}` | config → images_dir | 图片目录名 |

### 动态表格（build-variant.js 从 config 数组生成）

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `{{#SPECS_TABLE_ROWS}}` | config → specs.{market}.rows[] | 技术参数表行 |
| `{{#PARTS_TABLE_ROWS}}` | config → parts[] | 零件表行 |
| `{{#BUTTONS_TABLE_ROWS}}` | config → buttons[] | 按键功能表行 |
| `{{#BRAND_INFO_ROWS}}` | config → brands.{brand} | 品牌商信息表 |
| `{{#MANUFACTURER_INFO_ROWS}}` | config → manufacturer | 制造商信息表 |

### 手工编辑区域

```html
<!-- @CONTENT:safety:start -->
  ... 安全须知内容（手动编写）...
<!-- @CONTENT:safety:end -->
```

`@CONTENT` 区域内的内容由人工（或 AI）编写，build-variant.js 不替换其内容，仅替换其中的 `{{}}` 占位符。

---

## 六、AI Agent 路由

| 任务 | Agent | 说明 |
|------|-------|------|
| 新建/重构模板 HTML | `swiss-manual-writer` | 创建新产品母版、修复模板结构 |
| 审计/对齐/比较/PDF 核验 | `swiss-content-auditor` | D1-D8 八维度审计 |
| 设计标准参考 | — | 先读 `DESIGN-STANDARD.md` |
| 新产品完整流程 | — | 先读 `SOP-new-product.md` |
| Skill 入口 | — | 先读 `skills/swiss-manual-a5/SKILL.md` |

> **硬规则**：不要用旧的 `manual-writer` / `manual-auditor` agent 处理 Swiss 任务，除非明确要走旧 A4 链路。

---

## 七、环境依赖

| 依赖 | 版本要求 | 检查命令 | 用途 |
|------|----------|----------|------|
| Node.js | ≥ 18 | `node -v` | build-variant.js, export-pdf.js, _audit-visual.js |
| Playwright | 最新 | `npx playwright --version` | PDF 导出 + 审计截图 |
| Python | ≥ 3.8 | `python --version` | make-booklet.py |
| PyMuPDF | 最新 | `python -c "import fitz"` | booklet PDF 合并 |

---

## 八、常见问题

| 问题 | 原因 | 解法 |
|------|------|------|
| `Warning: image not found` | `images_dir` 字段或文件名不匹配 | 检查 config.json `images_dir` 和 images/ 目录内文件名 |
| PDF 图片空白 | 图片路径相对引用错误 | 在 `swiss/` 目录下运行命令 |
| 参数仍显示旧数据 | config.json 未保存 / JSON 格式错误 | 运行 `node -e "JSON.parse(require('fs').readFileSync('products/{型号}/config.json','utf8'))"` |
| 繁体转换不全 | S2T_MAP 缺字 | 在 build-variant.js 的 S2T_MAP 中补充 |
| Booklet 页数不对 | PDF 不是 4 的倍数 | 在 HTML 末尾加空白 `.page` 补齐 |
| OVERFLOW 审计失败 | 内容超出 A5 页面高度 | 对该页添加 compact 类或拆分为两页 |
| 图片 STRETCHED 审计失败 | 封面图用了 width:100% | 改为 `width:auto;max-width:85%` |

---

## 九、产出规格

| 项目 | 规格 |
|------|------|
| 单页 PDF | A5 (148×210mm) |
| Booklet | A4 landscape (297×210mm)，对折后为 A5 |
| 每产品变体数 | 21 (7地区 × 3品牌) |
| 当前总产出 | 43 PDF + 43 Booklet（V23: 22, IMT050: 21） |

---

*最后更新：2026-03-09 | 版本：v2.0*
