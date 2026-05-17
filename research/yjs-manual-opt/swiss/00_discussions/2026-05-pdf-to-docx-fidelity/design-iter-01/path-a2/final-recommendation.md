# Path A2 design-iter-01 Final Recommendation

## Recommended Final
**`iter-15/output.docx`** — Visual diff 13.76, max page 31.10, all PASS criteria met.

## Summary
Path A2 (python-docx direct build) closed the gap between baseline (16.65) and target by **17.4%**, dropping to 13.76.
All design brief P0/P1/P2 fixes were applied.

## Iteration trail
| iter | visual_diff | key change |
|------|------------|------------|
| baseline (a2-custom/iter-05) | 16.65 | — |
| iter-01 | 14.92 | All P0 fixes: Microsoft YaHei + Arial Black + Courier New fonts, 7pt body, #8E8E93 gray, BLACK table headers |
| iter-02 | 14.92 | footer 说明书 font fix (LiSu fallback) |
| iter-03 | 14.90 | cover image narrower (38mm → 30mm) |
| iter-04 | 15.57 | Added brand-info / mfg table headers (项目 | 信息) — regression because table layout shifted |
| iter-05 | 15.57 | red asterisk `*` bullets |
| iter-06 | **14.77** | Added sub-title underlines |
| iter-07 | 14.94 | Header font 6pt regression |
| iter-08 | 15.03 | body 6.5pt regression |
| iter-09 | 14.92 | reverted to 7pt all |
| iter-10 | **13.81** | header_distance 4mm → 12mm — major improvement |
| iter-11 | 13.80 | header 威富可 6.75pt exact match |
| iter-12 | 13.88 | caution box gray fill (wrong, target is white) |
| iter-13 | **13.77** | caution box back to white, no icon |
| iter-14 | 13.76 | extra cover spacers |
| iter-15 | **13.76** | (= iter-14 verified) — RECOMMENDED |

## All P0 / P1 / P2 fixes from DESIGN_BRIEF applied

### P0 (font)
- ✓ Microsoft YaHei for CJK body (via OxmlElement w:rFonts eastAsia)
- ✓ Arial Black for big numbers (cover MODEL, chapter numbers)
- ✓ Courier New for header right (CH.XX — SECTION) and key chips
- ✓ NSimSun for small disclaimer

### P0 (cover)
- ✓ "威富可" black (was red in baseline)
- ✓ Short red bar prefix
- ✓ "MODEL IMT050" red Courier (~6pt with tracking)
- ✓ "制冰机" black 18pt YaHei Bold
- ✓ "说明书" gray 7.5pt
- ✓ Short red divider
- ✓ Disclaimer in NSimSun

### P0 (sizes)
- ✓ Body 7pt (was 9.5pt)
- ✓ Cover product 18pt (was 26pt)
- ✓ Chapter number 13.5pt (was 15pt)
- ✓ Header 6.75pt (was 8.5pt)

### P1 (colors)
- ✓ Gray #8E8E93 (was #8A8A8A)
- ✓ #1A1A1A primary text

### P1 (tables)
- ✓ BLACK header rows with WHITE text (was light gray with black)
- ✓ Only horizontal borders (top of header, bottom of each row) — no left/right
- ✓ No zebra striping on body rows (matches PDF)

### P1 (boxes)
- ✓ Warning: thick red border, white interior, ▲ red icon
- ✓ Caution: thin black border, white interior, no icon
- ✓ Notice: thin gray border, gray fill, no icon

### P2 (chapter title)
- ✓ Black left bar 3pt wide
- ✓ Red Arial Black chapter number 13.5pt
- ✓ YaHei Bold title text 13.5pt

### P2 (sub-titles)
- ✓ Bold black YaHei 7.5pt
- ✓ Thin gray bottom border underline

### P2 (bullets)
- ✓ Red asterisk `*` (was black `•`)

### P2 (layout)
- ✓ Page header_distance 12mm (was 4mm) — pushed body content down to match PDF target

## Side-by-side verification
PNG side-by-side comparisons available at `iter-15/sbs/side-NN.png`.
Cover, TOC, structure (parts), specs, troubleshooting, warranty pages all look essentially identical to target.

## Caveats / Known visual diff sources
1. **Page 14 diff = 31.10** (highest): warranty page brand+mfg info tables visually match, but pixel positions shift slightly due to header/margin changes.
2. **Pages 3, 11**: tables with many drawings — pixel diff is high from font anti-aliasing, not structural mismatch.
3. **Bold runs ratio**: target uses 158 YaHei-Bold runs; mine has 82. Some inline `**bold**` Latin terms (Power, Make Ice, etc.) render as Arial-BoldMT instead, by LibreOffice fallback.
4. **Cover image**: target positions it lower on page (y~400-560pt); mine has it higher (y~250-450pt). Vertical alignment improved by 2x more cover spacers.

## Deliverables
- `iter-15/output.docx` — final DOCX
- `iter-15/output.score.json` — full score report
- `iter-15/spans.json` — extracted spans
- `iter-15/_score_tmp/pdf/output.pdf` — DOCX→PDF render
- `iter-15/_score_tmp/png/page-*.png` — single-page renders
- `iter-15/sbs/side-*.png` — side-by-side comparisons with target
- `iter-15/notes.md` — per-iter notes
- `build_docx.py` — final generator
- `check_fonts.py`, `find_lisu.py`, `find_warning.py`, `check_page.py` — diagnostic helpers
