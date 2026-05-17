# design-iter-44c path-sz13-down — STATUS

## Outcome: WIN at iter-5 (W35)

**Accepted**: `iter-5/output.docx`
- Scores: **mean 8.20 → 8.19 / max 12.06 → 11.99** (W34 → W35)
- Mean -0.01, max -0.07. No regressions ≥ 0.05.
- Gates: validate PASS (328 paragraphs), Word COM open PASS (3.94s), editable 100%, wt_count=446
- Upgraded `final/imt050-wevac-eu-cn.docx` W34 → W35; staged as
  `final/candidates/W35-iter44c-sz13-gray-spacing-5to2.docx`

## Baseline (W34 final)
- score: mean 8.20, max 12.06
- per-page: 2.88 3.25 11.69 6.35 10.34 4.35 7.73 7.83 11.51 10.02 11.09 9.97 10.63 12.06 3.34
- hardest: p14 12.06, p3 11.69, p9 11.51, p11 11.09

## Cohort grep (iter-1, against W34 baseline)
- sz=13 rPr blocks: **177 total**
- spacing distribution: 143 at val=5, 24 at val=8, 10 NONE
- color distribution: 117 GRAY (1A1A1A) / 50 BLACK (000000) / 10 RED (E63846)
- font distribution: 150 Arial / 17 Arial Black / 10 Courier New
- combo:
  - **117 Arial GRAY spacing=5** (body small text — largest cohort)
  - 24 Arial BLACK spacing=8 (already wide, not touched)
  - 17 Arial Black BLACK spacing=5
  - 10 Courier RED no-spacing
  - 9 Arial BLACK spacing=5

## Iterations (against W34 baseline 8.20/12.06)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | grep sz=13 cohort | — | — | — | 177 total, 143 at sp=5, 117 GRAY |
| 2 | sz=13 all spacing 5→2 | 143 | 8.19 | 11.99 | ✅ first win (mean -.01, max -.07); p4 +.04 |
| 3 | sz=13 all spacing 5→3 | 143 | 8.19 | 11.99 | ✅ tied iter-2; p10/p15 tiny diff |
| 4 | sz=13 all spacing 5→1 | 143 | 8.21 | 12.02 | ❌ overshoots p11/p14 |
| **5** | **sz=13 GRAY-only 5→2** | **117** | **8.19** | **11.99** | **✅ CLEANEST: p4 unchanged, p15 -.03** |
| 6 | sz=13 BLACK-only 5→2 | 26 | 8.20 | 12.06 | ❌ inert (BLACK cohort contributes nothing) |
| 7 | sz=13 GRAY-only 5→3 | 117 | 8.19 | 11.99 | ✅ tied iter-5; p15 unchanged (not -.03) |

## Per-page accepted (iter-5 vs W34)
```
W34:    2.88 3.25 11.69 6.35 10.34 4.35 7.73 7.83 11.51 10.02 11.09 9.97 10.63 12.06 3.34
iter-5: 2.88 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31
delta:  .00  .00  .00   .00  .00   .00  +.01 +.01 .00   .00   -.08  .00  .00   -.07  -.03
```
**No regressions ≥ 0.05**. Improvements on p11 (-.08), p14 (-.07), p15 (-.03). Cleanest win in series.

## Sweet spot finding (NEW, sz=13)
- **sz=13 GRAY (1A1A1A) Arial body spacing: 5→2 wins** (max -.07, mean -.01)
- **sz=13 BLACK cohort is inert** — Arial+ArialBlack BLACK 5→2 alone gave 0 movement
- val=2 = val=3 in this cohort (same scores). val=1 overshoots.
- All gains concentrated on GRAY body small-text. GRAY-only is *strictly better* than all-cohort
  because p4 (with BLACK Arial Black accents) doesn't regress when BLACK is skipped.
- Confirms hypothesis: sz=11/sz=12/sz=13 small-size cohorts all want DOWN direction (over-spaced by LO)

## Word safety
Word COM rendering: 3.94 seconds, no errors. Pack-time validate.py: 328→328 paragraphs PASS.
No styles.xml/scheme/page edits. Pure rPr w:spacing surgical edits on 117 GRAY sz=13 rPr blocks.

## Stacking confirmed
W34 contained W33 (sz=11+sz=12 spacing 5→2) + earlier wins. iter-44c adds **117 sz=13 GRAY
spacing 5→2** — orthogonal lever, all earlier improvements survive untouched.

## Lever evaluation
1. sz=13 GRAY 5→2 — winning move (cleanest result)
2. sz=13 BLACK 5→2 — inert, don't bother stacking
3. sz=13 all 5→1 — too aggressive, overshoots
4. sz=13 all 5→3 — works but tied 5→2 with no marginal benefit

## Next angles (if asked to continue)
1. **sz=13 GRAY 5→2 + sz=13 BLACK 5→2 stacked** — already disproven (iter-2 = iter-5 in mean/max
   but iter-2 has p4 +.04 regression). Skip.
2. **sz=10 differential**: sz=10 has 53 sites split GRAY/RED — try GRAY-only 5→2 (parallel to sz=13).
3. **sz=14 non-BLACK spacing DOWN (8→5)**: WHITE banner / GRAY 1A1A1A reverse of W32 BLACK.
4. **sz=24/sz=28 heading kerning**: untested heading-style cohorts.
5. **paragraph-level w:spacing (sectPr lineRule/line)**: untested in this round.
