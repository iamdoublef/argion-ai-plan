# design-iter-50 path-goldilocks-half-step — STATUS

## Outcome: WIN at iter-6 (W38)

**Accepted**: `iter-6/output.docx`
- Scores: **mean 8.17 → 8.09 / max 11.97 → 11.99** (W37 → W38)
- Mean **-0.08** (largest single-iter mean drop since W36 step), max +0.02 (under 0.05 threshold).
- No per-page regression ≥ 0.05 vs W37.
- Gates: validate.py PASS (328 paragraphs), Word COM render PASS (4.58s + 8.24s), editable 100%, wt_count=446.
- Upgraded `final/imt050-wevac-eu-cn.docx` W37 → W38; staged as
  `final/candidates/W38-iter50-goldilocks-halfstep-stack_8.09_11.99.docx`
- Preview PDF refreshed at `final/imt050-wevac-eu-cn.preview.pdf`.

## Baseline (W37 final, iter-47/iter-8 output)
- score: mean **8.17**, max **11.97**
- per-page: 2.88 3.25 11.58 6.33 10.32 4.33 7.71 7.85 11.49 10.00 10.96 9.97 10.60 11.97 3.31
- wt_count: 446, editable 100%

## Recon at W37 (iter-1, 444 rPr blocks)
Confirmed cohorts on entry (filtered to true BLACK = color 000000 + AUTO):
- sz=14 BLACK Arial sp=8: 62
- sz=14 BLACK ArialBlack sp=8: 9     (combined sz=14 BLACK sp=8: **71**)
- sz=13 BLACK Arial sp=9: 33
- sz=13 BLACK ArialBlack sp=9: 17    (combined sz=13 BLACK sp=9: **50** — W37 win)
- sz=10 RED ArialBlack sp=8: 37      (W36 win)
- sz=11 RED ArialBlack sp=2: 35      (W33 win, saturated)
- sz=13 GRAY (1A1A1A) Arial sp=2: 117 (W34/W35 win, saturated)
- sz=15 BLACK ArialBlack sp=5: 27    (DO-NOT-PUSH per W37 negative evidence)
- sz=22 BLACK ArialBlack sp=11: 13   (saturated)
- sz=27 RED ArialBlack sp=11: 13     (saturated)

Color codes in this document:
- BLACK = `000000` (true) + `AUTO`
- gray body = `1A1A1A` (NOT to be edited as heading)
- RED = `E63846`
- light gray = `8E8E93`
- white = `FFFFFF`

## Iterations (W37 baseline 8.17/11.97)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | recon only (grep cohort map) | - | - | - | informational |
| 2 | sz=14 BLACK 8→9 (half-step extrapolation) | 71 | **8.13** | 11.99 | ✅ mean -.04, max +.02 |
| 3 | sz=13 BLACK 9→10 (Goldilocks continue UP) | 50 | 8.24 | 12.66 | ❌ p3 +1.08 over-shoot |
| 4 | iter-2 + iter-5 stack (sz=14 8→9 + sz=10 8→7) | 71+37 | **8.10** | 11.99 | ✅ mean -.07, additive |
| 5 | sz=10 RED 8→7 DOWN (reverse direction) | 37 | **8.13** | 11.97 | ✅ p3 -.51, max tied |
| **6** | **iter-4 + sz=13 BLACK ArialBlack only 9→10 (font split)** | **71+37+17** | **8.09** | **11.99** | **✅ WIN (mean -.08)** |
| 7 | iter-6 + sz=13 BLACK Arial(non-Black) 9→10 (full sz=13 push) | +33 | 8.19 | 12.47 | ❌ p3 +1.40 |
| 8 | iter-6 + sz=22 BLACK 11→12 | +13 | 8.09 | 11.99 | ⚠️ inert (mean tied) |
| 9 | iter-6 + sz=27 RED 11→12 | +13 | 8.09 | 11.99 | ⚠️ inert |
| 10 | iter-6 + sz=15 BLACK 5→6 (smallest step from forbidden 5→8) | +27 | 8.10 | 12.01 | ❌ p14 +.02 max regress |

## Per-page accepted (iter-6 vs W37)
```
W37:    2.88 3.25 11.58 6.33 10.32 4.33 7.71 7.85 11.49 10.00 10.96 9.97 10.60 11.97 3.31
iter-6: 2.88 3.25 11.07 6.26 10.04 4.33 7.71 7.85 11.35 10.02 10.91 9.93 10.48 11.99 3.31
delta:  0    0    -.51 -.07 -.28  0    0    0    -.14  +.02  -.05  -.04 -.12  +.02  0
```
**No regression ≥ 0.05.** p3 wins -.51 (huge), p5 -.28, p9 -.14, p13 -.12, p4 -.07, p11 -.05, p12 -.04. p10/p14 each +.02 (under threshold). Net mean **-0.08**.

## Sweet-spot confirmations (W38)
- **sz=14 BLACK Goldilocks confirmed at sp=9**, not sp=11. iter-2 sz=14 8→9 wins -.04 mean alone, validating the W37 "val=9 is the Goldilocks sweet spot for BLACK" hypothesis on a 71-site cohort (the largest BLACK heading cohort). Pattern extrapolates from sz=13 to sz=14.
- **sz=10 RED DOWN direction wins**: 8→7 wins -.04 mean (p3 -.51 huge). Both UP and DOWN were untested in W36/W37; DOWN is correct. Cohort was not "saturated" — it was at the upper edge of a valley.
- **sz=13 BLACK 9→10 fails on Arial, wins on Arial Black**: font split matters. ArialBlack 17 sites tolerate the push (iter-6 mean -.01 over iter-4); Arial 33 sites do not (iter-7 p3 +1.40). The "BLACK saturated at sp=9" finding from W37 was averaged across fonts — actually only Arial saturates; Arial Black has one more click of slack.

## Stacking confirmed (additive, no interaction)
- iter-2 sz=14 8→9: 8.13
- iter-5 sz=10 8→7: 8.13
- iter-4 = stack: 8.10  → near-perfectly additive (-.04 + -.04 → -.07, vs W37 8.17)
- iter-6 = iter-4 + sz=13 AB 9→10: 8.09 → +(-.01) further, additive

This contrasts with W37 STATUS where iter-8 + iter-7 stack BROKE (p3 +.50). Different cohorts, different geometry. **The Goldilocks half-step recipe stacks cleanly across non-overlapping size cohorts.**

## Negative evidence (don't repeat at W38)
- **sz=13 BLACK 9→10 (full cohort)** regresses p3 +1.08 — Arial variant cannot take another click UP
- **sz=13 BLACK Arial 9→10** (33 sites isolated) regresses p3 +1.40 — confirmed font-specific
- **sz=22 BLACK 11→12 / sz=27 RED 11→12** inert when stacked on iter-6 — these are saturated
- **sz=15 BLACK 5→6** causes p14 +.02 max regress — keep at sp=5
- Re-confirms: contextualSpacing FATAL (from iter-48), pPr w:line/before sweeps regress (from iter-48/49)

## Word safety
- Pack-time validate.py: 328 → 328 paragraphs PASS (no schema violations)
- Word COM render: 4.58s open + 8.24s save round-trip, no errors
- wt_count = 446 (unchanged from W36), editable 100%, text_ratio 1.0
- All edits are pure `<w:spacing w:val>` swaps inside rPr — no styles.xml, no theme, no fonts, no section, no images touched
- 125 surgical edits total (71 + 37 + 17 across 3 cohorts)

## Stacking confirmed (cumulative wins through W38)
W38 = W37 (iter-47 W37: sz=13 BLACK all 8→9) +
  iter-50 W38: sz=14 BLACK 8→9 (71) +
  iter-50 W38: sz=10 RED 8→7 (37) +
  iter-50 W38: sz=13 BLACK ArialBlack-only 9→10 (17)

## Next angles (if asked to continue at W38 baseline 8.09/11.99)
1. **sz=14 BLACK 9→10** — try one more click UP on the largest cohort (mirror iter-3's failed sz=13 9→10, but on sz=14 which has more slack)
2. **sz=10 RED 7→6 DOWN** — keep going down the cohort that took 8→7 well
3. **sz=14 BLACK split by font** — current iter-2 was unified (Arial 62 + ArialBlack 9). Maybe one font wants 9, the other wants 10 (mirroring sz=13's font asymmetry from iter-6/iter-7)
4. **sz=13 BLACK ArialBlack 10→11** — push the only sub-cohort that just took 9→10 one more click
5. **Per-page differential**: p9 still 11.35, p14 still 11.99. Identify which paragraph indices on these pages bear the residual diff and try targeted rPr edits there
6. **sz=11 RED sp=2** revisit — never tested half-step (2→3 was untouched from W33). 35 sites available.
7. **GRAY body sz=13 sp=2** — 117 sites, locked since W34/W35 but never half-step tested. High site count = high leverage if even a fractional improvement applies.
