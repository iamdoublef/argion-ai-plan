# design-iter-41 path-kern-smallsz — STATUS

## Outcome: WIN at iter-11 (W33)

**Accepted**: `iter-11/output.docx`
- Scores: **mean 8.28 / max 12.14 → 8.28 / 12.06 (max -0.08)**
- Mean held; max broke through (W32 plateau cracked on max dimension)
- Per-page deltas all ≤ +0.04 (no >0.05 regressions; big wins on p5 and p14)
- Gates: validate PASS (328 paragraphs), Word COM open PASS (7s), editable 100%, wt_count=446, no image hack
- Upgraded `final/imt050-wevac-eu-cn.docx` W32 → W33; preview.pdf refreshed; staged as
  `final/candidates/W33-iter41-sz11sz12-tighten-spacing.docx`

## Baseline (W32 final)
- score: mean 8.28, max 12.14 (p14 12.14 hardest, p9 11.81 second, p5 10.38 third)
- spacing distribution: 272 sites at val=5, 136 at val=8 (W32 winning move already applied: 71 sz=14 BLACK at val=8)
- sz=14 cohort: all 88 already at val=8 (W32 saturated)
- Untouched: sz=10 (53), sz=11 (35), sz=12 (33) cohorts

## Cohort grep (iter-1, this run's discovery)
- w:kern in `word/document.xml`: **0 sites** (kerning never enabled on body)
- w:kern in styles.xml/stylesWithEffects.xml: 4 sites total, only on sz=52 heading style (val=28)
- sz=11: all 35 = Red Arial Black accent, spacing=5
- sz=12: 33 total — Courier mono (11 NONE), Arial Black (18 with spacing=5), Arial (4 with spacing=5). Colors: WHITE 15 / GRAY 10 / BLACK 6 / RED 2.

## Iterations (against W32 baseline 8.28/12.14)

| iter | change | mean | max | verdict |
|------|--------|------|-----|---------|
| 1 | grep w:kern current state | — | — | doc body has 0 kern, only 4 in styles |
| 2 | kern val=2 on sz=14 BLACK (71) | 8.28 | 12.14 | inert (LO ignores low threshold) |
| 3 | kern val=14 on all sz=14 (88) | 8.28 | 12.13 | -0.01 max only, negligible |
| 4 | sz=12 spacing 5→8 (22 sites) | 8.28 | 12.14 | tiny p4 -0.03, otherwise flat |
| 5 | sz=11 spacing 5→8 (35 sites) | 8.29 | 12.17 | ❌ regression (wrong direction) |
| 6 | sz=12 5→8 + kern val=14 sz≥12 (22+327) | 8.28 | 12.14 | flat |
| 7 | sz=14 non-BLACK spacing 8→9 (17 sites) | 8.28 | 12.14 | flat |
| 8 | sz=11 spacing 5→3 (35 sites, REDUCE) | 8.28 | 12.11 | ✅ first signal (max -0.03) |
| 9 | sz=11 spacing 5→2 (35 sites) | 8.28 | 12.07 | ✅ max -0.07 |
| 10 | sz=11 spacing REMOVE (35 sites) | 8.30 | 12.07 | ❌ p5 +0.20 mean regresses |
| **11** | **sz=11 + sz=12 spacing 5→2 stacked (57)** | **8.28** | **12.06** | **✅ ALL gates** |
| 12 | iter-11 + sz=10 spacing 5→2 (+15 sites) | 8.28 | 12.06 | ❌ p4 +0.06 over tolerance |

## Per-page accepted (iter-11 vs W32)
```
W32:    2.88 3.25 11.69 6.34 10.38 4.35 7.73 7.83 11.81 10.02 11.09 9.96 11.40 12.14 3.34
iter-11:2.88 3.25 11.69 6.35 10.34 4.35 7.73 7.83 11.85 10.02 11.09 9.97 11.41 12.06 3.34
delta:  .00  .00  .00   +.01 -.04  .00  .00  .00  +.04  .00   .00   +.01 +.01 -.08  .00
```
Improvements: p5 -0.04, p14 -0.08. Regressions all ≤ +0.04.

## Sweet spot finding (NEW)
- **sz=14 cohort: spacing UP** wins (W32: 5→8 on BLACK = max -0.06, mean -0.03)
- **sz=11 + sz=12 cohort: spacing DOWN** wins (W33: 5→2 = max -0.08)
- **Opposite directions for different size cohorts** — sz=14 body letters need MORE space (LO under-spaces them), sz=11/sz=12 small accents need LESS space (LO over-spaces them on small fonts)
- **sz=10 too sensitive** — including it pushes p4 over tolerance
- **w:kern is essentially inert** in LO Writer for this template — useful only on sz=52 headings already styled (no body benefit)

## Lever ineffectiveness confirmed
1. w:kern in body — LO ignores or so subtle as to be unmeasurable. Don't bother further.
2. sz=14 non-BLACK spacing 8→9 — non-BLACK runs (banner, gray, single red) have too little area to move the needle.
3. sz=12 spacing UP — wrong direction. DOWN is correct.
4. Removing spacing entirely (val=0) — overshoots wrap recompute, mean +0.02.

## Word safety
Word COM rendering: 7 seconds, no errors. Pack-time validate.py: 328→328 paragraphs PASS.
No styles.xml/scheme/page edits. Pure rPr w:spacing surgical edits on 57 specific small-size rPr blocks.

## Stacking confirmed
W32 contained iter-36 (margin) + iter-37 (5 design fixes) + iter-38 (keycap chip) + iter-39
(sz=14 BLACK 5→8). Iter-41 adds **57 more small-size spacing tweaks (sz=11 + sz=12 5→2)** —
orthogonal lever, all earlier improvements survive untouched.

## Next angles (if asked to continue)
1. **sz=10 differential**: sz=10 has 53 sites split GRAY/RED — try only one color subset
   (iter-12 went too broad). GRAY-only or RED-only might pass.
2. **sz=13 spacing DOWN (5→2)**: parallel to sz=11/sz=12 winning move; iter-39 ruled out
   sz=13 UP, but DOWN is unexplored. 177 sites — large lever.
3. **sz=14 non-BLACK spacing DOWN (8→5)**: WHITE banner / GRAY 1A1A1A reverse of W32 BLACK.
4. **Differential per-page**: spacing=2 ONLY on pages 5/14 paragraphs via paragraph-id mapping.
5. **paragraph-level w:spacing (sectPr lineRule/line)**: untested in this round.
