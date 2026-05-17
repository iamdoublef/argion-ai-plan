# design-iter-45 path-sz10-gray-only — STATUS

## Outcome: NO BREAKTHROUGH — sz=10 cohort saturated

**Result**: All 9 iterations score equal-or-worse than W35 (8.19/11.99).
No upgrade to `final/`. W35 remains the production champion.

The brief's hypothesis that GRAY-only avoids over-tolerance is **confirmed**
(iter-2/3/4 all safe even at extreme val=-2), but the sz=10 cohort lacks any
moveable lever — every spacing tweak is either inert (no measurable shift)
or hits a heading style (iter-8 broke p3).

## Baseline (W35 final, refreshed)
- score: mean 8.19, max 12.06 → 8.19, max 11.99 (per refreshed final score.json)
- per-page: [2.88, 3.25, 11.69, 6.35, 10.34, 4.35, 7.74, 7.84, 11.51, 10.02, 11.01, 9.97, 10.63, 11.99, 3.31]

## Cohort grep (iter-1) — REALITY DIFFERS FROM BRIEF

Brief assumed sz=10 had GRAY 1A1A1A + BLACK + RED. Actual distribution:

- **sz=10 total: 53 rPr blocks** in `word/document.xml`
- color distribution: 37 RED E63846 / 16 LIGHT-GRAY 8E8E93 / 0 BLACK / 0 dark-GRAY 1A1A1A
- font distribution: 37 Arial Black / 14 Courier New / 2 Arial
- spacing distribution: 24 at val=8 / 15 at val=5 / 14 NONE

Combos with text samples:

| font / color / spacing | count | what it is |
|------------------------|-------|------------|
| Arial Black / RED E63846 / spacing=8 | 24 | red bullet markers (heading style) |
| Arial Black / RED E63846 / spacing=5 | 13 | red bullet markers (body) |
| Courier New / GRAY 8E8E93 / NONE     | 14 | page running headers ("CH.01 — SAFETY", "IMT050 — 说明书") |
| Arial / GRAY 8E8E93 / spacing=5      | 2  | fine-print disclaimers ("使用产品前请仔细阅读…") |

**"GRAY-only" for sz=10 = 16 sites total** — much smaller cohort than sz=13's 117.

## Iterations (against W35 baseline 8.19/11.99)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | grep current state | — | — | — | sz=10 distribution charted |
| 2 | GRAY 8E8E93 spacing→2 (all incl. NONE) | 16 | 8.19 | 11.99 | tied — inert |
| 3 | GRAY 8E8E93 spacing→3 | 16 | 8.19 | 11.99 | tied — inert |
| 4 | GRAY 8E8E93 spacing→-2 (extreme DOWN) | 16 | 8.19 | 11.99 | tied — DOWN-safe even at extreme |
| 5 | GRAY+RED stacked 8E8E93 →2 / E63846 5→2 | 29 | 8.19 | 11.99 | tied — RED drives, GRAY adds nothing |
| 6 | RED E63846 spacing 5→2 (13 sites) | 13 | 8.19 | 11.99 | tied — p4 +0.05, p10 -0.02 cancel |
| 7 | broad sz=10 spacing 5→2 (RED+Arial-GRAY) | 15 | 8.19 | 11.99 | tied — iter-41/12 reproduction, now CLEAN on W35 |
| 8 | RED E63846 spacing 8→5 (24 heading bullets) | 24 | **8.21** | **12.03** | ❌ p3 +0.34 regression (heading sites) |
| 9 | Courier GRAY 8E8E93 add spacing=10 UP | 14 | 8.19 | 11.99 | tied — inert |

## Per-page comparison (best variants vs W35)
```
W35:    2.88 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31
iter-2: 2.89 3.25 11.69 6.35 10.34 4.35 7.74 7.84 11.51 10.02 11.01 9.97 10.63 11.99 3.31  (Δ p1 +0.01)
iter-6: 2.88 3.25 11.69 6.40 10.34 4.35 7.74 7.84 11.51 10.00 11.01 9.97 10.63 11.99 3.31  (Δ p4 +0.05, p10 -0.02)
iter-7: 2.89 3.25 11.69 6.40 10.34 4.35 7.74 7.84 11.51 10.00 11.01 9.97 10.63 11.99 3.31  (Δ p4 +0.05, p10 -0.02)
```

## Brief hypothesis verification

**Confirmed**:
1. GRAY-only IS DOWN-safe — iter-2/3/4 with vals 2, 3, -2 all clean. No p4 shift.
2. RED spacing=5 cohort (the 13 bullets that iter-41/12 hit) on W35 base is now SAFE
   too — p4 +0.05 is balanced by p10 -0.02. iter-12's over-tolerance was a W32-context
   issue; W34/35's accumulated optimizations relaxed the constraint surface.

**Refuted/Refined**:
1. The brief assumed sz=10 contained dark GRAY 1A1A1A (like sz=13). It does NOT —
   sz=10 GRAY is 8E8E93 (the lighter footer/disclaimer gray), only 16 sites,
   mostly in low-pixel-area locations (page-corner running headers).
2. There's no breakthrough lever in this cohort — all DOWN-safe paths are inert
   on score, all UP paths break headings. The cohort is geometrically saturated.

## Lever ineffectiveness summary

1. **Courier 8E8E93 sz=10 running headers (14)** — too low pixel area, no measurable effect.
2. **Arial 8E8E93 sz=10 fine-print (2)** — too few sites, sub-resolution.
3. **Arial Black E63846 spacing=5 bullets (13)** — p4 ± p10 cancel, net zero.
4. **Arial Black E63846 spacing=8 bullets (24)** — heading-style, MUST stay at 8.

## Word safety (for all variants)

Word COM rendering: 7 seconds typical, no errors. Pack-time validate.py: 328→328
paragraphs PASS on every iter. wt_count=446. editable 100%. Pure rPr w:spacing edits.

## Next angles (priority for future runs)

The sz=10 cohort is exhausted. Next levers to explore:

1. **sz=13 BLACK 5→2 separately** (W35 GRAY-only didn't include the 50 BLACK
   sz=13 sites; sz=13 broad iter-2 added p4 +0.04 but the BLACK subset alone
   could be cleaner now that GRAY is already DOWN).
2. **sz=14 non-BLACK spacing DOWN (8→5)** — WHITE banner / GRAY 1A1A1A reverse
   of W32 BLACK. Still untested.
3. **paragraph-level w:spacing (sectPr lineRule/line)** — fully untested in any run.
4. **Differential per-page**: spacing-only on pages 3 / 9 / 11 / 14 paragraphs via
   paragraph-id mapping. Pages 11 and 14 already broke at iter-44b for sz=13 GRAY;
   targeted moves on remaining hot pages (3, 9) may shift max.
5. **sz=16/sz=18 cohort grep** (heading sizes never touched). Surprising hot pages
   p3, p9 dominated by mid-size headers might respond to UP moves.
6. **w:positionV / w:position vertical shift** — never tested anywhere.

## Stacking confirmation

W35 (= W33 + W34's 117 GRAY sz=13 5→2) is preserved exactly — no upgrades made.
All 9 iterations operated only on sz=10 cohort, orthogonal to prior W33/W35 levers.
`final/imt050-wevac-eu-cn.docx` and its `.score.json` are unchanged.
