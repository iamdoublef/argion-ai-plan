# Final Recommendation

## Recommended Deliverable

Use:

`iter-03/output.docx`

## Chosen Path

I chose a custom `python-docx` generator using the source HTML as the page/layout guide and the same embedded image assets.

This is closest to path 2, with the HTML used as the already-approved visual pagination source. I did not use `pdf2docx`, because it violates the editable-paragraph constraint. I also did not use LibreOffice/Pandoc/Mammoth as the main path because they risk layout drift and TOC-field failure, while the existing JS generator was already diagnosed as over-paginating.

## Why This Candidate Wins

- DOCX to PDF renders to 15 pages, meeting the `<=16` page gate.
- Text is Word-native: 345 real Word paragraphs.
- Tables are Word-native: 18 real Word tables.
- Images are inline embedded image runs: 17 inline drawings.
- No text boxes: `w:txbxContent` count is 0.
- No anchored/floating drawings: anchor count is 0.
- TOC is a static editable TOC with visible entries, so headless conversion cannot leave it blank.

## Verification Evidence

- DOCX: `iter-03/output.docx`
- LibreOffice PDF: `iter-03/pdf/output.pdf`
- Rendered PNGs: `iter-03/png/`
- Side-by-side comparison PNGs: `iter-03/side_by_side/`
- Contact sheet: `iter-03/contact-sheet.png`

The supplied `compare_pdfs.py compare` command crashed inside Pillow `ImageFont` drawing on this Windows environment. I used the supplied tool successfully for DOCX to PDF and PDF to PNG, then generated equivalent side-by-side PNGs with a font-safe local fallback.

## Remaining Risk

This is not a pixel-perfect PDF clone. It is a Word-native editable manual that keeps the approved 15-page structure and visual language. That tradeoff is appropriate because the customer requirement is editable Word content, not fixed PDF reconstruction.

