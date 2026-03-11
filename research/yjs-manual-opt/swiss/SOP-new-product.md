# SOP：Swiss 说明书双轨交付与本地化生产流程

## 目标

把 Swiss 说明书统一到一条可生产、可维护、可审计的双轨生产线：

- 自有品牌：`HTML + PDF`
- ODM 客户：`DOCX + PDF`
- 结构源只认 JSON
- 译文编辑面只认翻译工作簿
- `PDF` 用于审稿和交付；若发生应急 hotfix，下一版必须回写正式源头

本 SOP 适用于 `research/yjs-manual-opt/swiss/` 当前 A5 共享母版体系。

## 当前范围

- 适用于现有产品维护和新产品首版接入
- 不做 Web 后台
- 不把 Excel 提升为结构主源
- 不让翻译人员改 HTML
- 不再使用运行时逐字简转繁作为正式发布链路

## 正式输入

### 结构源

每个产品只认下面 4 类正式结构输入：

- `products/<product>/product.json`
- `products/<product>/images.json`
- `products/<product>/content/source/manifest.json`
- `products/<product>/content/source/chapters/*.json`

说明：

- `product.json`：产品事实、规格、按钮、零件、品牌矩阵、区域矩阵
- `images.json`：语义图片 ID、文件映射、用途、归属
- `manifest.json`：章节顺序、目录标题、页眉引用、启用状态
- `chapters/*.json`：单章页面结构和 block 结构

### 译文源

正式译文由下面两层组成：

- `products/<product>/i18n/compiled/<locale>.json`
- `products/<product>/i18n/workbooks/<locale>.xlsx`

说明：

- `compiled/<locale>.json`：正式编译输入，供构建器使用
- `workbooks/<locale>.xlsx`：翻译和审核人员的编辑面

不再使用：

- `config.json`
- `content.<lang>.json`
- 模板内正文
- 运行时逐字简转繁（已移除）

## 正式输出

### 自有品牌线

- `output/*.html`
- `output/*.pdf`

### ODM 线

- `output/*.docx`
- `output/*.pdf`

说明：

- `HTML` 只用于技术预览和定位问题
- `PDF` 是审稿和最终交付界面
- `DOCX` 是 ODM 客户的可编辑交付稿，不是正式源头

## 目录结构

```text
products/<product>/
├─ product.json
├─ images.json
├─ images/
├─ content/
│  └─ source/
│     ├─ manifest.json
│     └─ chapters/
│        ├─ 01-*.json
│        ├─ 02-*.json
│        └─ ...
└─ i18n/
   ├─ compiled/
   │  ├─ zh-CN.json
   │  ├─ zh-HK.json
   │  ├─ zh-TW.json
   │  ├─ en.json
   │  ├─ de.json
   │  └─ it.json
   └─ workbooks/
      ├─ zh-CN.xlsx
      ├─ zh-HK.xlsx
      ├─ zh-TW.xlsx
      ├─ en.xlsx
      ├─ de.xlsx
      └─ it.xlsx
```

## 结构规则

### 1. 章节来源

- 章节顺序、目录文字、页眉引用只认 `manifest.json`
- 每章正文只认 `chapters/*.json`
- 章节数量和顺序由数据决定，不写死在模板里

### 2. 正式 block 类型

正式内容只允许：

- `paragraph`
- `bullet_list`
- `warning_box`
- `caution_box`
- `notice_box`
- `sub_title`
- `figure`
- `figure_row`
- `step_flow`
- `table_ref`
- `qa_list`
- `contact_block`
- `warranty_card`
- `split_panel`

禁止：

- `html_fragment`
- 任何原始 HTML 片段

### 3. 文本 token

文本字段只允许：

- `**粗体**`
- `[btn:按钮名]`
- `\n`

不允许：

- `<b>...</b>`
- `<span>...</span>`
- 其他原始 HTML 标签

### 4. 图片规则

- `images.json` 使用语义图片 ID，不在正文里直接写文件名
- 程序性图片必须标记：
  - `kind: "procedural"`
  - `usage_ref`
- `usage_ref` 格式固定为：
  - `chapter_id.page_key.step_id`
  - 或 `chapter_id.page_key.block_id`
- 共享装饰图单独标记为 `kind: "shared"`

### 5. 本地化规则

- `zh-HK` 与 `zh-TW` 必须是独立 locale catalog
- 术语、单位、品牌语言、警示语必须参考 `standards/` 下的规范资产
- 新产品结构草稿、译文草稿和本地化审计，优先复用：
  - `standards/ai-new-product-structure-prompt.md`
  - `standards/ai-translation-draft-prompt.md`
  - `standards/ai-localization-audit-prompt.md`

## 新产品首版流程

### Step 1：准备资料

准备以下输入：

- 简版 Word / 源稿
- 产品图片
- 参数资料
- 品牌与售后信息

### Step 2：模型生成草稿

模型只允许做：

- 结构草稿
- 多语言翻译初稿
- 单位和术语统一建议
- 图片绑定建议
- 自审问题清单

模型不允许直接发布成品。

### Step 3：人工确认结构事实

人工确认：

- 章节划分
- 步骤与图片对应
- 参数、按钮、零件事实
- 品牌和保修信息

### Step 4：建立结构源

创建或更新：

- `product.json`
- `images.json`
- `content/source/manifest.json`
- `content/source/chapters/*.json`

### Step 5：生成译文工作簿

```powershell
cd D:\work\private\yjsplan\research\yjs-manual-opt\swiss
node tools/export-translation-workbook.js --product products/<product> --all
```

### Step 6：翻译审核

翻译人员只改：

- `i18n/workbooks/<locale>.xlsx`

不改：

- HTML
- CSS
- 章节结构 JSON
- 图片绑定

### Step 7：编译译文

```powershell
node tools/compile-translation-workbook.js --product products/<product> --all
```

### Step 8：构建 HTML

```powershell
node tools/build-variant.js --product products/<product> --region cn
```

### Step 9：导出 PDF / DOCX

```powershell
node tools/export-pdf.js output/<product>-<brand>-<market>-<region>.html
node tools/export-docx.js --product products/<product> --region <region>
```

### Step 10：审计

```powershell
node tools/_audit-visual.js output/<product>-<brand>-<market>-<region>.html
```

### Step 11：人工抽检

必须抽检这些关键页：

- 封面
- 目录
- 安全第一页
- 结构 / 控制面板页
- 操作页
- 保修页
- 保修卡续页

ODM 任务额外确认：

- DOCX 能在 WPS 正常打开
- 图片、表格、页眉页脚完整

### Step 12：批量生成

确认单变体通过后，再跑全矩阵：

```powershell
node tools/build-variant.js --product products/<product> --all
node tools/export-pdf-batch.js
node tools/export-docx.js --product products/<product> --all
```

## 现有产品维护流程

现有产品维护只改：

- `product.json`
- `images.json`
- `content/source/manifest.json`
- `content/source/chapters/*.json`
- `i18n/workbooks/<locale>.xlsx`

标准顺序：

1. 改结构或事实 JSON
2. 如涉及译文，更新 workbook 并编译 catalog
3. 重建 HTML
4. 重导 PDF
5. 如涉及 ODM，重导 DOCX
6. 跑视觉审计
7. 抽检关键页

## PDF hotfix 规则

- 允许在临出货前对 PDF 做极少量应急修改
- 但 PDF 不是正式源头
- 所有 hotfix 必须登记，并在下一版回写：
  - `product.json`
  - `images.json`
  - `content/source/...`
  - `i18n/compiled/...`
  - `i18n/workbooks/...`

禁止形成：

- PDF 一套
- JSON 一套
- 工作簿又一套

## 验收标准

- A5 共享母版视觉统一
- 所有内容来自结构源 + 译文 catalog
- 译文审核不需要碰 HTML
- `zh-HK`、`zh-TW` 不再依赖逐字简转繁发布
- ODM 可稳定输出 DOCX
- 无 unresolved placeholder
- 无 raw HTML
- 无 `html_fragment`
- 无横向顶出
- 无图片变形
- 无保修卡裁切
- 程序性图片与步骤一一对应

## 2026-03 Word 支线补充规则

- `DOCX` 为独立的 A5 可编辑支线，不再按“PDF 影子稿”导出。
- `HTML/PDF` 与 `DOCX` 共用同一份 JSON 内容源和译文 catalog，但排版引擎完全分开。
- `DOCX` 采用单一 Word 母版骨架 + 品牌主题包；不允许按产品复制 Word 模板。
- `DOCX` 的目标是“可编辑且体面”，不是 1:1 还原 `PDF`。
- 若目标 `DOCX` 正被 WPS/Word 占用，导出器允许落旁路文件 `.__staged.docx`，待锁释放后再替换正式文件。