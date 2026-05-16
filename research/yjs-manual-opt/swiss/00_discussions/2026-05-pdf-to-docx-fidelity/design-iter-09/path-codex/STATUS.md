# STATUS

Status: IMPROVED, GOAL NOT MET

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
- Overall visual diff: `9.71`
- Max page diff: `13.46`
- Per-page diffs: `[3.62, 3.51, 13.46, 7.79, 11.76, 7.35, 8.13, 8.09, 13.36, 9.89, 12.39, 10.22, 12.70, 12.99, 10.36]`

Goal result:
- Overall visual diff `< 8.5`: NOT MET
- Max page diff `< 13.0`: NOT MET
- Anti-cheat/editability constraints: MET

Worst-page result:
- p3 target `<11`: `13.46` NOT MET
- p9 target `<11`: `13.36` NOT MET
- p11 target `<11`: `12.39` NOT MET
- p13 target `<11`: `12.70` NOT MET, improved from `13.09`
- p14 target `<12`: `12.99` NOT MET, improved from `14.60`

Iteration log:

| Iter | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt iter-08 selected builder unchanged | 9.84 | 14.60 | Baseline |
| iter-01 | Added non-compact warning-box bullet `line_spacing=1.20` | 9.84 | 14.60 | Neutral, kept |
| iter-02 | Increased step badge-to-text gap by one space | 9.84 | 14.60 | Kept; p9 `13.37 -> 13.36` |
| iter-03 | Scoped troubleshooting table to full thin cell borders | 9.84 | 14.60 | Neutral, kept |
| iter-04 | Added scoped pre-gap before WEEE / R600a note | 9.82 | 14.60 | Kept; p13 `13.09 -> 12.70` |
| iter-05 | Reduced warranty separator `space_before` to `8pt` | 9.82 | 14.60 | Neutral, kept |
| iter-06 | Reduced warranty separator `space_before` to `0pt` | 9.82 | 14.60 | Neutral, kept |
| iter-07 | Reduced compact-warranty non-card table row height `248 -> 246` | 9.78 | 14.05 | Kept |
| iter-08 | Reduced compact-warranty non-card table row height `246 -> 244` | 9.74 | 13.46 | Kept; p14 `13.40` |
| iter-09 | Reduced compact-warranty non-card table row height `244 -> 242` | 9.71 | 13.46 | Selected; p14 `12.99` |
| iter-10 | Applied `line_spacing=1.20` to compact-safety warning bullets | 9.90 | 16.38 | Reverted; p3 regressed |

Retained builder changes versus iter-08 selected:
- Non-compact warning-box bullets accept `line_spacing=1.20` without affecting compact-safety pages.
- Step text gap after the numbered badge widened by one space.
- Troubleshooting page table uses full thin cell borders.
- WEEE / R600a note receives a scoped pre-gap.
- Warranty separator image uses `space_before=0`.
- Compact-warranty non-card tables use row height `242`.

Render note:
- Project scoring render through LibreOffice produced the expected 15 pages and is the acceptance basis.
- Documents artifact-tool render was also attempted at `selected/artifact_render`; it produced 26 pages with rotated/split content, so it is not reliable for this DOCX in this workspace.

Remaining blockers:
- p3 is now the max page at `13.46`. Applying the requested `1.20` spacing to compact-safety warning bullets caused a hard regression to `16.38`.
- p9 remains `13.36`; the step badge gap only provided a `0.01` improvement.
- p11 remained score-neutral after border refinement.
- The requested `<8.5` overall and `<13.0` max were not reached without violating the regression rule.
