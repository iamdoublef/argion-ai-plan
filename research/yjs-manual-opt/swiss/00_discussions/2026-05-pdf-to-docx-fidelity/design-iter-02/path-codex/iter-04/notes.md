# Iteration 04 Notes

Change:
- Added `w:tblGrid` columns based on first-row HTML percentage widths.
- Kept per-cell widths, alert-cell fix, and spacing constants from prior iterations.

Score:
- Overall visual diff: 13.30.
- Max page diff: 25.75.
- Pages: 15 target / 15 candidate.
- Text ratio: 1.0.
- Editability: 100.0%.

Worst-page check:
- p3 17.99, p5 14.49, p6 14.70, p7 17.01, p9 12.71, p10 13.50, p11 16.97, p13 15.02, p14 25.75.

Read:
- `w:tblGrid` is honored by LibreOffice and fixed the warranty table column proportions.
- Page 14 remains too low mainly because the builder inserts a full blank paragraph after each table; next pass should reduce/remove that spacer.
