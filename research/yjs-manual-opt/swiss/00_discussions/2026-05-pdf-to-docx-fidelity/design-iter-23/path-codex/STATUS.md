# design-iter-23 path-codex status

## Result

- Final candidate: `output.docx`
- Final retained change: compact-safety alert icon aspect `6.9mm x 5.2mm -> 5.2mm x 5.2mm`
- Final score: `8.67 / 12.35`
- Starting score: `8.67 / 12.35` from W27 / design-iter-22 path-codex
- Net movement: scoreboard unchanged; p3 improved `12.04 -> 12.03`
- Goal missed: target was visual `< 8.0` or max `< 12.0`
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | W27 starter reproduced | 8.67 | 12.35 | reference |
| iter-1 | Disable char spacing on all bullet-list runs | 8.78 | 13.05 | rejected |
| iter-2 | Disable char spacing only on ordinary bullet lists | 8.71 | 12.42 | rejected |
| iter-3 | Body paragraph `space_after=-0.5pt` | n/a | n/a | invalid: Word spacing-after is unsigned |
| iter-4 | First-line indent `2.0mm` on all body paragraphs | 8.67 | 12.36 | rejected |
| iter-5 | First-line indent `2.0mm` only on compact-warranty body paragraphs | 8.67 | 12.36 | rejected |
| iter-6 | Subtle gray label-cell shading on p14 warranty structured tables | 8.72 | 13.08 | rejected |
| iter-7 | Compact-safety alert icon made square | 8.67 | 12.35 | kept as neutral p3 tie-break |
| iter-8 | Page 14 top margin `10.2mm -> 9.8mm` | 8.75 | 13.59 | rejected |

## Final Verification

Command:

`python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png`

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- editable: `100.0`
- pass overall: `true`
- PNG visual QA: inspected all 15 rendered pages from `_score_tmp/png`; no clipping, overlap, missing glyphs, or broken tables observed.

Final per-page visual diffs:

`[2.93, 3.25, 12.03, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.14, 10.01, 11.70, 12.35, 3.65]`

Remaining hard pages:

- p14: `12.35`
- p11: `12.14`
- p3: `12.03`
- p9: `11.99`

## Notes

- The fresh char-spacing idea is directionally wrong unless scoped even more narrowly; removing bullet spacing broadly regressed p3 and p14.
- `space_after=-0.5pt` cannot be expressed through `python-docx` because Word stores `w:after` as an unsigned value.
- First-line paragraph indents were visually neutral on overall but nudged max worse.
- Subtle warranty table label-cell shading was the largest p14 regression in this run.
- Page 14 vertical-margin movement was also strongly wrong; p14 jumped to `13.59`.
- The only safe local movement was preserving the compact-safety icon aspect ratio, reducing p3 by `0.01` with no overall/max penalty.
