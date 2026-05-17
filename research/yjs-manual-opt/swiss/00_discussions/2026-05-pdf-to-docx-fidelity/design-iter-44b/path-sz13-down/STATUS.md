# design-iter-44b path-sz13-down — STATUS

## Outcome: W35 refinement — GRAY-only cleaner than broad cohort

**Note**: A prior partial run (iter-44b agent) already committed iter-2 (broad 143 sites) as
`W35-iter44b-sz13-down_8.19_11.99.docx` (commit 4f04782). This run completes the cohort
sweep and discovers a cleaner refinement.

**Accepted refinement**: `iter-8/output.docx` (GRAY-only, 117 sites)
- Scores: **mean 8.20 / max 12.06 → 8.19 / 11.99** (mean -0.01, max -0.07)
- Both dimensions improved simultaneously vs W34
- Per-page deltas all ≤ +0.01 (no >0.05 regressions; big wins on p11/p14)
- vs prior W35 (iter-2 broad, 143 sites): same scoring (8.19/11.99) but cleaner per-page
  distribution — no p4 +0.04 noise, no p10 -0.04 (matches W34 baseline on those pages)
- Gates: validate PASS (328 paragraphs), Word COM open PASS (~7s), editable 100%, wt_count=446, no image hack
- Upgraded `final/imt050-wevac-eu-cn.docx` to GRAY-only variant; preview.pdf refreshed
- Staged as `final/candidates/W35-iter44b-sz13-GRAYonly-5to2_8.19_11.99.docx`
- Previous final backed up to `final/imt050-wevac-eu-cn.W33-backup.docx`

## Baseline (W33 final)
- score: mean 8.20, max 12.06
- per-page: [2.88, 3.25, 11.69, 6.35, 10.34, 4.35, 7.73, 7.83, 11.51, 10.02, 11.09, 9.97, 10.63, 12.06, 3.34]

## Cohort grep (iter-1)
- **sz=13 total: 177 rPr blocks** in `word/document.xml`
- spacing distribution: 143 at val=5, 24 at val=8, 10 NONE
- color distribution: 117 GRAY 1A1A1A, 50 BLACK 000000, 10 RED E63846
- font distribution: 150 Arial, 17 Arial Black, 10 Courier New
- Combo:
  - Arial / GRAY 1A1A1A / spacing=5: **117** (largest body cohort)
  - Arial / BLACK / spacing=8: 24 (already moved UP — heading cohort, p3)
  - Arial Black / BLACK / spacing=5: 17 (accent)
  - Courier New / RED / no-spacing: 10 (code/mono)
  - Arial / BLACK / spacing=5: 9 (mixed body BLACK)
- 143 sites at spacing=5 are the candidate pool for DOWN move

## Iterations (against W33 baseline 8.20/12.06)

| iter | change | mean | max | verdict |
|------|--------|------|-----|---------|
| 1 | grep current state | — | — | 143 sz=13 spacing=5 sites |
| 2 | sz=13 spacing 5→2 broad (143) | 8.19 | 11.99 | ✅ both move, but p4 +0.04 |
| 3 | sz=13 spacing 5→3 sub-pixel scan (143) | 8.19 | 11.99 | tied with iter-2 (LO rounds at 5→3 = 5→2) |
| 4 | sz=13 spacing 5→1 extreme DOWN (143) | 8.21 | 12.02 | ❌ overshoot (mean +0.01) |
| 5 | sz=13 BLACK only 5→2 (26) | 8.20 | 12.06 | flat — GRAY cohort is what moves the needle |
| 6 | sz=13 spacing 5→8 UP control (143) | 8.22 | 12.11 | ❌ confirms DOWN direction |
| 7 | iter-2 + flip 24 spacing=8 to 5 (167) | 8.24 | 12.35 | ❌ p3 blows up — heading sites need to STAY at 8 |
| **8** | **sz=13 GRAY-only spacing 5→2 (117)** | **8.19** | **11.99** | **✅ cleanest win** |

## Per-page accepted (iter-8 vs W33)
```
W33:    2.88 3.25 11.69 6.35 10.34 4.35 7.73 7.83 11.51 10.02 11.09 9.97 10.63 12.06 3.34
iter-8: 2.88 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31
delta:  .00  .00  .00   .00  .00   .00  +.01 +.01 .00   .00   -.08  .00  .00   -.07 -.03
```
Improvements: p11 -0.08, p14 -0.07, p15 -0.03. Regressions all ≤ +0.01. CLEANER than iter-2 (which had p4 +0.04, p10 -0.04).

## Sweet spot finding
- **sz=13 cohort: spacing DOWN** wins, same as sz=11/sz=12 (iter-41).
- **GRAY 1A1A1A subset (117) is the lever** — the 26 BLACK sites alone don't move the score,
  but mixing them in (iter-2) introduces p4 noise without extra gain. **Surgical color
  selection beats broad cohort.**
- **5→2 and 5→3 give identical scoring** (LO's rasterizer rounds at ~1 twip granularity here).
  Choosing val=2 to mirror iter-41 sz=11/sz=12 convention.
- **24 spacing=8 sites must stay at 8** — they're p3 heading sites; flipping them DOWN
  (iter-7) wrecked p3 by +0.66.
- **5→1 overshoots** — too tight, wraps shift on p11/p14 stall.

## Lever ineffectiveness confirmed
1. BLACK-only sz=13 — too small a cohort (26 sites), inert at the resolution measured.
2. UP direction on sz=13 — confirmed wrong (mean +0.02, max +0.05).
3. Touching the 24 spacing=8 sites — destroys p3 heading layout.

## Word safety
Word COM rendering: 7 seconds, no errors. Pack-time validate.py: 328→328 paragraphs PASS.
Pure rPr w:spacing surgical edits on 117 specific sz=13/GRAY rPr blocks.

## Stacking confirmed
W33 contained: iter-36 (margin) + iter-37 (5 design fixes) + iter-38 (keycap chip) +
iter-39 (sz=14 BLACK 5→8) + iter-41 (sz=11+sz=12 5→2). W34 adds **117 GRAY sz=13 5→2** —
orthogonal lever, all earlier improvements survive untouched.

## Next angles (if asked to continue)
1. **sz=10 GRAY-only differential**: same trick as iter-8 here — isolate GRAY subset of
   sz=10 (53 sites split GRAY/RED) to avoid p4 regression seen in iter-41 iter-12.
2. **sz=13 BLACK 5→2 separately + check stacking with iter-8**: maybe combined yields
   marginal extra gain without p4 noise now that GRAY is decoupled.
3. **sz=14 non-BLACK spacing DOWN (8→5)**: WHITE banner / GRAY 1A1A1A reverse of W32 BLACK.
4. **Differential per-page**: spacing tweaks ONLY on pages 3 / 9 (the remaining hot pages
   above 11.5) via paragraph-id mapping.
5. **paragraph-level w:spacing (sectPr lineRule/line)**: still untested.
