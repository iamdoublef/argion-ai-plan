# W27 vs Target PDF — Design Audit (iter-34)

**Scope**: Qualitative design diff between `final/imt050-wevac-eu-cn.docx` (W27, score 8.67/12.35) and the master `output/imt050-wevac-eu-cn.pdf`. Static expert review — no docx edits.

**Method**:
1. 15 side-by-side comparison PNGs from LibreOffice raster of W27 vs target (`comparisons/page-XX-sidebyside-LO.png`).
2. 15 side-by-side from Microsoft Word raster of W27 (`comparisons/page-XX-sidebyside-WORD.png`) — to factor out LO rendering bugs.
3. 4 diff heatmaps on hard pages p3/p9/p11/p14 + 5 extra heatmaps for p5/p7/p8/p12/p13 (`diffmaps/page-XX-heatmap.png`).
4. 6 focused 2x crops on structural defects (`diffmaps/page-XX-crop-*.png`).
5. XML inspection of `word/document.xml` and `word/styles.xml` (`_work/docx_inspect.json`).
6. Font/size histograms per page from target PDF via PyMuPDF (`_work/target_pdf_inspect.json`).
7. Per-page row/column ink-density profiles for vertical/horizontal shift detection (`_work/stats.json`).

**Both LO and Word renderers agree** on every defect documented below — none is a rendering artifact.

---

## 0. Cross-cutting (systemic) defects

These show up on multiple pages and explain most of the diff that 30 rounds of pixel iteration couldn't close.

### 0.1 Body font size: W27 uses uniform 8pt, target varies 6.5pt - 7.5pt by content type

Evidence — target PDF body font sizes by page (from PyMuPDF):

| Page | Content type | Target body MicrosoftYaHei size |
|---|---|---|
| p3, p4 | Safety bullet list (dense) | **6.98pt** |
| p7 | Function table | 6.6pt; header **6.0pt white** |
| p8 | Spec table | 6.67pt; header 6.0pt white |
| p9 | Operation text | **7.5pt** (more breathing room) |
| p11 | Trouble table | 6.52pt; header 6.0pt white |
| p14 | Warranty mixed | 6.67pt (table) + 7.5pt (body) |

W27 docx body uses `BodyText3 sz=16` (half-points) → **8pt** everywhere; `Caption sz=18` → 9pt; `MacroText sz=20` → 10pt. The XML never drops below 8pt for body content.

**Why this matters**: 8pt vs 7pt at A5 width (148mm) is the difference between a tight, technical-document look and a slightly clumsy "blown up" feel. The font ratios cascade: target uses bigger headings (13.5pt) relative to smaller body (~7pt) — a 1.93x ratio. W27 has 14pt headings vs 8pt body — only 1.75x. Visual hierarchy reads weaker.

**This single change probably accounts for ~30% of the residual mean diff** because every glyph stroke ends up at a different sub-pixel position.

### 0.2 W27 box content has table-cell top border; target has fill-only

Inspect of `word/document.xml` (table indices 0/1/2 — these are the WARNING/CAUTION/NOTICE boxes on p3 & p4):

```
table 0 (WARNING):  tblBorders all nil, cell top tcBorder sz=12 color=E63946
table 1 (CAUTION):  tblBorders all nil, cell top tcBorder sz=8  color=000000
table 2 (NOTICE):   tblBorders all nil, cell shading F2F2F7, top border null
```

Target PDF (visual inspection of `comparisons/page-04-sidebyside-LO.png` and `page-04-sidebyside-WORD.png`):
- CAUTION block: pale-red **fill rectangle**, NO border at all
- NOTICE block: pale-gray **fill rectangle**, NO border at all
- WARNING block (p3): pale-red fill rectangle + thin red top accent ONLY

W27 visually shows a black hairline outlining all 4 sides of CAUTION because the cell `top` border is rendered AND adjacent paragraph cells leave residual default borders. This is the dominant signal on p4 (LO_diff 7.09) and contributes to p3 (12.04).

### 0.3 W27 lacks the "keycap chip" convention for button labels

Target inline-styles every button name as a black-bordered monospaced chip:
```
[Power]  电源   点击开机，长按关机。
[Make Ice] 制冰   切换制冰尺寸（S/M/L）...
```
W27 renders them as two-line stacked plain text inside the cell:
```
1
Power
电源        点击开机，长按关机。
```

This pattern appears on **p7 (functions table)** AND **p11 (trouble table — ADD WATER 亮红灯, ICE FULL 亮红灯)**. Two pages, structural mismatch.

Target uses `Arial-BoldMT 6.0pt WHITE on dark fill` for the header row label "NO. / 按键" and `Arial-Black 5.25-6.0pt` for keycap chips. W27 doesn't render any of these chips — they collapse into the 8pt regular body run.

### 0.4 Table-cell zebra fill weight is over-saturated in W27

W27 uses `F2F2F7` (very pale lavender-gray) for zebra-strip rows on tables 3/4/5/etc. Target uses `EEEEEE`/`EBEBEB` neutral gray (no blue/purple tint). The hue diff is small (~3 pts on R-channel) but the SATURATION diff and the LARGER fraction of rows that are zebra-tinted in W27 makes W27 look more colored.

Also: target only zebras rows that contain DATA (skipping spacer rows), while W27 zebras every other row uniformly.

### 0.5 Paragraph after-spacing too small for narrow text + small font

`styles.xml`:
- `BodyText after=120` (twips) → **6pt** after each body paragraph
- `Heading2/3/...8 before=200 after=0` → 10pt before + 0 after

Target visually has wider gaps between bullet items inside CAUTION/NOTICE boxes AND between sub-section headings. Estimated target spacing:
- Between bullet items in CAUTION/NOTICE: **~8-10pt** (vs W27 ~5-6pt)
- After sub-section heading (e.g. "放置与首次使用") before first bullet: **~6pt** (vs W27 ~3-4pt)
- Between TOC entries on p2: target ~17-18pt line height, W27 ~14pt → diff of 3-4pt per entry, multiplied over 10 entries = 30-40pt of unused vertical space at bottom of TOC

This is the dominant signal on p5 (LO_diff 10.94), p12 (10.01), p13 (11.70), and the ink_ratio_c_over_t < 0.93 stats reflect that W27 packs more lines into the same vertical and target leaves more breathing room.

### 0.6 Cell vertical padding too small

`row_heights` for tables 3, 4, 5 are `atLeast 215-225 twips` (~10.75-11.25pt min). With 8pt font + 6pt after-paragraph, the cell can only ever be that tight. Target visually has rows around **14-15pt tall** for the same content. The fix is either:
- Increase `trHeight val` from 215 to ~280-300, OR
- Add cell margins via `tcMar top/bottom`, OR
- Use a paragraph `before=40 after=40` inside cells.

### 0.7 Section margins are aggressively tight

`pgMar`: top=578, right=567, bottom=567, left=567 (twips). That's 1.02cm top, 1.0cm L/R/B. Target visually shows ~1.4cm left margin (text starts at ~28pt from page edge = ~0.99cm) but uses larger TOP margin. The top header band rule is at y≈36pt = 1.27cm from page top; W27 has it at ~28pt = 0.99cm. **W27 sits ~3-4pt higher on every page** — this is also why `vertical_shift_px` is +10 on p1 (`stats.json`).

### 0.8 Mid-text colors slightly cooler in W27

Target body text color = `#1A1A1A` (RGB 26,26,26 — confirmed from cell shading "1A1A1A" in W27 too — match). But target's RED `#E63846` vs W27 cell border `#E63946`: G channel diff `0x38` vs `0x39`. Visually irrelevant. Gray dividers: target `#CCCCCC` ↔ W27 `#CCCCCC` — match.

The 1-step red shade is NOT the source of any meaningful pixel diff. Skipped.

---

## 1. Page-by-page findings

### p1 — Cover (LO_diff 2.93, easy)

**Visual** (see `comparisons/page-01-sidebyside-LO.png` + `diffmaps/page-01-crop-footer.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| 制冰机 title position | y≈730 px (3.0cm from top) | y≈770 px (3.2cm) | low — drift of ~5px |
| 说明书 subtitle | placed immediately under title | larger gap above subtitle | low — ~3pt diff |
| Red dash mark below 说明书 | thin red line visible | thin red line visible | match |
| Footer text | one paragraph, justified-wraps to 2 lines on a single block | TWO paragraphs, line break after "并妥善保管。" | **MEDIUM** — visible structure mismatch |
| Footer position | text sits IMMEDIATELY above bottom margin | text leaves ~12px gap above bottom rule | low |

**Vertical shift on p1**: profile stats says `vertical_shift_px = +10` → W27 sits 10 raster-pixels lower (or content shifted up).

**Fix priority**: medium — split footer into 2 paragraphs.

---

### p2 — Table of Contents (LO_diff 3.25, easy)

**Visual** (see `comparisons/page-02-sidebyside-LO.png` + `diffmaps/page-02-crop-toc-spacing.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| TOC line spacing | ~40 px between entries | ~50 px between entries | **HIGH** — affects every page's layout cascade |
| 目录 heading top | y≈220 px | y≈220 px | match |
| Section labels | 01 02 03... red bold | same | match |
| Page numbers (right-aligned) | match | match | match |

**Fix priority**: medium — increase TOC line spacing from `line=null` to something explicit like `line=320 lineRule=auto` (16pt line height).

---

### p3 — Safety / WARNING block (LO_diff 12.04, **HARD**)

**Visual** (see `comparisons/page-03-sidebyside-LO.png` + `diffmaps/page-03-heatmap.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Title "01 安全须知" | 13-14pt, red 01 + black 安全须知 | 13.5pt, red 01 + black 安全须知 | match |
| WARNING block top border | red `#E63946` sz=12 (1.5pt) | red rule visible too (sz≈10 equiv) | low |
| WARNING block BG fill | none (only borders) | **pale-red fill `#F9EFEF`** behind text | **HIGH** — color is wrong |
| Bullet `•` glyph | uniform 8pt body | bullet appears as `•` at 6.98pt | medium — needs font shrink |
| Body text size | 8pt MicrosoftYaHei | **6.98pt MicrosoftYaHei** | **HIGH** — see 0.1 |
| Line spacing between bullets | tight | **20% wider** | **HIGH** — see 0.5 |
| Bottom-of-page free space | ~80px white | ~110px white | derived from line spacing |

**Heatmap interpretation** (`diffmaps/page-03-heatmap.png`):
- Bottom-left inferno: warning block is uniformly orange → every bullet line position drifts because line spacing differs
- Bottom-right mask (red on diff>18): entire WARNING block highlighted → not a local issue, systemic font + spacing
- p99 diff = 215 → there are pixels with 215/255 brightness diff → strong text outline mismatch

**Fix priority**: HIGH — change body font from 8pt to 7pt; add fill `#F9EFEF` to WARNING table cell; widen list spacing.

---

### p4 — Safety continued / CAUTION + NOTICE (LO_diff 7.09)

**Visual** (see `comparisons/page-04-sidebyside-LO.png` + `diffmaps/page-04-crop-caution-notice-boxes.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| CAUTION block border | **visible black hairline all 4 sides** | NO border, fill only | **HIGH** |
| CAUTION fill | none | pale pink `#FDECEC`/`#FFEEEE` | **HIGH** |
| NOTICE block border | visible top border + faint sides | NO border, fill only | **HIGH** |
| NOTICE fill | `F2F2F7` pale lavender | pale gray `#F5F5F5` (neutral) | medium — hue tint |
| Bullet item spacing inside boxes | ~5-6pt | ~8-10pt | **HIGH** — see 0.5 |
| Body font | 8pt | 6.98pt | **HIGH** |

**Fix priority**: HIGH — remove cell borders, add cell fills, increase intra-box paragraph spacing.

---

### p5 — Product & Usage Tips (LO_diff 10.94)

**Visual** (see `comparisons/page-05-sidebyside-LO.png` + `diffmaps/page-05-heatmap.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Section headings (放置与首次使用 etc.) bottom border | hairline `sz=6` 0.75pt black under heading | similar but at LOWER Y position | medium — Y drift |
| Bullet item line spacing | tight | wider (~20%) | **HIGH** — see 0.5 |
| Bottom whitespace | ~100px | ~280px | net effect — content takes less vertical |
| Body text color | `#1A1A1A` | `#1A1A1A` | match (W27 styles.xml NOT verified but inferred from histo color 1710618) |

**ink_ratio_c_over_t = 0.91** — W27 has 9% less ink. This means W27's smaller fonts pack more chars per page but somehow LESS total ink — counterintuitive. Likely explanation: **target's emphasis runs use HEAVIER weight (MicrosoftYaHei-Bold for sub-headings) more frequently**, and W27's headings use MicrosoftYaHei-Regular as the default for sub-section labels.

**Fix priority**: medium — widen line spacing on section bullets; verify sub-section headings use Bold weight.

---

### p6 — Product Structure (LO_diff 6.19)

**Visual** (see `comparisons/page-06-sidebyside-LO.png` + `diffmaps/page-06-crop-structure-table.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Diagram image | identical | identical | match |
| Table column count | 4 (编号 名称 编号 名称) | 4 same | match |
| Table header row fill | `#1A1A1A` dark gray | dark gray | match |
| Header text color | white | white | match |
| Row heights | atLeast 215 twips (~10.75pt) | ~14pt visible | **HIGH** — rows too short |
| Cell top border | `sz=4 color=CCCCCC` (0.5pt) | matches | match |
| Zebra fill | `F2F2F7` (lavender tint) | neutral gray | medium — tint |
| Internal vertical divider between col2/col3 | visible | barely visible | low |

**Fix priority**: medium — increase row height to ~280 twips; change zebra fill to neutral `#F0F0F0`.

---

### p7 — Product Functions (LO_diff 7.81)

**Visual** (see `comparisons/page-07-sidebyside-LO.png`, `-WORD.png`, `diffmaps/page-07-heatmap.png`, `page-07-crop-keycap-table.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Diagram + 3 labelled buttons (CLEAN MAKE ICE POWER) | visible | identical | match |
| Function table cell content layout | **TWO-LINE: "Power\\n电源"** stacked | **ONE-LINE: `[Power] 电源`** chip + label | **CRITICAL** |
| Keycap chip styling | none — plain text | thin black border around English label, monospace font (Arial-BoldMT 6pt) | **CRITICAL** |
| First column width | wide enough to hold 2 lines | narrow — only "1 [Power]" fits | **HIGH** |
| Row heights | ~40px each (5 rows) | ~25px each | **HIGH** |
| Table header text | "No. / 按键" "功能说明" white on dark | "NO. / 按键" "功能说明" white on dark | match — but font is regular vs Arial-BoldMT in target |

**Heatmap** (`diffmaps/page-07-heatmap.png`): the entire function table region glows red. This is the highest-density structural defect in the document.

**Fix priority**: **CRITICAL** — restructure cells to inline-style English label as keycap chip + Chinese tag, single-line.

---

### p8 — Technical Specifications (LO_diff 7.84)

**Visual** (see `comparisons/page-08-sidebyside-LO.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Table header fill | `#1A1A1A` | dark | match |
| Header text "参数" "规格" | regular bold weight | Arial-BoldMT 6.0pt | match-ish |
| Body cells font | 8pt | **6.67pt** mix of MicrosoftYaHei + ArialMT | **HIGH** — font size + run-level font mix |
| Row heights | ~28px (atLeast 225 twips ≈ 11.25pt) | ~28-29px target visually | match |
| Number rows count | 16 rows visible | 16 visible | match |
| Vertical divider between col1/col2 | visible thin line | absent in target | medium |

**Fix priority**: HIGH — drop body font to 7pt; remove the internal vertical column divider on the spec table.

---

### p9 — Operation Guide (LO_diff 11.99, **HARD**)

**Visual** (see `comparisons/page-09-sidebyside-LO.png` + `diffmaps/page-09-heatmap.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Body text font | 8pt | **7.5pt** (note: bigger than other pages — operation content uses larger font) | medium |
| Numbered list markers (1/2/3) in red square chips | visible — red filled squares | red filled squares same | match in design |
| Number-marker → text gap | tight (~6pt) | wider (~10pt) | medium |
| Sub-section heading "如何制作子弹冰" weight | Bold MicrosoftYaHei | **MicrosoftYaHei-Bold 7.5pt** | match |
| Diagram captions (MAX / FULL BUCKET) | match in design | match | match |
| Body line spacing under step labels | tight | wider | medium |

**Heatmap**: most red is concentrated in the step body areas around the diagrams — text reflows at slightly different Y positions because of font size + spacing diffs.

**Fix priority**: HIGH — drop body font to 7.5pt on this page specifically (operation chapter); widen number-marker → text gap.

---

### p10 — Operation Guide cont. (LO_diff 10.14)

**Visual** (see `comparisons/page-10-sidebyside-LO.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| 提示 NOTICE inline section | matches CAUTION/NOTICE styling on p4 | matches | (inherits 0.2 fix) |
| Number chips | match | match | match |
| Body text font | 8pt | 7.5pt | **HIGH** (same as p9) |
| Bullet `•` items inside NOTICE | tight spacing | wider | medium |

**Fix priority**: HIGH — same as p9 + 0.2 + 0.5.

---

### p11 — Troubleshooting Table (LO_diff 12.14, **HARD**)

**Visual** (see `comparisons/page-11-sidebyside-LO.png` + `diffmaps/page-11-heatmap.png` + `page-11-crop-trouble-header-band.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Header row fill | dark `#1A1A1A` | dark | match |
| Header text "故障现象 可能原因 解决方案" | white | **6.0pt MicrosoftYaHei-Bold WHITE** color 16777215 | match-ish |
| Body cell font | 8pt | **6.52pt** | **HIGH** |
| Keycap inline `[ADD WATER 亮红灯]` / `[ICE FULL 亮红灯]` | plain "（ADD WATER 亮红灯）" parens | inline keycap chip | **HIGH** (= 0.3) |
| Row 1 col 1 "不能开机" wraps or single line | single line | single line | match |
| Solution column width | narrower in W27 → wraps to 3 lines | wider in target → 2 lines | **HIGH** — column width imbalance |
| Bottom DISCLAIMER box | `F2F2F7` fill + thin border | `#F0F0F0` fill, no border | medium |
| DISCLAIMER text wrap | wraps to 2 short lines | one line | medium |
| 防触电图标 icon position in DISCLAIMER | left-aligned | left-aligned | match |

**Heatmap**: header row is solid red (font weight + color level diff), then specific cells (where keycaps live) are very red, then the entire 解决方案 column has positional drift due to font/line-spacing.

**Fix priority**: **CRITICAL** — keycaps + body font + column widths.

---

### p12 — Maintenance (LO_diff 10.01)

**Visual** (see `comparisons/page-12-sidebyside-LO.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Step number chips (red filled) | visible | visible | match |
| Sub-section heading "自动清洁" weight | regular bold | regular bold | match |
| Body line spacing under each step | tight | wider | **HIGH** (= 0.5) |
| 日常保养 bullet `•` items | indented plain text, NO `•` glyph | `•` bullets clearly visible | **HIGH** — bullet glyph missing |
| Bottom whitespace | ~150px | ~250px | net effect |

**Fix priority**: HIGH — restore `•` bullet glyph on 日常保养 list; widen spacing.

---

### p13 — Installation / Storage / Disposal (LO_diff 11.70)

**Visual** (see `comparisons/page-13-sidebyside-LO.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Section heads (包装运输, 安装, 存储与拆除) bottom border `sz=6` | visible | visible | match |
| Bullet `•` items | tight spacing, regular weight | wider, some emphasis-bold | **HIGH** |
| 警告 inline danger note at bottom | colored box, similar to CAUTION/NOTICE | matches in design | (inherits 0.2) |
| Body font | 8pt | 6.98pt | **HIGH** |

**Fix priority**: medium (cumulative effect of 0.1 + 0.5 + 0.2).

---

### p14 — Brand & Warranty Info (LO_diff 12.35, **HARD — worst page**)

**Visual** (see `comparisons/page-14-sidebyside-LO.png` + `diffmaps/page-14-heatmap.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| 品牌商信息 table (3 rows: 品牌商 / 网址 / 客服邮箱) | header row dark fill, body rows zebra | matches in pattern | match |
| 授权制造商 table (2 rows) | matches | matches | match |
| Row heights | atLeast 215 twips (~10.75pt) | ~14pt visible | **HIGH** — see 0.6 |
| Body font | 8pt MicrosoftYaHei + 8pt ArialMT for emails | **6.67pt** mixed MicrosoftYaHei + ArialMT | **HIGH** — see 0.1 |
| Header row text "品牌名称 / 内容" color | white | white | match |
| 保修信息 paragraph | regular flow, no special block | normal flow | match |
| 三包条款 bullet list (产品自购买之日起整机保修18个月...) | tight 8pt | wider 7.5pt | **HIGH** |
| Centered email "support@wevactech.com" with em-dash bracket | match in shape | match | match |

**Heatmap**: the table rows are uniformly red because every row Y position drifts by 2-3px due to row-height mismatch, AND the dark cell backgrounds have slightly different shades (`#1A1A1A` in W27 vs whatever the target actually uses — could be slightly different).

**Fix priority**: **HIGH** — biggest single-page contribution to overall diff. Row heights + font sizes need to change together.

---

### p15 — Warranty Card (LO_diff 3.65, easy)

**Visual** (see `comparisons/page-15-sidebyside-LO.png`):

| Element | W27 | Target | Severity |
|---|---|---|---|
| Form table 9 rows | match | match | match |
| Label column / input column zebra | match | match | match |
| Row heights | atLeast 215 twips | similar | match |
| Body font | 8pt | 8pt visible — possibly target keeps standard size here | match |

**Fix priority**: LOW — already converged.

---

## 2. What the 30-iteration pixel optimizer missed

The pixel-diff loss function rewards local color matches. It can't:
1. **Reduce a font size** — that changes glyph topology globally, immediately spikes the diff before settling
2. **Remove a border** without an alternative fill — pixel diff sees the temporary white gap
3. **Restructure a table cell** — collapsing 2 stacked runs into 1 inline run breaks every pixel in the cell
4. **Add a fill color** to a previously-bordered box — the optimizer doesn't know to compensate by widening the box
5. **Change row heights** consistently across a table — moves every cell by the same delta, triggers all-row diff spikes

These are precisely the 5 classes of defect this audit identified. Iter-34's design task is to **make these moves manually with known-good values**, then let pixel-iteration converge in 5-10 rounds rather than 30+.

