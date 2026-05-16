# STATUS

Status: PASS

Selected output: `iter-02/output.docx`

Verification command:

```powershell
$env:PYTHONUTF8='1'; python .\build_b2_docx.py .\iter-02\output.docx; python ..\..\score_candidate.py .\iter-02\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```

Verification result:

- Pages: target `15`, candidate `15`
- Text ratio: `1.0`
- Editable: `100.0%`
- Overall visual diff: `10.74`
- Max page diff: `17.74`
- Stop gate: met

No Python command failed. Work stopped at iter-02 because the explicit stop condition was met.
