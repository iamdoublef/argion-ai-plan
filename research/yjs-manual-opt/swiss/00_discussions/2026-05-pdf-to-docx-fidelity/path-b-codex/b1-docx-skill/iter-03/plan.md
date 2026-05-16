# iter-03 plan

Goal: polish the 15-page iter-02 output so key PDF reference elements are visibly closer.

Changes vs iter-02:
- Replace tab-stop TOC rows with a fixed-width real Word table so page numbers are visible.
- Use explicit margin-width tab stops in headers/footers to stop right-side clipping.
- Render continuation source-page headings with the same left bar and red chapter number treatment as chapter starts.

Checks:
- Generate `output.docx`.
- Run Anthropic `unpack.py`, `pack.py`, `validate.py`.
- Convert/render/compare with `compare_pdfs.py`.
- Verify no text boxes, visible TOC entries/page numbers, 15-page PDF, and editable paragraphs/tables/images.
