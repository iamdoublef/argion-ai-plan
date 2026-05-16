# design-iter-24 path-A status

## Result

- Final candidate: `output.docx`
- Final retained change: OOXML `w:autoSpaceDE w:val="0"` and `w:autoSpaceDN w:val="0"` on all paragraphs
- Final score: `8.67 / 12.35`
- Starting score: `8.67 / 12.35` from rebuilt W27 / design-iter-22 builder
- Net movement: unchanged; no scoring improvement found in the 5-iteration OOXML branch
- Anti-cheat: pass (`wt_count=445`, `image_hack_detected=false`, `text ratio=1.0`)

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | Rebuilt `design-iter-22/path-codex/build_b2_docx.py` | 8.67 | 12.35 | reference |
| iter-1 | p14 paragraphs and table paragraphs `w:spacing line=240 lineRule=exact` | 9.39 | 23.08 | rejected |
| iter-2 | all paragraphs `w:autoSpaceDE=0` and `w:autoSpaceDN=0` | 8.67 | 12.35 | kept, neutral |
| iter-3 | all text runs `w:kern val=14` | 8.67 | 12.37 | rejected |
| iter-4 | p14 brand/manufacturer tables `w:tblpPr` floating table positioning | 8.91 | 15.99 | rejected |
| iter-5 | p11 paragraph/table exact line spacing `220` plus auto spacing off | 9.06 | 18.01 | rejected |

## Final Verification

Command:

`python ..\..\score_candidate.py .\output.docx --target "D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf" --baseline-pngs ..\..\baseline\target_png`

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- `wt_count`: `445`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- editable: `100.0`
- pass overall: `true`
- PNG visual QA: inspected contact sheets from `_score_tmp/png`; no obvious clipping, overlap, missing glyphs, or broken tables observed.

Final per-page visual diffs:

`[2.93, 3.25, 12.04, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.14, 10.01, 11.70, 12.35, 3.65]`

Remaining hard pages:

- p14: `12.35`
- p11: `12.14`
- p3: `12.04`
- p9: `11.99`

## Notes

- `w:spacing line=240 lineRule=exact` is strongly wrong on p14; it doubles the p14 max-region penalty.
- Floating `w:tblpPr` on p14 tables is also wrong; it destabilizes the warranty layout without improving other pages.
- `w:kern val=14` slightly worsens max on p14 and should not be carried forward.
- Disabling East Asian auto spacing is visually neutral under LibreOffice scoring and is the only non-regressive requested OOXML post-process retained.
