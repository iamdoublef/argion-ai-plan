# design-iter-31 path-swiss-pipeline status

## Result

Backported W27 visual parameters into the **Swiss pipeline**
(`swiss/tools/export-docx.js`). Pipeline retains full multi-SKU + multi-language
templating; visual fidelity is now meaningfully closer to the target PDF.

| Source | Score (mean / max) |
|---|---|
| W27 reference (python-docx, single-shot, NOT templated) | **8.67 / 12.35** |
| Swiss pipeline baseline (before iter-31) | 13.87 / 26.65 |
| **Swiss pipeline iter-31 (final)** | **11.74 / 18.83** |

Delta vs baseline: mean -2.13 (-15.4%), max -7.82 (-29.3%).
Delta vs W27 gold: mean +3.07 (still behind), max +6.48.

The remaining gap to W27 is structural: W27 parses the rendered HTML and lays out
a flat document that matches the PDF page-by-page; Swiss generates from JSON +
data, producing different paragraph trees that LibreOffice flows slightly
differently. Closing the last 3 points would require either:

1. Matching specific page break decisions per-product (not portable)
2. Adopting a constraint-based layout pass (out of scope)

## Verification

- Pages: target 15, candidate 15 (no extra pages)
- Text ratio: 1.0 (all source text preserved)
- Editable %: 100.0 (no text boxes, no image-rendering hacks)
- wt_count: 361 (real `<w:t>` runs)
- Validates in `docx` skill's `validate.py`: PASSED
- No `autoSpaceDE`/`autoSpaceDN` OOXML that breaks MS Word (the W28 trap)
- Builds cleanly for: cn / gb / hk / de / it / tw, brands wevac / vesta / act,
  SKUs imt050 / v23

## Iteration table (selected key iterations)

| Iter | Change | Mean | Max | Decision |
|---|---|---:|---:|---|
| baseline | export-docx.js as-is | 13.87 | 26.65 | reference |
| 1 | W27 font sizes (body 14, table body 14, table header 12, small 11) | 13.72 | 26.26 | kept |
| 2 | Tighter alert box, manual bullet prefix, inline step flow | 13.13 | 26.39 | kept |
| 3 | Add footer to TOC + body sections, header size to 6.75pt | 13.21 | 26.46 | kept |
| 14 | Tune cell margins, fix caution-box no triangle | 13.86 | 28.09 | kept |
| 18 | Add `cellWarranty` margins for chapter 10 tables | 13.67 | 30.08 | kept |
| 19-20 | Tune `cellWarranty` to 32 v / 80 left | 13.64 | 29.54 | kept |
| 21 | Normal cell margins 40 v / 60 h (was 30 / 60) | 13.62 | 29.54 | kept |
| 22 | **BREAKTHROUGH: body line spacing 278 (was 189/buggy 0.79)** | **12.76** | **19.48** | kept |
| 23 | Body line 280 | 12.69 | 19.51 | kept |
| 24 | Bullet line 270 | 12.58 | 19.51 | kept |
| 25 | Alert bullet line 250 | 12.52 | 19.51 | kept |
| 26 | Render `[btn:Key]` as Courier on F2F2F7 shading | 12.51 | 19.46 | kept |
| 29 | Honor figure `block.max_height` (e.g. 72mm) | **11.74** | 18.83 | kept |
| 30 | Add compact-safety detection for 12+ item warning boxes | 11.88 | 18.83 | rejected |
| 31 | Same as iter-30 but only when itemCount ≥ 12 | **11.74** | 18.83 | **kept** |

## Final visual diffs per page (lower=better)

```
p1:  3.09   (cover)
p2:  5.14   (TOC)
p3: 18.27   (safety warning, 24 items — densest page)
p4:  7.92   (safety continued, 9 items)
p5: 13.47   (usage tips, bullets)
p6: 11.59   (structure parts table)
p7: 15.53   (features + buttons table)
p8: 10.20   (specs table)
p9: 14.71   (operation step flow)
p10: 12.65  (operation maintenance steps)
p11: 18.83  (troubleshooting table - MAX)
p12: 11.26  (maintenance text)
p13: 13.99  (installation / storage)
p14: 13.82  (warranty info tables)
p15:  5.60  (warranty bullets)
```

## Key visual parameters backported from W27

### Sizes (half-points)

| Param | Baseline | W27 | iter-31 |
|---|---|---|---|
| body text | 14 (7pt) | 14.1 | 14 |
| sub-title | 14 | 15 (7.5pt) | 15 |
| section title | 18 | 18 (9pt) | 18 |
| chapter num (red) | 27 | 27 (13.5pt) | 27 |
| chapter title (bold) | 22 | 22 (11pt) | 22 |
| TOC title | 30 | 30 (15pt) | 30 |
| table body | 15 | 13.4 (6.7pt) | 14 |
| table header | 14 | 12 (6pt) | 12 |
| cover MODEL | 11 | 12 (6pt) | 12 |
| cover company / disclaimer | 14 | 11 (5.4pt) | 11 |
| header brand | 14 | 13 (6.75pt) | 13 |
| header meta (right) | 11 | 11 (5.4pt) | 11 |
| small / footer | 10 | 11 (5.4pt) | 11 |

### Layout

| Element | Baseline | W27 | iter-31 |
|---|---|---|---|
| Body line spacing | `Math.max(180, size*13.5)` = 189 = **0.79 line BUG** | 240*1.16=278 | **280** |
| Bullet glyph | docx-js numbering • | manual `•   ` red Arial-Black 5.8pt | manual `•   ` red Arial-Black 7pt (size 14) |
| Bullet indent | left:420 hanging:210 | left:180 hanging:180 | left:180 hanging:180 |
| Bullet line spacing | 16 dxa = 0.07 line | 1.13 line | 270 |
| Alert box padding | 55 v / 90 h | 46 v / 176-110 h | 46 v / 176-110 h |
| Step flow | 2-col table with badge cell | inline shaded run | **inline shaded run** |
| Footer | (missing!) | 2-cell table with thin top rule | **2-cell table with thin top rule** |
| `[btn:Key]` token | bold accent text | Courier on F2F2F7 shading | Courier on F2F2F7 shading |
| Figure `max_height` | ignored | honored | **honored** |
| compact-warranty cell pad | (none) | 52 v / 87 left | 32 v / 80 left |

## Templating preservation

### Multi-SKU verification

| SKU | Brand | Region | Build | DOCX size |
|---|---|---|---|---|
| imt050 | wevac | cn | OK | 560.4 KB |
| imt050 | wevac | gb | OK | 559.1 KB |
| imt050 | wevac | hk | OK | 560.5 KB |
| imt050 | wevac | de | OK | 559.9 KB |
| imt050 | wevac | it | OK | (deferred) |
| imt050 | wevac | tw | OK | (deferred) |
| v23 | wevac | cn | OK | 1705.8 KB |
| v23 | vesta | cn | OK | 1705.7 KB |
| v23 | act | cn | OK | 1705.7 KB |

### Theme-config addition

`brand-themes.json > <brand>.docx` now accepts three additional optional override blocks:

- `sizes`: any subset of `bodySize, subtitleSize, sectionTitleSize, chapterNumberSize, chapterTitleSize, coverBrandSize, coverTypeSize, coverProductSize, coverModelSize, coverCompanySize, tocTitleSize, tocChapterSize, tocTextSize, tocPageSize, headerBrandSize, headerMetaSize, smallSize, tableBodySize, tableCompactSize, tableHeaderSize`
- `images`: any subset of size presets (`cover`, `figure`, `splitPanel`, `stepSingle/Double/Triple[Compact]`, `rowSingle/Double/Triple`, `inlineIcon`)
- `margins`: any subset of cell-margin sets (`cellNormal`, `cellCompact`, `cellWarranty`, `alertCell`, `noteCell`)

The W27-tuned values are the default; brands can override per-product if they have specific requirements (e.g. Vesta wants larger body text, ACT wants tighter tables).

No brand-themes.json content was changed — the new keys are optional and inherit from the new W27-tuned defaults in `export-docx.js`.

## Word compatibility

- All test variants open in MS Word (validated via `office/validate.py`)
- No `autoSpaceDE`/`autoSpaceDN` OOXML attributes (the W28 trap)
- All text in `<w:t>` editable runs (not text boxes, not page-image hacks)
- All images embedded as inline `<wp:inline>` drawings
- 12 sections, 20 tables, 17 drawings

## Files

- `final.docx` — final IMT050 wevac CN output (also at `swiss/output/imt050-wevac-eu-cn.docx`)
- `export-docx.final.js` — final tool source (now installed at `swiss/tools/export-docx.js`)
- `export-docx.baseline.js` — snapshot of original tool before iter-31 began
- `iter-1.docx` ... `iter-31.docx` — intermediate iteration outputs
- `iter-*.score.json` — per-iteration scoring results
- `diff-page-*.png` — diff visualizations used for debugging
- `STATUS.md` — this file

## Risks and future work

1. **Worst page is page 11 troubleshooting (18.83)**. The table cell margins
   for troubleshooting are close, but the disclaimer caution box at the bottom
   pushes content slightly differently from W27. A targeted compact-troubleshoot
   margin set could help (similar to compact-safety / compact-warranty).
2. **Page 3 safety warning (18.27)** is the densest single page. Reducing the
   line spacing inside the warning box to 0.96 (W27 tight mode) could help but
   risks affecting page 4 which has fewer items. The 12-item threshold added
   in iter-31 makes this safe.
3. **No regression testing** on V23 PDF vs DOCX — V23 has different layout
   and may benefit from different parameter values. Future iteration could
   add per-product overrides in brand-themes.json.
4. **Multilingual long-text** (DE/IT) was NOT scored, only built. The
   line-spacing tuning may or may not help with longer-language pagination.
