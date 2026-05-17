# design-iter-46 path-docx-skill-continue — STATUS

## Outcome: WIN at iter-10 (W36)

**Accepted**: `iter-10/output.docx`
- Scores: **mean 8.19 → 8.18 / max 11.99 → 11.97** (W35 → W36)
- Mean -0.01, max -0.02. No regressions ≥ 0.05.
- Gates: validate.py PASS (328 paragraphs), Word COM render PASS (3.98s + 7.24s), editable 100%, wt_count=446
- Upgraded `final/imt050-wevac-eu-cn.docx` W35 → W36; staged as
  `final/candidates/W36-iter46-headings-up-stack.docx`

## Baseline (W35 final)
- score: mean 8.19, max 11.99
- per-page: 2.88 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31
- wt_count: 446, editable 100%

## Cohort recon (444 rPr blocks total)
- sz=36/30: 1 each, BLACK Arial Black sp=5
- sz=27: 13 RED Arial Black sp=5 (BIG red H1)
- sz=22: 13 BLACK Arial Black sp=5 (H1)
- sz=15: 27 BLACK Arial Black sp=5 (+ 1 GRAY + 1 RED) (H2-ish)
- sz=14: 71 BLACK sp=8 (W32 win), 4 GRAY sp=8, 1 RED sp=8, 12 WHITE sp=8
- sz=13: 26 BLACK sp=5, 24 BLACK sp=8, 117 GRAY sp=2 (W35), 10 RED no-sp
- sz=12: scattered (W33 5→2 applied)
- sz=11: 35 RED Arial Black sp=2 (W33 win)
- sz=10: 53 mixed (37 RED, 14 GRAY8E Courier, 2 GRAY8E Arial)
- w:position: only 1 site total (lever has no purchase)
- w:vertAlign: 0 sites (no native targets)

## Iterations (W35 baseline 8.19/11.99)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | sz=15 BLACK 5→8 | 27 | 8.22 | 12.04 | ❌ regression (p5/p12/p13 worse) |
| 2 | sz=22 BLACK 5→8 | 13 | 8.18 | 11.98 | ✅ first win (mean -.01, max -.01) |
| 3 | iter-2 + sz=27 RED 5→8 | 13+13 | 8.18 | 11.98 | ✅ stack tied iter-2, broader per-page gains |
| 4 | iter-3 + sz=13 BLACK 5→8 | +26 | 8.18 | 11.98 | ✅ tied, tiny extra gain on p6/p11 |
| 5 | iter-4 + sz=11 RED 2→0 | +35 | 8.21 | 11.98 | ❌ p5 +.23, p13 +.24 (RED bullet over-tightened) |
| 6 | iter-4 + sz=15 BLACK 5→8 | +27 | 8.20 | 12.02 | ❌ confirms sz=15 5→8 hurts even stacked |
| 7 | iter-4 + sz=14 GRAY 8→11 | +4 | 8.19 | 12.12 | ❌ max regression (p14 +.14), GRAY cohort saturated at 8 |
| 8 | iter-4 with sz=22/27 pushed 5→11 | 13+13+26 | 8.18 | **11.97** | ✅ new max best (p14 -.02) |
| 9 | iter-8 with sz=22/27 5→14 | 13+13+26 | 8.18 | 11.98 | ⚠️ tied mean, max -.01 regression vs iter-8 |
| **10** | **iter-8 + sz=10 RED 5→8** | 13+13+26+13 | **8.18** | **11.97** | **✅ WIN: matches iter-8 with extra p4 -.01** |

## Per-page accepted (iter-10 vs W35)
```
W35:     2.88 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31
iter-10: 2.88 3.25 11.67 6.29 10.32 4.33 7.71 7.85 11.49 10.00 10.99 9.97 10.60 11.97 3.31
delta:   0    0    -.02  -.06 -.02  -.02 -.03 +.01 -.02  -.02  -.02  0    -.03  -.02   0
```
**No regressions ≥ 0.05.** Improvements on every changed page (p3 -.02, p4 -.06, p5 -.02,
p6 -.02, p7 -.03, p9 -.02, p10 -.02, p11 -.02, p13 -.03, p14 -.02). Only +.01 on p8 (immaterial).

## Sweet spot findings (NEW, heading cohorts)
- **sz=22 BLACK Arial Black 5→11 wins** (UP direction, parallel to W32 sz=14 BLACK 5→8)
- **sz=27 RED Arial Black 5→11 wins** (UP direction, BIG red H1 cohort)
- **sz=13 BLACK Arial spacing 5→8 wins** (UP direction, was inert at 5→2 in W34, but UP works)
- **sz=10 RED Arial Black 5→8 wins** (marginal, p4 -.01)
- **sz=15 BLACK Arial Black 5→8 LOSES** — solo regression, persists when stacked (iter-6).
  Likely already on the "right side" of LO's rendering curve for that size.
- **sz=14 GRAY 8→11 LOSES** — saturated at 8 (W32 win).
- **sz=11 RED 2→0 LOSES badly** (already optimally tight after W33 5→2).

## Pattern (heading cohorts)
- BLACK Arial Black headings sz=22/27/13 — over-tightened by LO, want UP movement (5→8 or 5→11)
- sz=15 is exception (already correctly tight)
- Sweet target spacing for heading UP cohort: **val=11** is at least as good as val=8, val=14 starts regressing

## Word safety
Word COM rendering: 3.98 + 7.24 = ~11s pipeline, no errors. Pack-time validate.py: 328→328
paragraphs PASS. No styles.xml/scheme/page/font edits. Pure rPr w:spacing surgical edits on
65 sites (13 + 13 + 26 + 13).

## Stacking confirmed
W35 contained W34 (sz=13 GRAY 5→2) + W33 (sz=11/12 5→2) + W32 (sz=14 BLACK 5→8) + earlier wins.
iter-46 adds **sz=22 BLACK 5→11 + sz=27 RED 5→11 + sz=13 BLACK 5→8 + sz=10 RED 5→8** — all
heading/accent cohorts, complementary to body cohorts already tuned.

## Negative evidence captured (for future agents)
- sz=15 BLACK 5→8 always regresses (solo + stacked)
- sz=11 RED 2→0 hurts p5/p13 by +.23/+.24 — RED bullet body has DOWN limit at 2
- sz=14 GRAY 8→11 regresses p14
- w:position lever has only 1 native site — not exploitable
- w:vertAlign lever has 0 native sites — not exploitable without changing semantics

## Next angles (if asked to continue)
1. **sz=10 RED 5→11 / 8→11 push further** — try same UP saturation test as sz=22/27
2. **sz=10 RED 8→11** — the 24 sites already at sp=8 might want sp=11 (heading-cohort pattern)
3. **sz=15 GRAY/RED solo (the 1+1 sites)** — too small to matter alone
4. **Mixed heading vals (5→9, 5→10, 5→12)** — fine-tune optimum
5. **sz=36/30 single sites** — try UP direction on these orphan headings
6. **sz=13 BLACK sp=8 → sp=11** — 24 untouched sites at sp=8 from earlier iter
