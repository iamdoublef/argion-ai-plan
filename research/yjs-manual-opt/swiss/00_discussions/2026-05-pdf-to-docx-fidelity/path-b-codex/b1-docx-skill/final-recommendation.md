# Final recommendation

Use `iter-03/output.docx` as the B1 DOCX candidate.

Why this is the recommended file:
- It converts to a 15-page PDF, matching the target page count.
- It keeps customer-editable Word structure: real paragraphs, real Word tables, and embedded image runs.
- It avoids `pdf2docx` and contains no detected text boxes in `word/document.xml`.
- The TOC is visible in headless LibreOffice conversion because it is real editable content, not a Word field awaiting refresh.
- The key Swiss visual language is present: red chapter numbers, black left title bars, accent lines, alert boxes, zebra tables, headers, footers, and warranty card.

Primary output:
- `iter-03/output.docx`

Verification artifacts:
- `iter-03/pdf/output.pdf`
- `iter-03/png/`
- `iter-03/side_by_side/`
- `iter-03/unpacked/`
- `iter-03/notes.md`

Known caveat:
- The file is optimized for editable Word delivery. It is visually close to the PDF reference, but not a fixed-position PDF clone.
