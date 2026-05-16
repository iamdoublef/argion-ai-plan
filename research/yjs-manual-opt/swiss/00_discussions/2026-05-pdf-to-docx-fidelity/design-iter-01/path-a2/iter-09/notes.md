# iter-09 — Table header size normalization

## Changes from iter-06
- Tried smaller table headers (6pt) — caused regression because text positions shifted
- Reverted all table header sizes to 7pt (same as iter-06)
- Table margins slightly compressed (30 twips top/bottom instead of 40)

## Result
- Visual diff: **14.92** (was 14.77 in iter-06) — marginal regression
- iter-06 remains slightly better — possibly because of more breathing room in tables

## Decision
Continue from iter-06 baseline. Try other quality improvements.
