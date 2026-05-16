# design-iter-25 path-codex status

## Result

- Final candidate: `output.docx`
- Final retained change: none beyond the W28/path-A seed (`w:autoSpaceDE=0` and `w:autoSpaceDN=0`)
- Final score: `8.67 / 12.35`
- Starting score: `8.67 / 12.35`
- Net movement: unchanged; no scoring improvement found in the 6 requested unexplored OOXML probes
- Anti-cheat: pass (`wt_count=445`, `image_hack_detected=false`, `text ratio=1.0`, `editable=100.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | `design-iter-24/path-A/output.docx` seed | 8.67 | 12.35 | reference |
| iter-1 | Real `w:numPr` bullet numbering with `w:ilvl=0`, exact indent/hanging, literal bullet run removed | 8.72 | 12.69 | rejected |
| iter-2 | `w:textAlignment w:val="auto"` on all non-empty hard-page paragraphs/table paragraphs | 8.67 | 12.35 | neutral, not retained |
| iter-3 | `w:rPr/w:position=-1` on all hard-page text runs | 9.76 | 18.69 | rejected |
| iter-4 | Add `w:szCs` matching existing `w:sz` on all hard-page text runs | 8.67 | 12.35 | neutral, not retained |
| iter-5 | Add `w:noWrap` on all p11/p14 table cells | 8.67 | 12.35 | neutral, not retained |
| iter-6 | Page-specific margin overrides via existing per-page `sectPr` | 8.92 | 13.53 | rejected |

## Final Verification

Command:

`PYTHONUTF8=1 python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png`

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `445`
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

- `w:numPr` is directionally wrong for the current LibreOffice scorer: it worsens p3 and p14 even with exact `w:ind` and `w:ilvl`.
- `w:rPr/w:position` is strongly wrong on all hard pages; even a `-1` half-point offset creates large vertical drift.
- `w:textAlignment=auto`, `w:szCs`, and `w:noWrap` are effectively ignored or visually neutral in this scorer path.
- Page-specific section margin overrides are unsafe here; moving later pages shifts adjacent-page diffs and worsens p13 without improving the hard pages.
- Detailed machine-readable evidence is in `experiment-summary.json`.
