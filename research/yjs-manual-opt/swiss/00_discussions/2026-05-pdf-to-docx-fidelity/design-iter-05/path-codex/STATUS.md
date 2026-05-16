# STATUS

Status: PARTIAL PASS, STOPPED AFTER EDITABLE-ONLY ITERATION BUDGET

Selected output:
- `iter-04/output.docx`

Selected builder:
- `build_b2_docx.py`

Verification command:

```powershell
$env:PYTHONUTF8='1'
python .\build_b2_docx.py .\iter-04\output.docx
python ..\..\score_candidate.py .\iter-04\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs "..\..\baseline\target_png"
```

Selected result:
- Pages: target `15`, candidate `15`
- Text ratio: `1.00`
- Editable: `100.0%`
- `wt_count`: `457`
- Image bytes: `533482`
- Image hack detected: `false`
- Overall visual diff: `10.31`
- Max page diff: `17.67`

Stop condition:
- Overall visual diff `< 9.0`: NOT MET
- Max page diff `< 14.0`: NOT MET
- Editable / anti-cheat constraints: MET

Decision:
- Use `iter-04/output.docx` as the best valid editable output from this run.
- Do not use `iter-06` or any page-rendered/image-rescue approach.
