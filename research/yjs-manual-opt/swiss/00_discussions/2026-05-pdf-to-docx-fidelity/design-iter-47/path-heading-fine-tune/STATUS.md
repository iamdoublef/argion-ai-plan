# design-iter-47 path-heading-fine-tune — STATUS

## Outcome: WIN at iter-8 (W37)

**Accepted**: `iter-8/output.docx`
- Scores: **mean 8.18 → 8.17 / max 11.97 → 11.97** (W36 → W37)
- Mean -0.01, max tied. No regressions ≥ 0.05.
- Gates: validate.py PASS (328 paragraphs), Word COM render PASS (3.11s + 6.55s), editable 100%, wt_count=446
- Upgraded `final/imt050-wevac-eu-cn.docx` W36 → W37; staged as
  `final/candidates/W37-iter47-sz13-black-8to9_8.17_11.97.docx`

## Baseline (W36 final, iter-46/iter-10 output)
- score: mean 8.18, max 11.97
- per-page: 2.88 3.25 11.67 6.29 10.32 4.33 7.71 7.85 11.49 10.00 10.99 9.97 10.60 11.97 3.31
- wt_count: 446, editable 100%

## Cohort recon after W36 (444 rPr blocks total)
Confirmed iter-46 already landed:
- sz=22 BLACK Arial Black sp=11: 13
- sz=27 RED Arial Black sp=11: 13
- sz=10 RED Arial Black sp=8: 37 (all moved to sp=8)
- sz=13 BLACK Arial sp=8: 33
- sz=13 BLACK Arial Black sp=8: 17 (combined: 50 BLACK at sp=8)
- sz=14 BLACK sp=8: 62 (W32 win, saturated)
- sz=11 RED sp=2: 35 (W33 win, saturated)
- sz=13 GRAY sp=2: 117 (W34/W35 win, saturated)
- sz=15 BLACK sp=5: 27 (DO-NOT-PUSH negative evidence)

## Iterations (W36 baseline 8.18/11.97)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | recon only (grep current state) | - | - | - | informational |
| 2 | sz=10 RED Arial Black 8→11 | 37 | 8.20 | 12.00 | ❌ p3 +.33 (over-tightens at val=11) |
| 3 | sz=13 BLACK 8→11 (Arial+Arial Black) | 50 | 8.24 | 12.60 | ❌ p3 +.93 (severe over-tighten) |
| 4 | sz=22 BLACK 11→10 | 13 | 8.18 | 11.98 | ⚠️ tied mean, max +.01 p14 |
| 5 | sz=22 BLACK 11→12 | 13 | 8.18 | 11.97 | ⚠️ effectively tied; p5 +.01 |
| 6 | sz=27 RED 11→10 | 13 | 8.18 | 11.98 | ⚠️ tied mean, max +.01 p14 |
| 7 | sz=10 RED 8→9 | 37 | 8.18 | 11.97 | ⚠️ rounds same; unrounded slightly worse (p3 +.07) |
| **8** | **sz=13 BLACK 8→9 (Arial+Arial Black)** | **50** | **8.17** | **11.97** | **✅ WIN (mean -.01, max tied)** |
| 9 | iter-8 + sz=10 RED 8→9 stack | 50+37 | 8.21 | 12.08 | ❌ p3 +.50 (stacking breaks) |
| 10 | iter-8 + sz=30/36 orphans 5→8 | 50+1+1 | 8.17 | 11.97 | ⚠️ ties iter-8; p1 +.02 (orphan UP slight cost) |

## Per-page accepted (iter-8 vs W36)
```
W36:    2.88 3.25 11.67 6.29 10.32 4.33 7.71 7.85 11.49 10.00 10.99 9.97 10.60 11.97 3.31
iter-8: 2.88 3.25 11.58 6.33 10.32 4.33 7.71 7.85 11.49 10.00 10.96 9.97 10.60 11.97 3.31
delta:  0    0    -.09 +.04  0     0    0    0    0     0     -.03  0    0     0     0
```
**No regressions ≥ 0.05.** p3 wins -.09; p11 wins -.03. p4 +.04 (under threshold). Net mean -.01.

## Sweet spot findings (W37)
- **sz=13 BLACK (all fonts) sp=8 → sp=9 wins** — smaller increment beats 8→11
  - This is the "Goldilocks" between iter-46 finding (5→8 wins) and iter-3 (8→11 over-shoots)
- **sz=22 BLACK 11→{10,12} both tied** — val=11 is local optimum, no improvement in either direction
- **sz=27 RED 11→10 ties mean, slight max regression** — val=11 is local optimum
- **sz=10 RED 8→9 ties unrounded slightly worse** — cohort is saturated at val=8
- **sz=10 RED 8→11 regresses (p3 +.33)** — over-tighten, similar to sz=13 8→11 pattern
- **Stacking sz=13 8→9 with sz=10 8→9 breaks** — interaction effect, not additive

## Pattern (heading cohorts after W37)
- sz=22/27 saturated at sp=11 (val=11 is the precise optimum)
- sz=13 BLACK saturated at sp=9 (one click tighter than W36's sp=8 — half-step improvement)
- sz=10 RED saturated at sp=8 (W36's value is optimal; cannot push 9 or 11 without regression)
- sz=14 BLACK saturated at sp=8 (W32 win, unchanged)

The "sp=9" Goldilocks finding suggests sz=13 lives on a different curve than sz=22/27.
Smaller heading sizes need smaller spacing perturbations.

## Word safety
Word COM rendering: 3.11 + 6.55 = ~10s pipeline, no errors. Pack-time validate.py: 328→328
paragraphs PASS. No styles.xml/scheme/page/font edits. Pure rPr w:spacing surgical edits on
50 sites (sz=13 BLACK Arial 33 + Arial Black 17).

## Stacking confirmed (cumulative wins)
W37 contains W36 (iter-46 5→11 22/27, BLACK 13 5→8, RED 10 5→8) +
**iter-47 W37: sz=13 BLACK 8→9 (Goldilocks step)**.

## Negative evidence captured (for future agents)
- sz=10 RED 8→11 regresses p3 +.33 — must use sp=8 (or sp=9 if accept p3 +.07)
- sz=13 BLACK 8→11 regresses p3 +.93 — severe over-tighten
- sz=22 BLACK 11→{10,12} both tied — local optimum
- sz=27 RED 11→10 slight max regression — local optimum
- sz=13 BLACK 8→9 + sz=10 RED 8→9 stack breaks (p3 +.50) — interaction effect
- sz=30/36 orphan 5→8 costs p1 +.02 — orphan headings prefer sp=5

## Next angles (if asked to continue)
1. **sz=13 BLACK 9→10** — try one more click UP from W37 win
2. **sz=14 BLACK 8→9** — extend Goldilocks pattern to next size cohort
3. **sz=15 BLACK 5→6 / 5→7** — smallest possible step from forbidden 5→8
4. **mixed Arial vs Arial Black split** — split sz=13 cohort by font to find finer optimum
5. **sz=10 RED 8→7 DOWN** — opposite direction, since both 9/11 hurt
6. **sz=22/27 finer split (Arial Black variants)** — already homogeneous; limited room
