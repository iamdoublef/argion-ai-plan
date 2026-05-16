# Iteration 03 Notes

Change:
- Parsed first-row HTML `width:%` values and applied them to DOCX table cells with `w:tcW`.
- Kept iteration 02 alert-cell fix and spacing constants.

Score:
- Overall visual diff: 13.45.
- Max page diff: 27.87.
- Pages: 15 target / 15 candidate.
- Text ratio: 1.0.
- Editability: 100.0%.

Worst-page check:
- Same score profile as iteration 02.

Read:
- Setting per-cell widths alone was ignored by LibreOffice for these fixed tables.
- Next pass must also rewrite `w:tblGrid`; otherwise page 14 keeps equal-width columns and address text wraps.
