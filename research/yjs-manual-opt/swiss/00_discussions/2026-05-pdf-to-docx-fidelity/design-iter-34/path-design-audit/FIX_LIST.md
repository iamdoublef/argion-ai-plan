# TOP 10 Fix List — most likely to break the plateau

Sorted by **(visual impact) × (1 / fix difficulty)**. Each entry includes a concrete docx-level change.

Legend:
- **Impact**: estimated reduction in `overall_mean_diff` (currently 8.67) if applied alone, holding others constant. Aggregate caveat: many fixes overlap, the total isn't simply additive.
- **Difficulty**: rated 1 (one-line XML attribute change) to 5 (architectural restructure)
- **Path**: docx file path inside the zip + element

---

## #1 — Drop body font from 8pt to 7pt (uniform)
**Impact: ~1.2-1.5 pt of mean diff** | **Difficulty: 1** | **Pages affected: 3,4,5,8,11,13,14 (every dense-text page)**

Change `word/styles.xml`:
- `BodyText3 rPr/sz val=16` → **`val=14`** (8pt → 7pt)
- `Caption rPr/sz val=18` → **`val=16`** (9pt → 8pt) for table headers
- Leave `Heading1-9` unchanged (target keeps headings at 13.5pt and W27's 14pt is close enough)

Optional: per-style override for operation pages (p9, p10, p14) — keep BodyText at 7.5pt there. Target uses **7.5pt for body** in operation/warranty chapters but **6.5-7pt for safety/spec/trouble tables**.

If you only do ONE thing from this list, do this.

---

## #2 — Restructure p7 function-table cells to inline keycap chips
**Impact: ~1.0 pt (p7 alone goes from 7.81 → ~3)** | **Difficulty: 4** | **Pages affected: 7, also 11 (trouble) inherits keycap convention**

Current p7 cell structure (W27, table 4):
```
<tc><p>1</p><p>Power</p><p>电源</p></tc>  <tc><p>点击开机...</p></tc>
```
Should become:
```
<tc>
  <p>
    <r>1 </r>
    <r style="Keycap"><borderTop+left+right+bottom 0.5pt black, fontFamily=Courier or Arial-BoldMT>Power</r>
    <r> 电源</r>
  </p>
</tc>
<tc><p>点击开机...</p></tc>
```

Practical implementation: define a new character style `Keycap` with:
- `rFonts ascii="Arial Black" hAnsi="Arial Black"`
- `sz val=12` (6pt)
- `bdr top/left/right/bottom sz=4 color=000000 val=single` (paragraph-borders are stronger but in OOXML `<w:r><w:rPr><w:bdr ...>` gives run-level borders that draw around the inline text)
- 1-2pt cell padding via `tcMar`

Then change the data in cells from stacked runs to single inline run.

This applies to all 5 button labels on p7 AND the `[ADD WATER 亮红灯]` `[ICE FULL 亮红灯]` on p11 (about 7 keycap chip instances total).

---

## #3 — Remove cell borders on CAUTION/NOTICE boxes; add fill-only treatment
**Impact: ~0.6 pt** | **Difficulty: 2** | **Pages affected: 3, 4, 10, 13 (every page with CAUTION/NOTICE)**

For tables 1 (CAUTION) and 2 (NOTICE) in `word/document.xml`:
- Currently: `tcBorders top sz=8 color=000000` on CAUTION cell; NOTICE has no border but inherits zebra
- Change: REMOVE all `tcBorders` from the box cells
- Currently: NOTICE cell has `shd fill=F2F2F7` (lavender)
- Add: CAUTION cell `<w:shd w:val="clear" w:color="auto" w:fill="FDECEC"/>` (pale red-pink to match target)
- Change: NOTICE fill from `F2F2F7` to `F5F5F5` (drop the blue tint)

For table 0 (WARNING on p3):
- Keep the red top accent line (`tcBorder top sz=12 color=E63946`)
- Add fill `<w:shd w:fill="F9EFEF"/>` (pale red, slightly more red than CAUTION because WARNING is the most severe)

---

## #4 — Widen paragraph spacing inside bullet lists (intra-box and section bodies)
**Impact: ~0.5 pt** | **Difficulty: 1** | **Pages affected: 3, 4, 5, 12, 13**

In `word/styles.xml`:
- `BodyText spacing after=120` → **`after=80`** (drop slightly)
- Add new style `BulletItem` (or modify ListContinue/ListContinue2):
  - `spacing before=0 after=60 line=320 lineRule=auto` → 16pt line height, 3pt after
- For paragraphs inside CAUTION/NOTICE table cells: add direct `<w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>` to each `<w:p>` inside the boxes

Concrete: target has ~10pt between bullet items in CAUTION box, W27 has ~5-6pt. Adding 4pt of `before` per bullet `<w:p>` gives the needed breathing room.

---

## #5 — Increase TOC line spacing on p2
**Impact: ~0.4 pt (p2 alone)** | **Difficulty: 1** | **Pages affected: 2**

The TOC entries are 10 plain paragraphs styled as Body or a TOC style. Currently line height is auto (~12pt). Target uses ~18pt.

Find the 10 TOC paragraphs in `word/document.xml` (look for the entries `01 安全须知`, `02 产品及使用提示`...) and either:
- Wrap each with `<w:pPr><w:spacing w:line="360" w:lineRule="auto"/></w:pPr>` (18pt line)
- OR add a new `TOC1` style with that spacing and apply via `<w:pStyle w:val="TOC1"/>`

---

## #6 — Increase row heights for data tables (p6 structure, p8 specs, p11 trouble, p14 warranty)
**Impact: ~0.4 pt** | **Difficulty: 1** | **Pages affected: 6, 8, 11, 14**

For tables 3, 4, 5, and the p14 warranty tables in `word/document.xml`:
- `<w:trHeight w:val="215" w:hRule="atLeast"/>` → **`w:val="280" w:hRule="atLeast"`** (10.75pt → 14pt min)

Combined with #1 (smaller font), this gives the same cell content with more vertical padding above and below.

Alternative: keep `trHeight` and add `<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/></w:tcMar>` to each `tcPr`.

---

## #7 — Switch zebra fill from `F2F2F7` (lavender) to neutral `F0F0F0`
**Impact: ~0.3 pt** | **Difficulty: 1 (search-replace)** | **Pages affected: 6, 7, 8, 11, 14, 15**

In `word/document.xml`, search-replace:
- `w:fill="F2F2F7"` → **`w:fill="F0F0F0"`** (all occurrences)

The lavender tint reads as colored against the pure white rows; the neutral gray reads as expected zebra.

If wanting to match target even closer, use `EEEEEE` (slightly lighter) — but verify the exact target fill by sampling target PNG pixels in cell row regions.

---

## #8 — Split p1 footer into 2 paragraphs
**Impact: ~0.15 pt (p1 alone, p1 already at 2.93)** | **Difficulty: 1** | **Pages affected: 1**

Current p1 footer (`word/document.xml` near end of page 1 section):
```
<w:p><w:r><w:t>使用产品前请仔细阅读本说明书，并妥善保管。 说明书中的产品...请以实物为准。</w:t></w:r></w:p>
```

Change to:
```
<w:p><w:r><w:t>使用产品前请仔细阅读本说明书，并妥善保管。</w:t></w:r></w:p>
<w:p><w:r><w:t>说明书中的产品、配件等插图均为示意图，仅供参考。由于产品的更新与升级，产品实物与示意图可能略有差异，请以实物为准。</w:t></w:r></w:p>
```

---

## #9 — Restore `•` bullet glyph on p12 日常保养 list
**Impact: ~0.15 pt (p12 alone, currently 10.01)** | **Difficulty: 1** | **Pages affected: 12 (possibly 13)**

p12's 日常保养 list items in W27 render as indented plain text without `•` glyph. Target shows `•` as run prefix.

Either:
- Add a numbering definition `<w:numPr>` to each list paragraph referencing a `numId` whose abstract format is `<w:lvlText w:val="•"/>`
- OR add `<w:t>•   </w:t>` literally at the start of each list paragraph's run

The first is the proper Word way; the second is the brute-force way (and matches what other sections of the doc are already doing — search for `•` in document.xml to confirm).

---

## #10 — Reduce internal vertical column dividers on data tables (p6, p8)
**Impact: ~0.1 pt** | **Difficulty: 2** | **Pages affected: 6, 8**

Target's data tables have ONLY horizontal row dividers + header fill — NO vertical column dividers. W27's tables show a faint vertical line between `编号` and `名称` columns (and on p8 between `参数` and `规格`).

For tables 3, 5 (and similar) in `word/document.xml`:
- Currently each `tcBorder` has no explicit `left/right` so it falls back to table default — which is `nil` per the inspect data, so this MIGHT already be OK
- BUT the LO/Word renderers might draw a thin gridline anyway because of the `tblGrid` default in some Office variants
- Add explicit `<w:tcBorders><w:left w:val="nil"/><w:right w:val="nil"/></w:tcBorders>` to every cell where you want NO vertical divider visible

Cross-check: look at `comparisons/page-06-sidebyside-LO.png` and `page-08-sidebyside-LO.png` to confirm the faint vertical line is present in W27 LO render.

---

## Bonus (lower impact, but free)

### #B1 — Tighten header band Y position (-3pt top margin)
**Impact: ~0.1 pt across all pages** | **Difficulty: 1**

`sectPr/pgMar top=578` → **`top=720`** (push content down by ~3pt to align W27 with target's top-header band Y position).

This will trigger a global vertical shift of -10 raster-pixels on p1 and similar shifts on other pages. Combined with the per-page profile shift data in `_work/stats.json`, this single change should close the systemic offset.

### #B2 — Verify red brand color exact match
**Impact: <0.05 pt** | **Difficulty: 1**

W27 uses `#E63946` (RGB 230,57,70); target uses `#E63846` (RGB 230,56,70). Diff is 1 step in green channel. Replace all `E63946` with `E63846` in `word/document.xml` and `word/styles.xml`. Invisible to eye but kills the pixel-level mismatch.

---

## Suggested Iteration Order

If running a single "iter-34" pass, apply in this order:
1. **#1 first** (font size) — biggest signal, cascades through everything else
2. **#3** (boxes) — quick visual win on p3/p4
3. **#7** (zebra hue) — search-replace, no risk
4. **#6** (row heights) — pair with #1 to keep cells readable
5. **#4** (spacing) — fixes the vertical drift on p5/p12/p13
6. **#8** (footer split) — trivial p1 fix
7. **#5** (TOC spacing) — p2 trivial
8. Re-score; check if **#2** (keycap chips) is still needed — likely yes, p7/p11 won't move without it
9. **#2** if score still > 6.0
10. **#9, #10, #B1, #B2** for cleanup

Predicted score after #1+#3+#6+#7 alone: **overall_mean_diff ~ 5.5-6.0** (from current 8.67). After full list: **3.5-4.5**.
