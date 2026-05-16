# Iteration 01 Notes

Change:
- Increased body line spacing from 1.08 to 1.16.
- Increased bullet line spacing from 1.05 to 1.13 and bullet `space_after` from 1.2 pt to 1.6 pt.
- Increased warning/caution/note vertical cell padding from 70 to 78 dxa.
- Increased table vertical cell padding and set table paragraph line spacing to 1.05.
- Added `w:trHeight` minimums to table rows.
- Increased step-flow line spacing from 1.04 to 1.10.

Score:
- Overall visual diff: 13.65.
- Max page diff: 27.87.
- Pages: 15 target / 15 candidate.
- Text ratio: 1.0.
- Editability: 100.0%.

Worst-page check:
- p3 18.41, p5 14.49, p6 14.77, p7 17.04, p9 12.71, p10 14.23, p11 17.06, p13 15.22, p14 27.87.

Read:
- Global expansion helps p6, p7, p9, p11, and p14.
- It hurts p3, p5, p10, and p13, so the next pass should keep table/list expansion but reduce alert/body expansion.
