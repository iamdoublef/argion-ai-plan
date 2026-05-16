# design-iter-19 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `8.73 / 12.48`
- Starting score: `9.25 / 13.00` from W23 / design-iter-18 baseline
- Net movement: overall `-0.52`, max `-0.52`
- Goal hit: visual `< 9.0` and max `< 12.5`
- Constraint target: anti-cheat compliant

Final retained candidate is `iter-6`. Rejected iterations were not promoted.

## Retained changes

1. `warranty-card` tables are no longer treated as black-header tables.
   - First row is rendered as a normal form row.
   - Zebra fill starts on row 2.
   - Text remains editable.

2. `compact-warranty` tables use a wider left cell margin and top vertical alignment.
   - Left margin `55 -> 87 dxa`.
   - Vertical alignment `center -> top`.

3. `step-figures` inline image row uses tighter p9 positioning.
   - Left indent `33mm -> 30mm`.
   - Gap string `12 spaces -> 7 spaces`.

## Iterations

| Candidate | Overall | Max | Key page movement | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 9.25 | 13.00 | p9 `13.00`, p14 `12.61`, p15 `10.28` | reference |
| iter-1 | 8.81 | 13.00 | p15 `10.28 -> 3.65` | kept |
| iter-2 | 8.80 | 13.00 | p14 `12.61 -> 12.57`, p15 `3.65 -> 3.55` | kept |
| iter-3 | 8.80 | 13.00 | p14 `12.57 -> 12.46` | kept |
| iter-4 | 8.92 | 14.30 | compact-warranty body text 7.5pt | rejected |
| iter-5 | 8.81 | 13.22 | table-based two-image step row | rejected |
| iter-6 | 8.73 | 12.48 | p9 `13.00 -> 11.99` | final |
| iter-7 | 9.05 | 17.19 | compact-warranty section title 13.5pt | rejected |
| iter-8 | 8.77 | 13.06 | compact-safety warning bullet spacing | rejected |

## Final Verification

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

`[2.93, 3.25, 12.46, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.48, 10.01, 11.7, 12.46, 3.65]`

Remaining hard pages:

- p11: `12.48`
- p3: `12.46`
- p14: `12.46`
- p9: `11.99`

## Notes

- p14 did not break below `12.0`; the best safe p14 movement was `12.61 -> 12.46`.
- The biggest win came from the warranty-card first-row rendering bug and p9 step-figure inline positioning.
- Attempts to force target-metadata font sizes on compact warranty content caused large layout regressions in Word/LibreOffice.
