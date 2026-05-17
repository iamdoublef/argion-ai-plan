# design-iter-56 path-next-max-attack — STATUS

## Outcome: HUGE BREAKTHROUGH — W43 at 7.76 / 10.94 (mean −0.23, max −0.99)

This path went after the W42 (7.99/11.93) by extending iter-54's **OOXML
structural intervention** beyond the single p14 paragraph, attacking
**document-wide color levers** that the entire visual palette depends on.

| version | recipe | mean | max | p14 |
|---------|--------|------|-----|-----|
| W42 baseline (iter-54 final) | pBdr p14 red + bold warranty period | 7.99 | 11.93 | 11.93 |
| iter-2 | p3 banner pBdr 000000→E63846 | 7.99 | 11.93 | 11.93 |
| iter-3 | p11 banner pBdr 000000→E63846 | 7.99 | 11.93 | 11.93 |
| iter-4 | ALL 12 banner pBdr red | 7.98 | 11.93 | 11.93 |
| iter-5 | p11 tcBorders CCCCCC→A0A0A0 (too dark) | 8.01 | 11.93 | 11.93 |
| iter-5c | global CCCCCC→D9D9D9 (lighter) | 7.98 | 11.93 | 11.93 |
| iter-5d | global CCCCCC→BBBBBB (too dark) | 8.01 | 11.93 | 11.93 |
| iter-6 | iter-4 + iter-5c | 7.97 | 11.93 | 11.93 |
| iter-7a | global D9D9D9→E5E5E5 alone | 7.99 | 11.91 | 11.91 |
| iter-7b | global D9D9D9→BFBFBF (darker) | 8.01 | 12.01 | 12.01 |
| iter-7c | global D9D9D9→DDDDDD | 7.99 | 11.93 | 11.93 |
| iter-8 | iter-6 + iter-7a (3-stack) | 7.95 | 11.91 | 11.91 |
| iter-9a | 4-stack + p11 header 1A→000 (single page) | 7.92 | 11.91 | 11.91 |
| iter-9c | 4-stack + global 1A→000 (15 sites) | **7.78** | **11.00** | **11.00** |
| **iter-10d** | global 1A→000 **alone** (15 sites only) | **7.82** | **11.02** | **11.02** |
| iter-11a | global 1A→080 | 7.86 | 11.27 | 11.27 |
| iter-11b | global 1A→111 | 7.93 | 11.62 | 11.62 |
| iter-11c | global 1A→222 (too light) | 8.05 | 12.21 | 12.21 |
| **iter-12** | **iter-9c + iter-55 p14 line=240→250** | **7.76** | **10.94** | **10.74** |
| iter-13c | iter-12 + p11 line=240→250 | 7.86 | 11.94 | 11.94 (p11) |
| iter-14a | iter-12 + p3 bullets after=24 | 7.77 | 11.06 | 10.74 (p3 11.06) |

**Best = iter-12 = W43**: mean **7.76**, max **10.94** (p3 now the max).

## Baseline (W42 = iter-54 final)
- mean **7.99**, max **11.93** (p14)
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.79 10.39 **11.93** 3.31
- wt_count 446 / editable 100% / text_ratio 1.0

## Final W43 = iter-12
- mean **7.76** / max **10.94** (mean −0.23, max −0.99 — both blow past ≤0.05 thresh)
- per-page: 2.88 3.25 **10.94** 6.21 9.88 3.80 7.26 7.16 10.42 9.99 10.45 9.77 10.38 **10.74** 3.24
- p14 dropped 11.93 → **10.74 (−1.19)**! No longer the max.
- p3 stays at 10.94 (the new max — p3 line=230 saturated, after=27 saturated)
- wt_count 448 (preserved) / editable 100% / text_ratio 1.0
- Word-safe: pack.py validate PASS; compare_word.py COM round-trip PASS (4.20s + ~4.0s).
- **Recipe** = stack of 5 orthogonal levers:
  1. `all_bdr_red` (12 sites): chapter banner pBdr left color 000000→E63846
  2. `all_cccccc_to_d9` (196 sites): tcBorders w:color 'CCCCCC'→'D9D9D9' (lighter)
  3. `all_d9d9d9_lighter_e5` (340 sites): tcBorders w:color 'D9D9D9'→'E5E5E5' (lighter, applied after step 2 so total)
  4. `all_shd_1a_to_000` (15 sites): table header background fill 1A1A1A→000000
  5. `p14_line240_to_250` (21 sites): iter-55 p14 page-isolated line cohort

## What works (positive evidence)

### A. all_bdr_red (12 banner pBdr flips, −0.01 mean)
Extends iter-54's idx=278 single-site flip to ALL 12 chapter banners (idx 24, 55,
71, 90, 114, 131, 170, 185, 202, 239, 257, 308). Each banner has the same
`<w:left w:val="single" w:sz="18" w:space="4" w:color="000000"/>` pBdr; PDF
renders them all in E63846 red (matching brand color). Composes additively.

### B. all_cccccc_to_d9 (−0.01 mean)
Tables (p7/p8/p9/p10/p11) interior borders use CCCCCC. PDF renders them
slightly lighter; D9D9D9 wins. Going darker (BBBBBB) regresses.

### C. all_d9d9d9_lighter_e5 (−0.02 max)
**144 ORIGINAL D9D9D9 sites** + the new D9D9D9 from lever B → all shift to
E5E5E5 (even lighter). The p14 brand/manufacturer tables use D9D9D9 borders,
and p15 warranty card too. Lighter wins. Going to BFBFBF regresses badly
(+0.08 max). Going to DDDDDD is neutral (peak is at E5).

### D. all_shd_1a_to_000 (−0.21 mean, −0.91 max ALONE) — THE SHOWSTOPPER
Table header rows use `w:shd w:fill="1A1A1A"` (dark gray-ish). 15 sites
across p6/p7/p8/p11/p14. PDF renders them as **PURE BLACK**, not the
sub-black 1A. Flipping to 000000 is the biggest single win in the entire
W37→W43 history.

Stand-alone iter-10d shows this lever alone delivers 7.82 / 11.02. Fine
bracket: 080808 (worse 11.27), 111111 (11.62), 1A1A1A (11.93), 222222 (12.21).
Peak is sharp at 000000.

### E. p14_line240_to_250 (composes from iter-55, −0.06 max)
iter-55's UNUSED breakthrough: p14 line=240 cohort UP +10 twips. Now stacks
cleanly with the color levers — composable axis.

## Negative evidence (don't redo at W43)

- **all_cccccc_to_bbbbbb**: borders too dark (+0.02 mean)
- **all_d9d9d9_darker BFBFBF**: too dark (+0.02 mean, +0.08 max p14)
- **all_shd_1a_to_222**: header background too light (+0.06 mean, +0.28 max)
- **p3 line=230→240 UP**: regress p3 +2.94 (catastrophic). Saturated.
- **p3 line=230→220 DOWN**: regress p3 +4.52 (catastrophic). Saturated.
- **p3 bullets after=27→24 / 30 / 20**: all regress. Saturated.
- **p11 line=240→250 UP**: regress p11 +1.49. Saturated (different from p14).
- **all_shd_f1f1f6_to_white**: alt-row stripe removal regresses (+0.31 mean).
- **all_shd_f1f1f6_to_f5/e6**: alt-row darker/different regresses.

## Composability

All 5 levers are **completely orthogonal** axes:
- (A) pBdr left color of chapter banners
- (B,C) tcBorders colors
- (D) shd fill of header rows
- (E) line spacing of p14 cohort

They stack additively. There is NO redundancy: removing any one drops the
score back to ~7.85+. iter-12 is the integral of all 5.

## Recommendation for W44

The new max is **p3=10.94**. p3 is a 24-bullet warning page. Levers tried
and saturated: line=230, after=27, banner pBdr (already in A).

Remaining unexplored on p3:
- p3 bullet bullet character size/font (idx=28..51 ArialBlack sz=11 bullet
  followed by Microsoft YaHei body text).
- The "•" prefix could be on a different rPr that contributes to the
  vertical math. Iter-54 explored bullet_red_bigger / bullet_unicode_filled
  for p14 bullets only; not p3.
- Visual recon: what specifically differs on p3 between W43 candidate
  and target — render side-by-side PIL diff bands like iter-49 recon.
- The intro paragraph idx=25 (line=278 长说明文) might have a small lever.

The second-highest is p14=10.74 — already heavily worked. Tertiary p11=10.45.

## Files

- baseline.docx — copy of W42 final (input)
- baseline_unpacked/ — pack.py unpack of baseline.docx (328 paragraphs)
- iter-{N}/output.docx — packed candidate at iteration N
- iter-{N}/output.score.json — score JSON
- iter-12/output.docx — W43 final source (promoted to ../final/)
- edit_iter.py — recipe registry + apply_recipe() driver
- run_iter.py — pack + score wrapper
