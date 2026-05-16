# STATUS

Status: COMPLETE

Final candidate:
- `iter-02/output.docx`

Verification:
- Command: `PYTHONUTF8=1 python ..\..\score_candidate.py iter-02\output.docx --target D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf --baseline-pngs D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\baseline\target_png`
- Pages: target 15 vs candidate 15
- Text ratio: 8.53
- Editable: 100.0%
- Overall visual diff: 7.29
- Max page diff: 12.87
- PASS overall: true

Stop condition:
- Visual diff < 9.0: MET
- Max page diff < 14.0: MET

Files:
- Final builder: `build_b2_docx.py`
- Editable iter-01 builder backup: `build_b2_docx_editable_iter01.py`
- Final output: `iter-02/output.docx`
- Final score: `iter-02/output.score.json`
