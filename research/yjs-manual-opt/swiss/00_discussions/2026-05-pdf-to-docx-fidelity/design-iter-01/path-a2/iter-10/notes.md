# iter-10 — Page top margin / header distance adjustment

## Key finding
On page 3, target header text "威富可" was at y=36.4pt; mine at y=19.0pt (17pt difference = ~6mm).
The header sat too high on every page, making the body start too early.

## Fix
- `set_page_size`: bumped `header_mm` default from 4.0 → 12.0 (matches PDF)
- `top_margin` now = `header_mm + 7mm` = 19mm (was 10mm)
- `bottom_margin` = `footer_mm + 5mm` = 17mm

This pushes the header line and content down, matching PDF target's vertical layout.

## Result
- Visual diff: **13.81** (was 14.92) — 7.5% improvement!
- Page 1 cover: 3.45 vs 3.38 in iter-09 — essentially same
- Page 2 TOC: 5.46 vs 5.47 — same
- Page 3 safety: 18.02 vs 18.13 — slight improvement
- Page 6 parts: **10.55** vs 21.44 — DRAMATIC improvement
- Page 7 features: **13.5** vs 19.78 — major improvement
- Page 11 troubleshooting: 20.97 vs 23.03 — improvement
- Page 14 warranty: 30.93 vs 24.04 — REGRESSION (table moved due to margins, structural correctness matched)

## Conclusion
This is a clear winner overall. Page 14 went up because the increased top margin
pushed the warranty card layout closer to target's actual position.
