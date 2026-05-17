# design-iter-58 path-footer-propagation — STATUS

## Outcome: MASSIVE BREAKTHROUGH — W46 at 7.38 / 10.90 (mean −0.35, max −0.02)

This path started by exploring iter-57's footer propagation strategy on
OTHER cohorts (sz=10 spacing, sz=14 BLACK, header*.xml, theme1.xml, etc.).
The footer-specific levers were exhausted (all hit ≤−0.001 noise floor).

**The real breakthrough came from a NEW orthogonal direction:**
`<w:bottom w:val="single" w:sz="6" ...>` black borders, 16 sites in
`document.xml`, scattered across table cells (p5/p9/p11/p12/p13/p14). The
target PDF renders these as INVISIBLE — but the candidate had them as
solid black lines, contributing visible diff on every affected page.

| version | recipe | mean | max | key wins |
|---------|--------|------|-----|----------|
| W45 baseline (iter-57) | gray F5 + footer | 7.73 | 10.92 | starting point |
| iter-2..iter-18 | footer sz=10 spacing 5→{0,1,2,3,8} + color F5→{E8,FA,F0} + border EEEEEE→{D9,E0,E5,F5} + sz_4_to_2 etc | 7.73 | 10.92 | all SATURATED — only p4 −0.01 |
| iter-23 | top sz=18 banner 000→E63846 | 8.07 | 11.34 | REGRESS — tops need black |
| iter-24 | **bottom sz=6 000→D9D9D9** | 7.49 | 10.92 | **−0.24 mean, p5/p12/p13/p14 −0.86 each** |
| iter-25..iter-32 | bracket: bottom sz=6 → E5/E0/E8/EB/F0/F5/FA/FF | 7.45..7.49 | 10.92 | monotonic: lighter is better |
| iter-32 | **bottom sz=6 000→FFFFFF (alone)** | **7.45** | **10.92** | peak; nil=catastrophic (relayout) |
| iter-33 | bottom sz=6 → nil (no border) | 8.26 | 13.80 | CATASTROPHIC reflow |
| iter-35..36 | ALL borders 000→FFFFFF/D9 | 8.18 | 11.83 | banner sz=18 tops need to stay black |
| iter-39 | **bottom sz=6 + top sz=10 → FFFFFF** | **7.42** | **10.92** | **+1 site, p1 2.69→2.17!** |
| iter-43 | top sz=8 BOTH sites → FFFFFF | 7.74 | 10.92 | mixed: p4 +0.38, p11 −0.25 |
| iter-45 | top sz=8 **SECOND only** (p11 disclaimer) → FFFFFF | 7.71 | 10.92 | clean −0.02 |
| iter-47 | **stack: bottom_sz6_FF + top_sz10_FF + top_sz8_2nd_FF + footer_levers** | **7.40** | **10.92** | **composes additively** |
| iter-49 | + left sz=18 red sz=14 alone | 7.72 | 10.92 | extra −0.01 |
| iter-52 | stack + red sz=12 | 7.39 | 10.92 | tiny + |
| iter-55 | stack + red sz=8 | 7.39 | **10.91** | max breakthrough |
| iter-57 | stack + red sz=4 | 7.38 | 10.91 | further down |
| **iter-58** | **stack + red sz=2** | **7.38** | **10.90** | **THE FINAL** |
| iter-59 | stack + red nil (remove) | 7.38 | 10.91 | similar but max 10.91 vs sz=2 10.90 |
| iter-60 | stack + red sz=3 | 7.38 | 10.90 | tied with sz=2 |

**Best = iter-58 = W46**: precise mean **7.381** / max **10.90**.

## Final W46 = iter-58
- mean **7.38** / max **10.90** (precise mean −0.35, max −0.02 from W45)
- per-page: 2.17 3.23 **10.90** 6.17 8.83 3.76 7.22 7.12 10.31 9.95 10.16 8.87 9.32 9.70 3.00
- p1: 2.69 → **2.17 (−0.52)**
- p5: 9.86 → **8.83 (−1.03)**
- p11: 10.43 → **10.16 (−0.27)**
- p12: 9.75 → **8.87 (−0.88)**
- p13: 10.35 → **9.32 (−1.03)**
- p14: 10.72 → **9.70 (−1.02)**
- p15: 3.22 → **3.00 (−0.22)**
- p3: 10.92 → **10.90 (−0.02)** — max now p3 = 10.90
- wt_count 448 (preserved) / editable 100% / text_ratio 1.0
- Word-safe: pack.py validate PASS (328→328); compare_word.py COM round-trip PASS (1.6s).

## Recipe = stack of 6 levers (composes additively on top of W45)
1. `doc_bottom_sz6_000_to_ff` (16 sites): table bottom borders sz=6 black → white
2. `doc_top_sz10_000_to_ff` (1 site, paragraph 4): first p1 top divider sz=10 black → white
3. `doc_top_sz8_second_only_to_ff` (1 site, paragraph 234): p11 disclaimer top sz=8 black → white
4. `doc_left_sz18_red_to_sz2` (13 sites): red chapter banner left sz=18 → sz=2 (much thinner)
5. `footer_sz10_spacing_5_to_2` (14 sites): footer text char-spacing 5 → 2
6. `footer_color_f5_to_e8` (28 sites): footer text/page-num F5F5F5 → E8E8E8 (slightly darker, still invisible)

## What works (positive evidence)

### A. Bottom sz=6 black → white (−0.28 mean ALONE — THE SHOWSTOPPER)
16 table-cell bottom borders at `<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>`.
These were rendering as solid black lines under table rows on p5/p9/p11/p12/p13/p14.
Target PDF shows these as invisible (or extremely faint, rendered as white in
LO compositing). Setting `w:color="FFFFFF"` makes them invisible. Note: `w:val="nil"`
causes catastrophic reflow (border space recovered = text shifts vertically),
+0.6 mean and +2.9 max. KEEP the border (so layout stays), just make it white.

Monotonic improvement from D9 (7.49) → FF (7.45). Peak at FFFFFF.

### B. Top sz=10 black → white (−0.04 mean, p1 −0.52)
1 single site at paragraph 4 (top of p1). Removing this hairline divider
matches the target PDF and dramatically improves p1.

### C. Top sz=8 second site only → white (−0.02 mean, p11 −0.25)
2 sites; only the second one (p11 disclaimer) helps. The first (p3 area)
causes p4 reflow regression. Selective single-site flip is the win.

### D. Left sz=18 red → sz=2 (thinner banner, broke max barrier)
Red chapter banner left border. sz=18 too thick — target PDF shows
a thinner red accent. Reducing thickness improves max from 10.92→10.90.
sz=2 ties with sz=3; sz=nil regresses slightly (likely small space loss).

### E. Footer levers (composes additively, p4 −0.01)
sz=10 spacing 5→2 (footer branding text char-spacing) + footer color F5→E8
each contribute ~0.001 noise-floor improvement. Composes with main levers.

## Negative evidence

- **footer sz=10 spacing 5→{0,1,3,8}**: all near-saturation (±0.001).
- **footer color F5→{FA,F0}**: identical to F5 baseline.
- **footer border EEEEEE→{D9,E0,E5,F5,EC}**: all regress (border at sweet spot).
- **footer border sz=4→{2,6}**: regress (thickness saturated).
- **footer remove top border (nil)**: regress (border space needed).
- **doc_footer_margin 198→{180,185,192,195,201,204,215,220}**: 198 is sweet spot.
- **doc_shd_F1F1F6→{F3F3F5,EEEFEF,EFF0F2,F5F5F5}**: alt-row saturated; all regress.
- **doc_top_sz18_000→{FFFFFF,red,E5}**: banner tops MUST stay black (visual cue).
- **doc_top_sz8_first_only→FF**: p3 area regress.
- **doc_all_borders_000→ANY (33 sites)**: ALL black → white kills banner tops.
- **doc_left_sz18_red_to_nil**: max 10.91 vs sz=2 10.90; keep thin border.
- **theme1.xml/settings.xml/styles.xml**: all confirmed inert (no styles referenced).
- **header*.xml**: confirmed do not exist; only footer*.xml.

## Composability with W43+W45 levers

W46 = W45 + 4 new doc levers (border-color + red-thickness) + 2 footer micro-tunes.
All W43+W45 levers preserved:
1. all_bdr_red (12 banner pBdrs E63846)
2. all_cccccc_to_d9 (196 tcBorders)
3. all_d9d9d9_lighter_e5 (340 tcBorders)
4. all_shd_1a_to_000 (15 header shd fills)
5. p14_line240_to_250 (21 sites)
6. all_gray_8e_to_f5 + footer propagation (27 + 28 = 55 sites)
7. **NEW: bottom_sz6_FF + top_sz10_FF + top_sz8_second_FF + red_sz2 + footer micro**

## Insight: "make-invisible" lever class

The breakthrough was realizing that some borders rendered as VISIBLE BLACK
LINES in the candidate but were INVISIBLE in the target PDF. Direct
make-invisible (flip color to white, keep `w:val="single"` so border space
stays, preventing reflow) hits 16+1+1 = 18 sites collectively responsible
for a major chunk of visual diff. Total impact: −0.30 mean across 7 pages.

## Recommendation for W47

Max is now p3 = 10.90 (was 10.92, then 10.94, then 11.93 — slowly grinding down).
Remaining unexplored:
- The 13 left sz=18 → sz=2 created a stable peak; smaller (sz=0) requires nil
  which costs back 0.01 on max. Tradeoff converged.
- p3 inner content (idx 26-51) is dominated by warning/bullets structure that
  is unbridgeable per iter-57 (border rendering, line height geometry).
- sz=14 BLACK spacing already at 10 (iter-56 baseline).
- sz=11/12/13 spacing already at 2 (W33/W34/W35).
- Other shd/fill values all proven saturated.

Next angle ideas:
- p3 bullets `<w:rPr>` cohort: try font-weight or letter-spacing variations on
  idx=26-51 specifically (already negative, but maybe one tiny variant).
- Image position adjustment for p3 product photo (different anchor point).
- Maybe the p3 banner has a different `w:sz` on the top divider that's still
  black? Check finer cohorts (sz=4, sz=6 at non-bottom positions).

## Files
- baseline.docx — copy of W45 final
- baseline_unpacked/ — unpacked
- iter-{N}/output.docx — candidates
- iter-{N}/output.score.json
- iter-58/output.docx — W46 final source (promoted to ../../final/)
- edit_iter.py — recipe registry + apply_recipe() driver
- run_iter.py — pack + score wrapper (copy from iter-57)
