# iter-01 plan

Goal: reduce the generated editable DOCX from 24 pages toward the 15-page PDF reference without using pdf2docx or text frames.

Changes vs baseline:
- Tighten DOCX typography to A5 scale: body/table fonts, line height, paragraph spacing, table cell margins, alert box padding.
- Reduce image presets slightly so figure-heavy chapters do not push extra pages.
- Remove automatic page breaks for continued/warranty subpages; let Word flow content within each chapter section.
- Replace the docx-js TOC field with real editable Word paragraphs containing visible TOC entries and source-page-derived page numbers.
- Add missing `ctx.lang` so cover disclaimer language resolves correctly.

Checks:
- Generate `output.docx`.
- Validate/unpack with Anthropic DOCX scripts.
- Convert DOCX to PDF with the comparison tool, render PNGs, and create side-by-side images.
