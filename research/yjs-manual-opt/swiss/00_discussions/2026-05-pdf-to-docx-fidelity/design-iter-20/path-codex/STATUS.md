# design-iter-20 path-codex status

## Result

- Final candidate: `output.docx`
- Final score: `8.71 / 12.40`
- Starting score: `8.73 / 12.48` from W24 / design-iter-19 final
- Net movement: overall `-0.02`, max `-0.08`
- Stretch goal missed: target was visual `< 8.0` and max `< 11.5`
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`)

Final retained candidate is `iter-8`. Rejected iterations were not promoted.

## Retained changes

1. `compact-ts` caution/disclaimer block receives a small spacer before the alert box.
   - p11 moved `12.48 -> 12.40`.
   - This targeted the disclaimer block sitting too high after the troubleshooting table.

2. `compact-safety` alert icon is shifted left with a paragraph indent correction.
   - p3 moved `12.46 -> 12.40`.
   - Text remains editable and the source icon is unchanged.

3. `compact-warranty` bullet list spacing is tightened.
   - p14 moved `12.46 -> 12.35`.
   - Only the warranty bullet list line/after spacing changed; table row styling was left intact.

4. Troubleshooting compact table cell margin `42 -> 32 dxa` was retained as neutral.
   - It had no measurable score effect under the current row-height constraints.

## Iterations

| Candidate | Overall | Max | Key page movement | Decision |
| --- | ---: | ---: | --- | --- |
| baseline | 8.73 | 12.48 | p3 `12.46`, p11 `12.48`, p14 `12.46`, p9 `11.99` | reference |
| iter-1 | 8.73 | 12.48 | p11 table margin `42 -> 32 dxa`; no measurable movement | neutral |
| iter-2 | 8.84 | 14.10 | compact warning line-height tightened; p3 regressed | rejected |
| iter-3 | 8.73 | 12.48 | p9 inline image run position; no measurable movement | neutral |
| iter-4 | 9.37 | 13.66 | section-title spacing reduction; broad regression | rejected |
| iter-5 | 8.73 | 12.52 | warranty separator image restored; p14 regressed | rejected |
| iter-6 | 8.72 | 12.46 | p11 `12.48 -> 12.40` | kept |
| iter-7 | 8.72 | 12.46 | p3 `12.46 -> 12.40` | kept |
| iter-8 | 8.71 | 12.40 | p14 `12.46 -> 12.35` | final |

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

`[2.93, 3.25, 12.4, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.4, 10.01, 11.7, 12.35, 3.65]`

Remaining hard pages:

- p3: `12.40`
- p11: `12.40`
- p14: `12.35`
- p9: `11.99`

## Notes

- The stretch goal likely needs a larger p3/p11/p14 structural move, not just small spacing nudges.
- LibreOffice ignored the attempted inline image run-position offset on p9.
- Adding the warranty separator image matched the target asset count but worsened p14, so it stayed rejected.
