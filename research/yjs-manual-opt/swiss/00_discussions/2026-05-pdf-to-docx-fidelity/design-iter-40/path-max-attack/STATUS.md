# design-iter-40 path-max-attack — STATUS

## Outcome: BREAKTHROUGH — TWO STACKED WINS

### W34 (iter-16, STACKED): mean 8.28 → 8.20 (-0.08), max 12.14 → 12.06 (-0.08)
**Stacked iter-9 (p13/p9 line tune) on iter-41's W33 (sz=11/12 spacing tighten)**
- Both improvements present: mean -0.08 AND max -0.08
- Per-page wins: p9 -0.30, p13 -0.77, p14 -0.08 (max), p5 -0.04
- gates: validate PASS, Word COM open PASS (6.25s), editable 100%, wt_count=446
- Promoted: `final/imt050-wevac-eu-cn.docx` W33 → W34
- Staged: `final/candidates/W34-iter40-stacked-on-iter41_8.20_12.06.docx`

### iter-9 (standalone, W33b): mean 8.28 → 8.21 (-0.07), max 12.14 unchanged
Baseline iter-9 win on its own (without iter-41 stack)
- Staged: `final/candidates/W33-iter40-p13-p9-line-tune_8.21_12.14.docx`

## Context correction
Task spec referenced W31 baseline 8.49/12.26 (the keycap-chip iter-38 result), but
between task spec and execution **iter-39 W32 (8.28/12.14) became the actual final**.
The active `final/imt050-wevac-eu-cn.docx` was W32, and that's what we used.

## Baseline (W32, post iter-39)
- score: mean 8.28, max 12.14 (p14 12.14 hardest, p9 11.81 second)
- per-page: 2.88 3.25 11.69 6.34 10.38 4.35 7.73 7.83 11.81 10.02 11.09 9.96 11.40 12.14 3.34
- max sources: p14 (12.14), p9 (11.81), p3 (11.69)

## Iteration log

| iter | change | mean | max | verdict |
|------|--------|------|-----|---------|
| 1 | p11 tcW 1596/2395/3265 → 1500/2800/2956 | 8.36 | 12.35 | ❌ p11 +1.26 |
| 2 | p11 tcW → 1700/2200/3357 | 8.30 | 12.14 | ❌ p11 +0.34 |
| 3 | p3 w:line 230 → 225 (tighten) | 8.39 | 13.35 | ❌ p3 +1.66 |
| 4 | p3 w:line 230 → 240 (loosen) | 8.45 | 14.17 | ❌ p3 +2.48 |
| 5 | p13 w:line 271 → 265 (tighten) | 8.37 | 12.76 | ❌ p13 +1.36 |
| **6** | **p13 w:line 271 → 278 (loosen)** | **8.23** | **12.14** | **✅ -0.05 mean** |
| 7 | p13 271 → 285 (more loosen) | 8.24 | 12.14 | ⚠ worse than iter-6 |
| 8 | iter-6 + p9 271 → 278 | 8.29 | 12.76 | ❌ p9 +0.95 |
| **9** | **iter-6 + p9 271 → 264 (tighten)** | **8.21** | **12.14** | **✅ -0.07 mean** |
| 10 | iter-9 + p14 278 → 271 | 8.28 | 13.20 | ❌ p14 +1.06 |
| 11 | iter-9 + p14 278 → 285 | 8.25 | 12.69 | ❌ p14 +0.55 |
| 12 | iter-9 + p5 271 → 278 | 8.23 | 12.14 | ❌ p5 +0.34 |
| 13 | iter-9 + p5 271 → 264 | 8.35 | 12.45 | ❌ p5 +2.07 |
| 14 | iter-9 + p10 264 → 271 | 8.24 | 12.14 | ❌ p10 +0.40 |
| 15 | iter-9 + failure tbl line 240 → 245 | 8.22 | 12.14 | ❌ p11 +0.19 |
| **16** | **STACK iter-9 ON iter-41 W33 base** | **8.20** | **12.06** | **✅ both dims win** |

## Per-page accepted (iter-9 vs W32)
```
W32:    2.88 3.25 11.69 6.34 10.38 4.35 7.73 7.83 11.81 10.02 11.09 9.96 11.40 12.14 3.34
iter-9: 2.88 3.25 11.69 6.34 10.38 4.35 7.73 7.83 11.48 10.02 11.09 9.96 10.65 12.14 3.34
delta:  .00  .00  .00   .00  .00   .00  .00  .00  -.33  .00   .00   .00  -.75  .00   .00
```

## Key findings

1. **Page-specific line spacing direction matters**:
   - p13 wants LOOSEN (271 → 278): -0.75 page diff
   - p9 wants TIGHTEN (271 → 264): -0.33 page diff
   - Same paragraph type (sz=14 bullets with w:line=271), opposite optima
   - **Hypothesis**: depends on number of wrap lines per page. If page is just under
     fitting one extra line, loosening helps move text onto next line matching PDF.

2. **All other pages at local optimum**:
   - p3 line=230: tightening (-5) catastrophic (+1.66), loosening (+10) catastrophic (+2.48)
   - p5 line=271: both directions regress (+0.34 / +2.07)
   - p10 line=264: tighten or loosen both regress
   - p14 line=278: both directions catastrophic regress

3. **p11 tcW saturated**: original 1596/2395/3265 column widths are tightly tuned;
   any perturbation (smaller or larger spread) causes +0.34 to +1.26 regression.

4. **Sweet spot is sparse**: only p9 and p13 yielded improvements among 6 attack pages.
   p14 (the actual current max) shows no obvious lever.

## Word safety
- Word COM rendering: 6.6 seconds, no errors, opens cleanly in MS Word.
- Pack-time validate.py: 328→328 paragraphs, all validations PASS.
- No settings.xml/scheme/page edits; pure pPr w:line surgical edit on 15 paragraphs
  (11 in p13, 4 in p9).

## Diff vs W32
- 11 lines changed in p13 region (`w:line="271"` → `w:line="278"`)
- 4 lines changed in p9 region (`w:line="271"` → `w:line="264"`)
- 15 total line edits, no other modifications

## Acceptance verification
- ✅ mean 8.21 < 8.28 baseline (-0.07)
- ✅ max 12.14 = 12.14 (no max regression)
- ✅ no per-page > +0.05 regression
- ✅ wt_count = 446 (≥300)
- ✅ editable_pct = 100%
- ✅ text ratio = 1.0
- ✅ pages 15:15
- ✅ Word COM open PASS

## Next angles
1. **p14 (12.14 hardest)** — the only true max ceiling left. Line spacing both
   directions regress; try w:before/after micro-tune instead, or rPr w:spacing
   on p14-specific runs.
2. **p3 (11.69) and p11 (11.09)** — locally saturated for line spacing; try
   `w:after` lever (currently 27/32/40) or letter-spacing on sub-cohorts.
3. **Differential cross-page rPr w:spacing** — some pages liked 5→8 (iter-39's win),
   others (p10/p12) regressed at 5→8. Try 5→9 ONLY on p13 cohort, 5→7 elsewhere.
4. **Per-page sectPr pgMar fine-tune** — iter-36 found global optimum; per-page
   adjustments (use multiple sectPr blocks) might unlock new gains.
5. **w:kern** in rPr — never tried.

## Working files
- Best docx: `iter-9/output.docx`
- Apply scripts: `iter-9/apply.py` (15-line edit, stacks p13 loosen + p9 tighten)
- Word verify: `iter-9/output_word.pdf`
