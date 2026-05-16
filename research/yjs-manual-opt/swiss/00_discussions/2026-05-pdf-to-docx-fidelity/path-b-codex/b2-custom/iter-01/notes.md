# Iteration 01 Notes

## Path Chosen

Custom `python-docx` generator driven by the already paginated source HTML.

Rationale:
- The source HTML already has the target 15-page structure.
- `python-docx` guarantees real Word paragraphs, real tables, and embedded image runs.
- Static editable TOC avoids the known empty-TOC issue from headless field conversion.

## Result

- Generated `output.docx`.
- LibreOffice DOCX to PDF conversion produced 15 pages.
- Main defect: step numbers rendered as full-width black table bars.
- Side-by-side compare tool crashed after page 1 due a Pillow `ImageFont` access violation.

