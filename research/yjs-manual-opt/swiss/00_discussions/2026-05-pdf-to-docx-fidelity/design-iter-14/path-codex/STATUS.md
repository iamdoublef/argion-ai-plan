# design-iter-14 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.58 / 13.18`
- Starting score: `9.60 / 13.30`
- Net improvement: overall `-0.02`, max `-0.12`
- Goal: any improvement: MET

## Kept changes

1. Warning/list paragraph spacing is explicit:
   - Bullet paragraph `space_before = 0`.
   - Warning-box bullet `space_after = 0.5pt`.
   - These were score-neutral but keep the intended compact warning-box formatting deterministic.
2. Slight positive character spacing:
   - Added `CHAR_SPACING_TWIPS = 2` to non-mono runs.
   - This improved Page 3 from `13.30` to `13.18` and overall from `9.60` to `9.58`.
3. Body text size:
   - `BODY_PT = 7.05` was score-neutral versus `7.2`.
   - `BODY_PT = 6.85` was rejected.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.60 | 13.30 | Reproduced design-iter-13 output | reference |
| iter-1 | 9.60 | 13.30 | Bullet `space_before = 0` | neutral, kept |
| iter-2 | 9.60 | 13.30 | Warning bullets `space_after = 0.5pt` | neutral, kept |
| iter-3 | 9.60 | 13.30 | `BODY_PT 7.2 -> 7.05` | neutral, kept |
| iter-4 | 9.82 | 14.19 | `BODY_PT 7.05 -> 6.85` | rejected, regression > 0.05 |
| iter-5 | 9.59 | 13.38 | Character spacing `-2` twips | rejected, max regression > 0.05 |
| iter-6 | 9.58 | 13.18 | Character spacing `+2` twips | kept best |
| output | 9.58 | 13.18 | Rebuilt from kept code | final |

## Constraint verification

Final `output.score.json`:

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- `editable_pct`: `100.0`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python .\build_b2_docx.py .\output.docx
python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```
