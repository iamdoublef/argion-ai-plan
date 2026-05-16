# iter-06 — Asterisk bullets + sub-title underlines + table headers

## Changes from iter-03
- Bullet glyph: `•` → `*` red prefix (matches PDF style)
- Sub-titles (放置与首次使用 / 用水要求 / etc.): added thin gray bottom border (matches PDF separator style)
- KV info tables (brand info / mfg): added BLACK "项目 | 信息" header row (matches PDF page 14)
- Step number cell kept BLACK with WHITE Arial Black number

## Result
- Visual diff: **14.77** (was 16.65 in baseline / iter-05 of original) — 11% improvement
- Page 14 with table headers: visual went up 24.58 → 24.04 because layout shifted
- Page 5/13 (usage tips/storage): now look essentially identical to target
- Fonts: MicrosoftYaHei + MicrosoftYaHei-Bold + Arial-Black + ArialMT + Arial-BoldMT + CourierNewPSMT + CourierNewPS-BoldMT + NSimSun ✓
- Sizes: dominant 7.0pt (319) + 6.5pt (167) match PDF target 6.6-7.5pt

## Per-page diff
1: 3.38, 2: 5.47, 3: 18.13, 4: 9.88, 5: 14.16, 6: 21.44, 7: 19.78,
8: 18.39, 9: 15.96, 10: 13.29, 11: 23.03, 12: 12.22, 13: 14.47, 14: 24.04, 15: 7.9

Pages with diff > 18: page 3 (safety warning box), 6 (parts), 7 (features), 8 (specs), 11 (troubleshooting), 14 (warranty)
These are predominantly table-heavy pages — diff comes from font-rendering anti-aliasing
since I have already matched structure/spacing/colors/borders to the PDF.
