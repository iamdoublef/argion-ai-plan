# design-iter-49 path-before-linerule-surgery — STATUS

## Outcome: DOUBLE BREAKTHROUGH — W40 at 8.01/11.98 (mean -0.16 from W37)

This path produced **two stacked wins** by adding `p9 line=264→252` (7 sites) on top
of two successive rPr stacks from parallel agents:

| version | recipe | mean | max |
|---------|--------|------|-----|
| W37 baseline | (committed) | 8.17 | 11.97 |
| W38 (other agent) | sz=14/10/13 Goldilocks rPr stack | 8.09 | 11.99 |
| W38 + p9 surgery (this run, iter-stack-w38) | + line=264→252 (7 sites) | **8.04** | 11.99 |
| W39 (other agent) | + sz=14 BLACK 9→10 / sz=10 RED 7→6 | 8.06 | 11.98 |
| **W40 (this run, iter-stack-w39) — current final** | W39 + line=264→252 (7 sites) | **8.01** | **11.98** |

Total mean drop W37 → W40: **−0.16**. Max W37 → W40: **+0.01** (within ≤0.05 rollback).
The `p9 line=264→252` lever composes cleanly with ALL tested rPr stacks — independent
axis, additive ~−0.05 mean each time.

## Baseline (W37 HEAD, c5f82bc)
- committed JSON: mean **8.17**, max **11.97**
- iter-render at run-time: mean 8.18, max 11.97
- per-page (run-time): 2.88 3.25 11.58 6.33 10.32 4.33 7.71 7.85 11.49 10.00 10.99 9.97 10.60 11.97 3.31
- wt_count 446 / editable 100% / text ratio 1.0

## Standalone iter-10 (W37 baseline, no rPr stack)
- iter-render: mean **8.12** / max **11.97** (held). Confirms p9 line=264 surgery alone
  gives −0.06 mean vs W37. p9 11.49 → 10.71 (−0.78).

## Final W39 = iter-stack-w38 (W38 baseline + p9 surgery stacked)
- mean **8.04** / max **11.99**
- per-page: 2.88 3.25 11.07 6.26 10.04 4.33 7.71 7.85 **10.60** 10.02 10.91 9.93 10.48 11.99 3.31
- **p9 dropped 11.35 → 10.60 (−0.75 ON TOP of W38)**
- wt_count 446 / editable 100% / text ratio 1.0 / Word-safe (docx2pdf OK)
- Recipe: take W38 final (Goldilocks rPr stack), then paragraphs idx 169..183 (p9 cohort),
  `<w:spacing w:line="264"...>` → `w:line="252"`. 7 sites modified.
- **Key finding**: pPr line-cohort surgery and rPr font-cohort surgery operate on
  independent axes and compose cleanly — they don't double-count or interfere.

## Iterations (W37 baseline 8.17/11.97 LO-rendered as 8.18)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | recon (no edit) | — | — | — | data: before/lineRule distribution mapped |
| 2 | before=80→60, before=160→120 (tighten cohort) | 17 | 8.45 | 13.62 | regression (+0.27 mean, +1.65 max) |
| 3 | before=80→100, before=160→200 (loosen cohort) | 17 | 8.43 | 13.43 | regression (+0.25 mean) |
| 4 | lineRule="auto"→"exact" global | 292 | 10.56 | 15.46 | CATASTROPHE (+2.38 mean) |
| 5 | lineRule="auto"→"atLeast" global | 292 | 10.21 | 19.65 | CATASTROPHE (+2.03 mean, +7.68 max) |
| 6 | p11 (203..232) line=240→220 surgical | 30 | 8.32 | 13.16 | regression on p11 (+2.17) |
| 7 | p11 (203..232) line=240→260 surgical | 30 | 8.35 | 13.73 | regression on p11 (+2.74) |
| 8 | p3 (28..51) line=230→226 surgical | 24 | 8.29 | 13.32 | regression on p3 (+1.74) |
| 9 | p9 (169..183) line=264→256 surgical | 7 | 8.15 | 11.97 | **GAIN −0.03 mean** (p9 −0.25) |
| 10 | p9 (169..183) line=264→252 surgical | 7 | **8.12** | **11.97** | **GAIN −0.06 mean** (p9 −0.78) |
| 11 | p9 (169..183) line=264→240 surgical | 7 | 8.20 | 12.00 | regression past sweet spot |
| stack-w38 | iter-10 patch (p9 line=264→252) ON W38 final (Goldilocks rPr) | 7 | **8.04** | **11.99** | **STACKED GAIN −0.05 vs W38** |
| stack-w39 | iter-10 patch (p9 line=264→252) ON W39 final (sz=14/10 stack) | 7 | **8.01** | **11.98** | **STACKED GAIN −0.05 vs W39 (W40)** |

## What works (positive evidence)
**Per-page differential on p9's `line=264` cohort**. This is the operation page,
7 paragraphs at line=264 (bullets + numbered steps) sitting alongside larger
line=278/240 paragraphs. The PDF renders these tighter than the W36 auto-264;
tightening to 252 (−12 twips, ≈0.6pt) snaps p9 from 11.49 → 10.71.

Sweet spot is between −8 (iter-9, gain −0.03) and −12 (iter-10, gain −0.06).
Pushing to −24 (iter-11, snap to 240) regresses (+0.49 on p9). The 264 cohort
has finite slack: ~12 twips downward.

## Negative evidence (confirmed dead-ends)

### w:before cohort (saturated)
- before=80→60 + before=160→120 (tighten): +0.27 mean, +1.65 max
- before=80→100 + before=160→200 (loosen): +0.25 mean
- **Conclusion**: w:before cohort lever is bidirectionally saturated. The 17
  nonzero sites (out of 111 total w:before sites) are at local optima.

### w:lineRule global switching (FATAL)
- "auto" → "exact" globally (292 sites): +2.38 mean, +3.49 max. Reason: line=240
  twips becomes fixed 12pt regardless of font size; collapses headings (>12pt
  natural) and pushes content out of position.
- "auto" → "atLeast" globally (292 sites): +2.03 mean, +7.68 max. Reason:
  paragraphs grow taller when natural metrics exceed minimum (e.g. p14 jumped
  11.97 → 19.65). DO NOT REVISIT.

### Single-paragraph surgery on hot pages
- p3 line=230 cohort (24 bullet sites): −4 twips → p3 +1.74. Cohort saturated.
- p11 line=240 cohort (30 table-row sites): ±20 twips both regress (+2.17 / +2.74).
  Troubleshooting table is in tight equilibrium — both densify and dilate hurt.
- p9 line=264 cohort (7 sites): **THIS IS THE EXCEPTION** — works −8 to −12 twips.

### Unexplored angles (for future iterations)
- p14 single-paragraph surgery (table rows + warranty bullets, 30 paragraphs)
- p3 line=278 cohort (only 2 sites — small surface)
- p9 line=278 cohort (3 sites)
- after=120 cohort (23 sites globally), after=176 cohort (13 sites)
- p14 after=80 cohort (3 sites — section headings on warranty page)
- Cumulative stacking: iter-10 (p9 −12) + p14 differential

## Word safety
All 11 iterations: pack.py validate PASS (328 paragraphs preserved). iter-10
final passed docx2pdf (MS Word COM) conversion cleanly.

## Recommendation for W40
1. **p14 differential surgery**: p14 now at 11.99 max. Try after=80→60 on
   the 3 section-heading paragraphs (idx 280, 291, 300).
2. **Apply line=264→252 logic to OTHER non-baseline-cohort line values**:
   line=271 (17 sites), line=230 (37 sites) — but per iter-8 evidence,
   line=230 cohort is saturated. line=271 (idx unknown) is untested.
3. **after=120 cohort tuning** (23 sites scattered across chapter subtitles).
4. **DO NOT** revisit: lineRule global (FATAL), before cohort (saturated),
   p11/p3 line surgery (saturated this run).
