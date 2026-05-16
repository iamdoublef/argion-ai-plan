# Final Recommendation

Recommended candidate: `iter-05/output.docx`

Why:
- It is the first and best iteration that meets the requested thresholds.
- Overall visual diff is 12.88, below the target of 13.0.
- Max page diff is 19.59, below the target of 22.
- Page count, text ratio, and editability all remain intact.

Key fixes to keep:
- Reuse the first table-cell paragraph for alert titles. This removes Word's implicit blank paragraph from warning/caution/note boxes.
- Preserve HTML table percentage widths by writing both `w:tcW` and `w:tblGrid`. This prevents warranty/address rows from wrapping differently from the PDF.
- Remove the blank paragraph after tables. The post-table spacer was the main cause of the page 14 vertical drift.
- Keep the moderate line-height expansion from iteration 01 for body, bullet, step, and table text; it helped several mid-document pages without breaking page count.

Score summary:

| Iteration | Overall diff | Max page diff | Result |
| --- | ---: | ---: | --- |
| B2 iter-04 baseline | 13.80 | 28.30 | Fails requested max-page target |
| iter-01 | 13.65 | 27.87 | Improved, still high max |
| iter-02 | 13.45 | 27.87 | Alert top gap improved |
| iter-03 | 13.45 | 27.87 | Cell widths alone not honored |
| iter-04 | 13.30 | 25.75 | Table grid improved page 14 |
| iter-05 | 12.88 | 19.59 | Recommended |

Worst-page scores for recommended candidate:

| Page | Diff |
| ---: | ---: |
| 3 | 17.99 |
| 5 | 14.49 |
| 6 | 14.70 |
| 7 | 17.01 |
| 9 | 12.71 |
| 10 | 13.50 |
| 11 | 16.89 |
| 13 | 15.02 |
| 14 | 19.59 |

Remaining risk:
- Page 3 remains visually busy because alert typography and icon placement still differ from browser/PDF rendering, but it is under the max-page threshold.
- The scoring path relies on LibreOffice conversion; Word/WPS may still render small metric differences differently.
