# iter-03 notes

Result:
- Final candidate: `iter-03/output.docx`.
- DOCX -> PDF rendered to 15 pages.
- `compare_pdfs.py compare` completed successfully and wrote all 15 side-by-side images.
- Anthropic scripts used:
  - `unpack.py` succeeded.
  - `pack.py` succeeded.
  - `validate.py` passed with `PYTHONUTF8=1`.

Evidence:
- Page count: 15 rendered PNG pages in `iter-03/png/`.
- Side-by-side set: 15 images in `iter-03/side_by_side/`.
- Editable structure check against unpacked `word/document.xml`:
  - No `<wp:txbx>`, `<w:txbxContent>`, or `<v:textbox>` matches.
  - `<w:t>` count: 2019.
  - `<w:tbl>` count: 144.
  - `<w:drawing>` count: 17.

Observed:
- TOC is visible and editable, implemented as a real Word table with real text and visible page numbers.
- Chapter starts and continuation pages use the black left bar plus red chapter number treatment.
- Warning/caution/notice boxes, tables, and warranty card are real Word tables.
- Images are embedded image runs.
- Header/footer right-side text and page numbers no longer clip.

Remaining visual differences:
- This is a high-fidelity editable Word reconstruction, not a pixel-perfect PDF clone.
- Some figure/table vertical positions differ by normal Word layout behavior.
- Cover image and white-space balance are close enough for the editable DOCX objective but not exact PDF tracing.
