# design-iter-39 path-docx-skill-stack — STATUS

## Outcome: STACK SUCCEEDED at iter-9 (W32)

**Accepted**: `iter-9/output.docx`
- Scores: **mean 8.30 → 8.27 (-0.03)**, max 12.20 → 12.22 (+0.02, within 0.05 tolerance)
- Per-page deltas all <= +0.03 (no >0.05 regressions, big improvements on p5/p9/p13)
- gates: validate PASS, Word COM open PASS (3s), editable 100%, wt_count=446, no image hack
- Upgraded `final/imt050-wevac-eu-cn.docx` W31 → W32; preview.pdf refreshed; staged as
  `final/candidates/W32-iter39-sz14-black-spacing8-stacked.docx`

## Important context correction
Task spec said baseline was W30 final 8.57/12.26. ACTUAL HEAD baseline is W31 (post iter-38
keycap chip) at **8.30/12.20**. Original numbers in this STATUS were measured against
the stale baseline; reran iter-2/7/9/10 against the correct W31 baseline.

## Baseline (W31 final, post iter-38)
- score: mean 8.30, max 12.20 (p14 12.20 hardest, p9 11.88 second)
- spacing distribution unchanged from W30: 360 sites at val=5, 48 at val=8
- sz=14 body: 88 sites at val=5 (iter-35's winning move from W27 never propagated forward)
- sz=14 black: 71 sites at val=5 (purest body text lever)
- sz=13: 143 sites at val=5

## Iterations (re-measured against W31 baseline)

| iter | change | mean | max | p10 Δ | p12 Δ | verdict |
|------|--------|------|-----|-------|-------|---------|
| 1 | verify baseline | 8.30 | 12.20 | — | — | baseline |
| 2 | sz=14 (all 88, both colors) 5→8 | 8.28 | 12.14 | +.10 | +.11 | ❌ per-page reg |
| 7 | sz=14 black-only (71) 5→9 | 8.27 | 12.23 | +.08 | +.07 | ❌ per-page reg |
| **9** | **sz=14 black-only (71) 5→8** | **8.27** | **12.22** | **+.03** | **+.03** | **✅ ALL gates** |
| 10 | iter-9 + sz=14 white (12) 5→7 | 8.28 | 12.22 | +.08 | +.10 | ❌ regression |

## Per-page accepted (iter-9 vs W31)
```
W31:    2.88 3.25 11.66 6.34 10.65 4.35 7.73 7.83 11.88 9.92 11.09 9.85 11.53 12.20 3.34
iter-9: 2.88 3.25 11.66 6.34 10.38 4.35 7.73 7.83 11.78 9.95 11.09 9.88 11.40 12.22 3.34
delta:  .00  .00  .00   .00  -.27  .00  .00  .00  -.10  +.03 .00   +.03 -.13  +.02 .00
```
Improvements: p5 -0.27, p9 -0.10, p13 -0.13. Regressions: all under 0.05.

## Sweet spot finding
For LibreOffice Writer on this Arial/Microsoft YaHei mixed CJK template:
- sz=14 BLACK body sweet spot is val=5 → val=8 (+3 twip = ~0.15pt per char)
- val=5 → val=9 (+4 twip) overshoots wrap on p10/p12 (shorter Chinese lines)
- val=10+ catastrophic
- sz=13 spacing increase universally bad — DO NOT touch sz=13
- sz=14 white banner increase also marginally bad
- The 3-twip differential is the same magic number found in iter-35 (W27 baseline)

## Word safety
Word COM rendering: 3 seconds, no errors, opens cleanly in MS Word.
Pack-time validate.py: 327→327 paragraphs, all validations PASS.
No settings.xml/scheme/page edits; pure rPr w:spacing surgical edit on 71 sz=14 black runs.
Diff vs W31: only 71 lines changed (`<w:spacing w:val="5"/>` → `<w:spacing w:val="8"/>` inside
71 specific sz=14 black rPr blocks).

## Stacking confirmed
W31 already contained iter-36 (multi-dim sectPr/pgMar margin tuning) + iter-37 (5 design
fixes) + iter-38 (keycap chip on p7). The rPr w:spacing lever is genuinely orthogonal:
all three earlier improvements survive untouched, and the rPr change adds a 0.03 mean +
0.27 p5 gain on top.

## Next angles (if asked to continue)
1. **sz=12 / sz=11 body**: smallest size cohorts not yet explored
2. **Differential per-page**: spacing=9 ONLY on pages 5/9/13 via paragraph-id mapping
3. **w:kern**: kerning lever in rPr (different mechanism than tracking)
4. **Combine with iter-36 margin micro-shift on p10/p12** (those pages now have +0.03)
