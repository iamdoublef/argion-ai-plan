# iter-61 path-p3p9p10-cohort STATUS

Building on W48 = 7.27/10.13 (iter-60 iter-23). Attack: p3 (10.03), p9 (9.94), p10 (9.79) +
untouched cohorts (w:after=120, w:spacing val=5, w:before=170).

## Baseline = W48 (iter-60 iter-23) per-page diffs
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

## iter-1 grep evidence (cohort distribution)

Note: brief said w:before=200 — does NOT exist in document (no matches).
Closest cohort is `w:before="170"` (7 sites).

| cohort | total | p1 | p2 | p3 | p4 | p5 | p6 | p7 | p8 | p9 | p10 | p11 | p12 | p13 | p14 | p15 |
|--------|------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| w:after=120 | 23 | - | 10 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| w:spacing val=5 | 33 | 6 | 11 | - | - | 3 | - | - | - | **3** | - | - | 3 | 3 | 3 | 1 |
| w:before=170 | 7 | 1 | - | - | - | 2 | - | - | - | **2** | - | - | - | 2 | - | - |
| w:before=80 | 10 | - | - | - | - | 1 | - | - | - | 1 | - | - | 3 | 1 | 3 | 1 |

Key observations:
- **p3** has neither val=5 nor before=170 cohort sites; only `after=120` (1 site)
- **p9** is on 3 untouched cohorts: val=5 (3), before=170 (2), before=80 (1), after=120 (1)
- **p10** has after=120 (1) but no val=5 or before cohorts
- **p3 specific levers** need to come from p3's own spacing/run patterns

## Run log

| iter | recipe | mean | max | note |
|------|--------|------|------|------|
