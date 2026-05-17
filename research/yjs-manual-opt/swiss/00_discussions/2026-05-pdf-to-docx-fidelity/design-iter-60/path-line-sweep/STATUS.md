# iter-60 path-line-sweep STATUS

Building on W47 = 7.28/10.16 (iter-59 iter-56). New angle: per-page line cohort sweeps,
char-spacing surgery on disclaimer cells, p11-targeted reflow.

## Headline: W48 = iter-23 = **7.27 / 10.13**
Precise mean **7.2680** / max **10.13** (W47 was 7.2767 / 10.16).
Mean −0.0087, **max −0.03 (small but real)**.

| run | recipe | mean | max | note |
|-----|--------|------|------|------|
| iter-1  | global line=240→238 | 7.55 | 10.63 | regress (p3 +0.6) |
| iter-2  | global line=240→242 | 7.37 | 10.61 | regress |
| iter-3  | global line=240→241 | 7.28 | 10.16 | inert (lineRule=auto rounds) |
| iter-4  | global line=240→244 | 7.45 | 11.28 | regress |
| iter-5  | p11-only line=240→238 | 7.28 | 10.20 | regress slight |
| iter-6  | p11-only line=240→242 | 7.31 | 10.61 | regress |
| iter-7  | p11 trHeight 225→215 | 7.30 | 10.51 | regress |
| iter-8  | p11 trHeight 225→240 | 7.43 | 12.50 | disaster |
| iter-9  | p11 trHeight 225→220 | 7.30 | 10.46 | regress |
| iter-10 | p11 cellmar bottom 32→28 | 7.31 | 10.63 | regress |
| iter-11 | p11 disclaimer tblBorders nil→black | 7.28 | 10.16 | inert (tcBorders shadow) |
| iter-12 | p11 disclaimer tcBorders sz=6 black | 7.31 | 10.61 | regress |
| iter-13 | p11 disclaimer tcBorders sz=4 black | 7.29 | 10.40 | regress |
| iter-14 | p11 banner text F5F5F5→808080 | 7.28 | 10.16 | tie |
| iter-15 | p11 banner text F5F5F5→333333 | 7.28 | 10.16 | tie |
| iter-16 | global F5F5F5→A0A0A0 (banner) | 7.29 | 10.17 | regress slight |
| iter-17 | p11 disclaimer padding 176/110→60/60 | 7.29 | 10.29 | regress |
| iter-18 | p11 disclaimer body w:spacing val=10→0 | **7.27** | **10.13** | **WIN** |
| iter-19 | global w:spacing val=10→0 | 7.46 | 10.77 | disaster |
| iter-20 | targeted Arial sz=14 black spacing=10→0 (62 sites) | 7.45 | 10.76 | regress |
| iter-21 | iter-18 + disclaimer heading val=10→0 | 7.28 | 10.21 | regress |
| iter-22 | iter-18 + p11 cell val=2→0 | 7.27 | 10.13 | tiny win (precise mean ↓0.0007) |
| iter-23 | iter-22 + p12-p14 cell val=2→0 | **7.27** | **10.13** | **W48 = THE FINAL** (p13 −0.15, p14 −0.02) |
| iter-24 | iter-23 + p9-p10 val=2→0 | 7.28 | 10.26 | broke p11 |
| iter-25 | iter-23 + p15 val=2→0 | 7.27 | 10.13 | tie 23 (no diff) |

## Final W48 = iter-23
- mean **7.27** / max **10.13** (precise 7.2680, max −0.03 from W47)
- per-page: 2.17 3.23 10.03 6.38 8.55 3.77 7.18 7.05 9.94 9.79 10.13 8.84 9.25 9.67 3.04
- p11: 10.16 → **10.13 (−0.03)**
- p12: 8.85 → **8.84 (−0.01)**
- p13: 9.40 → **9.25 (−0.15)** ← biggest single win
- p14: 9.69 → **9.67 (−0.02)**
- p15: 2.96 → **3.04 (+0.08)** ← small regress (acceptable, net positive)
- wt_count 448 (preserved) / editability 100% / text_ratio 1.0
- Word-safe: COM round-trip PASS.

## Recipe = stack of 8 levers on top of W47 (W47's 6 + 2 new):
1. (W47) inner_E5E5E5_to_F5F5F5 (340 sites)
2. (W47) line_252_to_244 (7 sites)
3. (W47) line_264_to_260 (9 sites)
4. (W47) line_230_to_228 (37 sites)
5. (W47) line_271_to_273 (13 sites)
6. (W47) before_160_to_170 (7 sites)
7. **(NEW) p11 disclaimer body w:spacing val=10→0** (1 site) — disclaimer text wraps tighter
8. **(NEW) p11–p14 cells w:spacing val=2→0** (~100 sites scoped to 4 pages) — cell text horizontal compaction matches target

## What worked (positive evidence)

### A. iter-18: disclaimer body char-spacing val=10→0 (−0.03 max)
The disclaimer cell on p11 has body run with `<w:spacing w:val="10"/>` adding 10×1/120 in
char spacing. Removing forces text to wrap closer to target's 1-line wrap. Single-site
change but the cell wrap difference dominated p11 diff. Heading change (sz=13 Arial Black)
regresses — the heading is shorter and benefits from looser spacing.

### B. iter-22+23: p11-p14 cell text val=2→0 (−0.15 p13, −0.02 p12/p14)
Cells in dense tables (p11 troubleshooting, p13 install, p14 disposal) use `<w:spacing
w:val="2"/>` (2/120 char spacing). Target renders with tighter cells. Scoped to pages with
table content avoids reflow disaster on p9-p10 (which have different cell width/wrap).

## What didn't work (negative evidence — for future iters)

- **Global line=240 sweeps** (±1, ±2, ±4): line=240 has 500 sites globally; any change
  cascades reflow on dense pages, breaking max. lineRule=auto rounds ±1 inert.
- **p11-only line=240 ±2/4**: also regresses — local p11 reflow shifts other tables.
- **trHeight 225 ±5/15**: p11 row heights are tight; reducing wraps cells, expanding
  inflates row.
- **Disclaimer cell black tcBorders**: matches target visually but adds 2-4 px thickness
  pushing text down → p11 max +0.13~+0.45.
- **Banner F5F5F5 text → darker**: text is dark-on-white anyway; LO renders identical.
- **Global spacing val=10→0** (88 sites): widespread reflow disaster.
- **Disclaimer cell padding reduction**: changes wrap but max regresses.

## Strategy notes for iter-61+ (next attack angles)

- **p3 (10.03), p9 (9.94), p10 (9.79)**: now the next maxes. p11 is no longer "the" max.
  Targeted p3-p10 cell tweaks (within their tables) likely next sweet spot.
- **Banner BG / page header**: the candidate top banner shows BLACK bar; target also
  black bar. But the right-aligned chapter name uses F5F5F5 (almost invisible). May not
  matter visually.
- **Untouched cohort**: w:after=120 (35 sites), before=200 (18 sites), val=5 (33 sites),
  val=6 (37 = list bullets).
- **Acceptable regressions**: p15 +0.08 in iter-23 — caused by disclaimer body reflow
  affecting p11 sectPr boundary. Net positive so retained.

## Validation

```
PYTHONUTF8=1 python compare_word.py iter-23/output.docx iter-23/output.word.pdf
# OK: ... -> ...output.word.pdf  (MS Word COM round-trip PASS)

PYTHONUTF8=1 python score_candidate.py iter-23/output.docx ...
# wt_count 448, text_ratio 1.0, editable 100%, PASS overall
```
