# W31-winner.docx — Change Log

## Baseline chain
- W29 (iter-33): 8.63/12.30 — pgMar top +3 子像素
- iter-37 W30: 8.54/12.24 — 设计修复 (zebra/border/red/footer)
- iter-36 W30a: 8.57/12.26 — 多维 pgMar (W29 baseline)
- **W31 = iter-37 W30 baseline + iter-36 pgMar 增量**: **8.30/12.20**

## Result

- **Mean diff:** 8.54 → **8.30** (−0.24 vs iter-37 W30; −0.33 vs W29)
- **Max diff:** 12.24 → **12.20** (−0.04 vs iter-37 W30; −0.10 vs W29)
- **Per-page improvers:** p3, p4, p5, p6, p7, p10, p11, p13, p14, p15 (10 pages improved, 0 regressed)
- **Editability:** wt_count=446, image_hack=false (anti-cheat passes)
- **Word COM:** 15 pages rendered, validates against iter-37/iter-9 baseline

## Spec (delta vs iter-37 iter-9 baseline)

```json
{
  "3":  {"right": 3},
  "4":  {"top": 10},
  "5":  {"right": 3, "top": 3},
  "6":  {"top": 20},
  "7":  {"right": 3, "top": 3},
  "9":  {"right": 2},
  "10": {"top": -5},
  "11": {"top": -17, "right": 1},
  "13": {"top": 3},
  "14": {"right": 5, "top": -3},
  "15": {"top": 3}
}
```

## Absolute pgMar values (W31 vs iter-37 baseline)

| Page | top (iter37→W31) | right (iter37→W31) |
|------|---------|-----------|
| p3   | 581 (-) | 567 → **570** |
| p4   | 578 → **588** | 567 (-) |
| p5   | 581 → **584** | 567 → **570** |
| p6   | 578 → **598** | 567 (-) |
| p7   | 578 → **581** | 567 → **570** |
| p9   | 581 (-) | 567 → **569** |
| p10  | 578 → **573** | 567 (-) |
| p11  | 578 → **561** | 567 → **568** |
| p13  | 581 → **584** | 567 (-) |
| p14  | 579 → **576** | 567 → **572** |
| p15  | 578 → **581** | 567 (-) |

Pages p1, p2, p8, p12 unchanged.

## Single-page wins (biggest contributors)

| Page | Delta from W29 baseline | Lever |
|------|-------------------------|-------|
| p6 | 6.19 → 4.35 (**-1.84**) | top +20 (extra whitespace at top) |
| p4 | 7.09 → 6.34 (-0.75) | top +10 + iter-37 fixes |
| p11 | 12.14 → 11.09 (-1.05) | top -17 + right +1 |
| p15 | 3.65 → 3.34 (-0.31) | top +3 + iter-37 footer fix |
| p3 | 11.89 → 11.66 (-0.23) | right +3 + iter-37 zebra/border |
| p14 | 12.30 → 12.20 (-0.10) | right +5 + top -3 + iter-37 |
| p13 | 11.68 → 11.53 (-0.15) | top +3 + iter-37 |
| p10 | 10.14 → 9.92 (-0.22) | top -5 + iter-37 |

## Method

1. unpacked iter-37 iter-9.docx (W30 design fixes) → `iter37_iter9_unpacked/`
2. wrote `build_on_iter37.py` to apply per-page pgMar deltas
3. ran 20 rounds of sweep (r1-r20) — first 10 on W29 baseline (iter-36 W30a), then 10 stacked on iter-37 baseline (r11-r20)
4. found: **w:top large positive deltas (+10..+20)** are sweet spots for pages with sparse content (p4, p6, p15)
5. validated: validate.py PASS, Word COM PASS, 15 pages

## Files

- `iter37_iter9.docx` — iter-37 W30 baseline (design fixes)
- `iter37_iter9_unpacked/` — fresh unpacked copy used as patch source
- `r1-plan.json` … `r20-plan.json` — per-round sweep specs
- `r1.results.json` … `r20.results.json` — per-round outcomes
- `r20-final-best.docx` — winning candidate (= W31-winner.docx)
- `W31-winner.docx` — final winner copy
- `STATUS.md` — full iteration narrative
- `build_on_iter37.py`, `sweep37.py` — automation scripts
