# design-iter-48 path-pPr-spacing — STATUS

## Outcome: NO BREAKTHROUGH at W36 (8.18/11.97) after 10 iterations

Strong negative evidence: paragraph-level `pPr w:spacing` cohorts are saturated at the
W36 baseline. Both global and differential per-page surgical edits fail to improve mean
or max. Best result is **tie** (iter-8). All other iterations regress.

## Baseline (W36 final, from iter-46/path-docx-skill-continue/iter-10)
- mean **8.18**, max **11.97**
- per-page: 2.88 3.25 11.67 6.29 10.32 4.33 7.71 7.85 11.49 10.00 10.99 9.97 10.60 11.97 3.31
- wt_count: 446, editable 100%

## pPr recon (328 paragraphs total)
- 328 paragraphs, 328 have pPr, 307 carry `<w:spacing>`, 0 carry `<w:contextualSpacing>`
- **w:line cohorts**: 240×175, 278×45, 230×37, 271×17, 264×16
- **w:before cohorts**: 0×93, 80×10, 160×7
- **w:after cohorts**: 0×138, 27×37, 32×32, 120×23, 40×22, 80×17, 176×13
- **w:lineRule**: auto×292 (all `auto`, no `exact` or `atLeast`)

## Section/page mapping (sectPr-bearing paragraph indices)
[9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
→ page 14 = paras 277..306 (worst page at 11.97)

## Iterations (W36 baseline 8.18/11.97)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | line=240 → 232 (global tighten -8) | 175 | 8.93 | 13.15 | regression (huge) |
| 2 | line=240 → 248 (global loosen +8) | 175 | 8.49 | 13.02 | regression |
| 3 | line=240 → 242 (global loosen +2) | 175 | 8.29 | 12.06 | regression |
| 4 | line=230 → 232 (global +2) | 37 | 8.27 | 13.19 | regression (p3 +1.5) |
| 5 | line=278 → 271 (global -7) | 45 | 8.42 | 13.07 | regression |
| 6 | after=27 → 20 (global -7) | 37 | 8.40 | 14.54 | regression (p3 +2.87) |
| 7 | contextualSpacing add on line=240 cohort | 175 | 13.40 | 31.87 | CATASTROPHE |
| 8 | page-14 only line=240 → 244 (+4 differential) | 23 | **8.18** | **11.97** | tie (inert) |
| 9 | page-14 only line=240 → 250 (+10 differential) | 23 | 8.21 | 12.55 | regression on p14 |
| 10 | page-14 only line=240 → 236 (-4 differential) | 23 | 8.24 | 12.90 | regression on p14 |

## Negative evidence (for future agents)

1. **line=240 cohort is saturated**. Both directions regress globally even with ±2 step.
   Movement of ±8 produces +0.31..+0.75 mean regression.
2. **line=230 cohort is saturated**. +2 produces p3 +1.5 regression (cohort sits at p3 hot zone).
3. **line=278 cohort is saturated**. -7 regresses to 8.42.
4. **after=27 cohort is saturated**. -7 regresses badly (p3 +2.87, max +2.57).
5. **contextualSpacing is FATAL at any scale**. Adding it to 175 sites moved
   mean from 8.18 → 13.40 (+5.22) and max from 11.97 → 31.87 (+19.90). Even with
   correct schema position (after spacing/ind, before jc). LO collapses paragraph
   spacing too aggressively. **DO NOT REVISIT.**
6. **Differential p14 line=240** is inert at +4 (tie) and regresses at ±10/±4 magnitude.
   The page-14 line=240 cohort has no usable slack via pPr line.
7. **Schema gotcha**: contextualSpacing must come AFTER `w:ind` (or `w:spacing` if no ind),
   BEFORE `w:jc/textDirection`. CT_PPrBase order. iter-7 v1 failed with pack-time
   validation error.

## Untested angles (out of scope for this run)
- `w:before` lever (untouched globally; recon shows 111 sites with values 0/80/160/400)
- `w:lineRule="exact"` / `"atLeast"` switching (currently all `auto`)
- Other worst-page differentials (p3, p9, p11 paragraphs)
- after=32 cohort (32 sites), after=120 cohort (23 sites), after=176 cohort (13 sites)
- Single-paragraph surgical edits inside p14 cohort (which paragraph is the actual
  hot spot, not all 23 of them)

## Word safety
All 10 iterations: pack.py validate PASS (328 paragraphs preserved), no styles/scheme
edits. iter-7 failed validate (schema order) — caught at pack-time, never made it
to render. All produced docs were Word-safe to the extent renderable.

## Recommendation
**pPr w:spacing lever is exhausted at W36 baseline.** Future iterations should target:
- `w:before` cohort (truly untested)
- `w:lineRule` switching (truly untested)
- Per-page differential on `p3` (next worst page at 11.67) using OTHER levers
- Image hack / drawing relocation (different mechanism entirely)
- Section pgMar deltas (W30 stacked, but maybe per-section narrower margin shifts)
