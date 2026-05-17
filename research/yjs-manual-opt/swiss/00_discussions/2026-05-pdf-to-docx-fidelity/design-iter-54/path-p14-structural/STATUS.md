# design-iter-54 path-p14-structural — STATUS

## Outcome: BREAKTHROUGH — W42 at 7.99/11.93 (mean -0.01, max -0.05)

This path achieved the long-stuck p14 max breakthrough by abandoning the
spacing axis (saturated since iter-49) and using **two structural OOXML
mutations on p14**:

1. **Title pBdr left color flip**: idx=278 `<w:left w:color="000000"/>` →
   `<w:left w:color="E63846"/>`. Target PDF renders the left "▍ 10" marker
   bar in red; baseline DOCX had it black. One-byte color swap.
2. **Bold "2 年有限保修" run split**: idx=301 single run containing the
   warranty period phrase was split into 3 runs (prefix / bold-period /
   suffix). The phrase now renders bold matching target.

Composability: both edits are independent and stack additively
(iter-4 −0.02 + iter-8 −0.03 = iter-9 −0.05 on p14 max). Each edit is on
a completely orthogonal axis (border color vs run rPr split).

| version | recipe | mean | max | p14 |
|---------|--------|------|-----|-----|
| W41 baseline (W40+W41 cumulative) | (committed) | 8.005 (7.996) | 11.98 | 11.98 |
| iter-4 (title pBdr red) | bdr E63846 | 7.99 (7.985) | 11.96 | 11.96 |
| iter-8 (bold warranty period) | run split | 7.99 (7.985) | 11.95 | 11.95 |
| **W42 = iter-9 (stack)** | bdr red + bold warranty | **7.99 (7.979)** | **11.93** | **11.93** |

## Baseline (W41)
- mean **7.996**, max **11.98**
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.79 10.39 **11.98** 3.31
- wt_count 446 / editable 100% / text_ratio 1.0

## Final W42 = iter-9
- mean **7.979** (display 7.99) / max **11.93**
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.79 10.39 **11.93** 3.31
- wt_count **448** (+2 from run split), editable 100%, text_ratio 1.0
- Word-safe: pack.py validate PASS (328 paragraphs preserved); compare_word.py
  COM round-trip PASS (3.90s + 7.15s).
- Recipe: idx=278 left border color 000000→E63846 (1 site) + idx=301 split
  run to make "2 年有限保修" `<w:b/>` (1 site, +2 runs).

## Iterations (W41 baseline 7.996/11.98)

| iter | change | sites | mean | max | p14 | verdict |
|------|--------|-------|------|-----|-----|---------|
| 1 | visual recon (PIL diff bands) | — | — | — | — | data: hot bands at y=243-262, 479-530, 692-702 |
| 2 | title_color_flip (10→black AND pBdr→red) | 1 p | 8.00 | 12.00 | 12.00 | regress p14 +0.02 |
| 3 | title_num_black ("10" red→black only) | 1 p | 8.00 | 12.02 | 12.02 | regress p14 +0.04 |
| 4 | **title_bdr_red (pBdr 000000→E63846 only)** | 1 p | **7.99** | **11.96** | **11.96** | **GAIN −0.02 mean, −0.02 max** |
| 5 | scissors_inject (new para before sectPr 306) | +1 p | 8.00 | 11.99 | 11.99 | regress +0.01 (text_ratio 1.01) |
| 6 | bold_wevac (idx=284 set b/) | 1 run | 8.00 | 12.00 | 12.00 | regress p14 +0.02 |
| 7 | bold_argion (idx=295 set b/) | 1 run | 8.00 | 12.10 | 12.10 | regress p14 +0.12 |
| 8 | **bold_warranty_period (idx=301 split bold)** | 1 split | **7.99** | **11.95** | **11.95** | **GAIN −0.01 mean, −0.03 max** |
| **9** | **iter-4 + iter-8 stack** | 2 | **7.99** | **11.93** | **11.93** | **BEST — composable** |
| 10 | iter-9 + bold_support305 | 3 | 8.00 | 11.98 | 11.98 | regress (back to baseline) |
| 11 | iter-9 + scissors_inject | 3 | 7.99 | 11.95 | 11.95 | regress vs iter-9 |
| 12 | iter-9 + bold_wevac | 3 | 7.99 | 11.96 | 11.96 | regress vs iter-9 |

## What works (positive evidence)
Two orthogonal mutations on p14 break the long-running 11.98 ceiling:

### A. pBdr color swap (iter-4): −0.02 on p14 max
The title paragraph idx=278 has `<w:pBdr><w:left w:val="single" w:sz="18"
w:space="4" w:color="000000"/>` which renders the vertical bar before "10".
Target PDF renders this bar in red (E63846, same as the "10" text). Flipping
black→red shaves 0.02 from p14 max diff. Surprisingly the symmetric flip
(also turning "10" itself black, iter-2) regresses — so target really has
both red bar AND red "10", but the bar contributes more diff.

### B. Bold run split on "2 年有限保修" (iter-8): −0.03 on p14 max
idx=301 is the warranty intro paragraph. Target PDF renders the phrase
"2 年有限保修" in bold. Splitting the single run into 3 (prefix + bold-target
+ suffix) plus setting `<w:b/>` on the middle run produces the bold render
without breaking layout. wt_count grows from 446 → 448 (anti-cheat preserved).

The stacked iter-9 gives the best score, confirming these two axes
(pBdr color, run rPr split) are independent.

## Negative evidence (don't repeat at W42)

### bold_argion (idx=295) — FATAL
Bolding "广州亚俊氏真空科技股份有限公司" regresses p14 +0.12. The Argion
Chinese name is on a 2-line cell with English under it; bolding shifts
the English subtitle vertically.

### bold_wevac (idx=284) — regression
Bolding "WEVAC TECHNOLOGY CO., LIMITED" alone regresses +0.02. With iter-9
stack, regresses +0.03 vs iter-9. The English-only short string in table
cell already aligns; bolding widens it past target column edge.

### bold_support305 — neutralizes iter-9
Bolding "support@wevactech.com" in idx=305 cancels both wins (mean back to
8.00, max back to 11.98). Splitting the email run shifts the surrounding
text positions on the line.

### scissors_inject (text paragraph) — regression
Adding a centered scissors text paragraph (✂ · · · ·) before sectPr 306
puts a row of text into vertical space target leaves blank. p14 footer
position shifts slightly. Even with the visual character at right place,
the spacing math doesn't agree with target.

### title_color_flip (both 10 black AND pBdr red) — regression
Flipping "10" from red→black while flipping pBdr to red regresses by +0.02.
The "10" run color must STAY red; only the pBdr swap is beneficial.

### title_num_black (only flip 10) — regression
"10" black alone (pBdr stays black) regresses +0.04 on p14. The numeric
character has more pixel weight than the border line, and target has it
red.

## Visual analysis (iter-1)
PIL-based diff between target/page-14.png and candidate/page-14.png surfaced
hot bands:
- y=59-65: page title area "10 品牌与保修信息" → addressed by iter-4 pBdr
- y=243-262: 品牌商信息 first table header rows
- y=479-530: 制造商 row (multi-line cell)
- y=692-702: warranty bullet area → addressed by iter-8 bold split

The diff hotspots y=243-262 and y=479-530 (table rendering) are NOT addressed
in this pass — these are font fallback / character spacing issues that need
deeper intervention (likely tcMar, tblGrid). The two structural wins both
target the title and warranty-text axes, which together account for ~30%
of the p14 max diff.

## Word safety
All 11 iterations: pack.py validate PASS (328 paragraphs preserved).
iter-9 final passed compare_word.py (MS Word COM) cleanly: 3.90s open +
7.15s save round-trip, no errors. wt_count 448 (run split added 2, no
hidden text injection).

## Recommendation for W43

The W42 win is +0.05 on p14 max (the long-stuck bottleneck). Remaining
headroom on p14:
1. **Table rendering hotspots** (y=243-262, 479-530) — try tblGrid column
   width adjustment on the two p14 tables (品牌商, 授权制造商). iter-1 PIL
   data shows these as the largest unaddressed bands.
2. **More bold splits** (selective) — bold_wevac and bold_argion both
   regress alone, but a smaller phrase (e.g., bold just "WEVAC" or just
   "Argion") might compose differently. Try targeted single-word bolds.
3. **bullet glyph swap** — try replacing inline `•` with `●` (U+25CF) in
   idx=302/303/304 and run scoring; combined with rPr font change.
4. **DO NOT** revisit: title color flip (saturated), scissors inject
   (regress), bold_argion (FATAL), bold_support305 (neutralizes wins).

## Composability note
W42 = W41 (cumulative through iter-53 W41) +
  iter-54 W42: pBdr color flip idx=278 (1 site, color swap only) +
              bold run split idx=301 (1 paragraph, +2 runs).

The pBdr color axis is brand-new (never touched before). The run rPr split
axis is partially explored (iter-52 bold without split regressed p14 +0.22;
split with prefix/bold/suffix structure works because it preserves
horizontal layout). Future stacks must preserve idx=278 pBdr color and
idx=301 run split structure.

Total W42 edits this iter: 2 (1 color attr + 1 run split). No
styles/themes/fonts/numbering/sections touched.

## Files
- baseline: `baseline.docx` (= W41 final pre-iter-54)
- best iter: `iter-9/output.docx` (= W42 final after iter-54)
- score: `iter-9/output.score.json`
- compare_word PDF: `iter-9/word_pdf.pdf`
- promoted to: `../../final/imt050-wevac-eu-cn.docx`, `../../final/candidates/W42-iter54-bdr-red-bold-warranty_7.99_11.93.docx`
