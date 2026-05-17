# iter-59 path-invisible-borders STATUS

Building on W46 = 7.38/10.90 (iter-58). New angle: line spacing per-page cohorts
+ alt-row stripe variants, all stacked on the iter-58 stack of 6 levers.

## Headline: W47 = iter-56 = **7.28 / 10.16**
Precise mean **7.2767** / max **10.16** (W46 was 7.381/10.90).
Mean −0.10, **max −0.74 (broke the 10.9 barrier)**.

| run | recipe | mean | max | note |
|-----|--------|------|------|------|
| iter-0  | (baseline = W46) | 7.3807 | 10.90 | W46 confirmed |
| iter-1  | top sz=8 first→FF | 7.4067 | 10.90 | regress (p4 6.17→6.56) |
| iter-2  | inner E5→E0 | 7.3867 | 10.90 | regress |
| iter-3  | inner E5→EB | 7.3733 | 10.90 | win small |
| iter-4  | banner sz=18→sz=12 | 7.9333 | 11.56 | disaster |
| iter-5  | line=278→274 | 7.5380 | 11.06 | regress |
| iter-6  | inner E5→EC | 7.3733 | 10.90 | win small |
| iter-7  | inner E5→F0 | 7.3720 | 10.90 | win small |
| iter-8  | inner E5→EE | 7.3727 | 10.90 | win small |
| iter-9  | inner E5→F5 | **7.3707** | 10.90 | best single |
| iter-10 | inner E5→FF | 7.3767 | 10.90 | tie baseline |
| iter-11 | after=27→24 | 7.40 | 11.02 | regress |
| iter-12 | after=27→30 | 7.53 | 13.32 | disaster |
| iter-13 | top sz=12 red→sz=8 | 7.39 | 11.05 | regress |
| iter-14 | after=40→30 | 7.39 | 10.90 | regress |
| iter-17 | F5 + line=252→248 | 7.3613 | 10.90 | best double |
| iter-18 | F5 + line=252→256 | 7.3620 | 10.90 | close |
| iter-20 | F5 + 252→244 + 264→260 | 7.3540 | 10.90 | triple win |
| iter-22 | F5 + line=252→244 | 7.3580 | 10.90 | best 2-lever |
| iter-24 | F5 + 252→244 + 264→260 | 7.3507 | 10.90 | triple best |
| iter-29 | + line=230→228 | **7.3020** | **10.16** | MAX BARRIER BROKEN |
| iter-30 | + line=230→232 | 7.46 | 12.67 | disaster (opposite dir) |
| iter-33 | + line=230→226 | 7.51 | 12.92 | too aggressive |
| iter-38 | + line=271→273 | **7.2800** | 10.16 | quint win |
| iter-40 | + 271→275 | 7.3080 | 10.16 | regress |
| iter-43 | + 271→277 | 7.3413 | 10.16 | regress |
| iter-56 | + before=160→170 | **7.2767** | 10.16 | **W47 = THE FINAL** |
| iter-60 | + before=160→165 | 7.2767 | 10.16 | tie 56 |
| iter-61 | + before=160→175 | 7.2820 | 10.16 | regress |
| iter-65 | + before=160→168 | 7.30 | 10.16 | regress |
| iter-67 | + after=32→30 | 7.2860 | 10.16 | regress |
| iter-69 | + cellmar 32→30 | 7.31 | 10.52 | regress |
| iter-71 | + left sz=2 space 4→6 | 7.2827 | 10.16 | regress |
| iter-72 | + left sz=2 space 4→2 | 7.2767 | 10.16 | tie 56 (inert) |

## Final W47 = iter-56
- mean **7.28** / max **10.16** (precise mean −0.103, **max −0.74** from W46)
- per-page: 2.17 3.23 **10.03** 6.38 8.55 3.77 7.18 7.05 9.94 9.79 10.16 8.85 9.40 9.69 2.96
- p3: 10.90 → **10.03 (−0.87)**
- p4: 6.17 → **6.38 (+0.21)**
- p5: 8.83 → **8.55 (−0.28)**
- p7: 7.22 → **7.18 (−0.04)**
- p8: 7.12 → **7.05 (−0.07)**
- p9: 10.31 → **9.94 (−0.37)**
- p10: 9.95 → **9.79 (−0.16)**
- p11: 10.16 → **10.16 (0)**
- p12: 8.87 → **8.85 (−0.02)**
- p13: 9.32 → **9.40 (+0.08)**
- p14: 9.70 → **9.69 (−0.01)**
- p15: 3.00 → **2.96 (−0.04)**
- wt_count 448 (preserved) / editable 100% / text_ratio 1.0
- Word-safe: pack.py validate PASS (328→328); compare_word.py COM round-trip PASS.

## Recipe = stack of 6 NEW levers on top of W46
1. `inner_E5E5E5_to_F5F5F5` (340 sites): table inner border color E5→F5 (much lighter)
2. `line_252_to_244` (7 sites): table-row line spacing, more compact
3. `line_264_to_260` (9 sites): table-row line spacing, slight compaction
4. `line_230_to_228` (37 sites): list/bullet line spacing, slight compaction — **THE MAX-BREAKER**
5. `line_271_to_273` (13 sites): banner line spacing, slight expansion — improves p5
6. `before_160_to_170` (7 sites): paragraph spacing-before, slight expansion — improves p9

## What works (positive evidence)

### A. Inner border E5→F5 (−0.010 mean, monotonic)
340 sites of table cell borders at `<w:* w:val="single" w:sz="4" w:space="0" w:color="E5E5E5"/>`.
The target PDF rendering shows even lighter borders than E5E5E5. F5F5F5 was sweet spot
in 5-point sweep: EB→EC→EE→F0→F5 (all wins), FF (back to baseline). Lighter than F5
breaks (too washed out). Darker than EB regresses. **Bracket: E0=regress, EB/EC/EE/F0/F5=win, FF=neutral**.

### B. Line=252→244 (−0.005 mean, p9 improvement)
7 sites of `<w:spacing w:line="252"/>`. Tightens table-internal text vertical layout
to better match target. 248 was first try, 244 better, 240/236 broke max.

### C. Line=264→260 (−0.001 mean)
9 sites; similar table-row tightening. 256 was too aggressive.

### D. Line=230→228 (−0.078 mean, **max 10.90→10.16**)
37 sites of `<w:spacing w:line="230"/>` — the breakthrough.
This cohort is likely list/bullet line-height. **228 is the only sweet spot**:
226 broke max to 12.92; 232 broke max to 12.67. Single-step compaction needed.

### E. Line=271→273 (−0.022 mean, p5 improvement)
13 sites; banner line-height. Counterintuitive direction (UP not down) — improves
p5 by 0.33 because banner spacing tightens to match target. 275/277 regress.

### F. Before=160→170 (−0.002 mean, p9 −0.18)
7 sites of `<w:spacing w:before="160"/>` — paragraph spacing-before. Slight expansion
matches target better. 165 ties, 175/180 regress.

## Negative evidence (W47 levers tried, abandoned)

- **top sz=8 first→FF**: regresses p4 0.39 (confirmed iter-58 finding).
- **banner top sz=18→sz=12/14/16/20/22**: catastrophic max regression. Banner MUST stay sz=18.
- **line=278 (Title) any direction**: hurts somewhere; sensitive structural cohort.
- **line=264→256 (more aggressive than 260)**: p12 hurts.
- **line=240 (154-site body cohort)**: too sensitive, both directions regress.
- **after=27/40/120 changes**: all regress badly (p3 reflow).
- **before=80/160 farther than 170**: regress.
- **cellMar w=32/36 changes**: regress.
- **alt-row shd F1F1F6→F5/F0/EBEBEC**: regress (iter-58 finding confirmed).
- **left sz=2 red space=4 changes**: inert or regress.

## Composability with W46 (and earlier) stack
W47 = W46 + 6 new doc levers (E5→F5 color, 5 line/before tunings).
All W46 levers preserved (bottom sz6 FF, top sz10 FF, top sz8 second FF, left sz18→sz2,
footer micro-tunes, all prior W43/W45 stack).

## Insight: "line spacing per-page" lever class
After exhausting the make-invisible cohort in iter-58, this iter discovered a new
fertile lever class: **line spacing tweaks targeting specific cohorts (7-45 site
buckets)**. Each cohort represents a distinct paragraph type (banner, body, list,
table-row). Sweet spots are typically 1-3 units away from the original value; further
breaks layout. The line=230 cohort was the max-breaker; line=271 a smaller win;
others (240/278) too sensitive to touch.

## Recommendation for W48

Max is now p11 = 10.16. Remaining unexplored:
- p11 disclaimer cohort: examine paragraph 234 area for tuneable elements.
- spacing-after small cohorts (after=20=7, after=60=7).
- font-related rPr cohorts (w:rFonts, kerning, sz=21).
- pgMar (margins) — iter-58 said inert but try with new base.
- Text run-level letter-spacing variants on bullet/disclaimer text.

## Files
- baseline.docx — copy of W46 final
- baseline_unpacked/ — unpacked
- iter-{N}/output.docx — candidates
- iter-{N}/output.score.json
- iter-56/output.docx — W47 final source (promoted to ../../final/)
- edit_iter*.py — recipe registry + apply_recipe() drivers
- run_iter.py — pack + score wrapper
