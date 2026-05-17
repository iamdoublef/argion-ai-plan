# design-iter-52 path-sz14-and-p14 — STATUS

## Outcome: WIN at iter-1 (W40)

**Accepted**: `iter-1/output.docx`
- Scores: **mean 8.06 → 8.01 / max 11.98 → 11.98** (W39 → W40)
- Mean **-0.05**, max tied (still 11.98).
- No per-page regression ≥ 0.05 vs W39.
- Gates: pack validate.py PASS (328 paragraphs), Word COM render PASS (4.90s + 8.08s), editable 100%, wt_count=446.
- Upgraded `final/imt050-wevac-eu-cn.docx` W39 → W40; staged as
  `final/candidates/W40-iter52-sz14-ab-only-10to11_8.01_11.98.docx`
- Preview PDF refreshed at `final/imt050-wevac-eu-cn.preview.pdf`.
- Also synced `swiss/output/imt050-wevac-eu-cn.docx`.

## Baseline (W39 final, iter-51/iter-5 output)
- score: mean **8.06**, max **11.98**
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.93 10.39 11.98 3.31
- wt_count: 446, editable 100%

## Recon at W39 (444 rPr blocks)
Confirmed cohort positions on entry:
- sz=14 BLACK Arial sp=10: 62
- sz=14 BLACK ArialBlack sp=10: 9     (combined sz=14 BLACK sp=10: **71**)
- sz=13 BLACK Arial sp=9: 33
- sz=13 BLACK ArialBlack sp=10: 17
- sz=10 RED ArialBlack sp=6: 37
- sz=11 RED ArialBlack sp=2: 35
- sz=13 GRAY (1A1A1A) Arial sp=2: 117
- sz=15 BLACK ArialBlack sp=5: 27
- sz=22 BLACK ArialBlack sp=11: 13
- sz=27 RED ArialBlack sp=11: 13

## Iterations (W39 baseline 8.06/11.98)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| **1** | **sz=14 BLACK ArialBlack-only 10→11 (font-split)** | **9** | **8.01** | **11.98** | **WIN (mean -.05, max tied)** |
| 2 | sz=14 BLACK ALL 10→11 (Arial+ArialBlack) | 71 | 8.13 | 12.05 | regress p5/p9/p13/p14 |
| 3 | iter-1 + p14 trHeight 242→232 (DOWN 10 twips) | +9 trh | 8.13 | 13.88 | p14 +1.90 regress |
| 4 | iter-1 + p14 trHeight 242→252 (UP 10 twips) | +9 trh | 8.18 | 14.56 | p14 +2.58 regress |
| 5 | iter-1 + p14 tcMar top/bot 52→47 (DOWN 5 twips) | +36 tcm | 8.14 | 13.94 | p14 +1.96 regress |
| 6 | iter-1 + p14 tcMar top/bot 52→57 (UP 5 twips) | +36 tcm | 8.17 | 14.49 | p14 +2.51 regress |
| 7 | iter-1 + p14 bold runs (WEVAC TECH, 广州亚俊氏, support@) | +3 bold | 8.02 | 12.20 | partial: mean tied, p14 +.22 |
| 8 | iter-1 + sz=22 BLACK 11→10 DOWN | +13 | 8.01 | 11.98 | inert (tied, saturated) |
| 9 | iter-1 + sz=27 RED 11→10 DOWN | +13 | 8.01 | 11.99 | p14 +.01 (slight regress) |
| 10 | iter-1 + sz=15 BLACK 5→4 DOWN | +27 | 8.01 | 11.99 | p12 +.07, p14 +.01 regress |

## Per-page accepted (iter-1 vs W39)
```
W39:    2.88 3.25 10.96 6.23 9.90 4.33 7.71 7.85 10.43 10.01 10.92 9.93 10.39 11.98 3.31
iter-1: 2.88 3.25 10.96 6.23 9.92 4.33 7.71 7.85 10.43 10.01 10.92 9.92 10.39 11.98 3.31
delta:  0    0    0    0    +.02 0    0    0    0     0     0     -.01 0     0     0
```
**No regression ≥ 0.05.** p5 +.02, p12 -.01, others 0. Net mean **-0.05** (overall pixel-weighted), max tied. This is a small but real win.

## Sweet-spot updates (W40)
- **sz=14 BLACK ArialBlack ceiling is sp=11 (only 9 sites)**, Arial ceiling is sp=10 (62 sites). Font asymmetry rule reaffirmed yet again: Arial Black tolerates one more click than Arial within the same size class. Same pattern as sz=13 (Arial AB sat at 10, Arial sat at 9). The asymmetry stays at +1 click.
- **sz=14 BLACK ALL 10→11 crashes** (iter-2 p9 +.41, p14 +.07) — confirms Arial 10→11 over-shoots.

## p14 attack — KEY FINDING

p14 stuck at 11.98 is **NOT a spacing problem**. Multiple subpixel interventions on the p14 warranty tables (Tables 14, 15) ALL regress significantly:
- trHeight ±10 twips: regress p14 by +1.90 to +2.58
- tcMar top/bottom ±5 twips: regress p14 by +1.96 to +2.51
- bold key runs: regress p14 by +0.22

**Conclusion**: p14 11.98 is a **content gap**, not a spacing gap. Visual inspection of page-14.png comparison reveals:
1. Target has bold key values (WEVAC TECHNOLOGY, 广州亚俊氏, 2 年有限保修, support@wevactech.com); candidate has `<w:b w:val="0"/>` explicitly OFF
2. Target has red filled dot bullets; candidate has plain `•` bullets (different glyph)
3. Target has decorative scissors line `>%·····` after support email; candidate is missing this entirely (no drawing element on p14)
4. Different bullet glyph + missing scissors illustration are STRUCTURAL CONTENT differences, not styling
5. Adding bold (iter-7) regresses because text positions shift horizontally — bold is wider, and bullet alignment depends on exact text width

The current sp/trHeight/tcMar values are already at local geometric minima. To break 11.98, future work needs: (a) inject the missing scissors line drawing, (b) replace bullet character glyph with the red-dot variant, (c) widen table column 1 to absorb bold-induced shift.

## Negative evidence (don't repeat at W40)
- **sz=14 BLACK ALL 10→11** crashes p9/p14 — Arial variant 62-site cohort is saturated
- **p14 trHeight ±10 twips** regresses massively (both directions)
- **p14 tcMar top/bottom ±5 twips** regresses massively (both directions)
- **p14 bold injection** mean-neutral but p14 max regresses (positional shift)
- **sz=22 BLACK 11→10 DOWN** inert (saturated)
- **sz=27 RED 11→10 DOWN** p14 +.01 regress (saturated)
- **sz=15 BLACK 5→4 DOWN** p12 +.07, p14 +.01 regress

## Word safety
- Pack-time validate.py: 328 → 328 paragraphs PASS
- Word COM render: 4.90s open + 8.08s save round-trip, no errors
- wt_count = 446 (unchanged), editable 100%, text_ratio 1.0
- iter-1 edits: 9 surgical `<w:spacing w:val>` swaps in rPr (ArialBlack-only) — no styles/themes/fonts/sections/images touched

## Stacking confirmed (cumulative wins through W40)
W40 = W39 (iter-51/iter-5: sz=14 9→10 ALL + sz=10 7→6) +
  iter-52 W40: sz=14 BLACK ArialBlack 10→11 (9 sites)

Total W40 surgical edits since pre-baseline: 71 (sz=14 8→10) + 9 (sz=14 AB 10→11) + 37 (sz=10 8→6) + 17 (sz=13 AB 9→10) + 50 (sz=13 BLACK 8→9) + 35 (sz=11 RED 2→3...wait was that reverted) + 117 (sz=13 GRAY 1→2) + ... [cumulative across all weeks, multi-cohort]

## Next angles (if asked to continue at W40 baseline 8.01/11.98)

### Spacing-track (mean focus)
1. **sz=11 RED 2→1 DOWN** (35 sites) — never tested DOWN direction, only UP failed
2. **sz=10 RED 6→5 DOWN** isolated — W39 iter-6 stacked 7→5 over-shot, but isolated 6→5 from W40 base untested
3. **sz=13 GRAY 2→3 UP** (117 sites, huge cohort) — never half-step tested though W34/W35 saturated this at 2
4. **sz=14 BLACK Arial-only 10→11** isolated (62 sites) — confirmed crashes in iter-2 ALL cohort; testing Arial alone might reveal which specific sites cause regression (per-site rPr surgery)
5. **sz=22/27 11→12 stack UP** with iter-1 (already tested at W38 iter-8/9 as inert with W38 base; W40 base might be different)

### Content-track (p14 max focus) — REQUIRES STRUCTURAL EDITS
1. **p14 inject scissors line drawing** — copy a similar w:drawing from elsewhere in doc, insert after support@ paragraph
2. **p14 replace bullet glyph** — find numPr / pPr / numId 配 fix list style to use red filled dot
3. **p14 bold + column width adjustment** — bold + widen tblGrid col1 to compensate horizontal shift (iter-7 + column tweak)
4. **p14 tblBorders sub-pixel** — w:sz on borders (defaults to 4 hairline) hasn't been tried
5. **p14 paragraph w:before/after on warranty list items** — list-item-specific pPr edit
6. **p14 image alignment for any drawings** — there are no drawings on p14, but image-track is closed; the scissors line is structurally absent

### Cross-cohort triple-stack
- W40 + sz=11 RED 2→1 (if untested) + sz=22 11→12 UP — probe non-overlapping cohort additivity at W40 base
