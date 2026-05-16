# design-iter-16 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.51 / 12.89`
- Starting score: `9.53 / 12.96` from W21 / design-iter-15
- Net improvement: overall `-0.02`, max `-0.07`
- Goal: push visual below 9: not reached
- Constraint target: anti-cheat compliant: met

## Kept changes

- Kept W21 global text spacing:
  - `CHAR_SPACING_TWIPS = 5`
- Added scoped warning-list spacing:
  - `WARNING_CHAR_SPACING_TWIPS = 7`
  - Applies only to `warning-box` bullet-list runs.
- Restored the actual bullet glyph for list markers:
  - `*` -> `•`

These changes improved the highest pages while keeping all pages under 13 max diff.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.53 | 12.96 | W21 / design-iter-15 final | reference |
| iter-1 | 9.54 | 13.00 | `CHAR_SPACING_TWIPS 5 -> 6` | rejected, max overshot 13 |
| iter-2 | 9.54 | 12.87 | `CHAR_SPACING_TWIPS 5 -> 7` | rejected, max improved but overall regressed |
| iter-3 | 9.59 | 13.12 | `CHAR_SPACING_TWIPS 5 -> 8` | rejected, overshot |
| iter-4 | 9.52 | 12.91 | body spacing 5, warning-list spacing 7 | kept as intermediate best |
| iter-5 | 9.54 | 13.13 | warning-list spacing 8 | rejected, overshot |
| iter-6 | 9.52 | 12.91 | `BODY_PT 7.05 -> 7.10` on iter-4 | neutral |
| iter-7 | 9.52 | 12.91 | non-compact warning line spacing `1.10 -> 1.06` | neutral |
| iter-8 | 9.51 | 12.89 | iter-4 + actual bullet glyph | final winner |
| output | 9.51 | 12.89 | rebuilt from promoted builder | final |

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

`[2.95, 3.54, 12.8, 7.76, 11.57, 7.33, 8.11, 8.12, 12.89, 10.02, 12.29, 10.01, 12.22, 12.68, 10.34]`

Hard pages:

- p3: `12.80`
- p9: `12.89`
- p13: `12.22`
- p14: `12.68`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python .\build_b2_docx.py .\output.docx
python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```
