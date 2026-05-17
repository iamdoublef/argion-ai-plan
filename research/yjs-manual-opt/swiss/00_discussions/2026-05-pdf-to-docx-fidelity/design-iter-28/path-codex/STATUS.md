# design-iter-28 path-codex status

## Result

- Final candidate: `output.docx`
- Final retained change: none; restored W27 / design-iter-22 builder because every non-neutral probe regressed visual score.
- Final score: `8.67 / 12.35`
- MS Word compatibility: pass via `docx2pdf` / Word COM (`word_render.pdf` produced).
- Anti-cheat: pass (`wt_count=457`, `image_hack_detected=false`, `text ratio=1.0`, `drawings_count=16`).
- OOXML post-process: none.

## Iterations

| Candidate | Focused change | Overall | Max | Word COM | Decision |
| --- | --- | ---: | ---: | --- | --- |
| iter-1 | W27 starter rebuilt unchanged | 8.67 | 12.35 | pass | selected reference |
| iter-2 | Included source warranty separator image | 8.68 | 12.42 | pass | rejected |
| iter-3 | Compact-warranty table vertical cell padding `52 -> 42` twips | 8.92 | 16.15 | pass | rejected |
| iter-4 | Compact-warranty subtitle `space_after 4 -> 4.5pt` | 8.70 | 12.82 | pass | rejected |
| iter-5 | Compact-warranty subtitle `space_after 4 -> 3.5pt` | 8.71 | 12.83 | pass | rejected |
| iter-6 | Compact-warranty body/bullet text `7.05 -> 7.00pt` | 8.67 | 12.35 | pass | neutral, not retained |

## Final Verification

Build:

`PYTHONUTF8=1 python build_b2_docx.py output.docx`

Score:

`PYTHONUTF8=1 python ..\..\score_candidate.py output.docx --target ..\..\..\..\output\imt050-wevac-eu-cn.pdf --baseline-pngs ..\..\baseline\target_png`

Result:

- pages: target `15`, candidate `15`
- text ratio: `1.0`
- editable: `100.0`
- `wt_count`: `457`
- `txbx_count`: `0`
- `drawings_count`: `16`
- `image_hack_detected`: `false`
- pass overall: `true`

Word-open check:

`PYTHONUTF8=1 python ..\..\design-iter-06\compare_word.py output.docx word_render.pdf`

Result:

- `OK: ...\output.docx -> ...\word_render.pdf`
- exit code `0`

Final per-page visual diffs:

`[2.93, 3.25, 12.04, 7.09, 10.94, 6.19, 7.81, 7.84, 11.99, 10.14, 12.14, 10.01, 11.70, 12.35, 3.65]`

## Notes

- The source warranty separator image looks tempting because the PDF target contains it, but adding it regressed p14 and raised max diff.
- Compact-warranty table padding remains sensitive; reducing it caused a large p14 regression.
- Sub-point compact-warranty subtitle spacing moved p14 in the wrong direction both up and down.
- The 0.05pt compact-warranty body text reduction was Word-safe and score-neutral, but not retained because it did not improve the score.
- With the new Word compatibility gate, the safest result is the W27-compatible output at the same visual score.
