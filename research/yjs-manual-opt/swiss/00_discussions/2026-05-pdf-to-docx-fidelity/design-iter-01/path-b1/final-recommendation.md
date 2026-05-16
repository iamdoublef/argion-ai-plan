# final recommendation

Best candidate from this continuation: `iter-05/output.docx`.

Result:
- Visual diff improved from the stated best 14.14 to 13.96.
- Page count remains aligned at 15 pages.
- Editable text remains 100%.
- Required font families remain present: Microsoft YaHei, Arial Black, and Courier New.

Recommendation:
- Keep the `export-docx.js` changes from iter-05 as the current B1 candidate because they improve the score without page-count regression.
- Do not use iter-03 or iter-04; both created 16-page candidates due to cover/table pagination regressions.

Remaining work for the next pass:
- Focus page 14 warranty/brand tables first; it remains the max diff page at 24.36.
- Increase Arial Black usage where target uses it, especially bullet symbols and English emphasis, without changing pagination.
- Revisit table grid fidelity with targeted table styles rather than broad margin increases.
- Fine-tune warning-box icon placement after table/page stability is locked.
