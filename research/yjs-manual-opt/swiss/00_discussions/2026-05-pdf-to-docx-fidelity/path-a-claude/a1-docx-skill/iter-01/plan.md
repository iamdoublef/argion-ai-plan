# iter-01 plan — 紧凑化 + 静态 TOC + 修封面

## 起点观察（来自 baseline）
- 现有 `swiss/output/imt050-wevac-eu-cn.docx` 转 PDF = 24 页（目标 15）
- 封面：字距过大、底部 disclaimer 是英文（CN locale 应该是中文）
- 目录页几乎空白（TOC field 未刷新）
- 章节标题独占页（force page break + spacing 撑高）
- 整体行距偏松，单元格 padding 偏大

## 本轮目标
让 docx2pdf 后 ≤18 页（先收敛页数；具体到 16/15 留给后续 iter 进一步紧凑）。视觉相似度先把封面、目录、章节首页对上。

## 改动清单（写在 `code/export-docx-v2.js`）
1. **静态 TOC**：用 docx-js 自渲染一个两列表格（章节号+标题列、页码列），不再用 `new TableOfContents()`。先放占位页码 ("--")，让 LibreOffice 不需要刷新字段。
2. **章节首页移除强制分页**：`renderChapterHeading` 不再触发 pageBreakBefore；只在 page section 内部用 `pageBreakBefore: true` 标记的 page 才换页。
3. **`shouldPageBreakBeforePage` 收紧**：去掉 `pageKey.includes('warranty')` 触发（warranty 卡现在和保修页常常落同一页就行）；只在 `force_page_break=true` 或 `(续)/continued` 时分页。
4. **spacing 全局紧凑**：
   - 默认 paragraph `line: 280`（从 320 降）
   - `Heading1` spacing before 200 / after 80
   - `Heading2` spacing before 120 / after 40
   - `Heading3` spacing before 100 / after 30
   - `CELL_MARGINS` 改为 `{top:40, bottom:40, left:80, right:80}`
   - `sectionDivider` `after: 100`
5. **封面**：
   - `coverBrandSize`: 36 → 26
   - `characterSpacing`: 80 → 0（PDF 里"威富可"没有大字距）
   - `cover.width`: 360 → 260（PDF 里产品图小，居中偏左对齐）
   - 中文 locale 的 disclaimer 强制走中文路径（确认 lang 判断没问题）
   - 减少 cover 各段间距
6. **页眉/页脚**：保留现有右对齐 tab stop 实现。页眉右上字号略小（从 17 降到 14）避免溢出。

## 中文字体保留
- `cjkFont: 宋体`、`titleCjkFont: 黑体` 不动（LibreOffice 字体回退测试过基本能渲染）。

## 评估方式
1. `node code/export-docx-v2.js --region cn --product ../../../../../products/imt050`
2. 把生成的 docx 拷到 `iter-01/output.docx`
3. 跑 docx2pdf → render → compare
4. 阅读 side-XX，写 notes.md
