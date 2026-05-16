# Path A — Claude 路径任务简报

## 目标
把 `swiss/output/imt050-wevac-eu-cn.pdf` (15 页) 复刻为视觉 1:1 的 .docx。

## 基线诊断（来自 baseline/）
- 现有 DOCX 转 PDF 后 **24 页**（多 60%），需压缩到 ≤16 页
- TOC 字段空白（LibreOffice headless 不更新 Word 字段）
- 章节标题独占页（应紧接内容）
- 封面：品牌名字号过大、缺 letter-spacing、产品图过大、缺底部免责声明
- 表格/警告框/step 内边距偏大

## 关键资产
- 源数据：`swiss/products/imt050/{product.json, images.json}` + `swiss/products/v23/contents/*.json`
- 源 HTML（puppeteer 渲染 PDF 用）：`swiss/output/imt050-wevac-eu-cn.html`
- 目标 PDF：`swiss/output/imt050-wevac-eu-cn.pdf`
- 现有 DOCX 生成器：`swiss/tools/export-docx.js`（1646 行，已包含 A5 + 中文样式）
- 基线 PNG：`baseline/target_png/page-XX.png`（参考视觉）
- 对比工具：`compare_pdfs.py`（render / docx2pdf / compare / diff）

## 工具链（已验证）
- Node 22 + docx-js 9.6.0（项目 root 已装）
- Python 3.12 + PyMuPDF + python-docx + Pillow
- LibreOffice headless（`C:\Program Files\LibreOffice\program\soffice.exe`）

## 验收标准
1. DOCX → soffice 转 PDF → PyMuPDF 渲染后总页数 ≤16（理想 15）
2. 关键元素位置与目标 PDF 误差 <5%（红色 accent line、章节编号色块、表格边框、警告框）
3. 所有目标 PDF 中可见文本均在 DOCX 中存在且可编辑
4. TOC 渲染为静态表（5 项以上有页码）

## 输出约定
- 工作目录：`path-a-claude/iter-NN/`（NN 从 01 开始）
- 每个 iter 必须含：
  - `docx/imt050-wevac-eu-cn.docx` — 产物
  - `notes.md` — 这次改了什么、为什么、效果
  - `pdf_render/page-XX.png` — DOCX 转 PDF 再渲染的图
  - `side_by_side/side-XX.png` — 与 target 并排
- 改的代码：另存 `path-a-claude/iter-NN/code/` 或单独提交，不要污染 swiss/tools/ 主版本

## 评估命令
```powershell
python "swiss/00_discussions/2026-05-pdf-to-docx-fidelity/compare_pdfs.py" docx2pdf "<your.docx>" "<your_pdf_dir>"
python "<...>/compare_pdfs.py" render "<your_pdf_dir>/your.pdf" "<your_png_dir>"
python "<...>/compare_pdfs.py" compare "<...>/baseline/target_png" "<your_png_dir>" "<your_side_dir>" --label-a TARGET --label-b ITER
```
