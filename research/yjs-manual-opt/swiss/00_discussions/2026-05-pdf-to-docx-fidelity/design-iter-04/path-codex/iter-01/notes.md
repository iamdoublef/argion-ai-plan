# Iter 01 Notes

Applied focused editable-builder changes:
- Removed borders/icons from note boxes.
- Added real grid borders to structured tables.
- Removed the empty paragraph after image rows.
- Increased alert-box bullet indent.

Result:
- Overall visual diff: 10.70
- Max page diff: 18.38
- Pages: 15 / 15
- Text ratio: 1.00
- Editable: 100.0%

Per-page movement:
- p9 improved 13.64 -> 13.05.
- p10 improved 13.03 -> 11.06.
- p13 improved 13.79 -> 13.57.
- p11 worsened 12.36 -> 13.30 after grid borders.
- p14 worsened 17.74 -> 18.38 because warranty tables became taller.

Decision:
The editable path improved visible callout aesthetics but did not approach the required <9.0 overall target. Remaining score is dominated by LibreOffice/Word font and table rendering mismatch.
