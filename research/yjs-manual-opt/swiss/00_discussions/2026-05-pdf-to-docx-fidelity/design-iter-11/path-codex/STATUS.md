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
- Drawings count: `16`
- Image bytes: `530887`
- Image hack detected: `false`
- Overall visual diff: `9.67`
- Max page diff: `13.46`
- Per-page diffs: `[3.62, 3.51, 13.46, 7.79, 11.76, 7.35, 8.13, 8.09, 13.36, 9.89, 12.35, 10.22, 12.30, 12.93, 10.36]`

Goal result:
- Overall visual diff `< 8`: NOT MET
- Max page diff `< 11`: NOT MET
- Anti-cheat/editability constraints: MET

Iteration log:

| Iter | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt iter-10 starter unchanged | 9.68 | 13.46 | Baseline |
| iter-01 | Non-compact warning bullet line spacing `1.20 -> 1.10` | 9.68 | 13.46 | Neutral, kept |
| iter-02 | Added white border around black step number badge | 9.69 | 13.46 | Reverted |
| iter-03 | Normal bullet line spacing `1.13 -> 1.10` | 9.83 | 13.61 | Reverted |
| iter-04 | Removed warranty separator/scissor image | 9.67 | 13.46 | Kept; p14 `12.99 -> 12.93` |
| iter-05 | Reduced bullet symbol text gap from 4 spaces to 2 spaces | 9.72 | 13.62 | Reverted |
| iter-06 | Applied `1.10` line spacing to compact-safety warning bullets | 9.85 | 16.09 | Reverted |
| iter-07 | Removed black fill from step number badge | 9.71 | 13.57 | Reverted |
| iter-08 | Preserved compact-warranty paragraph inline bold/br | 9.68 | 13.46 | Reverted |

Retained builder changes versus iter-10 starter:
- Non-compact warning-box list line spacing is `1.10`.
- Warranty separator/scissor image is omitted.

Notes:
- The only measurable improvement was p14 from `12.99` to `12.93`; overall moved from `9.68` to `9.67`.
- p3 and p9 remain the hard blockers at `13.46` and `13.36`.
- Attempts to alter compact p3 spacing, ordinary bullet spacing, and step badge rendering all regressed max-page score.
