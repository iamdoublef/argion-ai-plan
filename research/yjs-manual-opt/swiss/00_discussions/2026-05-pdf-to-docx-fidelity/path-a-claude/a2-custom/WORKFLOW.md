# Path A2 工作流 — 一键复现

## 依赖
- Python 3.12 + python-docx 1.2.0 + PyMuPDF 1.26.6 + Pillow 9.5.0
- LibreOffice headless：`C:\Program Files\LibreOffice\program\soffice.exe`
- 资料路径：`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\`

## 一键生成 DOCX

```powershell
$base = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-a-claude\a2-custom"
python "$base\build_docx.py" "$base\iter-05\output.docx"
```

## 一键转 PDF + 渲染 PNG + 与目标对比

```powershell
$work = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity"
$slot = "path-a-claude\a2-custom\iter-05"

# 1. DOCX → PDF（LibreOffice headless）
python "$work\compare_pdfs.py" docx2pdf "$work\$slot\output.docx" "$work\$slot\pdf"

# 2. PDF → PNG（120dpi）
python "$work\compare_pdfs.py" render "$work\$slot\pdf\output.pdf" "$work\$slot\png" --dpi 120

# 3. 与目标 PDF 渲染（如果还没渲染过）
$tgt = "$base\path-a-claude\a2-custom\target_png_120"
if (-not (Test-Path $tgt)) {
    python "$work\compare_pdfs.py" render "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" $tgt --dpi 120
}

# 4. 生成单页 side-by-side（绕开 PIL 多页 segfault）
python "$base\sbs_one.py" $tgt "$work\$slot\png" "$work\$slot\sbs" TARGET A2-05

# 5. 数页数
python -c "import fitz; d=fitz.open(r'$work\$slot\pdf\output.pdf'); print('pages:', d.page_count); d.close()"
```

## 验证可编辑性

```powershell
# 检查 docx 是否含文本框 / 锚定形状
python -c @"
import zipfile, re
d = r'D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-a-claude\a2-custom\iter-05\output.docx'
with zipfile.ZipFile(d) as z:
    xml = z.read('word/document.xml').decode('utf-8')
print('w:tbl:', len(re.findall(r'<w:tbl[> ]', xml)))
print('w:p:', len(re.findall(r'<w:p[> ]', xml)))
print('inline pics:', xml.count('<wp:inline'))
print('anchored pics:', xml.count('<wp:anchor'))
print('txbxContent:', xml.count('txbxContent'))
"@
```

期望输出：
```
w:tbl: 29
w:p: 339
inline pics: 16
anchored pics: 0
txbxContent: 0
```

## 文件清单

```
path-a-claude/a2-custom/
├── BRIEF.md                    # 任务简报（输入）
├── build_docx.py               # 主构建脚本（800 行）
├── sbs_one.py                  # 对比工具（绕开 segfault）
├── final-recommendation.md     # 推荐方案
├── WORKFLOW.md                 # 本文件
├── target_png_120/             # 目标 PDF 渲染 PNG（120dpi）
├── iter-01/
│   ├── plan.md / notes.md / output.docx
│   ├── pdf-baseline/baseline.pdf (pandoc 路线测试 baseline)
│   └── png-baseline/, sbs-baseline/
├── iter-02/                   # 16 页中间版本
│   └── plan.md / notes.md / output.docx / pdf / png
├── iter-03/                   # 15 页接近版本
│   └── plan.md / notes.md / output.docx / pdf / png
└── iter-05/                   # ★ 最终版本
    ├── plan.md / notes.md
    ├── output.docx            # 交付文件
    ├── pdf/output.pdf
    ├── png/page-*.png
    └── sbs/side-*.png         # 与目标对比图
```

## 修改指南

要调整某种 block 的样式，按以下表查代码位置：

| 想改的元素 | 函数 | 行号大致 |
|---|---|---|
| 字体 / 大小 | `set_run_fonts` / `parse_inline_md` | 顶部 100 行内 |
| 封面 | `_add_cover` | ~280 |
| TOC | `_add_toc`, `_add_toc_entry` | ~370 |
| 章节标题 | `_add_section_title` | ~430 |
| 段落 | `_render_paragraph` | ~470 |
| 子标题 | `_render_sub_title` | ~480 |
| Bullet 列表 | `_render_bullet_list` | ~500 |
| 警告/注意/提示框 | `_render_box` | ~520 |
| 步骤序号 | `_render_step_flow` | ~600 |
| 图片 | `_render_figure` / `_add_image_paragraph` / `_add_image_row` | ~700 |
| Specs 表 | `_render_specs_table` | ~830 |
| Parts 表 | `_render_parts_table` | ~880 |
| Buttons 表 | `_render_buttons_table` | ~930 |
| Brand / Manufacturer 表 | `_render_brand_info_table` / `_render_manufacturer_info_table` | ~980 |
| 保修卡 | `_render_warranty_card` | ~1040 |
| 故障排除表（inline_table） | `_render_inline_table` | ~1000 |

要换 brand / market / locale，搜索 `wevac` / `"eu"` / `"zh-CN"` 替换。
