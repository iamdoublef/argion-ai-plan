# STATUS

Status: PARTIAL PASS, STOPPED AFTER 8 ITERATIONS

Selected output:
- `selected/output.docx`

Selected builder:
- `build_b2_docx.py`

Verification command:

```powershell
$env:PYTHONUTF8='1'
python .\build_b2_docx.py .\selected\output.docx
python ..\..\score_candidate.py .\selected\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs "..\..\baseline\target_png"
```

Selected result:
- Pages: target `15`, candidate `15`
- Text ratio: `1.00`
- Editable: `100.0%`
- `wt_count`: `457`
- Image bytes: `533482`
- Image hack detected: `false`
- Overall visual diff: `10.09`
- Max page diff: `15.35`

Stop condition:
- Overall visual diff `< 9.0`: NOT MET
- Max page diff `< 14.0`: NOT MET
- Iteration budget: REACHED
- Editable / anti-cheat constraints: MET

Decision:
- Use `selected/output.docx` as the best valid editable output from this run.
- Best improvement was localized warranty-table compaction, reducing p14 max from `17.67` to `15.35`.
- Do not use iter-04/05 warranty table settings; both crossed the LibreOffice table-layout threshold and regressed p14.
