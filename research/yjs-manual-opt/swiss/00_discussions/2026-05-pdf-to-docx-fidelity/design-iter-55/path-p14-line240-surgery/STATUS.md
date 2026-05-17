# design-iter-55 path-p14-line240-surgery — STATUS

## Outcome: BREAKTHROUGH — W43 at 7.98 / 11.68 (stacked on iter-54 W42)

Page-isolated **p14 line=240 cohort (21 sites) → 250** (UP +10 twips, ≈0.5pt looser
auto-line). Both axes improved.

**Stacking result (W43, shipped)**: applied on top of HEAD W42 (iter-54 path-p14-structural,
7.99/11.93). Final = **mean 7.98 / max 11.68**. p14 11.93 → 11.68 (−0.25). Word-safe
(compare_word PASS), wt_count 448 (≥300).

**Standalone result (on W41)**: my patch alone on W41 (8.00/11.98) gave 7.98/11.71
(p14 −0.27). Confirms composability — both iter-54 (structural) and iter-55 (line
spacing) gains stack cleanly because they touch disjoint paragraphs on p14.

The iter-49 / iter-53 page-isolated-line-cohort heuristic continues to work: PDF
renders the p14 WARRANTY tables and bullet trio looser than W41's auto-240; loosening
to 250 (+10 twips) closes the gap.

## Convergence note vs parallel iter-54

This run and the parallel iter-54 (p14 structural) BOTH targeted page 14. We
were warned not to touch the same elements, and recon confirmed disjoint cohorts:
- iter-54 touched p14 structural elements (different cohort)
- iter-55 touched p14 line=240 cohort (21 body-text sites idx 281..304 minus 291/300/301)

Result: the two patches compose. W41 (8.00/11.98) → W42 iter-54 (7.99/11.93) →
W43 iter-55 stacked (7.98/11.68). Cumulative max reduction: −0.30 across both runs.

## Baseline used by this run (W41 = HEAD final, 032aed3 + downstream)
- mean **8.00** (display) / max **11.98**
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.79 10.39 **11.98** 3.31
- wt_count 446 / editable 100% / text ratio 1.0

## Final achieved by this run = iter-4 = W42
- mean **7.98** / max **11.71** (p14 dropped 11.98 → 11.71, −0.27)
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 9.79 10.39 **11.71** 3.31
- wt_count 446 / editable 100% / text ratio 1.0 / Word-safe (compare_word.py PASS)
- Recipe: paragraphs idx 281..304 minus {291, 300, 301} (p14 sub-cohort,
  21 sites: 18 table rows + 3 bullets), `<w:spacing w:line="240" ...>` → `w:line="250"`.

## Iterations (W41 baseline 8.00/11.98)

| iter | change                              | sites | mean | max   | verdict                |
|------|-------------------------------------|-------|------|-------|------------------------|
| 1    | recon (no edit)                     | —     | —    | —     | mapped p14 line=240 (21 sites total: 18 table rows + 3 bullets) |
| 2    | p14 line=240→230 full (DOWN)        | 21    | 8.04 | 12.62 | regression (p14 +0.64) |
| 3    | *(skipped — see iter-2 result)*     | —     | —    | —     | DOWN saturated         |
| 4    | **p14 line=240→250 full (UP half)** | 21    | **7.98** | **11.71** | **GAIN −0.02 mean, −0.27 max — BEST** |
| 5    | p14 line=240→260 full (UP)          | 21    | 8.01 | 12.20 | regression (past peak) |
| 6    | p14 line=240→245 (fine bracket)     | 21    | 7.99 | 11.96 | gain but smaller than 250 |
| 7    | p14 line=240→255 (fine bracket)     | 21    | 8.00 | 12.06 | past peak              |
| 8    | p14 line=240→248 (fine bracket)     | 21    | 7.99 | 11.83 | gain but smaller than 250 |
| 9    | p14 line=240→252 (fine bracket)     | 21    | 7.99 | 11.89 | past peak              |
| 10   | p14 line=240→250 tables-only (18 sites) | 18 | 7.99 | 11.96 | regression vs full 21 — bullets matter |
| stack| iter-4 recipe applied on HEAD W42 (iter-54) | 21 | **7.98** | **11.68** | **GAIN composes — W43 final, p14 11.93 → 11.68** |

## What works (positive evidence)

**Page-isolated cohort surgery on p14 line=240 in the UP direction.** The 21 sites
break down as:

- **Table 1 (品牌商, 10 rows)**: idx 281..290 — `before=None after=0`
- **Table 2 (制造商, 8 rows)**: idx 292..299 — `before=None after=0`
- **Bullets (3 items)**: idx 302..304 — `before=0 after=5`

Loosening line=240 → 250 (+10 twips, ≈0.5pt extra leading on auto rule) slightly
expands each row/bullet, matching how the PDF rendered slightly looser. Crucially,
**all 21 must move together** — iter-10 (tables-only 18 sites) recovers only half
the gain (7.99 / 11.96). The 3 bullets contribute a measurable share.

Peak is sharp at exactly 250: 245/248/252/255 all give partial gains; 230 and 260
both regress.

## Negative evidence

- **DOWN direction (230) saturates immediately**: p14 +0.64. Tightening makes the
  table rows + bullets too close together, the PDF rasterizes more vertical gap.
- **Tables-only sub-cohort (18 sites)**: only recovers 50% of the gain. The bullets
  carry independent value.
- **Past the sweet spot (255+)** regresses cleanly. The peak is at +10 twips.

## Composability

The patch stacks on top of W41 (which already contained iter-49's p9-line, iter-52's
sz=14 BlackArial rPr, and iter-53's p12-line=271→260 patches). No interference.

## Word safety

iter-4 passed `compare_word.py` (MS Word COM) conversion cleanly. pack.py validate
PASS at every iteration (328 paragraphs preserved).

## Recommendation for W43

p14 max=11.71 is still the bottleneck max. Remaining surgical levers worth probing:

1. **p3 (10.96)** — line=230 page-isolated sub-cohort (24 sites on p3). Brief noted
   p3 line=230 saturated globally in iter-49; page-isolated has not been tried.
2. **p11 (10.92)** — table-heavy troubleshooting page; explore line cohort surgery.
3. **p14 line=278 mini-cohort** (idx 279, 280, 291, 300, 301, 305 — the 6 line=278
   "section heading + body text" sites on p14). NOT tried; might compose with this
   iter-55 patch.
4. **p14 after=176** on idx 277 (the CH.10 banner) — single-site probe.

**Do not** revisit: p14 line=240 (now saturated at 250), p14 after=80 (saturated
in iter-53), line=271 global (saturated), after=120 (FATAL).
