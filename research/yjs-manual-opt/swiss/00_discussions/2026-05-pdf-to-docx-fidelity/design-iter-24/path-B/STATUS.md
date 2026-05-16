# design-iter-24 path-B status

## Result

- Final candidate: `output.docx`
- Final retained change: `grid-all` default, adding explicit `w:tblGrid/w:gridCol` values to non-HTML tables as well as the existing HTML tables.
- Final score: `8.67 / 12.35`
- Starting score: `8.67 / 12.35` from W27 / design-iter-23 starter
- Net movement: scoreboard unchanged.
- Goal missed: target was visual `< 8.0` or max `< 12.0`.
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`, `editable=100.0`).

## Iterations

| Candidate | Focused change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| baseline | W27 starter from design-iter-23 | 8.67 | 12.35 | reference |
| iter-1 | Broad `w:rFonts w:hint="eastAsia"` on all non-mono runs | 10.62 | 22.31 | rejected |
| iter-2 | Explicit `w:gridCol` values for all tables | 8.67 | 12.35 | kept as neutral / reproducible default |
| iter-3 | SectPr docGrid / explicit portrait page properties | 15.08 | 25.25 | rejected; produced 16 pages |
| iter-4 | JPEG 300 dpi image embedding, same displayed dimensions | 8.68 | 12.35 | rejected |
| iter-5 | Convert inline drawings to anchored drawings | n/a | n/a | invalid; LibreOffice conversion failed |

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
- LibreOffice PNG visual QA: inspected all 15 score-rendered pages via `contact-sheet-final.png`, plus hard pages `page-03.png`, `page-09.png`, `page-11.png`, and `page-14.png` at original render size. No clipping, overlap, missing glyphs, or broken tables observed.
- Artifact-tool cross-render: command completed and wrote `artifact_render/`, but it rendered 26 pages with severe pagination/text-flow mismatch. This appears incompatible with the current scoreboard renderer path, so final acceptance evidence remains the project scoring script / LibreOffice render.

Final per-page visual diffs:

`[2.93, 3.25, 12.03, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.14, 10.01, 11.70, 12.35, 3.65]`

Remaining hard pages:

- p14: `12.35`
- p11: `12.14`
- p3: `12.03`
- p9: `11.99`

## Notes

- Broad East Asia font hinting is directionally wrong for this renderer; it shifted multiple pages and badly regressed p14.
- SectPr docGrid is also wrong here; it changed pagination to 16 pages and caused broad visual drift.
- JPEG 300 dpi embedding is nearly neutral but slightly worse overall and increases image bytes.
- Anchored drawing conversion is not safe in the current generated OOXML form because LibreOffice cannot convert the result.
