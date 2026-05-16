# design-iter-17 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.25 / 13.00`
- Starting score: `9.51 / 12.89` from W22 / design-iter-16
- Net movement: overall `-0.26`, max `+0.11`
- Goal: visual below 9: not reached
- Constraint target: anti-cheat compliant: met

## Kept changes

1. Shifted body pages down by 0.2mm:
   - `section.top_margin = Mm(10.2)` instead of `Mm(MARGIN_MM)`.
   - This was the broadest improvement, moving overall `9.51 -> 9.27`.
2. Matched table zebra shading to the Swiss design gray:
   - `ZEBRA_GRAY = "F2F2F7"` instead of `"F4F4F4"`.
   - This gave a small additional improvement, `9.27 -> 9.25`.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.51 | 12.89 | W22 / design-iter-16 final reproduced | reference |
| iter-1 | 10.46 | 14.30 | Header top hairline `size 18 -> 8` | rejected, broad regression |
| iter-2 | 10.06 | 13.50 | Top margin `10.0mm -> 9.8mm` | rejected |
| iter-3 | 9.27 | 13.00 | Top margin `10.0mm -> 10.2mm` | kept |
| iter-4 | 9.45 | 13.53 | Top margin `10.2mm -> 10.4mm` | rejected, overshot |
| iter-5 | 9.25 | 13.00 | Zebra gray `#F4F4F4 -> #F2F2F7` on iter-3 | final winner |
| iter-6 | 9.35 | 13.40 | Sub-title underline `size 6 -> 8` | rejected |
| iter-7 | 9.42 | 15.07 | Warning-box title `7.5pt` | rejected, p3 regression |
| iter-8 | 9.26 | 13.04 | Step badge number font `7.05pt -> 7.5pt` | rejected |
| output | 9.25 | 13.00 | Rebuilt from promoted builder | final |

## Constraint verification

Final `output.score.json`:

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- `editable_pct`: `100.0`

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
