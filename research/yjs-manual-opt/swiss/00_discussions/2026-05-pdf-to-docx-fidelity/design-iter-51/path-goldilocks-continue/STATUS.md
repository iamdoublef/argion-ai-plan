# design-iter-51 path-goldilocks-continue — STATUS

## Outcome: WIN at iter-5 (W39)

**Accepted**: `iter-5/output.docx`
- Scores: **mean 8.09 → 8.06 / max 11.99 → 11.98** (W38 → W39)
- Mean **-0.03**, max **-0.01** — both metrics improved simultaneously.
- No per-page regression ≥ 0.05 vs W38.
- Gates: pack validate.py PASS (328 paragraphs), Word COM render PASS (4.52s), editable 100%, wt_count=446.
- Upgraded `final/imt050-wevac-eu-cn.docx` W38 → W39; staged as
  `final/candidates/W39-iter51-goldilocks-continue-stack_8.06_11.98.docx`
- Preview PDF refreshed at `final/imt050-wevac-eu-cn.preview.pdf`.

## Baseline (W38 final, iter-50/iter-6 output)
- score: mean **8.09**, max **11.99**
- per-page: 2.88 3.25 11.07 6.26 10.04 4.33 7.71 7.85 11.35 10.02 10.91 9.93 10.48 11.99 3.31
- wt_count: 446, editable 100%

## Recon at W38 (iter-1, 444 rPr blocks — unchanged structure)
Confirmed cohort positions on entry:
- sz=14 BLACK Arial sp=9: 62
- sz=14 BLACK ArialBlack sp=9: 9     (combined sz=14 BLACK sp=9: **71**)
- sz=13 BLACK Arial sp=9: 33
- sz=13 BLACK ArialBlack sp=10: 17
- sz=10 RED ArialBlack sp=7: 37
- sz=11 RED ArialBlack sp=2: 35
- sz=13 GRAY (1A1A1A) Arial sp=2: 117
- sz=15 BLACK ArialBlack sp=5: 27
- sz=22 BLACK ArialBlack sp=11: 13
- sz=27 RED ArialBlack sp=11: 13

## Iterations (W38 baseline 8.09/11.99)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | recon only (confirm W38 cohorts) | - | - | - | informational |
| 2 | sz=14 BLACK ArialBlack-only 9→10 (font-split, mirror sz=13) | 9 | 8.09 | 11.99 | inert (only 9 sites) |
| 3 | sz=14 BLACK ALL 9→10 (full cohort, was expected to crash) | 71 | **8.07** | **11.98** | SURPRISE WIN |
| 4 | sz=10 RED 7→6 DOWN (continue DOWN direction) | 37 | **8.08** | 11.99 | win -.01 mean, p3 -.11 |
| **5** | **iter-3 + iter-4 stack (sz=14 9→10 + sz=10 7→6)** | **71+37** | **8.06** | **11.98** | **WIN (mean -.03, max -.01)** |
| 6 | sz=10 RED 7→5 DOWN (overshoot check) | 37 | 8.11 | 11.99 | regress p3 +.43 |
| 7 | sz=13 BLACK ArialBlack 10→11 (continue UP from W38) | 17 | 8.09 | 11.99 | inert, saturated |
| 8 | sz=13 BLACK Arial 9→10 (W38 known crash, re-confirm) | 33 | 8.19 | 12.47 | regress p3 +1.40 |
| 9 | iter-5 + sz=13 AB 10→11 stack | 71+37+17 | 8.06 | 11.98 | tied with iter-5 (inert add) |
| 10 | iter-5 + sz=11 RED 2→3 explore | 71+37+35 | 8.14 | 12.05 | regress p13 +.26, p5 +.34 |

## Per-page accepted (iter-5 vs W38)
```
W38:    2.88 3.25 11.07 6.26 10.04 4.33 7.71 7.85 11.35 10.02 10.91 9.93 10.48 11.99 3.31
iter-5: 2.88 3.25 10.96 6.23 9.90  4.33 7.71 7.85 11.22 10.01 10.92 9.93 10.39 11.98 3.31
delta:  0    0    -.11 -.03 -.14  0    0    0    -.13  -.01  +.01  0    -.09  -.01  0
```
**No regression ≥ 0.05.** p5 -.14 (biggest win), p9 -.13, p3 -.11, p13 -.09, p4 -.03, p10/p14 -.01. p11 +.01 (under threshold). Net mean **-0.03**, max **-0.01**.

## Sweet-spot updates (W39)
- **sz=14 BLACK Goldilocks sweet spot now at sp=10**, not sp=9. W38 had hypothesized sp=9 ceiling based on sz=13 analogue; reality is sz=14 has one more click of slack than sz=13. This is the key W39 discovery — extrapolation by size class is asymmetric.
- **sz=10 RED Goldilocks sweet spot now at sp=6**, after 8→7 (W38) → 7→6 (W39). 7→5 over-shoots (p3 +.43). The DOWN direction valley bottoms out near sp=6.
- **Font asymmetry rule reaffirmed**: sz=13 Arial vs ArialBlack still split — Arial cannot move from 9, ArialBlack tolerates 10 but not 11. Different fonts have different ceilings.

## Stacking confirmed (cumulative wins through W39)
W39 = W38 (iter-50 stack: sz=14 8→9 + sz=10 8→7 + sz=13 AB 9→10) +
  iter-51 W39: sz=14 BLACK 9→10 (71 sites, all fonts) +
  iter-51 W39: sz=10 RED 7→6 (37 sites)

Total W39 surgical edits since pre-baseline: 71 (sz=14 8→10) + 37 (sz=10 8→6) + 17 (sz=13 AB 9→10) + ... [cumulative across all weeks].

## Negative evidence (don't repeat at W39)
- **sz=10 RED 7→5** over-shoots — keep at sp=6 (W39 sweet spot)
- **sz=13 BLACK Arial 9→10** still crashes — Arial saturated since W37
- **sz=13 BLACK ArialBlack 10→11** inert (saturated at 10)
- **sz=11 RED 2→3** regresses p5/p9/p13 multi-page — saturated at 2
- **sz=15 BLACK 5→6** confirmed forbidden (W37 evidence)

## Word safety
- Pack-time validate.py: 328 → 328 paragraphs PASS
- Word COM render: 4.52s open + save round-trip, no errors
- wt_count = 446 (unchanged), editable 100%, text_ratio 1.0
- All edits pure `<w:spacing w:val>` swaps inside rPr — no styles/themes/fonts/sections/images touched
- 108 surgical edits this iter (71 + 37 across 2 cohorts)

## Next angles (if asked to continue at W39 baseline 8.06/11.98)
1. **sz=14 BLACK 10→11** — the recent W39 +1 click win opens question whether sz=14 has yet more slack (sz=13 ArialBlack saturated at 10; sz=14 with larger size might tolerate 11)
2. **sz=10 RED 6→5 isolated** — iter-6 stacked 7→5 was too much; isolated 6→5 from W39 base untested
3. **sz=14 BLACK split by font on 10→11** — if 10→11 over-shoots ALL, try ArialBlack-only (9 sites) like sz=13's AB-only strategy
4. **Per-page targeted attack**: residual hot pages are p3 (10.96), p5 (9.90), p9 (11.22), p11 (10.92), p13 (10.39), p14 (11.98). p14 has been stable at 11.99 for many weeks — needs different intervention (likely image alignment or specific paragraph)
5. **GRAY body sz=13 sp=2** (117 sites, locked since W34/W35) — highest site count, never half-step tested
6. **sz=22/27 sp=11** — saturated controls but never tested DOWN direction (11→10)
7. **Cross-cohort interactions**: now that sz=14 and sz=10 stack additively, test triple-stack with sz=15 BLACK or GRAY body to see if non-overlapping cohorts always compose
