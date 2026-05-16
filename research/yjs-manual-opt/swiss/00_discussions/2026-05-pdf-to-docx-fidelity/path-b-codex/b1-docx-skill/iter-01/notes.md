# iter-01 notes

Result:
- Generated `output.docx`.
- Anthropic `unpack.py` succeeded.
- Anthropic `pack.py` succeeded.
- Anthropic `validate.py` passed with `PYTHONUTF8=1`; without UTF-8, Windows GBK decoding caused validator read errors.
- DOCX -> PDF rendered to 14 pages.
- `png/` rendered successfully.
- `side_by_side/` was partially produced; comparison stopped after page mismatch.

Observed:
- Page count improved from 24 to 14, so the font/spacing compaction worked.
- TOC is visible as real editable Word paragraphs, not a headless Word field.
- All inspected text is in `word/document.xml` as `<w:t>`; no `<wp:txbx>`, `<w:txbxContent>`, or `<v:textbox>` matches were found.
- Layout is over-compressed versus the 15-page target: source continuation blocks merged, e.g. page 3 includes the start of CAUTION that should begin on target page 4.

Still wrong:
- Need restore page breaks between source page blocks so DOCX->PDF lands at 15 pages and target chapter continuation positions align.
- Need re-run side-by-side after page count matches.
