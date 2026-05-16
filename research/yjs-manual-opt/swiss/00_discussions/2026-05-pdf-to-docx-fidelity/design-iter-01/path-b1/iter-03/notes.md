# iter-03 notes

Changes tested:
- Removed interior footers from generated sections.
- Removed the duplicate chapter header-ref paragraph under each chapter title.
- Increased chapter title and TOC title sizes.
- Switched table defaults from horizontal borders to full-grid borders.
- Increased table cell margins, changed specs table to 50/50 columns, made specs labels regular weight.
- Added generic headers to brand/manufacturer info tables.
- Suppressed the text warning triangle when an image icon is present.

Score:
- Pages: target 15 vs candidate 16.
- Visual diff: 16.04 overall, max page 24.57.
- Text ratio: 0.96; editable 100%.

Assessment:
- Regression. The table margin/header changes increased pagination and pushed the candidate to 16 pages.
- Do not keep this full set. Next pass should reduce pagination pressure: restore compact table margins and defer brand/manufacturer table headers, while testing the cleaner chapter heading/footer/icon changes separately.
