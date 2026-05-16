# STATUS

Status: PARTIAL PASS, STOPPED AFTER 10 ITERATIONS

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
- Overall visual diff: `9.84`
- Max page diff: `14.60`
- Per-page diffs: `[3.62, 3.51, 13.46, 7.79, 11.76, 7.35, 8.13, 8.09, 13.37, 9.89, 12.39, 10.20, 13.09, 14.60, 10.36]`

Goal result:
- Overall visual diff `< 9.0`: NOT MET
- Max page diff `< 13.0`: NOT MET
- Anti-cheat/editability constraints: MET

Iteration log:

| Iter | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt W13 copied builder unchanged | 10.09 | 15.35 | Baseline |
| iter-01 | Lowered footer distance from `5mm` to `3.5mm` | 10.05 | 15.31 | Kept |
| iter-02 | Widened bullet-to-text gap from 2 to 3 spaces | 10.03 | 15.30 | Kept |
| iter-03 | Widened bullet-to-text gap from 3 to 4 spaces | 10.02 | 15.31 | Kept for lower overall |
| iter-04 | Increased `BODY_PT` from `7.0` to `7.2` | 10.02 | 15.31 | Neutral, kept |
| iter-05 | Expanded compact-warranty table padding/row height to `52/248` | 9.97 | 14.60 | Kept, biggest max improvement |
| iter-06 | Replaced table expansion with post-table spacer | 10.38 | 20.76 | Reverted |
| iter-07 | Added extra `space_before` for sub-titles after bullet lists | 9.85 | 14.60 | Kept |
| iter-08 | Increased compact-warranty table padding/row height to `53/250` | 9.92 | 15.72 | Reverted |
| iter-09 | Darkened compact-warranty borders to `#CCCCCC` | 9.86 | 14.65 | Reverted |
| iter-10 | Shifted non-note alert-box start padding from `110` to `176` twips | 9.84 | 14.60 | Kept, selected |

Retained builder changes versus W13:
- Footer distance lowered to `3.5mm`.
- Red bullet spacing widened to four spaces.
- `BODY_PT` set to `7.2`.
- Compact-warranty non-compact tables use `pad_v=52` and `row_height=248`.
- Sub-titles immediately after bullet lists use `before=8`.
- Non-note alert boxes use `pad_start=176`.

Remaining blockers:
- Page 14 remains the max page at `14.60`; compact-warranty table layout appears to have a LibreOffice threshold between `248` and `250` row height.
- Pages 3, 9, and 13 remain just above the target max threshold: `13.46`, `13.37`, `13.09`.
