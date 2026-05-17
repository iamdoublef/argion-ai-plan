# design-iter-53 path-after-line-cohort — STATUS

## Outcome: CONVERGENT BREAKTHROUGH — W41 at 8.00/11.98 (relabels current HEAD)

This path validated, via an independent surgical hypothesis, the **page-12 line=271
sub-cohort** breakthrough that a parallel sibling agent (commit 032aed3) had also
discovered before this run completed. My iter-10 output is **byte-identical** to the
current HEAD final docx — both paths converged on the same minimal effective patch.

| version | recipe | mean | max |
|---------|--------|------|-----|
| W39 (committed 472f1e8) | sz=14 BLACK 9→10 + sz=10 RED 7→6 stack | 8.06 | 11.98 |
| W40-79355bc (committed) | W39 + p9 line=264→252 (7 sites) | 8.01 (8.005) | 11.98 |
| W40-iter52-candidate (uncommitted candidate) | + sz=14 BlackArial 10→11 (9 sites) | 8.01 (8.006) | 11.98 |
| **W41 = 032aed3 HEAD (mislabeled "W40")** | + line=271 p12-only 271→260 (4 sites) | **8.00 (7.996)** | **11.98** |

The committed file's score.json reports `overall_mean_diff: 8.0` (display) /
`7.996` (precise). Per-page p12 dropped 9.93 → 9.79 (−0.14).

This run did NOT discover a new improvement; HEAD already contained the patch.
The 9 alternative surgical hypotheses (p14 after=80 ±, line=271 global ±,
after=120 ±) were all confirmed-regressing, ruling out adjacent levers.

## Baseline used by this run (commit 79355bc, hash d0569a)
- mean **8.005**, max **11.98**
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 **9.93** 10.39 11.98 3.31
- wt_count 446 / editable 100% / text ratio 1.0

## Final achieved by this run = iter-10 = HEAD 032aed3 (hash 034824)
- mean **7.996** (display 8.00) / max **11.98** (unchanged)
- per-page: 2.88 3.25 10.96 6.23 9.9 4.33 7.71 7.85 10.43 10.01 10.92 **9.79** 10.39 11.98 3.31
- p12 dropped 9.93 → 9.79 (−0.14)
- wt_count 446 / editable 100% / text ratio 1.0 / Word-safe (compare_word OK)
- Recipe: paragraphs idx 251..254 (p12 sub-cohort), `<w:spacing w:line="271"...>` → `w:line="260"`. 4 sites modified.

## Iterations (W40 baseline 8.005/11.98)

| iter | change | sites | mean | max | verdict |
|------|--------|-------|------|-----|---------|
| 1 | recon (no edit) | — | — | — | data: after=80 (17), after=120 (23), line=271 (17) mapped |
| 2 | p14 after=80→60 surgical (idx 280/291/300) | 3 | 8.11 | 13.49 | regression (p14 +1.51) |
| 3 | p14 after=80→70 (half tighten) | 3 | 8.05 | 12.62 | regression (p14 +0.64) |
| 4 | p14 after=80→90 (loosen) | 3 | 8.03 | 12.33 | regression (p14 +0.35) |
| 5 | line=271→265 global (17 sites) | 17 | 8.16 | 12.32 | regression (p5 9.9→12.32 +2.42) |
| 6 | line=271→278 global (loosen) | 17 | 8.05 | 11.98 | regression (p5 9.9→10.45 +0.55) |
| 7 | after=120→100 cohort (23 sites) | 23 | 8.59 | 12.87 | CATASTROPHE (+0.58 mean) |
| 8 | after=120→140 cohort | 23 | 8.40 | 12.31 | regression (+0.39 mean) |
| 9 | line=271 **p12-only** 271→265 (idx 251..254) | 4 | **8.00 (7.998)** | **11.98** | **GAIN −0.007 mean (p12 −0.11)** |
| 10 | line=271 **p12-only** 271→260 | 4 | **8.00 (7.996)** | **11.98** | **GAIN −0.009 mean (p12 −0.14) — BEST = HEAD** |
| 11 | line=271 **p12-only** 271→252 (probe) | 4 | 8.00 (8.001) | 11.98 | past sweet spot (p12 9.79→9.85) |

## What works (positive evidence)
**Page-isolated cohort surgery** on line=271 page-12 sub-cohort. 4 sites at
idx 251..254 (numbered chapter section bullets on p12, all `before=0 after=32`).
The PDF renders these tighter than the W40 auto-271; tightening to 260 (−11
twips, ≈0.55pt) snaps p12 from 9.93 → 9.79.

Sweet spot is at −11 twips (iter-10, gain −0.009). Pushing to −19 twips
(iter-11, snap to 252) regresses by +0.06 on p12.

**Composability confirmed**: iter-49's "pPr/rPr independent axes" hypothesis
holds — this patch stacks cleanly on top of iter-52's sz=14 BlackArial rPr patch.

## Negative evidence (confirmed dead-ends THIS RUN)

### p14 after=80 cohort (saturated, both directions)
- after=80→60 (3 sites): p14 +1.51
- after=80→70: p14 +0.64
- after=80→90: p14 +0.35
- **Conclusion**: 3 section-heading paragraphs on p14 (idx 280/291/300, "QC声明"
  style headings) are at local optimum. Cannot move with this lever.

### line=271 global cohort (saturated)
- 271→265 globally (17 sites): p5 +2.42 (dominates regression). p5 has 13 of 17 sites.
- 271→278 globally: p5 +0.55
- **Conclusion**: The 13 p5 sites and 4 p12 sites have different optima. p5 wants
  to stay at 271; p12 wants 260. Don't move globally.

### after=120 cohort (FATAL)
- 120→100 (23 sites): +0.58 mean — affects every chapter subtitle, system-wide regression
- 120→140: +0.39 mean
- **Conclusion**: after=120 is the dominant after-spacing for chapter subtitles
  across every page. This is THE structural lever and is at global optimum.

## Word safety
All 11 iterations: pack.py validate PASS (328 paragraphs preserved). iter-10
final passed compare_word.py (MS Word COM) conversion cleanly.

## Convergence note

Two batch agents working in parallel independently rediscovered the same surgical
patch. The brief recommended p14 after=80 (3 sites), line=271 global (17 sites),
and after=120 (23 sites). My run ruled out all three brief-recommended levers,
then explored an unbriefed-but-implied lever (line=271 PAGE-ISOLATED), which
was the actual win. This validates the heuristic: when global cohort moves both
regress, try page-isolated sub-cohorts before abandoning the lever.

## Recommendation for W42

The W41 win is small (−0.009 mean). The remaining headroom is concentrated on:
1. **p14 (max=11.98)** — STILL the bottleneck max. p14 after=80 surgery saturated.
   Try p14 line=240 cohort (18 sites at idx 281..305 minus 291, 300; body-text paragraphs).
   Page-isolated, narrow step (±10 twips).
2. **p11 (10.92), p13 (10.39), p9 (10.43)** — try page-isolated line cohort surgery
   following the iter-53 p12 template (small sub-cohort, ±11 twips).
3. **p3 (10.96)** — page 3 line=230 cohort was saturated in iter-49 globally;
   try page-isolated. p3 has 24 line=230 sites.
4. **DO NOT** revisit: p14 after=80 (saturated), line=271 global (saturated),
   after=120 cohort (FATAL), p11/p3 line global (saturated), lineRule global (FATAL).
