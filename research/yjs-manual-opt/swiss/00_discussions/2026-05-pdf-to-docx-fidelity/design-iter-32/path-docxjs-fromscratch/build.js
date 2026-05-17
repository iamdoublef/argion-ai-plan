// Build IMT050 A5 Chinese manual via docx-js, targeting W27 visual parity.
//
// Usage:  node build.js [outPath]
// Default outPath: ./output.docx
//
// Layout philosophy:
//   * A5 (148 mm x 210 mm), 9 mm margins on all sides.
//   * Cover, TOC, 13 body pages. Each body page = exactly one printed page,
//     so we emit one section per page (with its own footer/page number).
//   * Body text: 7 pt Microsoft YaHei (eastAsia hint) + Arial latin.
//   * Step badge: black-filled run with white Arial Black digit.
//   * Bullets: red unicode bullet glyph as inline run (W27 also uses this).
//
// All content is in content.js — the builder is brand/locale-agnostic.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import {
  AlignmentType, BorderStyle, Document, Footer, Header, HeightRule,
  ImageRun, LineRuleType, Packer, PageBreak, Paragraph, ShadingType,
  Tab, TabStopPosition, TabStopType, Table, TableCell, TableRow,
  TextRun, VerticalAlign, WidthType,
} from 'docx';

import { content } from './content.js';
import * as imageSize from 'image-size';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// =============================================================
// Constants — geometry, fonts, colors (mirror W27 builder)
// =============================================================
const PAGE_W_DXA = 8392;     // 148 mm
const PAGE_H_DXA = 11906;    // 210 mm
const MARGIN_MM = 10;
const MARGIN_DXA = Math.round(MARGIN_MM * 56.7); // 567
const CONTENT_W_DXA = PAGE_W_DXA - MARGIN_DXA * 2;  // 7258
const CONTENT_W_MM = 148 - MARGIN_MM * 2;            // 128
const MM_TO_DXA = 56.7;

const RED = 'E63946';
const BLACK = '000000';
const DARK = '1A1A1A';
const GRAY = '8E8E93';
const LIGHT_GRAY = 'F2F2F7';
const ZEBRA = 'F2F2F7';
const BORDER_GRAY = 'CCCCCC';

const LATIN_FONT = 'Arial';
const LATIN_BOLD_FONT = 'Arial Black';
const CJK_FONT = 'Microsoft YaHei';
const MONO_FONT = 'Courier New';
const CHAR_SPACING = 5;          // twips

// Sizes in half-points (docx-js convention: size is half-points)
const HP = (pt) => Math.round(pt * 2);
const BODY_PT = 7.05;
const SECTION_TITLE_PT = 9.0;
const SUB_TITLE_PT = 7.5;
const CHAPTER_NUM_PT = 13.5;
const CHAPTER_TITLE_PT = 11.0;
const TABLE_BODY_PT = 6.7;
const TABLE_HEADER_PT = 6.0;
const SMALL_PT = 5.4;

// =============================================================
// Run helpers — eastAsia font hint, char spacing, color, bold
// =============================================================

/**
 * Make a TextRun with full eastAsia font support, char spacing, color.
 * docx-js exposes the eastAsia font via `font.eastAsia`.
 */
function r({
  text,
  size = BODY_PT,
  bold = false,
  color = BLACK,
  mono = false,
  italic = false,
  characterSpacing = CHAR_SPACING,
  positionHalfPt = null,   // baseline raise in half-points
  shading = null,           // hex color or null
}) {
  const fontLatin = mono ? MONO_FONT : (bold ? LATIN_BOLD_FONT : LATIN_FONT);
  const options = {
    text,
    size: HP(size),
    bold,
    italics: italic,
    color,
    characterSpacing,
    font: {
      ascii: fontLatin,
      hAnsi: fontLatin,
      cs: fontLatin,
      eastAsia: mono ? MONO_FONT : CJK_FONT,
    },
  };
  if (positionHalfPt !== null) {
    options.position = positionHalfPt;
  }
  if (shading) {
    options.shading = { type: ShadingType.CLEAR, color: 'auto', fill: shading };
  }
  return new TextRun(options);
}

// =============================================================
// Block builders
// =============================================================

const IMAGE_ROOT = path.resolve(__dirname, '../../../../output/imt050-wevac-eu-cn').replace(/\\/g, '/');
const IMG_DIR_REAL = path.resolve(__dirname, '../../../..', 'output', 'images_imt050');

function imageBuffer(name) {
  const p = path.join(IMG_DIR_REAL, name);
  return fs.readFileSync(p);
}

function imageDimsMm(name) {
  const p = path.join(IMG_DIR_REAL, name);
  const buf = fs.readFileSync(p);
  // image-size 2.x exports default function returning {width,height}
  const fn = imageSize.imageSize ?? imageSize.default ?? imageSize;
  const dims = typeof fn === 'function' ? fn(buf) : fn.imageSize(buf);
  // assume 96 DPI as html default
  const dpi = 96;
  const wmm = (dims.width / dpi) * 25.4;
  const hmm = (dims.height / dpi) * 25.4;
  return { wmm, hmm, w: dims.width, h: dims.height };
}

function fitImage(name, maxWmm, maxHmm) {
  const d = imageDimsMm(name);
  const scale = Math.min(maxWmm / d.wmm, maxHmm / d.hmm);
  return { wmm: d.wmm * scale, hmm: d.hmm * scale };
}

function mmToEmu(mm) {
  return Math.round(mm * 36000);
}

function pt(v) { return Math.round(v * 20); } // twips

/* Header strip: top black rule + brand left, CH ref right */
function headerStrip({ brand, headerRef }) {
  return new Paragraph({
    spacing: { before: 0, after: pt(4), line: 240, lineRule: LineRuleType.AUTO },
    border: { top: { style: BorderStyle.SINGLE, size: 18, color: BLACK, space: 1 } },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W_DXA }],
    children: [
      r({ text: brand, size: 6.75, bold: true, color: BLACK }),
      r({ text: '\t', size: 6.0, color: GRAY, mono: true }),
      r({ text: headerRef, size: SMALL_PT, color: GRAY, mono: true }),
    ],
  });
}

/* Section title: red chapter num + black title, left thick rule */
function sectionTitle({ num, title }) {
  return new Paragraph({
    spacing: { before: 0, after: pt(6), line: 240, lineRule: LineRuleType.AUTO },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: BLACK, space: 4 } },
    indent: { left: pt(1.5 * 56.7 / 20) },  // 1.5 mm in twips
    children: [
      r({ text: num + ' ', size: CHAPTER_NUM_PT, bold: true, color: RED }),
      r({ text: title, size: CHAPTER_TITLE_PT, bold: true, color: BLACK }),
    ],
  });
}

/* Sub-title: bold 7.5pt with thin bottom border */
function subTitle(text, { before = 4 } = {}) {
  return new Paragraph({
    spacing: { before: pt(before), after: pt(4), line: 240, lineRule: LineRuleType.AUTO },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLACK, space: 1 } },
    children: [r({ text, size: SUB_TITLE_PT, bold: true })],
  });
}

/* Paragraph with optional rich runs.
 * Supports soft line breaks via "\n" inside a run.text by emitting
 * separate TextRuns with a `break: 1` in between.
 */
function bodyPara(block, { color = DARK, size = BODY_PT, after = 3 } = {}) {
  const children = [];
  const push = (text, opts) => {
    const lines = (text || '').split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (i > 0) {
        // Insert a soft line break via separate run with break property
        children.push(new TextRun({ text: '', break: 1, size: HP(opts.size || size) }));
      }
      children.push(r({ text: lines[i], ...opts }));
    }
  };
  if (block.runs) {
    for (const run of block.runs) {
      push(run.text, { bold: !!run.bold, color: run.color || color, size: run.size || size, mono: !!run.mono });
    }
  } else {
    push(block.text, { color, size });
  }
  return new Paragraph({
    spacing: { before: 0, after: pt(after), line: 278, lineRule: LineRuleType.AUTO },
    children,
  });
}

/* Bullet list (W27-style: unicode bullet character) */
function bulletList(items, {
  size = BODY_PT,
  redBullet = true,
  tight = false,
  indentMm = 3.2,
  lineSpacingMul = null,
  spaceAfterPt = null,
  bulletSize = null,
  characterSpacing = null,
} = {}) {
  const after = spaceAfterPt !== null ? spaceAfterPt : (tight ? 1.35 : 1.6);
  const lineMul = lineSpacingMul !== null ? lineSpacingMul : (tight ? 0.96 : 1.13);
  const bSize = bulletSize !== null ? bulletSize : (tight ? 5.25 : 5.8);
  const indentTwips = pt(indentMm * 56.7 / 20);
  const lineTwentieths = Math.round(lineMul * 240);
  const cs = characterSpacing !== null ? characterSpacing : CHAR_SPACING;
  return items.map((item) => {
    const runs = [];
    runs.push(r({
      text: '•    ',
      size: bSize,
      bold: true,
      color: redBullet ? RED : BLACK,
      characterSpacing: cs,
    }));
    if (typeof item === 'string') {
      runs.push(r({ text: item, size, color: BLACK, characterSpacing: cs }));
    } else if (item.runs) {
      for (const sub of item.runs) {
        runs.push(r({
          text: sub.text,
          size: sub.size || size,
          bold: !!sub.bold,
          color: sub.color || BLACK,
          mono: !!sub.mono,
          characterSpacing: cs,
        }));
      }
    }
    return new Paragraph({
      spacing: { before: 0, after: pt(after), line: lineTwentieths, lineRule: LineRuleType.AUTO },
      indent: { left: indentTwips, hanging: indentTwips },
      children: runs,
    });
  });
}

/* Step flow row: number badge + text */
function stepRow(step) {
  const runs = [];
  const numRun = r({
    text: '  ' + step.num + '  ',
    size: BODY_PT,
    bold: true,
    color: 'FFFFFF',
    shading: BLACK,
  });
  runs.push(numRun);
  runs.push(r({ text: '   ', size: BODY_PT }));
  if (step.textRuns) {
    for (const sub of step.textRuns) {
      runs.push(r({ text: sub.text, size: BODY_PT, bold: !!sub.bold, color: BLACK, mono: !!sub.mono }));
    }
  } else {
    runs.push(r({ text: step.text, size: BODY_PT, color: BLACK }));
  }
  return new Paragraph({
    spacing: { before: 0, after: pt(2), line: 264, lineRule: LineRuleType.AUTO },
    children: runs,
  });
}

/* Step figures: 1–3 small images centered with indent */
function stepFigures(step) {
  if (!step.figures || step.figures.length === 0) return [];
  const maxH = 24;
  const ratios = step.figures.map((n) => imageDimsMm(n));
  const runs = [];
  for (let i = 0; i < step.figures.length; i++) {
    const name = step.figures[i];
    const fit = fitImage(name, 45, maxH);
    runs.push(new ImageRun({
      type: 'png',
      data: imageBuffer(name),
      transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
      altText: { title: name, description: name, name: name },
    }));
    if (i !== step.figures.length - 1) {
      runs.push(new TextRun({ text: '       ', size: HP(7) }));
    }
  }
  return [new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: pt(5), line: 240, lineRule: LineRuleType.AUTO },
    indent: { left: pt(30 * 56.7 / 20) },
    children: runs,
  })];
}

/* Figure: single centered image */
function figureBlock({ image, maxHeightMm = 45, maxWidthMm = CONTENT_W_MM }) {
  const fit = fitImage(image, maxWidthMm, maxHeightMm);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: pt(8), line: 240, lineRule: LineRuleType.AUTO },
    children: [new ImageRun({
      type: 'png',
      data: imageBuffer(image),
      transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
      altText: { title: image, description: image, name: image },
    })],
  });
}

/* Status indicators row: span + img + span + img */
function indicatorRow(items) {
  const runs = [];
  for (const it of items) {
    runs.push(r({ text: it.label + ' ', size: 6.15 }));
    const fit = fitImage(it.image, 30, 4);
    runs.push(new ImageRun({
      type: 'png',
      data: imageBuffer(it.image),
      transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
      altText: { title: it.image, description: it.image, name: it.image },
    }));
    runs.push(r({ text: '   ', size: BODY_PT }));
  }
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: pt(8), after: pt(3), line: 240, lineRule: LineRuleType.AUTO },
    children: runs,
  });
}

/* Figure row: 2-3 images in single row */
function figureRow({ images, maxHeightMm = 26 }) {
  const cols = images.length;
  const cellW = CONTENT_W_DXA / cols;
  const rows = [new TableRow({
    children: images.map((name) => {
      const fit = fitImage(name, CONTENT_W_MM / cols - 2, maxHeightMm);
      return new TableCell({
        width: { size: Math.floor(cellW), type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 20, right: 20 },
        borders: noBorders(),
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 0 },
          children: [new ImageRun({
            type: 'png',
            data: imageBuffer(name),
            transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
            altText: { title: name, description: name, name: name },
          })],
        })],
      });
    }),
  })];
  return new Table({
    width: { size: CONTENT_W_DXA, type: WidthType.DXA },
    columnWidths: images.map(() => Math.floor(cellW)),
    borders: tableNoBorders(),
    rows,
  });
}

function noBorders() {
  return {
    top: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    bottom: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    left: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    right: { style: BorderStyle.NONE, size: 0, color: 'auto' },
  };
}

function tableNoBorders() {
  return {
    top: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    bottom: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    left: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    right: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'auto' },
    insideVertical: { style: BorderStyle.NONE, size: 0, color: 'auto' },
  };
}

/* Render a cell content spec into paragraphs */
function renderCellContent(spec, { color = DARK, size = TABLE_BODY_PT, bold = false }) {
  // Split on \n in plain strings into separate paragraphs
  const buildPara = (runs) => new Paragraph({
    spacing: { before: 0, after: 0, line: 240, lineRule: LineRuleType.AUTO },
    alignment: AlignmentType.LEFT,
    children: runs,
  });
  if (typeof spec === 'string') {
    const parts = spec.split('\n');
    return parts.map((part) => buildPara([r({ text: part, color, size, bold })]));
  }
  if (spec && spec.runs) {
    // single paragraph mixing runs; allow \n inside a run.text to split paragraph
    const paras = [];
    let currentRuns = [];
    for (const sub of spec.runs) {
      const lines = (sub.text || '').split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (i > 0) {
          paras.push(buildPara(currentRuns));
          currentRuns = [];
        }
        const subColor = sub.color || color;
        const subSize = sub.small ? 5.2 : (sub.size || size);
        currentRuns.push(r({
          text: lines[i],
          color: subColor,
          size: subSize,
          bold: !!sub.bold,
          mono: !!sub.mono,
        }));
      }
    }
    if (currentRuns.length) paras.push(buildPara(currentRuns));
    return paras;
  }
  return [buildPara([r({ text: '', color, size })])];
}

/* Structured table — zebra rows, dark header */
function buildTable(spec) {
  const cols = spec.columnsPct ? spec.columnsPct.length : (spec.header ? spec.header.length : (spec.rows[0] ? spec.rows[0].length : 1));
  const widths = (spec.columnsPct || Array(cols).fill(100 / cols))
    .map((pct) => Math.floor(CONTENT_W_DXA * pct / 100));
  // Pad/truncate to ensure sum == CONTENT_W_DXA
  const sum = widths.reduce((a, b) => a + b, 0);
  widths[widths.length - 1] += CONTENT_W_DXA - sum;

  const allRows = [];
  let rowIdx = 0;
  if (spec.header) {
    allRows.push({ cells: spec.header, isHeader: true });
    rowIdx = 1;
  }
  for (const row of spec.rows) allRows.push({ cells: row, isHeader: false });

  const tableRows = allRows.map((rowSpec, i) => {
    const isWarrantyCard = !!spec.warrantyCard;
    const isHeader = rowSpec.isHeader && !isWarrantyCard;
    let fill;
    if (isWarrantyCard) {
      fill = (i % 2 === 1) ? ZEBRA : 'FFFFFF';
    } else if (isHeader) {
      fill = DARK;
    } else if (i % 2 === 1) {
      // body rows: alternate, but i=0 is header so body starts at i=1
      fill = 'FFFFFF';
    } else {
      fill = ZEBRA;
    }
    const cells = [];
    for (let c = 0; c < cols; c++) {
      const cellSpec = rowSpec.cells[c] !== undefined ? rowSpec.cells[c] : '';
      const cellColor = isHeader ? 'FFFFFF' : DARK;
      const cellSize = isHeader ? TABLE_HEADER_PT : (spec.troubleshooting ? 6.7 : TABLE_BODY_PT);
      const paras = renderCellContent(cellSpec, { color: cellColor, size: cellSize, bold: isHeader });
      const cellBorders = spec.troubleshooting || spec.compactWarranty || isWarrantyCard
        ? {
            top: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' },
            left: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' },
            right: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' },
          }
        : {
            top: { style: BorderStyle.SINGLE, size: 4, color: BORDER_GRAY },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: BORDER_GRAY },
            left: { style: BorderStyle.NONE, size: 0, color: 'auto' },
            right: { style: BorderStyle.NONE, size: 0, color: 'auto' },
          };
      // W27 cell padding: pad_v = 32 (troubleshooting+compact), 52 (compact_warranty), 36 (default)
      //                   start_pad = 87 (compact_warranty) else 55
      let padV = 36;
      let padStart = 55;
      if (spec.compactWarranty && !isWarrantyCard) { padV = 52; padStart = 87; }
      else if (isWarrantyCard) { padV = 52; padStart = 87; }
      else if (spec.troubleshooting) { padV = 32; }
      const cellVAlign = spec.compactWarranty ? VerticalAlign.TOP : VerticalAlign.CENTER;
      cells.push(new TableCell({
        width: { size: widths[c], type: WidthType.DXA },
        margins: { top: padV, bottom: padV, left: padStart, right: 55 },
        shading: { type: ShadingType.CLEAR, color: 'auto', fill },
        verticalAlign: cellVAlign,
        borders: cellBorders,
        children: paras,
      }));
    }
    // Row height: warranty card uses taller rows, troubleshooting (compact) uses 225, compact_warranty regular tables use 242
    let rowHeight = 225;
    if (isWarrantyCard) rowHeight = 225;
    else if (spec.compactWarranty) rowHeight = 242;
    return new TableRow({
      height: { value: rowHeight, rule: HeightRule.ATLEAST },
      children: cells,
      tableHeader: isHeader,
    });
  });

  return new Table({
    width: { size: CONTENT_W_DXA, type: WidthType.DXA },
    columnWidths: widths,
    alignment: AlignmentType.CENTER,
    borders: tableNoBorders(),
    rows: tableRows,
  });
}

/* Alert box — 1-cell table with colored border + tinted fill */
function alertBox(spec, { compactSafety = false } = {}) {
  let borderColor, fillColor;
  if (spec.type === 'warning') {
    borderColor = RED;
    fillColor = 'FFFFFF';
  } else if (spec.type === 'caution') {
    borderColor = BLACK;
    fillColor = 'FFFFFF';
  } else { // note
    borderColor = GRAY;
    fillColor = LIGHT_GRAY;
  }

  const inner = [];

  if (spec.title) {
    const titleSize = compactSafety ? 6.38 : 6.5;
    const titleColor = spec.type === 'warning' ? RED : (spec.type === 'caution' ? BLACK : BLACK);
    inner.push(new Paragraph({
      spacing: { before: 0, after: pt(compactSafety ? 1 : 2), line: 240, lineRule: LineRuleType.AUTO },
      children: [r({ text: spec.title, size: titleSize, bold: true, color: titleColor })],
    }));
  }
  if (spec.icon) {
    // W27: compact_safety uses 6.9x5.2 mm, default 8x6
    const iconW = compactSafety ? 6.9 : 8;
    const iconH = compactSafety ? 5.2 : 6;
    const fit = fitImage(spec.icon, iconW, iconH);
    const iconPara = new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: pt(1), line: 240, lineRule: LineRuleType.AUTO },
      indent: compactSafety ? { left: pt(-3.1 * 56.7 / 20) } : undefined,
      children: [new ImageRun({
        type: 'png',
        data: imageBuffer(spec.icon),
        transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
        altText: { title: spec.icon, description: spec.icon, name: spec.icon },
      })],
    });
    inner.push(iconPara);
  }
  if (spec.items) {
    const bullets = bulletList(spec.items, {
      size: compactSafety ? 6.98 : BODY_PT,
      tight: compactSafety || spec.type === 'note',
      indentMm: 4.7,
      lineSpacingMul: (spec.type === 'warning' && !compactSafety) ? 1.10 : null,
      spaceAfterPt: (spec.type === 'warning' && !compactSafety) ? 0.5 : null,
      characterSpacing: spec.type === 'warning' ? 8 : null,
    });
    inner.push(...bullets);
  }
  if (spec.text) {
    inner.push(new Paragraph({
      spacing: { before: 0, after: pt(1), line: 240, lineRule: LineRuleType.AUTO },
      children: [r({ text: spec.text, size: BODY_PT, color: DARK })],
    }));
  }

  const borderSize = spec.type === 'note' ? 0 : (spec.type === 'warning' ? 12 : 8);
  const cellBorders = spec.type === 'note'
    ? noBorders()
    : {
        top: { style: BorderStyle.SINGLE, size: borderSize, color: borderColor },
        bottom: { style: BorderStyle.SINGLE, size: borderSize, color: borderColor },
        left: { style: BorderStyle.SINGLE, size: borderSize, color: borderColor },
        right: { style: BorderStyle.SINGLE, size: borderSize, color: borderColor },
      };

  const padStart = spec.type === 'note' ? 205 : 176;
  const padV = spec.type === 'note' ? 44 : 46;

  return new Table({
    width: { size: CONTENT_W_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_W_DXA],
    alignment: AlignmentType.CENTER,
    borders: tableNoBorders(),
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_W_DXA, type: WidthType.DXA },
        margins: { top: padV, bottom: padV, left: padStart, right: 110 },
        shading: { type: ShadingType.CLEAR, color: 'auto', fill: fillColor },
        verticalAlign: VerticalAlign.TOP,
        borders: cellBorders,
        children: inner,
      })],
    })],
  });
}

// =============================================================
// Page builders
// =============================================================

function buildCover() {
  const c = content.meta;
  const out = [];
  // cover-brand:  "── 威富可"
  out.push(new Paragraph({
    spacing: { before: pt(20), after: pt(138), line: 240, lineRule: LineRuleType.AUTO },
    children: [
      r({ text: '━━ ', size: 7.5, bold: true, color: RED }),
      r({ text: c.brand, size: 7.5, bold: true, color: BLACK }),
    ],
  }));
  // cover image
  if (c.coverImage) {
    const fit = fitImage(c.coverImage, 42, 32.5);
    out.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: pt(8), after: pt(30), line: 240, lineRule: LineRuleType.AUTO },
      children: [new ImageRun({
        type: 'png',
        data: imageBuffer(c.coverImage),
        transformation: { width: mmToEmu(fit.wmm) / 9525, height: mmToEmu(fit.hmm) / 9525 },
        altText: { title: 'cover', description: 'cover', name: 'cover' },
      })],
    }));
  }
  // MODEL IMTxxx (red mono)
  out.push(new Paragraph({
    spacing: { before: 0, after: pt(2), line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: 'MODEL ' + c.model, size: 6, bold: true, color: RED, mono: true })],
  }));
  // product name big bold
  out.push(new Paragraph({
    spacing: { before: 0, after: 0, line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: c.productName, size: 18, bold: true, color: DARK })],
  }));
  // subtitle small gray
  out.push(new Paragraph({
    spacing: { before: 0, after: pt(1), line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: c.coverSubtitle, size: 7.5, color: GRAY })],
  }));
  // short red divider
  out.push(new Paragraph({
    spacing: { before: 0, after: pt(113), line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: '━━━━', size: 7, bold: true, color: RED })],
  }));
  // cover-bottom (border-top + 2 lines)
  out.push(new Paragraph({
    spacing: { before: 0, after: pt(3), line: 240, lineRule: LineRuleType.AUTO },
    border: { top: { style: BorderStyle.SINGLE, size: 10, color: BLACK, space: 1 } },
    children: [r({ text: '', size: SMALL_PT })],
  }));
  out.push(new Paragraph({
    spacing: { before: 0, after: 0, line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: c.coverBottom, size: SMALL_PT, color: GRAY })],
  }));
  return out;
}

function buildToc() {
  const out = [];
  out.push(headerStrip({ brand: content.meta.brand, headerRef: content.meta.model + ' — ' + content.meta.coverSubtitle }));
  out.push(new Paragraph({
    spacing: { before: 0, after: pt(10), line: 240, lineRule: LineRuleType.AUTO },
    children: [r({ text: content.toc.title, size: 15, bold: true })],
  }));
  for (const item of content.toc.items) {
    out.push(new Paragraph({
      spacing: { before: 0, after: pt(6), line: 240, lineRule: LineRuleType.AUTO },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W_DXA }],
      children: [
        r({ text: item.num + '  ', size: 6.75, bold: true, color: RED, mono: true }),
        r({ text: item.name, size: 7.5, bold: true }),
        r({ text: '\t', size: 6.38, color: GRAY, mono: true }),
        r({ text: String(item.page), size: 6.38, color: GRAY, mono: true }),
      ],
    }));
  }
  return out;
}

function buildBodyPage(page) {
  const out = [];
  out.push(headerStrip({ brand: content.meta.brand, headerRef: page.headerRef }));
  out.push(sectionTitle(page.chapter));

  let prevWasList = false;
  for (let i = 0; i < page.blocks.length; i++) {
    const block = page.blocks[i];
    const afterList = prevWasList;
    prevWasList = block.type === 'bullets';

    switch (block.type) {
      case 'paragraph':
        out.push(bodyPara(block));
        break;
      case 'subtitle':
        out.push(subTitle(block.text, { before: afterList ? 8 : 4 }));
        break;
      case 'bullets':
        out.push(...bulletList(block.items, page.compactWarranty
          ? { lineSpacingMul: 1.0, spaceAfterPt: 0.25 }
          : {}));
        break;
      case 'warning':
      case 'caution':
      case 'note':
        out.push(alertBox({ type: block.type, ...block }, { compactSafety: page.compactSafety }));
        out.push(new Paragraph({ spacing: { before: 0, after: pt(2), line: 240, lineRule: LineRuleType.AUTO }, children: [] }));
        break;
      case 'figure':
        out.push(figureBlock({ image: block.image, maxHeightMm: block.maxHeightMm, maxWidthMm: block.maxWidthMm || CONTENT_W_MM }));
        break;
      case 'separator':
        out.push(figureBlock({ image: block.image, maxHeightMm: 4, maxWidthMm: 60 }));
        break;
      case 'figureRow':
        out.push(figureRow({ images: block.images, maxHeightMm: block.maxHeightMm || 26 }));
        out.push(new Paragraph({ spacing: { before: 0, after: pt(2), line: 240, lineRule: LineRuleType.AUTO }, children: [] }));
        break;
      case 'steps':
        for (const step of block.steps) {
          out.push(stepRow(step));
          if (step.figures) out.push(...stepFigures(step));
        }
        break;
      case 'indicators':
        out.push(indicatorRow(block.items));
        break;
      case 'table':
        out.push(buildTable({
          ...block,
          compactWarranty: page.compactWarranty,
        }));
        out.push(new Paragraph({ spacing: { before: 0, after: pt(2), line: 240, lineRule: LineRuleType.AUTO }, children: [] }));
        break;
      default:
        // skip unknown
        break;
    }
  }
  return out;
}

// =============================================================
// Section construction
// =============================================================

function makeSection({ children, pageNo = null }) {
  const footers = {};
  if (pageNo !== null) {
    footers.default = new Footer({
      children: [new Paragraph({
        spacing: { before: 0, after: 0, line: 240, lineRule: LineRuleType.AUTO },
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'EEEEEE', space: 1 } },
        tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W_DXA }],
        children: [
          r({ text: content.meta.productLine, size: SMALL_PT, color: GRAY }),
          r({ text: '\t', size: SMALL_PT, color: GRAY, mono: true }),
          r({ text: String(pageNo), size: SMALL_PT, color: GRAY, mono: true }),
        ],
      })],
    });
  }
  return {
    properties: {
      page: {
        size: { width: PAGE_W_DXA, height: PAGE_H_DXA },
        margin: {
          // W27 uses 10.2mm top, 10mm other sides → ~578 dxa top, 567 dxa side
          top: Math.round(10.2 * 56.7),
          bottom: Math.round(10 * 56.7),
          left: Math.round(10 * 56.7),
          right: Math.round(10 * 56.7),
          header: Math.round(4 * 56.7),
          footer: Math.round(3.5 * 56.7),
        },
      },
    },
    footers,
    children,
  };
}

function build() {
  const sections = [];
  sections.push(makeSection({ children: buildCover() }));
  sections.push(makeSection({ children: buildToc(), pageNo: 2 }));
  for (const page of content.pages) {
    sections.push(makeSection({ children: buildBodyPage(page), pageNo: page.pageNo }));
  }

  const doc = new Document({
    creator: 'docx-js fromscratch',
    title: 'IMT050 Wevac CN',
    description: 'IMT050 ice maker manual (A5, CN)',
    styles: {
      default: {
        document: {
          run: { font: LATIN_FONT, size: HP(BODY_PT) },
          paragraph: { spacing: { line: 240, lineRule: LineRuleType.AUTO } },
        },
      },
    },
    sections,
  });
  return doc;
}

const outPath = path.resolve(__dirname, process.argv[2] || 'output.docx');
const doc = build();
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log('Wrote', outPath, '(' + buf.length + ' bytes)');
});
