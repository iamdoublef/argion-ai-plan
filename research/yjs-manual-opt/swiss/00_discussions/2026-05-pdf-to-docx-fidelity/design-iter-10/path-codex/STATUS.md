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
python ..\..\score_candidate.py .\selected\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```

Selected result:
- Pages: target `15`, candidate `15`
- Text ratio: `1.00`
- Editable: `100.0%`
- `wt_count`: `456`
- Image bytes: `533482`
- Image hack detected: `false`
- Overall visual diff: `9.68`
- Max page diff: `13.46`
- Per-page diffs: `[3.62, 3.51, 13.46, 7.79, 11.76, 7.35, 8.13, 8.09, 13.36, 9.89, 12.35, 10.22, 12.30, 12.99, 10.36]`

Goal result:
- Overall visual diff `< 8.5`: NOT MET
- Max page diff `< 12.0`: NOT MET
- Anti-cheat/editability constraints: MET

Worst-page result:
- p3 target `<11`: `13.46` NOT MET
- p9 target `<10`: `13.36` NOT MET
- p11 target `<10`: `12.35` NOT MET, improved from `12.39`
- p13 target `<10`: `12.30` NOT MET, improved from `12.70`
- p14 target `<10`: `12.99` NOT MET

Iteration log:

| Iter | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt W15 starter unchanged | 9.71 | 13.46 | Baseline |
| iter-01 | Reduced compact-safety real alert icon size | 9.71 | 13.46 | Neutral, kept |
| iter-02 | Increased compact-safety warning bullet size | 9.91 | 16.66 | Reverted |
| iter-03 | Removed generated synthetic alert glyphs from boxes without real icons | 9.71 | 13.46 | Kept; p11 `12.39 -> 12.35` |
| iter-04 | Tuned WEEE / R600a pre-gap `7pt -> 5pt` | 9.69 | 13.46 | Kept; p13 `12.70 -> 12.42` |
| iter-05 | Tuned WEEE / R600a pre-gap `5pt -> 4pt` | 9.68 | 13.46 | Kept; p13 `12.42 -> 12.34` |
| iter-06 | Tuned WEEE / R600a pre-gap `4pt -> 3pt` | 9.68 | 13.46 | Kept; p13 `12.34 -> 12.30` |
| iter-07 | Preserved inline bold/br in body paragraphs | 9.68 | 13.46 | Reverted; p14 `12.99 -> 13.05` |
| iter-08 | Increased compact-safety alert top padding | 9.67 | 13.79 | Reverted; max regressed |
| iter-09 | Increased global body type size | 10.21 | 15.13 | Reverted |
| iter-10 | Increased troubleshooting table compact vertical padding | 9.68 | 13.46 | Neutral, kept |

Retained builder changes versus W15:
- Compact-safety real alert icons use a slightly smaller forced size.
- Synthetic triangle/info glyphs are no longer generated for alert boxes that do not have real icons.
- WEEE / R600a note pre-gap is tuned to `3pt`.
- Troubleshooting compact table vertical padding is scoped to `42` twips.

Notes:
- The new goal `<8.5 overall` and `<12.0 max` was not reachable within the required 10 focused iterations and regression guard.
- The largest blocker remains p3 at `13.46`; text-size and spacing attempts caused hard regressions.
- p9 stayed at `13.36`; body scale changes regressed the document.
- p14 stayed at `12.99`; preserving inline paragraph boldness looked closer semantically but worsened the visual score.
