# design-iter-26 path-codex status

## Result

- Final candidate: `output.docx`
- Final retained change: none beyond the W28/path-A seed (`w:autoSpaceDE=0` and `w:autoSpaceDN=0`)
- Final score: `8.67 / 12.35`
- Starting score: `8.67 / 12.35`
- Net movement: unchanged; no scoring improvement found in the 6 requested unexplored probes
- Anti-cheat: pass (`wt_count=445`, `image_hack_detected=false`, `text ratio=1.0`, `editable=100.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | `design-iter-24/path-A/output.docx` seed | 8.67 | 12.35 | reference |
| iter-1 | Resample all 16 embedded PNGs to inline display size at 150 DPI | 8.67 | 12.35 | neutral, not retained |
| iter-2 | Resample all 16 embedded PNGs to inline display size at 300 DPI | 8.67 | 12.35 | neutral, not retained |
| iter-3 | Round all 16 inline drawing extents to quarter-point EMU boundaries | 8.67 | 12.35 | neutral, not retained |
| iter-4 | Force non-mono `w:rFonts` to Arial/Arial/Microsoft YaHei with `w:hint=eastAsia` | 10.62 | 22.33 | rejected |
| iter-5 | Add `w:bookmarkStart`/`w:bookmarkEnd` before chapter/header paragraphs | 8.67 | 12.35 | neutral, not retained |
| iter-6 | Add `w:contextualSpacing w:val="1"` to all non-empty paragraphs | 13.86 | 33.63 | rejected |

## Final Verification

Command:

`PYTHONUTF8=1 python .\run_experiments.py`

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

- Image DPI resampling changes bytes substantially but not the hard-page score: 150 DPI shrank media bytes from `530887` to `218444`; 300 DPI raised them to `632787`.
- Quarter-point inline extent rounding slightly shifts some non-hard pages but does not move the overall or max score.
- The Arial/Yahhei fallback-chain probe is directionally wrong because it destroys useful bold/font metrics, especially p14.
- `w:contextualSpacing` is strongly wrong for this document; it collapses intended same-style spacing and produces large vertical drift.
- Bookmarks are visually inert under the current LibreOffice scorer.
- Detailed machine-readable evidence is in `experiment-summary.json`.
