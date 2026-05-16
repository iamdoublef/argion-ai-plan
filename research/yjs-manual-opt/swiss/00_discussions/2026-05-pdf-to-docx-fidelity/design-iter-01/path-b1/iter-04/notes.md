# iter-04 notes

Changes from iter-03:
- Restored table cell margins to the previous compact values.
- Removed the added brand/manufacturer info table headers from this test.
- Kept footer removal, duplicate chapter-ref removal, larger chapter/TOC title sizing, full-grid table borders, specs 50/50 columns, regular specs labels, and warning title icon suppression.

Score:
- Pages: target 15 vs candidate 16.
- Visual diff: 15.13 overall, max page 24.57.
- Text ratio: 0.96; editable 100%.

Assessment:
- Still a regression versus iter-02 because the cover second disclaimer line overflowed onto a new blank page 2. That shifted every later page by one.
- Page-level comparison shows the header/chapter cleanup improves early interior pages, but the cover overflow must be fixed before this candidate is meaningful.
