# design-iter-18 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.25 / 13.00`
- Starting score: `9.25 / 13.00` from W23 / design-iter-17
- Net movement: no retained improvement
- Goal: visual `< 9.0` and max `< 12.5`: not reached
- Constraint target: anti-cheat compliant: met

No tested focused change improved both metrics. I restored `build_b2_docx.py`
to the design-iter-17 starter and rebuilt the final `output.docx` from that
baseline so no no-op or regressing tweak is promoted.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.25 | 13.00 | W23 / design-iter-17 reproduced | reference |
| iter-1 | 9.25 | 13.13 | Left/right margin `10.0mm -> 10.2mm`, synced content width | rejected, max regression |
| iter-2 | 9.31 | 13.03 | Left/right margin `10.0mm -> 9.9mm`, synced content width | rejected |
| iter-3 | 9.25 | 13.00 | Bottom margin `10.0mm -> 10.2mm` | rejected, no movement |
| iter-4 | 9.25 | 13.00 | Bottom margin `10.0mm -> 9.8mm` | rejected, no movement |
| iter-5 | 9.30 | 12.88 | Body line spacing `1.16 -> 1.14` | rejected, max improved but overall regressed |
| iter-6 | 9.29 | 13.52 | Body line spacing `1.16 -> 1.18` | rejected |
| iter-7 | 9.29 | 13.00 | Table header text `6.0pt -> 7.0pt` | rejected |
| iter-8 | 9.25 | 13.00 | WARNING title `7.5pt` with Microsoft YaHei font override | rejected, no movement |
| output | 9.25 | 13.00 | Rebuilt from restored starter | final |

## Constraint verification

Final `output.score.json`:

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- editable: `100.0`

Per-page visual diffs:

`[2.93, 3.25, 12.46, 7.09, 10.94, 6.19, 7.81, 7.84, 13.0, 10.14, 12.48, 10.01, 11.7, 12.61, 10.28]`

Hard pages:

- p9: `13.00`
- p14: `12.61`
- p11: `12.48`
- p3: `12.46`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python .\build_b2_docx.py .\output.docx
python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```

