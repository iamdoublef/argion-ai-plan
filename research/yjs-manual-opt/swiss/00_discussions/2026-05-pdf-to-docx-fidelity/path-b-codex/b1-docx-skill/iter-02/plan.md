# iter-02 plan

Goal: keep iter-01's editable compact Word layout but restore the target's 15-page structure.

Changes vs iter-01:
- Add a page break before every second-or-later source page within a chapter.
- Keep the tighter typography, static editable TOC, smaller images, and reduced cell/alert margins.

Checks:
- Generate `output.docx`.
- Run Anthropic `unpack.py`, `pack.py`, `validate.py`.
- Convert/render/compare with `compare_pdfs.py`.
- Inspect page 3/4, TOC, tables, alert boxes, and text-frame absence.
