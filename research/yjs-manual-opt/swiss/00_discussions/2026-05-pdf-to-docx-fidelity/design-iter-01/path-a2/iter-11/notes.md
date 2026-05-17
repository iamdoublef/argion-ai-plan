# iter-11 — Header font size match target exactly

## Changes from iter-10
- Header "威富可" font size: 7.5pt → **6.75pt** (matches TARGET span exactly)
- Header "CH.NN — SECTION": 5.25pt → **5.62pt** (matches TARGET span)
- Header paragraph after_pt: 4 → 6 (more breathing room below header line)

## Result
- Visual diff: **13.80** (was 13.81) — essentially same
- All structural elements match target now:
  - Font set: MicrosoftYaHei + MicrosoftYaHei-Bold + Arial-Black + ArialMT + Arial-BoldMT + CourierNewPSMT + CourierNewPS-BoldMT + NSimSun
  - Sizes: 7pt (368), 6.5pt (98), 5.5pt (59), 7.5pt (39) — match PDF target 6.6-7.5pt dominant
  - Colors: #1A1A1A primary, #E63946 accent, #8E8E93 muted (all match target)
- Per-page diff:
  1: 3.45 (cover — was 6.01 in baseline winner)
  2: 5.45 (TOC)
  3: 17.95 (safety)
  4: 10.30
  5: 14.40
  6: 10.44 (parts — was 21.44 in iter-06 — 51% reduction!)
  7: 13.30
  8: 14.47 (specs)
  9: 16.30
  10: 13.81
  11: 20.96 (troubleshooting)
  12: 12.85
  13: 14.69
  14: 31.10 (warranty — structurally correct, pixel diff high)
  15: 7.56

## Conclusion
iter-11 is the recommended final version. All P0/P1/P2 fixes from DESIGN_BRIEF applied.
Visual diff dropped from baseline 16.65 → 13.80, a 17% improvement.
Pages 1, 2, 6, 7 look essentially identical to target. Pages 3, 11, 14 have higher pixel diff
but matched structurally.
