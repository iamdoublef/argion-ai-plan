# 共享任务简报 — PDF→可编辑 DOCX 还原

> 此文件被四个并行子任务（A1/A2/B1/B2）共同引用。

## 客户的真实目标（关键）

**客户要可编辑的 Word 文件用于局部修改**。PDF 只是视觉参考。
- ✗ 不可接受：把 PDF 文字塞进文本框/图片层（pdf2docx 默认输出）— 后续无法编辑
- ✓ 必须满足：所有文本以**普通 Word 段落/表格单元格**形式存在，可双击编辑
- ✓ 必须满足：图片以**真实嵌入图**形式存在，可替换、可缩放
- ✓ 视觉接近度："看起来像同一份说明书"，每页元素位置、色彩、章节结构对得上

## 目标 PDF
- 路径：`research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf`
- 页数：15
- 尺寸：A5（148×210mm）竖版
- 内容：威富可 IMT050 制冰机中文说明书，含封面、目录、10 章

## 输入资产
- 源 JSON：`swiss/products/imt050/{product.json, images.json}` + `swiss/products/v23/contents/*.json`
- 源 HTML（用于 PDF 渲染）：`swiss/output/imt050-wevac-eu-cn.html`（46KB）
- 现有 DOCX（待优化）：`swiss/output/imt050-wevac-eu-cn.docx`（24 页问题样本）
- 现有 DOCX 生成器：`swiss/tools/export-docx.js`
- 基线对比图：`swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/`
- 视觉诊断结论：`swiss/00_discussions/2026-05-pdf-to-docx-fidelity/log.md`

## 基线已识别问题（已经诊断完，不要重复诊断）
| 严重度 | 问题 | 修复方向 |
|---|---|---|
| P0 | 现 DOCX 24 页（应 ≤16） | 紧凑 spacing；移除多余 pageBreakBefore |
| P0 | TOC 空白 | 自渲染静态 TOC 表 |
| P0 | 章节标题独占空页 | 移除强制分页 |
| P1 | 封面：字号、字距、产品图、缺免责声明 | 减小字号、加 letter-spacing、缩图、补 disclaimer |
| P1 | 表格/警告框/step 内边距偏大 | 全面紧凑化 |

## 工具链（已验证）
- LibreOffice：`C:\Program Files\LibreOffice\program\soffice.exe`
- Node 22 + docx-js 9.6.0（项目 root `D:\work\private\yjsplan\` 已 npm install）
- Python 3.12 + PyMuPDF 1.26.6 + python-docx 1.2.0 + Pillow 9.5.0
- pandoc 3.9.0.2（路径见 PATH）
- docx skill 脚本：`C:\Users\iamdo\.claude\skills\docx\scripts\`
  - `office\unpack.py` — DOCX→XML 目录
  - `office\pack.py` — XML 目录→DOCX
  - `office\soffice.py` — 调 LibreOffice
  - `office\validate.py` — OOXML 校验
- 对比工具：`swiss/00_discussions/2026-05-pdf-to-docx-fidelity/compare_pdfs.py`
  - `render <pdf> <out_dir>` — PDF→PNG
  - `docx2pdf <docx> <out_dir>` — DOCX→PDF（通过 soffice）
  - `compare <a_dir> <b_dir> <out_dir>` — 并排对比图
  - `diff <a_dir> <b_dir> <out_dir>` — 像素差异热图

## 验收标准（必须全部达成才能停止）
1. **可编辑性**：用 Word 打开 DOCX，能选中任意文字段落直接编辑（不是文本框）
2. **页数**：DOCX 转 PDF 后 ≤16 页
3. **视觉相似度**：逐页 side-by-side 中，章节编号色块、accent 红线、表格、警告框位置误差 <5%
4. **文本完整**：目标 PDF 中所有可见文本都在 DOCX 中

## 输出约定
每个子任务把产物放在自己的目录下：
```
path-{a-claude|b-codex}/{slot}/iter-NN/
├── output.docx         # 这次产物
├── notes.md            # 这次改了什么、为什么、效果如何
├── pdf/                # DOCX→PDF 中间结果
├── png/                # PDF→PNG 中间结果
└── side_by_side/       # 与目标对比的并排图
```
其中 `{slot}`：
- `a1-docx-skill`（Claude path A1）
- `a2-custom`（Claude path A2）
- `b1-docx-skill`（Codex path B1）
- `b2-custom`（Codex path B2）

## 评估命令（粘贴可用）
```powershell
$work = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity"
$slot = "path-a-claude\a1-docx-skill\iter-01"  # 改成你自己的 slot
$mydocx = "$work\$slot\output.docx"
$mypdf = "$work\$slot\pdf"
$mypng = "$work\$slot\png"
$mysbs = "$work\$slot\side_by_side"
python "$work\compare_pdfs.py" docx2pdf "$mydocx" "$mypdf"
python "$work\compare_pdfs.py" render "$mypdf\output.pdf" "$mypng" --dpi 150
python "$work\compare_pdfs.py" compare "$work\baseline\target_png" "$mypng" "$mysbs" --label-a TARGET --label-b ITER
```
然后人工/Agent 检查 side_by_side 图片，记录差异，开下一个 iter-NN+1。

## 迭代要求
- **不停止**直到达成全部验收标准（除非用尽合理方法）
- 每个 iter 必须有具体的"上一轮改了什么"和"这一轮要改什么"
- 失败的 iter 也保留，方便回溯
- 共享心得：发现可用技巧立刻更新本 BRIEF 的"已知技巧"附录

## 已知技巧（共享发现，持续追加）

- LibreOffice 命令行 TOC 刷新：`soffice --headless --convert-to docx --outdir <dir> <doc.docx>`  本身**不刷新** TOC 字段；要用宏：
  ```
  --headless --norestore "macro:///Standard.Module1.RefreshTOC" 
  ```
  或直接放弃 docx-js 的 TOC field，手工渲染表格代替。
- docx-js `Paragraph.indent` 中 left 是 DXA，hanging 也是 DXA。
- Pillow 9.5.0 + LANCZOS 在多次循环下偶发 segfault，需显式 `close()` + `gc.collect()`。
- **docx skill validate.py 在 Windows 修复**：默认 gbk 编码会爆 `illegal multibyte sequence`，必须设 `PYTHONUTF8=1` 和 `PYTHONIOENCODING=utf-8`。命令模板：
  ```bash
  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python "C:/Users/iamdo/.claude/skills/docx/scripts/office/validate.py" "<docx>"
  ```
- **docx skill schemas 已下载补全**：`C:/Users/iamdo/.claude/skills/docx/scripts/office/schemas/` 含 39 个 xsd（ecma/ISO-IEC29500/microsoft/mce）。`pack.py` 和 `validate.py` 现在可正常用。
- **pack.py 跳过校验**：`python pack.py unpacked/ out.docx --original orig.docx --validate false` 可跳过 schema 校验（不推荐，但 debug 时方便）。

## PDF 实测样式（来自 baseline/pdf_probe.md）

**字体**（重要发现）：
- 中文主字体：**MicrosoftYaHei**（微软雅黑）— 不是宋体！238 spans 主力
- 中文加粗：MicrosoftYaHei-Bold
- 西文：ArialMT / Arial-Black / Arial-BoldMT
- 等宽：CourierNewPSMT（Model 号用）
- 兜底：NSimSun

**字号（pt）**：
- 正文：**7.5pt** 中文 / 6.7-7.0pt 西文 → DOCX size = **15** half-pt（现 export-docx.js 用 22 偏大）
- 副标题：约 13.5pt → DOCX size 约 **27**
- 章节大标题（如"制冰机"封面）：**18pt** → DOCX size **36**
- 小标签（Model/disclaimer/页脚）：5.2-6.0pt → DOCX size **10-12**

**配色**（精确取色）：
- 主黑：`#1A1A1A`（不是纯 #000000）
- Accent 红：`#E63946`（红色 line / 章节编号）
- 次要文字灰：`#8E8E93`
- 其他黑级：`#222222`、`#444444`

**页面**：A5，148.2 × 209.9 mm（420 × 595 pt）

**14 张图片**，主要分布在第 1、3、6-10 页

**现有 export-docx.js 偏差**：
- `cjkFont: '宋体'` → 应改 `'Microsoft YaHei'`
- `DOCX_PROFILE.text.bodySize: 22` → 应改 `15`（7.5pt × 2）
- 颜色 `accent: 'E63946'` 正确，`primary: '1A1A1A'` 正确
