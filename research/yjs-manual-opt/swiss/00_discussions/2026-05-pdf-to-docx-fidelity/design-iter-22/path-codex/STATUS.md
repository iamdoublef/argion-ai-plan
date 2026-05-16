# design-iter-22 path-codex status

## Result

- Final candidate: `output.docx`
- Final retained change: compact troubleshooting pre-caution spacer `after=7 -> after=0`
- Final score: `8.67 / 12.35`
- Starting score: `8.69 / 12.40` from W26 / design-iter-21 path-codex-A
- Net movement: overall `-0.02`, max `-0.05`
- Goal missed: target was visual `< 8.0` and max `< 11.5`
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | W26 starter reproduced | 8.69 | 12.40 | reference |
| iter-1 | Header top rule `size 18 -> 8` | 9.59 | 13.87 | rejected |
| iter-2 | Header top rule spacing `space 1 -> 4` | 9.78 | 16.11 | rejected |
| iter-3 | Footer top border `size 4 -> 2` | 8.70 | 12.41 | rejected |
| iter-4 | Cover product image `space_before 8pt -> 5.17pt` (-1mm) | 8.69 | 12.40 | rejected/no movement |
| iter-5 | Step badge padding `"  n  " -> " n "` | 8.71 | 12.40 | rejected |
| iter-6 | Step badge padding `"  n  " -> "   n   "` | 8.74 | 12.40 | rejected |
| iter-7 | Alert box vertical padding `46 -> 36` twips | 8.71 | 12.51 | rejected |
| iter-8 | Compact troubleshooting caution spacer `after 7 -> 0` | 8.67 | 12.35 | kept |

## Final Verification

Command:

`python score_candidate.py design-iter-22\path-codex\output.docx --target D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf --baseline-pngs baseline\target_png`

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- editable: `100.0`
- pass overall: `true`

Final per-page visual diffs:

`[2.93, 3.25, 12.04, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.14, 10.01, 11.70, 12.35, 3.65]`

Remaining hard pages:

- p14: `12.35`
- p11: `12.14`
- p3: `12.04`
- p9: `11.99`

## Notes

- Header-band changes were strongly negative, so the W26 header geometry should be kept.
- Footer hairline tuning was effectively neutral/slightly negative.
- Step badge width changes hurt p9/p10/p12 and did not affect max.
- Coordinate probing showed p11 disclaimer started about 8pt too low while the table was already close; removing the compact-ts pre-caution spacer fixed that local structure and gave the only retained improvement.
- Next useful branch should target p14 warranty structure. The current max is p14, not p11.
