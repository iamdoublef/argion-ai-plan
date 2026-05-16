# iter-01 — Base font/size/color overhaul

## Changes from prev winner (a2-custom/iter-05)
- Font tokens: added FONT_LATIN_BLACK (Arial Black), FONT_CN_SMALL (NSimSun)
- set_run_fonts: new flags `latin_black` and `small_cn`
- Color tokens: C_GRAY_TEXT changed from #8A8A8A to #8E8E93 (matches PDF)
- C_NEAR_BLACK added (#1A1A1A) for body text
- Cover: 
  - "威富可" black (not red) with red `━━` bar prefix
  - "MODEL IMT050" Courier-style tracking, red 6pt
  - "制冰机" 18pt YaHei Bold black
  - "说明书" 7.5pt YaHei gray
  - Short red divider line under 说明书
  - Disclaimer NSimSun 5.5pt gray (footer)
- Body header: top horizontal line + "威富可" left (YaHei Bold 7.5pt) + "CH.XX — XXXX" right (Courier 5.25pt gray)
- Body footer: "威富可 IMT050 说明书" 5.25pt gray + page number right
- Section title: chapter number now Arial Black, 13.5pt, RED — title YaHei Bold 13.5pt BLACK
- Body paragraph: 7pt (was 9pt) — matches PDF dominant size
- Bullets: 7pt (was 8.7pt)
- Box (warning/caution/notice): added ▲ icon, smaller body 6.5pt
- Tables: ALL switched to BLACK header (1A1A1A) + WHITE text; bodies have only horizontal lines (no left/right borders), no zebra
- Step flow: smaller num cell (4.5mm), Arial Black white number 7pt
- TOC: 18pt title (was 24pt); entries 7pt with Arial Black red number
- Normal style: 7pt default (was 9.5pt)

## Result
- Visual diff: **14.92** (was 16.65) — ~10% improvement
- Fonts now include Arial-Black ✓ and NSimSun ✓
- Main sizes are 7.0pt (315) and 6.5pt (167) — matches PDF target 6.6-7.5pt range
- Pages: 15 (target) ✓
- Text ratio: 1.0 ✓
- Editable %: 100 ✓
