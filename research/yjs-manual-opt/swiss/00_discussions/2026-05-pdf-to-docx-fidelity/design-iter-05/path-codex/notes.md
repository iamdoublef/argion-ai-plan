# design-iter-05 notes

Goal:
- Improve the real editable DOCX baseline from `design-iter-03/path-codex/iter-02/output.docx`.
- Keep `wt_count >= 300`, no page-as-image hack, text ratio within `0.95..1.20`, and embedded images under 800 KB.

Best valid result:
- `iter-04/output.docx`
- Overall visual diff: `10.31`
- Max page diff: `17.67`
- Pages: `15 / 15`
- Text ratio: `1.00`
- `wt_count`: `457`
- Image bytes: `533482`
- Image hack detected: `false`
- Editable percent: `100.0`

Iteration log:

| Iter | Change | Overall | Max | Editable gate |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt starter builder unchanged | 10.74 | 17.74 | PASS |
| iter-01 | Quiet note boxes, remove extra image-row spacer, alert bullet indent | 10.56 | 17.74 | PASS |
| iter-02 | Non-symmetric margin experiment | 11.23 | 18.41 | PASS, rejected |
| iter-03 | Add fine grid only to compact warranty tables | 10.55 | 17.67 | PASS |
| iter-04 | Tighten alert icon paragraph spacing | 10.31 | 17.67 | PASS, selected |
| iter-05 | Small body/table font-size experiment | 10.31 | 17.67 | PASS, no movement |
| iter-06 | Pandoc HTML-to-DOCX probe | 14.77 | 21.55 | PASS editable, rejected: 13 pages and missing images |
| iter-07 | Heavier warranty table borders | 10.38 | 18.38 | PASS, rejected |
| iter-08 | Taller compact warranty rows | 10.45 | 19.78 | PASS, rejected |

Selected builder changes:
- `note-box` now renders as a quiet shaded panel without the full bordered callout/icon treatment.
- Alert-box image paragraphs use tight spacing, which improved p3 from `17.38` to `13.81`.
- Image rows no longer add an empty spacer paragraph, improving p9/p10.
- Compact warranty tables get fine grid borders, improving p14 slightly from `17.74` to `17.67` and p15 from `10.53` to `10.41`.

Remaining blocker:
- p14 remains the max-diff page. Translation and row-height probes showed the page is not primarily a simple global offset issue.
- Overall did not reach `< 9`, and max did not reach `< 14` within the allowed editable-only iteration budget.

Anti-cheat verification:
- No full-page screenshots were embedded.
- `word/media` total for selected output is `533482` bytes.
- Independent zip check on `iter-04/output.docx`: `wt_count = 457`, media count `17`, image bytes `533482`.
