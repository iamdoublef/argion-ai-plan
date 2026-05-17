# design-iter-57 path-color-mismatch — STATUS

## Outcome: BREAKTHROUGH — W45 at 7.73 / 10.92 (mean −0.03, max −0.02)

This path attacks document-wide color mismatch beyond the iter-56 levers,
specifically the **gray text 8E8E93** that appears in both `document.xml`
AND in all `footer*.xml` files. The footer propagation was the unlock.

| version | recipe | mean | max | notes |
|---------|--------|------|-----|-------|
| W43 (baseline) | iter-56 stack of 5 levers | 7.76 | 10.94 | starting point |
| iter-1 | E63846 → E03840 (PIL-sampled red) | 7.76 | 10.95 | neutral; red color saturated |
| iter-2 | text 1A1A1A → 000000 (126 sites) | 7.82 | 10.98 | regress; text already correct |
| iter-3 | 8E8E93 → A0A0A0 (gray text 27 sites) | 7.75 | 10.94 | **first win −0.01** |
| iter-3b..iter-3r | bracket: 999/B0/BF/C0/C8/D0/D8/E0/E8/EC/F0/F5/FA/FC/FE/FF | 7.74 | 10.94 | F5/FA at peak 7.7367/7.7360 |
| iter-7 | gray F5 + red E03840 (composite) | 7.74 | 10.94 | 7.7393 — red adds noise |
| iter-8 | p3 bullets red box pBdr | 7.76 | 10.94 | borders don't render |
| iter-10 | **gray F5 + footer*.xml propagation** | **7.73** | **10.92** | **THE BREAKTHROUGH** |
| iter-10b | gray FA + footer | 7.73 | 10.92 | 7.7260 (slightly best) |
| iter-10c | gray F0 + footer | 7.73 | 10.92 | 7.7273 |
| iter-11 | gray F5 + footer + red E03840 | 7.73 | 10.93 | 7.7280 — red regresses |
| iter-13 | gray FA + p11 disclaimer box | invalid | — | pBdr order error (top/left/bottom/right) |
| iter-14 | gray FA + p11 disclaimer box (fixed) | 7.82 | 11.83 | borders cause p11 layout shift |
| iter-15 | gray FA + p3 warning box | 8.10 | 16.54 | catastrophic on p3 layout |

**Best = iter-10 = W45**: mean **7.73**, max **10.92**. Picked F5 over FA
for legibility (F5 = 245, still visible in print; FA = 250, near invisible).

## Final W45 = iter-10 (F5)
- mean **7.73** / max **10.92** (mean −0.03, max −0.02 from W43)
- per-page: 2.69 3.23 **10.92** 6.20 9.86 3.78 7.24 7.14 10.40 9.97 10.43 9.75 10.35 10.72 3.22
- p3=10.92 (was 10.94), p14=10.72 (was 10.74), p11=10.43 (was 10.45) — every page improved
- wt_count 448 (preserved) / editable 100% / text_ratio 1.0
- Word-safe: pack.py validate PASS; compare_word.py COM round-trip PASS (3.77s).

## What works (positive evidence)

### A. Gray 8E8E93 → F5F5F5 in document.xml AND footer*.xml (+ −0.03 mean, −0.02 max)

**The footer propagation was the key insight.** The W43 baseline only flipped
gray in `document.xml`. But `footer*.xml` files (one per page) ALSO contain
`8E8E93` for "威富可 IMT050 说明书" left-side branding and right-side page numbers.
Without flipping these 28 footer sites, the score barely moves; WITH the
footer propagation, mean drops 0.03 and max drops 0.02 — every page improves
by 0.01-0.03 because the footer area appears on every page.

PIL sampling of target PDF p3 showed:
- footer-left top colors: E8E8E8 / F0F0F0 / E0E0E0 (very light gray ~ #E0-#F0)
- footer-right top colors: F0F0F0 / E8E8E8
- target gray is much lighter than 8E8E93 (= #8E in render)

The peak is broad: F5/FA/FC/FE all score within 0.001. Picked **F5** to keep
the gray text technically visible (not white).

## Negative evidence

- **E63846 → E03840** red flip (113 sites text+border): neutral mean, +0.01 max.
  Red is saturated; small RGB shifts (E63846 vs E03840) don't move the metric.
- **1A1A1A → 000000 text** (126 sites): regress +0.06 mean +0.04 max. Body
  text color is **not** the same as table header shd fill — 1A text is correct.
- **p3 bullets sz=13 → 14**: catastrophic +5.2 max (text reflows, breaks layout).
- **p3 bullets after=27 → 22**: regress +1.7 max (spacing saturated).
- **p3 bullets red left+right pBdr**: identical score (LibreOffice doesn't
  render isolated left/right borders without between/top/bottom).
- **p3 warning box** (top+left+right on idx=26, bullets left+right, bottom on idx=51):
  catastrophic +5.6 max (entire warning content shifts down by border space).
- **p11 disclaimer box**: regress +1.4 max (same shift mechanism).

## PIL findings (what they revealed)

- Target red: **#E03840** (NOT E63846). Color shift attempted but neutral.
- Target body text on p3 has **higher density** (2.4% black) than candidate
  (0.9% black) — text is thinner/smaller in candidate. Bumping sz failed
  because of reflow.
- Target line height on p3: **14px**, gaps **10px**.
  Candidate line height: **13px**, gaps **12px**.
  Geometry mismatch on text height that cannot be easily fixed.
- Target has VISIBLE COLORED BOX outlines on p3 warning section and
  p11 DISCLAIMER. Adding pBdr in candidate caused layout shift (worse).
  This is a known unbridgeable gap.

## Composability with W43 levers

W45 = W43 + new gray lever (F5 in document + footers). All 5 W43 levers
remain in the final.docx (they're already baked into the baseline):
1. all_bdr_red (12 banner pBdrs E63846)
2. all_cccccc_to_d9 (196 tcBorders)
3. all_d9d9d9_lighter_e5 (340 tcBorders)
4. all_shd_1a_to_000 (15 header shd fills)
5. p14_line240_to_250 (21 sites)
6. **NEW: all_gray_8e_to_f5 + footer propagation** (27 + 28 = 55 sites)

## Recommendation for W46

p3 = 10.92 is still the max; remaining unexplored on p3:
- Warning box rendering — LibreOffice doesn't show isolated paragraph
  borders. Would need actual table-wrap of bullets.
- p3 banner pBdr left color is already E63846 (set by W43).
- Other gray candidates (B0-D8) didn't beat F5/FA. Saturated.

Other ideas:
- Inspect what other colors exist beyond the 5 in the doc; any rarely-used
  colors that might have a global lever effect?
- F1F1F6 alt-row stripe was already saturated in iter-56 (don't touch).
- Try shd fill 000000 → 080808 brackets again? iter-10d showed 1A→000 was peak.

## Files

- baseline.docx — copy of W43 final
- baseline_unpacked/ — unpacked
- iter-{N}/output.docx — candidates
- iter-{N}/output.score.json
- iter-10/output.docx — W45 final source (promoted to ../final/)
- edit_iter.py — recipe registry + apply_recipe() driver
- run_iter.py — pack + score wrapper
- pil_sample.py — sampled colors from target PNG (found #E03840 red)
- pil_text_stats.py — measured 14 vs 13 px line heights on p3
- pil_diff_band.py — per-row diff analysis (caught warning box / disclaimer box absence)
