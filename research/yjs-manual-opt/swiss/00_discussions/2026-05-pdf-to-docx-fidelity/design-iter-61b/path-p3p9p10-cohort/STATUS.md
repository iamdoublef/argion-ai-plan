# iter-61b path-p3p9p10-cohort STATUS

Built on W48 = 7.27/10.13 (iter-60). Attack: p3/p9/p10 + untouched cohorts.
**Result: W49 = 7.23 / 10.13** (best = iter-12, -0.04 mean vs W48).

## Baseline = W48 (iter-60) per-page diffs
| page | diff |
|-----|------|
| p1  | 2.17 |
| p2  | 3.23 |
| **p3** | **10.03** |
| p4  | 6.38 |
| p5  | 8.55 |
| p6  | 3.77 |
| p7  | 7.18 |
| p8  | 7.05 |
| **p9** | **9.94** |
| **p10** | **9.79** |
| p11 | 10.13 |
| p12 | 8.84 |
| p13 | 9.25 |
| p14 | 9.67 |
| p15 | 3.04 |
| **mean** | **7.27** / max **10.13** |

## Final = W49 (iter-12) per-page diffs
| page | diff | delta vs W48 |
|-----|------|------|
| p1  | 2.17 | 0 |
| p2  | 3.23 | 0 |
| p3  | 10.03 | 0 |
| p4  | 6.38 | 0 |
| p5  | 8.55 | 0 |
| p6  | 3.77 | 0 |
| p7  | 7.18 | 0 |
| p8  | 7.05 | 0 |
| **p9**  | **9.69** | **-0.25** |
| **p10** | **9.48** | **-0.31** |
| p11 | 10.13 | 0 |
| p12 | 8.84 | 0 |
| p13 | 9.25 | 0 |
| p14 | 9.67 | 0 |
| p15 | 3.04 | 0 |
| **mean** | **7.23** | **-0.04** |
| max | 10.13 | 0 |

## Winning recipe (iter-12)

```
p9-only: w:spacing val 2->0, 8->6, 6->4
p10-only: ALL w:spacing val cascading collapse to 0
  (10->6, 8->6, 6->4, 4->2, 2->0)
```

wt_count=448 (anti-cheat OK), text_ratio=1.0, editable_pct=100,
Word-safe (compare_word.py: OK).

## Run log (iter-61b)

| iter | recipe | mean | max | note |
|------|--------|------|------|------|
| 1 | iter-14_61 + p3 v6->4 | 7.35 | 11.44 | p3 BLEW UP (10.03->11.44). p3 char-spacing saturated downward |
| 2 | iter-14_61 + p10 v10->6 | 7.25 | 10.13 | p10 9.78->9.69. Direction confirmed |
| 3 | iter-2 + p3 v9->7 | 7.34 | 11.44 | p3 BLEW UP. Confirms p3 val=9 saturated |
| 4 | iter-2 + p3 v9->11 | 7.37 | 11.84 | Both directions saturated. SKIP p3 |
| 5 | iter-2 + p3 line=228->232 | 7.42 | 12.67 | Disaster. p3 line saturated |
| 6 | iter-2 + p9 v10->8 | 7.29 | 10.39 | p9 regressed (9.71->10.39). SKIP |
| 7 | iter-2 + p10 v8->6 | 7.25 | 10.13 | p10 9.69->9.68 marginal |
| 8 | iter-7 + p9 v5->3 | 7.25 | 10.13 | p9 regressed slightly. SKIP |
| 9 | iter-7 + p10 v6->4 (cascading) | 7.24 | 10.13 | p10 9.55. BREAKTHROUGH |
| 10 | iter-9 + p10 v4->2 | 7.24 | 10.13 | p10 9.55. Tiny gain |
| 11 | iter-10 + p10 v2->0 | 7.23 | 10.13 | p10 9.48. KEEP |
| **12** | **iter-11 + p9 v6->4** | **7.23** | **10.13** | **p9 9.69. BEST. PROMOTE** |
| 13 | iter-12 + p9 v10->8 | 7.27 | 10.35 | p9 10.35 regression. SKIP |
| 14 | iter-12 + global after=120->100 | 7.84 | 12.0 | Disaster. global after cohort BANNED |

## Newly saturated levers (add to METHODOLOGY.md banned list)

- p3 val=6 (24 sites) — BOTH directions saturated (6->4 BLOWS UP, would be 6->8 untested but high risk)
- p3 val=9 (24 sites) — BOTH directions saturated (9->7, 9->11 both BLOW UP)
- p3 line=228 (24 sites) — UP direction saturated (228->232 BLOWS UP)
- p9 val=10 (11 sites) — saturated (10->8 regresses; iter-13 reconfirms)
- global w:after=120 (35 sites) — saturated, regresses many pages

## Newly confirmed sweet zones (KEEP for stacking)

- **p10 ALL spacing values collapse to 0** — every step (10->6->4->2->0) improves
- p9 val=2 -> 0 (4 sites)
- p9 val=8 -> 6 (3 sites)
- p9 val=6 -> 4 (3 sites)
- p10 val=10 -> 6 deeper than W48's iter-14_61 (10->8)

## Next recommended angles

1. **p9 line=244 (7 sites)** — untouched line-spacing cohort on p9
2. **p10 line=228 (4 sites)** — untouched on p10
3. **p11 attack** — still at 10.13 (max bottleneck); needs creative new lever
4. **p14 (9.67)** — never attacked, possible easy win
