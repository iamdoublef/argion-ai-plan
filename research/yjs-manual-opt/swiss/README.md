# Swiss 说明书生产线

Swiss 当前已经从“手工改模板”切到“结构源 + 统一母版 + 双轨交付”。

## 当前目标

- 自有品牌：统一生成 `HTML + PDF`
- ODM 客户：统一生成 `DOCX + PDF`
- 结构源统一使用 JSON
- 译文审核统一使用 Excel 工作簿
- 审稿统一看 PDF

## 当前产品

- `V23`：真空封口机
- `IMT050`：制冰机

## 当前品牌

- `WEVAC`
- `Vesta`
- `ACT`

## 当前语言 / 地区

- `zh-CN`
- `zh-HK`
- `zh-TW`
- `en`
- `de`
- `it`

其中：

- `HK/TW` 已切到独立 locale catalog
- `ZA` 继续复用 `en`

## 一句话原理

模板只管长相，JSON 只管内容，工作簿只管译文，系统自动批量生成不同品牌、语言、地区的说明书。

## 核心目录

```text
swiss/
├─ DESIGN-STANDARD.md
├─ SOP-new-product.md
├─ README.md
├─ template/
│  ├─ *-master-*.html
│  └─ shared/
│     ├─ base/
│     │  ├─ core-shell.css
│     │  └─ brand-themes.json
│     ├─ cn/
│     ├─ en/
│     ├─ de/
│     └─ it/
├─ products/
│  ├─ v23/
│  │  ├─ product.json
│  │  ├─ images.json
│  │  ├─ content/source/
│  │  └─ i18n/
│  └─ imt050/
│     ├─ product.json
│     ├─ images.json
│     ├─ content/source/
│     └─ i18n/
├─ standards/
├─ tools/
├─ tests/
└─ output/
```

## 正式输入

### 结构源

- `products/<product>/product.json`
- `products/<product>/images.json`
- `products/<product>/content/source/manifest.json`
- `products/<product>/content/source/chapters/*.json`

### 译文源

- `products/<product>/i18n/compiled/<locale>.json`

### 译文编辑面

- `products/<product>/i18n/workbooks/<locale>.xlsx`

## 正式输出

### 自有品牌

- `HTML + PDF`

### ODM

- `DOCX + PDF`

## 品牌风格策略

不是为每个品牌复制一整套模板，而是：

- 共享组件系统
- 品牌主题包

主题包目前在：

- `template/shared/base/brand-themes.json`

控制范围包括：

- 强调色
- 页脚边线
- 封面强调线
- DOCX 基础颜色和字体

## 翻译策略

翻译人员不改 HTML，不改 CSS，不改章节结构 JSON。

正式流程是：

1. 从结构源抽取 `text_id`
2. 导出 `i18n/workbooks/<locale>.xlsx`
3. 翻译 / 审核只改 workbook
4. 编译回 `i18n/compiled/<locale>.json`
5. 渲染 `HTML / PDF / DOCX`

繁体策略：

- `zh-HK`、`zh-TW` 必须是独立译文
- 运行时逐字简转繁已移除，繁体完全依赖独立 locale catalog

## 常用命令

### 构建 HTML

```powershell
cd D:\work\private\yjsplan\research\yjs-manual-opt\swiss
node tools/build-variant.js --product products/imt050 --region cn
node tools/build-variant.js --product products/v23 --all
```

### 导出 PDF

```powershell
node tools/export-pdf.js output/imt050-wevac-eu-cn.html
node tools/export-pdf-batch.js
```

### 导出 DOCX

```powershell
node tools/export-docx.js --product products/imt050 --region hk
node tools/export-docx.js --product products/v23 --all
```

### 导出翻译工作簿

```powershell
node tools/export-translation-workbook.js --product products/imt050 --all
```

### 编译翻译工作簿

```powershell
node tools/compile-translation-workbook.js --product products/imt050 --all
```

### 视觉审计

```powershell
node tools/_audit-visual.js output/imt050-wevac-eu-cn.html
```

## 当前边界

- 结构源继续采用 JSON，不把 Excel 提升为结构主源
- 模型不负责最终排版
- 模型只用于新产品草稿、翻译初稿、本地化和质检建议
- PDF 可作为应急 hotfix 出口，但下一版必须回写正式源头

## 当前判断

这套方案适合：

- 自有品牌稳定批量生产
- 多品牌 / 多语言 / 多地区批量生成
- ODM 客户拿 DOCX 二次风格化

不再适合：

- 继续手改模板正文
- 继续长期直接改 PDF
- 继续把繁体发布建立在逐字转换上

## 2026-03 Word 支线补充规则

- `DOCX` 为独立的 A5 可编辑支线，不再按“PDF 影子稿”导出。
- `HTML/PDF` 与 `DOCX` 共用同一份 JSON 内容源和译文 catalog，但排版引擎完全分开。
- `DOCX` 采用单一 Word 母版骨架 + 品牌主题包；不允许按产品复制 Word 模板。
- `DOCX` 的目标是“可编辑且体面”，不是 1:1 还原 `PDF`。
- 中文 Word 基线固定为：
  - `research/yjs-manual-opt/swiss/template/shared/docx/base-template-cn.docx`
  - `research/yjs-manual-opt/swiss/WORD-BASE-TEMPLATE-CN.md`
- 新产品中文 Word 默认复用这套母版骨架，只微调内容和图片，不重做风格。
- 若目标 `DOCX` 正被 WPS/Word 占用，导出器允许落旁路文件 `.__staged.docx`，待锁释放后再替换正式文件。
