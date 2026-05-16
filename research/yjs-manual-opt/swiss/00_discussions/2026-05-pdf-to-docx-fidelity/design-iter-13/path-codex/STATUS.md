# design-iter-13 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `9.60 / 13.30`
- Baseline W18 reproduced: `9.67 / 13.35`
- Net improvement: overall `-0.07`, max `-0.05`
- Goal `visual < 9` and `max < 12`: not reached

## Kept changes

1. Cover page major rebalance:
   - Product image moved down toward target cover position.
   - Product image height reduced from `34mm` to `32.5mm`.
   - Cover lower text block moved down.
   - Page 1 diff improved from `3.62` to `2.94`.
2. Step figure two-image row structure:
   - Only two-image `step-figures` rows use paragraph-based placement with left indent.
   - Single-image and three-image rows stay on the original table path to avoid page 10 regressions.
   - Page 9 diff improved from `13.35` to `12.94`.

## Iterations

| Candidate | Overall | Max | Notes | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.67 | 13.35 | W18 reproduced | reference |
| iter-1 | 9.63 | 13.35 | Cover image/title/bottom block moved down | kept |
| iter-2 | 9.70 | 13.30 | Paragraph step figures for all counts; hurt page 10 | narrowed |
| iter-3 | 10.69 | 17.09 | Chapter title size 11pt -> 13.5pt | reverted, regression > 0.1 |
| iter-4 | 9.60 | 13.30 | Step-figure paragraph path limited to two-image rows | kept best |
| iter-5 | 9.73 | 14.74 | Alert box padding/icon retune | reverted, regression > 0.1 |
| iter-6 | 9.63 | 13.78 | Removed alert table wrapper via paragraph borders | rejected, max worse |
| iter-7 | 11.84 | 19.68 | Header band after-space shrunk to 4pt | reverted, regression > 0.1 |
| iter-8 | 9.60 | 13.30 | Warranty separator restored; page 14 worsened slightly | rejected |
| output | 9.60 | 13.30 | Rebuilt from kept code | final |

## Constraint verification

Final `output.score.json`:

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- `editable_pct`: `100.0`

Footer verification:

- In the scored A5 PDF, footer text/page numbers render at `y ~= 575-577pt`, matching the target A5 footer spans.
- No footer movement was kept because the current footer already aligns with target extraction; shrinking/moving other chrome caused regressions.

## Commands

```powershell
$env:PYTHONUTF8='1'
python build_b2_docx.py output.docx
python ..\..\score_candidate.py output.docx --target "D:/work/private/yjsplan/research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png
```

