# SOP：新产品说明书冷启动

**目标**：收到新产品 Word 原稿，按照本 SOP 操作，2天内交付通过审计的完整说明书（全语言/全品牌/PDF+Booklet）。

**适用范围**：Swiss风格模板系统（本目录），产品型号第一次生产说明书时使用。

---

## 前提 & 工具依赖

| 依赖 | 检查命令 | 备注 |
|------|----------|------|
| Node.js ≥ 18 | `node -v` | build-variant.js 运行时 |
| Playwright | `npx playwright --version` | PDF导出 |
| Python ≥ 3.8 | `python --version` | make-booklet.py |
| PyMuPDF | `python -c "import fitz"` | booklet 合并 |

---

## 步骤总览（checklist）

```
Day 1 上午：信息收集 & 数据结构化（Step 1-4）
Day 1 下午：首次构建 & 图片验证（Step 5-7）  
Day 2 上午：全量构建 + 审计（Step 8-10）
Day 2 下午：修复 + 发布（Step 11-12）
```

---

## Step 1：收件 & 信息登记

**操作**：

1. 将 Word 原稿放入：
   ```
   research/yjs-manual-opt/_inbox/{型号} 说明书-{版本}-{日期}.docx
   ```

2. 用 AI（Claude）阅读 Word 文件，填写下面的信息收集表（见 Step 2），确认后再开始。

**质量关卡**：原稿没有，不开工。

---

## Step 2：从原稿提取结构化数据

**目标**：将 Word 内容转化为机器可读的文本和图片，为填写 `config.json` 做准备。

### 2a. 提取文本

使用 AI 将 Word 原稿关键信息提取到 `source/extracted_{型号}.txt`，覆盖以下字段：

```
# extracted_{型号}.txt 结构
## 产品基本信息
- 型号（model）：
- 中文名称：
- 英文名称：
- 德文名称（如有）：
- 意大利文名称（如有）：

## 技术参数
### 欧标 (EU)
- 电压：
- 频率：
- 功率：
- 真空泵压力：

### 美标 (US)
- 电压：
- 频率：
- 功率：
- 真空泵压力：

## 零件清单
| 编号 | 中文名称 | 英文名称 | 德文名称 | 意文名称 |
|------|----------|----------|----------|----------|

## 按键功能表
| 编号 | 按键名称(EN) | 中文功能描述 | 英文功能描述 | 德文 | 意文 |
|------|-------------|-------------|-------------|------|------|

## 品牌信息（当前销售品牌）
- Wevac / Vesta / ACT（圈出适用）

## 保修年限：
```

### 2b. 提取图片

从 Word 文件提取原始图片（可通过改后缀为 `.zip` 解压 `word/media/` 获取）：

```powershell
# 复制 docx → zip
Copy-Item "_inbox\{型号}.docx" "_inbox\{型号}.zip"
Expand-Archive "_inbox\{型号}.zip" -DestinationPath "source\_docx_unzip_{型号}"
# 原始图片在 source\_docx_unzip_{型号}\word\media\
```

将 `word/media/` 下图片复制到：
```
source/images_{型号}_raw/
```

**质量关卡**：`extracted_{型号}.txt` 中技术参数、零件表、按键表无遗漏。

---

## Step 3：创建产品目录

### 3a. 判断产品类型

**先判断新产品是否与 V23（真空封口机）属于同一类型**：

| 问题 | 同类 → | 不同类 → |
|------|--------|---------|
| 产品功能是否为"真空封口/低温烹饪"？ | ✅ | ❌ |
| 按键/参数结构是否相似？ | ✅ | ❌ |

**同类（推荐）**：直接复用 V23 template HTML，只改 config.json + 图片即可。  
**不同类**：需要额外创建新的 template HTML（见步骤3c），工作量更大。

### 3b. 创建产品目录

```powershell
# 在 swiss/ 目录下执行：仅复制结构，不复制 template
New-Item -ItemType Directory "products\{型号小写}\images" -Force
# 例：New-Item -ItemType Directory "products\imt050\images" -Force

# 复制 V23 config.json 作为模板基础
Copy-Item "products\v23\config.json" "products\{型号小写}\config.json"
```

产生的目录结构：
```
swiss/products/{型号}/
├── config.json         ← 待修改（下一步）
└── images/            ← 待替换（Step 5）
```

### 3c.【仅不同类产品需要】创建专属 template HTML

不同产品类型（如制冰机、低温烹饪机等），需要为其创建专属模板：

```powershell
# 以下文件为新产品对应的模板（用于多语言渲染）
swiss/template/{型号小写}-master-cn.html    ← 中文模板
swiss/template/{型号小写}-master-en.html    ← 英文模板
swiss/template/{型号小写}-master-de.html    ← 德文模板（可选）
swiss/template/{型号小写}-master-it.html    ← 意文模板（可选）
```

**模板创建方法**：
1. 复制 `template/v23-master-cn.html` 为新型号模板
2. 替换所有产品相关内容区段（保留 `{{占位符}}` 和结构）
3. 测试单变体构建后再批量构建

在 `products/{型号}/config.json` 中补充模板引用：
```json
"template_override": "{型号小写}"
```

---

## Step 4：填写 config.json

打开 `swiss/products/{型号}/config.json`，依照 `extracted_{型号}.txt` 逐字段修改：

```json
{
  "product": {
    "model": "{型号大写}",          // 例 "IMT050"
    "name_cn": "真空封口机",         // 改为本产品中文名
    "name_en": "Vacuum Sealer",      // 改为本产品英文名
    "name_de": "Vakuumiergerät",     // 改为本产品德文名
    "name_it": "Sigillatrice",       // 改为本产品意文名
    "active_brand": "wevac",         // 默认品牌（可在构建时 --brand 覆盖）
    "active_market": "eu",           // 默认市场
    "images_dir": "images_{型号小写}"  // 例 "images_imt050"
  },
  "specs": {
    "eu": {
      "voltage": "220~240 Vac",     // 按原稿欧标
      "frequency": "50 Hz",
      "power": "190 W",
      "pump": "-958 mbar"
    },
    "us": {
      "voltage": "110~120 Vac",     // 按原稿美标（如无美标版去掉此块）
      "frequency": "60 Hz",
      "power": "190 W",
      "pump": "-28.3 inHg"
    }
  },
  // ... parts、buttons、brands等字段参照 V23 config.json 依原稿内容修改
}
```

**重点必填字段**：

| 字段 | 来源 | 影响 |
|------|------|------|
| `product.model` | 原稿 | 文件名、页眉 |
| `specs.eu/us` | 技术参数表 | 参数页 |
| `parts[].name_*` | 零件清单 | 零件图说明 |
| `buttons[].name_en` | 按键功能表 | 功能说明 |
| `images_dir` | 本产品 | 图片路径 |

**质量关卡**：
```powershell
# 语法检查
node -e "JSON.parse(require('fs').readFileSync('products/{型号}/config.json','utf8')); console.log('JSON OK')"
```

---

## Step 5：图片标准化

### 5a. 命名规范

将 `source/images_{型号}_raw/` 内的图片按以下规范重命名后，复制到 `swiss/products/{型号}/images/`：

```
命名格式：{型号小写}_{章节编号}_{序号}.{ext}
示例：
  imt050_02_01.svg    ← 第2章第1张图
  imt050_03_01.svg    ← 第3章第1张图
  imt050_parts.svg    ← 零件示意图（固定名）
  imt050_product.svg  ← 产品主图（固定名）
```

### 5b. 图片格式要求（来自 d5-manual-standard.md）

- 优先 SVG（矢量），次选 PNG（≥300 DPI）
- 所有图片宽度不超过印刷区（165mm）
- 图片内**不内嵌文字**（多语言切换需要，文字在 HTML 中）

### 5c. 更新 template 中图片引用

检查 `swiss/template/` 模板 HTML，确认 `{{images_dir}}/xxx.svg` 路径与你的图片文件名一致。

---

## Step 6：首次验证构建（单变体）

**先构建一个变体** 验证配置无误，再批量构建：

```powershell
cd d:\work\private\yjsplan\research\yjs-manual-opt\swiss

# 构建一个测试变体（CN / Wevac / EU）
node tools/build-variant.js --product products/{型号小写} --region cn

# 检查输出：output/{型号}-wevac-eu-cn.html
# 用浏览器打开 HTML，目测：
#   ✅ 产品名称正确
#   ✅ 技术参数为本产品数据（非V23数据）
#   ✅ 零件图显示正常
#   ✅ 按键表内容正确
```

**质量关卡**：单变体 HTML 目测通过后，再继续。

---

## Step 7：全量构建（21个变体）

```powershell
# 构建全部变体（7地区 × 3品牌 = 21个 HTML）
node tools/build-variant.js --product products/{型号小写} --all

# 预期输出：
# output/{型号}-wevac-eu-cn.html   ← 大陆简体
# output/{型号}-wevac-eu-hk.html   ← 香港繁体
# output/{型号}-wevac-us-tw.html   ← 台湾繁体
# output/{型号}-wevac-eu-gb.html   ← 英文
# output/{型号}-wevac-eu-de.html   ← 德语
# output/{型号}-wevac-eu-it.html   ← 意大利语
# output/{型号}-wevac-eu-za.html   ← 南非英文
# ... × 3 品牌 = 21 个
# BUILD MATRIX SUMMARY: OK: 21 | WARNING: 0
```

**如果有 WARNING**：查看日志，通常是图片找不到 → 检查 `images_dir` 字段和图片文件名。

---

## Step 8：导出 PDF（全量）

```powershell
# 确认 Playwright 已安装
cd d:\work\private\yjsplan\research\yjs-manual-opt\swiss

# 单文件测试（先测一个）
node tools/export-pdf.js output/{型号}-wevac-eu-cn.html

# 全量导出（输出到 output/ 下，同目录）
node tools/export-pdf.js output/*.html

# PDF 命名规则（自动）：{型号}-wevac-eu-cn.pdf
```

---

## Step 9：生成 Booklet（装订本版本）

Booklet = A4页面排列为小册子折叠打印格式（每张A4包含对开两页）。

**依赖**：`pip install pymupdf`

```powershell
cd d:\work\private\yjsplan\research\yjs-manual-opt\swiss

# 对 output/ 内所有 {型号} PDF 生成 booklet（跳过已有 booklet 文件）
python tools/make-booklet.py --all output/

# 或只处理本产品的 PDF（单文件）
python tools/make-booklet.py output/{型号}-wevac-eu-cn.pdf
# → 输出 output/{型号}-wevac-eu-cn-booklet-A4.pdf
```

---

## Step 10：运行审计（manual-auditor agent）

**调用方法**：在 Claude 中使用 `manual-auditor` agent，传入参数：

```
型号：{型号}
审计目标：swiss/output/ 下 {型号} 的全部 HTML（至少检查 cn/en/de 三语言版本）
基准文件：
  - data/d5-manual-standard.md
  - source/extracted_{型号}.txt
  - swiss/products/{型号}/config.json
```

**审计维度（7维度）**：
1. 内容完整性（章节/零件/按键全覆盖）
2. 技术参数准确性（对比 extracted_{型号}.txt）
3. 图片加载（0失败）
4. 排版合规（边距/字体/字号/分页）
5. 多语言一致性（结构一致、数量一致）
6. 品牌信息独立（品牌变体间不串号）
7. PDF 打印质量（翻页正确、无截断）

**期望结果**：每个维度 PASS（0 ERROR）。

**审计报告写入**：
```
swiss/output/audit-{型号}-v1.md
```

---

## Step 11：修复循环

```
审计报告 → 分级处理：
  ERROR   → 必须修复，修完重新构建该变体，重审计
  WARNING → 本版本记录，下版本修
  INFO    → 记录，不阻塞发布
```

**单变体快速修复**：
```powershell
# 修改 config.json 或模板后，仅重建受影响的变体
node tools/build-variant.js --product products/{型号小写} --region cn

# 重新导出 PDF
node tools/export-pdf.js output/{型号}-wevac-eu-cn.html
```

**质量关卡**：所有 ERROR 归零，且至少 CN + EN 版本 PASS 后，可以发布。

---

## Step 12：归档发布

```powershell
# 创建 release 目录
$DATE = Get-Date -Format "yyyy-MM-dd"
New-Item -ItemType Directory "releases\${DATE}_first-release-{型号}"

# 复制最终产物
Copy-Item output\{型号}*.html  "releases\${DATE}_first-release-{型号}\"
Copy-Item output\{型号}*.pdf   "releases\${DATE}_first-release-{型号}\"
Copy-Item output\audit-{型号}-v1.md "releases\${DATE}_first-release-{型号}\audit\"

# 更新 INDEX.md（保存阶段节点）
# 在 research/yjs-manual-opt/INDEX.md 追加：
# ### {日期} {型号}首版说明书发布（全量21变体，审计PASS）
# commit: uncommitted
# - ptr: file:research/yjs-manual-opt/releases/{DATE}_first-release-{型号}/
```

---

## 常见问题 & 解法

| 问题 | 原因 | 解法 |
|------|------|------|
| `Warning: image not found: xxx.svg` | `images_dir` 字段或文件名不匹配 | 检查 config.json `images_dir` 和 `images/` 目录内文件名 |
| PDF 图片空白 | 图片路径相对引用错误 | 确认 `node tools/export-pdf.js` 在 `swiss/` 目录下运行 |
| 技术参数仍显示V23数据 | config.json 未保存/JSON格式错误 | 重新检查JSON，运行语法检查命令 |
| 繁体转换不全 | S2T_MAP 未覆盖新字符 | 在 `build-variant.js` 的 `S2T_MAP` 补充缺失字符 |
| Booklet 页数不对 | PDF 总页数不是4的倍数 | 在 HTML 末尾加空白页补齐 |
| 审计报告中多语言参数不一致 | config.json 中 labels 字段多语言未同步 | 检查 `config.json > labels` 各语言字段 |

---

## 参考文件

| 文件 | 说明 |
|------|------|
| [data/d5-manual-standard.md](../data/d5-manual-standard.md) | 编写规范唯一基准 |
| [products/v23/config.json](products/v23/config.json) | 参考模板（V23产品） |
| [tools/build-variant.js](tools/build-variant.js) | 构建脚本完整说明 |
| [README.md](README.md) | 系统架构说明 |
| [../data/d2-ai-flow-proposal.md](../data/d2-ai-flow-proposal.md) | AI辅助内容生成方案（B阶段） |

---

*最后更新：2026-03-08 | 版本：v1.0*
