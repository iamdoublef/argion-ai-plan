# WORKFLOW

Run from repo root unless noted.

```powershell
cd D:\work\private\yjsplan
```

Generate the editable DOCX:

```powershell
node research\yjs-manual-opt\swiss\tools\export-docx.js `
  --product D:\work\private\yjsplan\research\yjs-manual-opt\swiss\products\imt050 `
  --region cn `
  --brand wevac
```

Stage into this slot:

```powershell
$slot = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-b-codex\b1-docx-skill"
$iter = "$slot\iter-03"
Copy-Item "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.docx" "$iter\output.docx" -Force
```

Run the required Anthropic DOCX skill scripts:

```powershell
python "C:\Users\iamdo\.claude\skills\docx\scripts\office\unpack.py" "$iter\output.docx" "$iter\unpacked"
python "C:\Users\iamdo\.claude\skills\docx\scripts\office\pack.py" "$iter\unpacked" "$iter\output.docx" --original "$iter\output.docx" --validate false
$env:PYTHONUTF8 = "1"
python "C:\Users\iamdo\.claude\skills\docx\scripts\office\validate.py" "$iter\output.docx"
```

Render and compare:

```powershell
$work = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity"
python "$work\compare_pdfs.py" docx2pdf "$iter\output.docx" "$iter\pdf"
python "$work\compare_pdfs.py" render "$iter\pdf\output.pdf" "$iter\png" --dpi 150
python "$work\compare_pdfs.py" compare "$work\baseline\target_png" "$iter\png" "$iter\side_by_side" --label-a TARGET --label-b B1-ITER-03
```

Editable-structure smoke check:

```powershell
rg -n "<wp:txbx|<w:txbxContent|<v:textbox" "$iter\unpacked\word\document.xml"
rg -o "<w:t" "$iter\unpacked\word\document.xml" | Measure-Object
rg -o "<w:tbl" "$iter\unpacked\word\document.xml" | Measure-Object
rg -o "<w:drawing" "$iter\unpacked\word\document.xml" | Measure-Object
```

Expected result:
- `validate.py`: `All validations PASSED!`
- DOCX->PDF: 15 pages rendered.
- Compare: 15 side-by-side images written.
- Text-box grep: no matches.
