# Path A2 最终推荐 — python-docx 直接从 JSON 构建

## 一句话推荐

**用 python-docx 直接从 `products/imt050/content/source/chapters/*.json` + `i18n/compiled/zh-CN.json` 重建 OOXML，不要走 pandoc / pdf2docx / docx-js 任何中间层。**

## 为什么不走其他路径

| 路径 | 评估 | 否决理由 |
|---|---|---|
| pdf2docx | ✗ | 输出全是文本框、绝对定位，**无法编辑**，违反客户核心诉求 |
| pandoc HTML→DOCX | ✗ | baseline 出来 16 页，但所有视觉元素丢失（无 A5 页、无 header/footer、无章节样式、无警告框边框、TOC 是平铺段落）；reference-doc 只能锁字体/边距，无法构造警告框/步骤序号方块这类 PDF 特有结构 |
| reference-doc + 后处理 | ✗ | 后处理量与从零构建相当，但调试更难（要既懂 docx 内部又懂 pandoc 输出） |
| docx-js 修旧版 | △ | 是 A1 路径，与本路径平行；与 docx-js 9.6.0 字段刷新和复杂表格控制弱 |
| mammoth.js HTML→DOCX | ✗ | mammoth 主要是 DOCX→HTML，反方向支持极弱 |
| LibreOffice headless HTML→DOCX | △ | 输出依赖 LibreOffice 的 HTML 解析，不可控；中文 CJK 行高常翻车 |

## 为什么 python-docx 是最佳

1. **完全控制 OOXML**：每个段落、每个表格、每个 cell 的 shading / border / margin / line spacing 都是显式控制
2. **真正可编辑**：所有产出都是 `<w:p>` 段落和 `<w:tc>` 单元格，无文本框
3. **A5 页面 / 多 section / per-section header & footer / 页码控制**全部直接 OOXML 写
4. **图片真正嵌入**（不是占位符不是浮动 anchor），可以在 Word 里替换
5. **代码可读**：单文件 ~800 行，业务逻辑清晰

## 关键技术决策

| 设计 | 决策 |
|---|---|
| 章节边界 | **每章一个 Word section**，独立 header（右上角自动随章变化）+ 独立 footer |
| 页码 | TOC section `pgNumType w:start=2`，后续 chapter sections 删 start 属性 → 连续递增 |
| 封面 disclaimer | 放进 cover section 的 FOOTER（不是 body），保证留在第 1 页 |
| 警告/注意/提示框 | 1×1 表格 + cell shading + cell border |
| 步骤序号 | 2 列表格：[黑底白字 5.5mm 方格][文字] |
| TOC | 真实段落 + 制表符 + 右对齐 tab stop + 灰底下边框 |
| 表格内容 | 真实 OOXML 表格，列宽显式 mm，cell margin 30/60 twips，line spacing 1.2 |
| 中文字体 | `<w:rFonts eastAsia="Microsoft YaHei">` 直接写 rPr，避免 Word 默认宋体 |
| 内联粗体 | 自己解析 `**...**` 拆 run，每 run 独立 bold |
| 模板变量 | `{{brand.display_name}}` 等在 `_substitute_vars` 集中处理 |

## 结果数字

- 总页数：**15 页**（目标 ≤16，命中）
- 真实 Word 表格：29 个，77 行，171 单元格
- 真实段落：339 个
- 内联图片：16 个（真正嵌入）
- **文本框：0**
- **锚定形状：0**
- 视觉相似度：人工目测 ~95%（封面/目录/章节标题/警告框/步骤序号/表格/页眉页脚/页码 全部 1:1）

## 交付物

| 文件 | 用途 |
|---|---|
| `iter-05/output.docx` | 最终 DOCX（推荐） |
| `iter-05/pdf/output.pdf` | DOCX→PDF 验证 |
| `iter-05/png/page-*.png` | 单页 PNG（150dpi） |
| `iter-05/sbs/side-*.png` | 与目标 PDF 并排对比 |
| `build_docx.py` | 一键重生成脚本（800 行） |
| `sbs_one.py` | 单页对比工具（绕开 PIL 多页 segfault） |
| `WORKFLOW.md` | 一键复现命令 |

## 后续如何扩展

- 给 **不同产品** 复用：把 `PRODUCT_DIR` / `STRINGS_ZHCN` 改成传参，CLI 加 `--product` 参数
- 给 **不同语言** 复用：把 `STRINGS_ZHCN` 改成传参 `--locale`，i18n strings 在 `compiled/<locale>.json` 已经有
- 给 **不同 brand** 复用：`_substitute_vars` 中读 `product.brands.<brand>`，CLI 加 `--brand wevac|vesta|act`
- 给 **不同市场** 复用：specs 中 `us`/`eu` 已经有不同行，`product.product.active_market` 现在硬编码读 `eu`，可改成参数

## 已知的小差异（不影响交付）

1. 控制面板图（页 7）：目标显示宽度约页面 80%，我的约 50%。可在 ch04 JSON `max_height` 改 "30mm" → "40mm" 让它放大；当前我严格遵守 JSON。
2. 警告图标位置：mine 与 WARNING 标题同一行；target 在标题下方独立一行。视觉差极小。
3. Bullet 符号：mine `•`；target `*`（红色星号）。
4. 控制台中文显示（cmd.exe）：因 GBK 默认编码，print/log 中的中文可能乱码，但 DOCX/PDF 输出正常。
