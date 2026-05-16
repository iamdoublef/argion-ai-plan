# iter-02 notes

Result:
- Generated `output.docx`.
- Anthropic `unpack.py`, `pack.py`, and `validate.py` passed (`PYTHONUTF8=1` for validator).
- DOCX -> PDF rendered to 15 pages.
- Text-frame check found no `<wp:txbx>`, `<w:txbxContent>`, or `<v:textbox>` in `word/document.xml`.
- TOC entries are visible editable text.

Observed:
- Page count now matches the 15-page target.
- Alert boxes, tables, drawings, and paragraphs are real Word structures.
- Page 3/4 content split now follows the target source-page split.

Still wrong:
- TOC page numbers are clipped/missing because right tab stops render outside the visible margin.
- Header/footer right-side text is clipped for the same reason.
- Continuation page headings are plain section titles; target uses the same left bar + red chapter number treatment.
