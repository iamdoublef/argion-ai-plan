# design-iter-21 path-codex-A status

## Result

- Final candidate: `output.docx`
- Final retained change: `WARNING_CHAR_SPACING_TWIPS = 8`
- Final score: `8.69 / 12.40`
- Starting score: `8.71 / 12.40` from W25 / design-iter-20 final
- Net movement: overall `-0.02`, max unchanged
- Goal missed: target was visual `< 8.0` and max `< 11.5`
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Key page movement | Decision |
| --- | --- | ---: | ---: | --- | --- |
| baseline | W25 starter reproduced | 8.71 | 12.40 | p3 `12.40`, p11 `12.40`, p14 `12.35`, p9 `11.99` | reference |
| iter-1 | `CHAR_SPACING_TWIPS 5 -> 4` | 8.74 | 12.41 | p11 `12.35` improved, p3/p9/p14 regressed | rejected |
| iter-2 | `CHAR_SPACING_TWIPS 5 -> 6` | 8.72 | 12.42 | p3 `12.38` improved, p11/p14 regressed | rejected |
| iter-3 | `CHAR_SPACING_TWIPS 5 -> 7` | 8.73 | 12.46 | p9 `11.98` improved only; p11 max regressed | rejected |
| iter-4 | `WARNING_CHAR_SPACING_TWIPS 7 -> 6` | 8.72 | 12.53 | p3 regressed to `12.53` | rejected |
| iter-5 | `WARNING_CHAR_SPACING_TWIPS 7 -> 8` | 8.69 | 12.40 | p3 improved `12.40 -> 12.04`; p11/p14 unchanged | kept |
| iter-6 | iter-5 plus per-page char spacing p1/p2 `4`, p11/p14 `7` | 8.69 | 12.46 | p11/p14 regressed | rejected |

## Final Verification

Command:

`python score_candidate.py design-iter-21\path-codex-A\output.docx --target D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf --baseline-pngs baseline\target_png`

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- editable: `100.0`
- pass overall: `true`

Final per-page visual diffs:

`[2.93, 3.25, 12.04, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.4, 10.01, 11.7, 12.35, 3.65]`

Remaining hard pages:

- p11: `12.40`
- p14: `12.35`
- p3: `12.04`
- p9: `11.99`

## Notes

- The warning text spacing change helps p3 but does not move p11/p14 enough to affect max.
- Global character spacing is too blunt: it trades one hard page for another and never clears the W25 max.
- Per-page character spacing for p11/p14 was directionally wrong under LibreOffice rendering; p11 became the max page at `12.46`.
- Next path should target p11/p14 structure or vertical placement rather than broader character spacing.
