# B2 Custom DOCX Workflow

## Generate

Run from this directory:

```powershell
python .\build_b2_docx.py .\iter-03\output.docx
```

The generator reads:

- `..\..\..\..\output\imt050-wevac-eu-cn.html`
- `..\..\..\..\output\images_imt050\*.png`

It creates an editable Word document using:

- real Word paragraphs for text
- real Word tables for tabular content
- inline image runs for figures
- static editable TOC entries

## Verify With Project Pipeline

```powershell
$work = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity"
$slot = "path-b-codex\b2-custom\iter-03"
$mydocx = "$work\$slot\output.docx"
$mypdf = "$work\$slot\pdf"
$mypng = "$work\$slot\png"
$mysbs = "$work\$slot\side_by_side"

python "$work\compare_pdfs.py" docx2pdf "$mydocx" "$mypdf"
python "$work\compare_pdfs.py" render "$mypdf\output.pdf" "$mypng" --dpi 150
python "$work\compare_pdfs.py" compare "$work\baseline\target_png" "$mypng" "$mysbs" --label-a TARGET --label-b B2
```

On this machine the final `compare` step crashed in Pillow font drawing. If that happens, use the generated `png` folder and run a font-safe side-by-side helper, or remove TrueType label drawing from `compare_pdfs.py`.

## Structural Editability Check

```powershell
@'
from zipfile import ZipFile
from pathlib import Path
from lxml import etree

p = Path("iter-03/output.docx")
with ZipFile(p) as z:
    doc_xml = z.read("word/document.xml")

root = etree.fromstring(doc_xml)
ns = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}

print("paragraphs", len(root.xpath(".//w:p", namespaces=ns)))
print("tables", len(root.xpath(".//w:tbl", namespaces=ns)))
print("inline_drawings", len(root.xpath(".//wp:inline", namespaces=ns)))
print("anchors", len(root.xpath(".//wp:anchor", namespaces=ns)))
print("textboxes", doc_xml.count(b"w:txbxContent"))
'@ | python -
```

Expected final values:

- paragraphs: 345
- tables: 18
- inline drawings: 17
- anchors: 0
- text boxes: 0

