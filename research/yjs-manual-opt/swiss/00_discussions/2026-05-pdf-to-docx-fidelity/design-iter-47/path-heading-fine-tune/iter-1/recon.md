# iter-1 — Recon (no apply)

Baseline = W36 (`baseline.docx`, sha256 a11b818..., mean 8.18 / max 11.97).

## Cohort distribution after W36 (444 rPr blocks)

### sz=10 (heading-cohort UP target)
- `('10', '8E8E93', '5', 'Arial')`: 2          # too few to act on
- `('10', '8E8E93', '_', 'Courier New')`: 14   # no spacing attr
- `('10', 'E63846', '8', 'Arial Black')`: **37**  # iter-46 moved 13→8; total now 37 at sp=8

### sz=13 (heading-cohort BLACK)
- `('13', '000000', '8', 'Arial')`: **33**     # iter-46 5→8 cohort lands here (Arial)
- `('13', '000000', '8', 'Arial Black')`: **17**  # other BLACK at sp=8 (Arial Black)
- `('13', '1A1A1A', '2', 'Arial')`: 117        # W35 win cohort, leave alone
- `('13', 'E63846', '_', 'Courier New')`: 10   # no spacing attr

So total `sz=13 BLACK sp=8` = 50 sites (33 Arial + 17 Arial Black). All candidates for 8→11.

### sz=22 (BIG H1 BLACK)
- `('22', '000000', '11', 'Arial Black')`: 13  # W36 terminal state

### sz=27 (BIG H1 RED)
- `('27', 'E63846', '11', 'Arial Black')`: 13  # W36 terminal state

### sz=14 (W32 win, saturated)
- `('14', '000000', '8', 'Arial')`: 62
- `('14', '000000', '8', 'Arial Black')`: 9
- `('14', '1A1A1A', '8', 'Arial')`: 4
- `('14', 'E63846', '8', 'Arial Black')`: 1
- `('14', 'FFFFFF', '8', 'Arial Black')`: 12

### sz=15 (negative evidence — DO NOT push UP)
- `('15', '000000', '5', 'Arial Black')`: 27

### sz=11 (W33 win, saturated DOWN)
- `('11', 'E63846', '2', 'Arial Black')`: 35

### sz=12 (mixed, W33 win)
- `('12', 'FFFFFF', '2', 'Arial Black')`: 15   # WHITE
- other small clusters at sp=2

### sz=30/36 (orphan headings)
- `('30', '000000', '5', 'Arial Black')`: 1
- `('36', '1A1A1A', '5', 'Arial Black')`: 1

## Plan

| iter | cohort | direction | sites |
|------|--------|-----------|-------|
| 2 | sz=10 RED Arial Black | 8→11 | 37 |
| 3 | sz=13 BLACK (Arial + Arial Black) | 8→11 | 50 |
| 4 | stack iter-2 + iter-3 | UP×2 | 87 |
| 5 | sz=22 BLACK 11→9 / 10 / 12 / 14 mini-sweep | local optimum | 13 |
| 6 | sz=27 RED 11→9 / 10 / 12 / 14 mini-sweep | local optimum | 13 |
| 7 | stack best-of-{2,3,5,6} | combined | n |
| 8-10 | explore: sz=30/36 orphan, sz=10 mixed, fallback | tail | small |
