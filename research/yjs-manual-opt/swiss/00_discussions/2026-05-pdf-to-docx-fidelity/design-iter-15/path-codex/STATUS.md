# design-iter-15 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.53 / 12.96`
- Starting score: `9.58 / 13.18` from W20 / design-iter-14
- Net improvement: overall `-0.05`, max `-0.22`
- Goal: improve W20 without violating anti-cheat constraints: MET

## Kept change

- Increased non-monospace character spacing:
  - `CHAR_SPACING_TWIPS = 2` -> `5`
  - This improved the hard pages without changing page count, text ratio, image count, or editability.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.58 | 13.18 | W20 / design-iter-14 final | reference |
| iter-1 | 9.57 | 13.18 | `CHAR_SPACING_TWIPS 2 -> 3` | improvement, superseded |
| iter-2 | 9.56 | 13.11 | `CHAR_SPACING_TWIPS 2 -> 4` | improvement, superseded |
| iter-3 | 9.53 | 12.96 | `CHAR_SPACING_TWIPS 2 -> 5` | kept best |
| iter-4 | 9.58 | 13.18 | `BODY_PT 7.05 -> 7.0` | neutral, rejected |
| iter-5 | 9.93 | 13.18 | Image output scale 98% | rejected, overall regression |
| iter-6 | 9.90 | 13.25 | Image output scale 102% | rejected, overall and max regression |
| iter-7 | 9.58 | 13.18 | Bullet asterisk tight/normal size 5.0/5.5pt | neutral, rejected |
| iter-8 | 9.58 | 13.19 | Footer hairline size 4 -> 3 | rejected, max regression |
| output | 9.53 | 12.96 | Rebuilt from kept builder | final |

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

`[2.95, 3.54, 12.96, 7.79, 11.57, 7.33, 8.11, 8.12, 12.91, 10.05, 12.29, 10.02, 12.23, 12.69, 10.34]`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python .\build_b2_docx.py .\output.docx
python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```
