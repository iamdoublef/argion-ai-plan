# Path A1 一键复现工作流

## 前置

- Windows + LibreOffice 在 `C:\Program Files\LibreOffice\program\soffice.exe`
- Node 22 + docx-js 9.6.0（`D:\work\private\yjsplan\node_modules` 已 install）
- Python 3.12 + PyMuPDF + Pillow + python-docx + sharp（项目已安装）

## 生成最终 DOCX（iter-03）

```powershell
$root = "D:\work\private\yjsplan"
$slot = "$root\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-a-claude\a1-docx-skill"
$iter = "$slot\iter-03"

# 1. 生成 DOCX (output 自动写到 iter-03/output.docx)
Set-Location $root
node "$iter\code\export-docx-v2.js" --region cn --product "research\yjs-manual-opt\swiss\products\imt050"

# 2. 转 PDF + 渲染 PNG
Set-Location "$root\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity"
python compare_pdfs.py docx2pdf "$iter\output.docx" "$iter\pdf"
python compare_pdfs.py render "$iter\pdf\output.pdf" "$iter\png" --dpi 150

# 3. 与目标 PDF 并排对比（可选）
python compare_pdfs.py compare "baseline\target_png" "$iter\png" "$iter\side_by_side" --label-a TARGET --label-b A1-03

# 4. 验证 DOCX 结构（可选）
python "C:\Users\iamdo\.claude\skills\docx\scripts\office\unpack.py" "$iter\output.docx" "$iter\unpacked-out"
# 检查 0 个 textbox（应输出 0）：
Select-String -Pattern "wp:txbx|w:txbxContent" -Path "$iter\unpacked-out\word\document.xml" -SimpleMatch | Measure-Object | Select-Object -ExpandProperty Count
```

## 期望结果

- `iter-03\output.docx` ≈ 558 KB
- `iter-03\pdf\output.pdf` 15 页
- `iter-03\png\` 15 张 PNG
- 0 个 textbox (`wp:txbx`)
- 319 个 `<w:t>` 普通文本节点

## 如果验收失败

1. 检查 LibreOffice 版本（建议 ≥ 7.0）
2. 检查 docx-js 版本：`node -e "console.log(require('docx/package.json').version)"` 应 9.6.0
3. 看错误日志：`$iter\pdf\` 目录下应有 output.pdf；若无，看 stderr
4. PNG 全空白：可能 LibreOffice 字体回退失败 — 安装思源黑体/Noto Sans CJK

## 修改源数据后重生成

输入数据来自 `swiss/products/imt050/`：
- `product.json` — 产品元数据
- `content/source/chapters/*.json` — 章节内容（10 个）
- `images.json` — 图片清单
- `i18n/compiled/zh-CN.json` — 中文译文（如有 placeholder）

修改任一文件后直接重跑步骤 1-2。

**注意**：若新增/删除章节或大幅改变章节长度，需要：
1. 先生成一次看实际 PDF 页码分布
2. 更新 `iter-03/code/export-docx-v2.js` 中 `PDF_PAGE_MAP` 静态映射
3. 再生成一次让目录页码与正文对齐

## 其他语言（EN/DE/IT 等）

```powershell
node "$iter\code\export-docx-v2.js" --region gb --brand wevac --product "research\yjs-manual-opt\swiss\products\imt050"
node "$iter\code\export-docx-v2.js" --region de --product "research\yjs-manual-opt\swiss\products\imt050"
```

- 字体会自动 fallback 到 `latinFont`(Arial)
- 中文专用样式（如"使用产品前请仔细阅读…"）会自动切到英文版

但 **TOC 页码映射** 是写死的中文版页数。其他语言需要重新校准。
