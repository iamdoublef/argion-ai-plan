# design-iter-21 path-codex-B status

## Goal

- Path B focus: image rendering / position.
- Target: visual `< 8.0` and max `< 11.5`.
- Starting score: `8.71 / 12.40` from W25 / design-iter-20.
- Anti-cheat guard: `wt_count >= 300`, no image hack, text ratio `<= 1.20`.

## Iterations

| Candidate | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| seed | W25 baseline reproduced in this workdir | 8.71 | 12.40 | reference |
| iter-1 | Cover product image scale 95% (`42x32.5mm -> 39.9x30.875mm`) | 8.69 | 12.40 | kept for overall; p1 `2.93 -> 2.66` |
| iter-2 | Cover product image scale 105% (`44.1x34.125mm`) | 8.73 | 12.40 | rejected; p1 `3.14` |
| iter-3 | Cover product image scale 110% (`46.2x35.75mm`) | 8.75 | 12.40 | rejected; p1 `3.42` |
| iter-4 | Cover image y-offset down 4pt at 95% scale | 8.69 | 12.40 | neutral; identical score to iter-1 |
| iter-5 | Step-figure width cap +10% | 8.70 | 12.40 | rejected; p9 worsened `11.99 -> 12.11` |
| iter-6 | Product structure diagram scale +5% | 9.16 | 13.21 | rejected; p6 worsened `6.19 -> 13.21` |

## Result

- Final candidate: `output.docx`
- Final score: `8.69 / 12.40`
- Starting score: `8.71 / 12.40`
- Net movement: overall `-0.02`, max unchanged.
- Goal missed: visual `< 8.0` and max `< 11.5`.
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, text ratio `1.0`).

## Retained Change

- Cover product image scale reduced to 95% of W25 current size:
  - `force_w 42mm -> 39.9mm`
  - `force_h 32.5mm -> 30.875mm`
  - p1 improved `2.93 -> 2.66`

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

Final per-page visual diffs:

`[2.66, 3.25, 12.4, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.4, 10.01, 11.7, 12.35, 3.65]`

## Notes

- Seed is the 100% cover scale test.
- 105% and 110% cover scale both worsened p1.
- Cover y-offset down 4pt had no measurable output movement.
- Step-figure width +10% worsened p9.
- Product structure diagram scale +5% caused a major p6 regression.
- Remaining max pages are p3 `12.40`, p11 `12.40`, and p14 `12.35`; the Path B image-focused changes did not move these.
