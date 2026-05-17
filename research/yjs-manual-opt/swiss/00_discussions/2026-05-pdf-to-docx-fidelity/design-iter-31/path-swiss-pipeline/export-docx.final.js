#!/usr/bin/env node
/**
 * export-docx.js 鈥?Generate editable Word document from structured JSON content
 *
 * Usage:
 *   node export-docx.js --region cn                     # V23 CN DOCX
 *   node export-docx.js --region gb --brand vesta       # V23 EN Vesta
 *   node export-docx.js --product ../products/imt050 --region de
 *   node export-docx.js --all                           # All variants
 *
 * Reads the same JSON data as build-variant.js, outputs .docx files.
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber,
  TabStopType, TabStopPosition, VerticalAlign, TableLayoutType, SectionType,
} = require('docx');

const {
  loadProductConfig, loadContentDocument, loadImagesManifest,
  loadLocaleCatalog, buildLocalizedRuntimeData, resolveBrandTheme,
  langSuffix,
} = require('./build-variant.js');

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}
const buildAll = args.includes('--all');
const productDir = path.resolve(getArg('product', path.resolve(__dirname, '..', 'products', 'v23')));
const regionKey = getArg('region', 'cn');
const brandKey = getArg('brand', null);
const outputDir = path.resolve(__dirname, '..', 'output');
const writeBaseTemplateCn = args.includes('--write-base-template-cn');
const baseTemplatePath = path.resolve(__dirname, '..', 'template', 'shared', 'docx', 'base-template-cn.docx');

const config = loadProductConfig(productDir);

// ---------------------------------------------------------------------------
// Constants 鈥?A5 page in DXA (1 inch = 1440 DXA, 1mm 鈮?56.7 DXA)
// ---------------------------------------------------------------------------
const MM = 56.7;
const PAGE_W = Math.round(148 * MM);
const PAGE_H = Math.round(210 * MM);
const MARGIN_X = Math.round(10 * MM);
const MARGIN_Y = Math.round(10 * MM);
const CONTENT_W = PAGE_W - MARGIN_X * 2;

// ---------------------------------------------------------------------------
// W27-tuned defaults (extracted from design-iter-22/path-codex/build_b2_docx.py).
// Sizes are in OOXML half-points (1 pt = 2). Margins in DXA (1 pt = 20).
// These are the "Swiss A5 booklet" baseline. Brands may override via
// brand-themes.json > <brand>.docx.sizes / .images / .margins.
// ---------------------------------------------------------------------------
const DEFAULT_DOCX_SIZES = {
  // Body / text
  bodySize: 14,            // 7.0pt (PDF measured 7.05pt -> 14.1 half-pt)
  subtitleSize: 15,        // 7.5pt -- sub_title (PDF 7.5pt)
  sectionTitleSize: 18,    // 9.0pt -- sub_title fallback
  chapterNumberSize: 27,   // 13.5pt -- chapter num (red)
  chapterTitleSize: 22,    // 11.0pt -- chapter title
  // Cover
  coverBrandSize: 15,      // 7.5pt -- brand top line
  coverTypeSize: 15,       // 7.5pt -- document subtitle
  coverProductSize: 36,    // 18.0pt -- product name big
  coverModelSize: 12,      // 6.0pt -- MODEL mono red (was 11)
  coverCompanySize: 11,    // 5.4pt -- footer disclaimer (was 14)
  // TOC
  tocTitleSize: 30,        // 15.0pt -- TOC title
  tocChapterSize: 14,      // 7.0pt -- chap num mono red
  tocTextSize: 15,         // 7.5pt -- chap name bold
  tocPageSize: 13,         // 6.5pt -- page number mono gray
  // Header / footer
  headerBrandSize: 14,     // 6.75pt bold -- header left
  headerMetaSize: 11,      // 5.4pt mono -- header right
  smallSize: 11,           // 5.4pt -- small/disclaimer/footer
  // Tables
  tableBodySize: 14,       // 6.7pt
  tableCompactSize: 13,    // 6.5pt
  tableHeaderSize: 12,     // 6.0pt
};

const DEFAULT_DOCX_IMAGES = {
  cover: { width: 119, height: 92 },         // 42x32.5 mm (~119x92 docx px @ 72dpi)
  figure: { width: 310, height: 205 },
  splitPanel: { width: 160, height: 130 },
  stepSingle: { width: 260, height: 160 },
  stepDouble: { width: 160, height: 118 },
  stepTriple: { width: 110, height: 88 },
  stepSingleCompact: { width: 220, height: 130 },
  stepDoubleCompact: { width: 138, height: 98 },
  stepTripleCompact: { width: 95, height: 76 },
  rowSingle: { width: 230, height: 140 },
  rowDouble: { width: 150, height: 105 },
  rowTriple: { width: 105, height: 82 },
  inlineIcon: { width: 22, height: 22 },
};

const DEFAULT_DOCX_MARGINS = {
  // Cell margins in DXA. W27 baseline:
  //  - normal table: pad_v=36, pad_l=55
  //  - compact (≥8 rows): pad_v=32, pad_l=55
  //  - compact-warranty (spread out): pad_v=52, pad_l=87
  cellNormal:   { top: 40, bottom: 40, left: 60, right: 60 },
  cellCompact:  { top: 38, bottom: 38, left: 60, right: 60 },
  cellWarranty: { top: 32, bottom: 32, left: 80, right: 60 },
  alertCell:    { top: 55, bottom: 55, left: 90, right: 90 },
  noteCell:     { top: 55, bottom: 55, left: 90, right: 90 },
};

let SIZES = { ...DEFAULT_DOCX_SIZES };
let IMAGES = { ...DEFAULT_DOCX_IMAGES };
let MARGINS = { ...DEFAULT_DOCX_MARGINS };

const DOCX_PROFILE = {
  templateId: 'A5_CN_BASE_V1',
  page: {
    width: PAGE_W,
    height: PAGE_H,
    marginX: MARGIN_X,
    marginY: MARGIN_Y,
  },
  // Backward-compat lookup tables — read by other Swiss modules.
  // Wrapped as getters so brand-theme overrides take effect at render time.
  get images() { return IMAGES; },
  get text() {
    return {
      bodySize: SIZES.bodySize,
      subtitleSize: SIZES.subtitleSize,
      sectionTitleSize: SIZES.sectionTitleSize,
      chapterNumberSize: SIZES.chapterNumberSize,
      chapterTitleSize: SIZES.chapterTitleSize,
      coverBrandSize: SIZES.coverBrandSize,
      coverTypeSize: SIZES.coverTypeSize,
      coverProductSize: SIZES.coverProductSize,
      coverModelSize: SIZES.coverModelSize,
      coverCompanySize: SIZES.coverCompanySize,
      tocTitleSize: SIZES.tocTitleSize,
      headerBrandSize: SIZES.headerBrandSize,
      headerMetaSize: SIZES.headerMetaSize,
      smallSize: SIZES.smallSize,
    };
  },
  get table() {
    return {
      bodySize: SIZES.tableBodySize,
      compactSize: SIZES.tableCompactSize,
      headerSize: SIZES.tableHeaderSize,
    };
  },
};

// ---------------------------------------------------------------------------
// Styling constants
// ---------------------------------------------------------------------------
const DEFAULT_DOCX_THEME = {
  primary: '1A1A1A',
  accent: 'E63946',
  light: '666666',
  muted: '8E8E93',
  font: 'Arial',
  latinFont: 'Arial',
  cjkFont: 'Microsoft YaHei',
  titleLatinFont: 'Arial Black',
  titleCjkFont: 'Microsoft YaHei',
  monoFont: 'Courier New',
  coverDivider: 'E63946',
  coverModel: 'E63946',
  coverType: '8E8E93',
  coverTitle: '1A1A1A',
  coverCompany: '8E8E93',
  chapterBar: '000000',
  chapterNumber: 'E63946',
  chapterTitle: '1A1A1A',
  chapterHeaderRef: '8E8E93',
  tocTitle: '1A1A1A',
  tocText: '666666',
  sectionTitle: '1A1A1A',
  accentDeep: 'B5202C',
  accentLight: 'FDF0F1',
  accentMid: 'F0A0A8',
  tableHeaderFill: '1A1A1A',
  tableHeaderText: 'FFFFFF',
  tableLabelFill: 'F4F4F4',
  tableBorder: 'CCCCCC',
  warningFill: 'FFF3D6',
  cautionFill: 'F7D9DD',
  noticeFill: 'DCECF8',
  warningBorder: 'E2C55A',
  cautionBorder: 'D9A7B3',
  noticeBorder: '9FC4DA',
  warningTitle: '856404',
  cautionTitle: '922B21',
  noticeTitle: '1A5276',
  warningText: '4A4A4A',
  cautionText: '4A4A4A',
  noticeText: '4A4A4A',
  boxBorder: 'D4D4D4',
  headerBorder: 'D9D9D9',
  headerText: '8E8E93',
  footerText: '8E8E93',
};

let ACTIVE_THEME = { ...DEFAULT_DOCX_THEME };
let FONT = buildFontBundle(DEFAULT_DOCX_THEME.latinFont, DEFAULT_DOCX_THEME.cjkFont);
let TITLE_FONT = buildFontBundle(DEFAULT_DOCX_THEME.titleLatinFont, DEFAULT_DOCX_THEME.titleCjkFont);
let MONO_FONT = buildFontBundle(DEFAULT_DOCX_THEME.monoFont, DEFAULT_DOCX_THEME.cjkFont);

function buildFontBundle(latin, cjk) {
  return {
    ascii: latin,
    hAnsi: latin,
    cs: latin,
    eastAsia: cjk,
  };
}

function applyDocxTheme(docxTheme = {}) {
  ACTIVE_THEME = {
    ...DEFAULT_DOCX_THEME,
    ...docxTheme,
    light: DEFAULT_DOCX_THEME.muted,
    muted: DEFAULT_DOCX_THEME.muted,
    headerText: DEFAULT_DOCX_THEME.headerText,
    footerText: DEFAULT_DOCX_THEME.footerText,
    coverType: DEFAULT_DOCX_THEME.coverType,
    coverCompany: DEFAULT_DOCX_THEME.coverCompany,
    chapterHeaderRef: DEFAULT_DOCX_THEME.chapterHeaderRef,
    latinFont: DEFAULT_DOCX_THEME.latinFont,
    cjkFont: DEFAULT_DOCX_THEME.cjkFont,
    titleLatinFont: DEFAULT_DOCX_THEME.titleLatinFont,
    titleCjkFont: DEFAULT_DOCX_THEME.titleCjkFont,
    monoFont: DEFAULT_DOCX_THEME.monoFont,
  };
  // Brand-themable: sizes / images / margins (defaults from W27 baseline).
  SIZES = { ...DEFAULT_DOCX_SIZES, ...(docxTheme.sizes || {}) };
  IMAGES = { ...DEFAULT_DOCX_IMAGES, ...(docxTheme.images || {}) };
  MARGINS = { ...DEFAULT_DOCX_MARGINS, ...(docxTheme.margins || {}) };
  FONT = buildFontBundle(ACTIVE_THEME.latinFont, ACTIVE_THEME.cjkFont);
  TITLE_FONT = buildFontBundle(ACTIVE_THEME.titleLatinFont, ACTIVE_THEME.titleCjkFont);
  MONO_FONT = buildFontBundle(ACTIVE_THEME.monoFont, ACTIVE_THEME.cjkFont);
}

function border(color = ACTIVE_THEME.boxBorder, size = 1, style = BorderStyle.SINGLE) {
  return { style, size, color };
}

const BORDER_LIGHT = border('CCCCCC');
const NO_BORDERS = {
  top: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
};
function boxBorders(color = ACTIVE_THEME.boxBorder) {
  return { top: border(color), bottom: border(color), left: border(color), right: border(color) };
}
function horizontalBorders(color = ACTIVE_THEME.tableBorder, size = 1) {
  return {
    top: border(color, size),
    bottom: border(color, size),
    left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  };
}
// CELL_MARGINS are now drawn from MARGINS (theme-overridable); call as functions.
function cellMargins() { return { ...MARGINS.cellNormal }; }
function cellMarginsCompact() { return { ...MARGINS.cellCompact }; }
function cellMarginsWarranty() { return { ...MARGINS.cellWarranty }; }
const DOCX_IMAGE_CACHE_DIR = path.resolve(outputDir, '_docx_raster_cache');

// ---------------------------------------------------------------------------
// Text token parsing: [btn:XXX] and **bold**
// ---------------------------------------------------------------------------
function parseTextTokens(text, base = {}) {
  const runFont = base.font || FONT;
  const { font: _font, ...runBase } = base;
  if (!text) return [new TextRun({ text: '', font: runFont, ...runBase })];
  const runs = [];
  const regex = /(\[btn:([^\]]+)\]|\*\*([^*]+)\*\*|<b>([^<]+)<\/b>)/g;
  let lastIndex = 0;
  let match;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      runs.push(new TextRun({ text: text.slice(lastIndex, match.index), font: runFont, ...runBase }));
    }
    if (match[2]) {
      // [btn:Power] -> monospace Courier black on light gray, wrapped in spaces
      runs.push(new TextRun({
        text: ` ${match[2]} `,
        bold: true,
        font: MONO_FONT,
        color: ACTIVE_THEME.primary,
        shading: { type: ShadingType.CLEAR, fill: 'F2F2F7', color: 'auto' },
        ...runBase,
      }));
    } else if (match[3]) {
      runs.push(new TextRun({ text: match[3], bold: true, font: runFont, ...runBase }));
    } else if (match[4]) {
      runs.push(new TextRun({ text: match[4], bold: true, font: runFont, ...runBase }));
    }
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < text.length) {
    runs.push(new TextRun({ text: text.slice(lastIndex), font: runFont, ...runBase }));
  }
  if (runs.length === 0) {
    runs.push(new TextRun({ text: '', font: runFont, ...runBase }));
  }
  return runs;
}

function readTextValue(value) {
  if (typeof value === 'string') return value;
  if (value && typeof value === 'object' && typeof value.text === 'string') return value.text;
  return '';
}

// ---------------------------------------------------------------------------
// Variable replacement in text: {{brand.display_name}} etc.
// ---------------------------------------------------------------------------
function resolveVars(text, vars) {
  if (!text) return text;
  return text.replace(/\{\{([^}]+)\}\}/g, (_, key) => vars[key] || `{{${key}}}`);
}

// ---------------------------------------------------------------------------
// Image loading helper
// ---------------------------------------------------------------------------
async function prepareImagesManifestForDocx(imagesManifest, imagesDir, cacheNamespace) {
  const cloned = {};
  const cacheDir = path.join(DOCX_IMAGE_CACHE_DIR, cacheNamespace);
  fs.mkdirSync(cacheDir, { recursive: true });
  let rasterizedCount = 0;

  for (const [key, figure] of Object.entries(imagesManifest || {})) {
    const clonedFigure = { ...figure };
    const absPath = path.join(imagesDir, figure.file);
    clonedFigure.absPath = absPath;

    if (fs.existsSync(absPath) && path.extname(absPath).toLowerCase() === '.svg') {
      const pngPath = path.join(cacheDir, `${key.replace(/[^a-z0-9._-]+/gi, '_')}.png`);
      await sharp(absPath, { density: 220 }).png({ compressionLevel: 9 }).toFile(pngPath);
      clonedFigure.docxFile = pngPath;
      rasterizedCount += 1;
    }

    cloned[key] = clonedFigure;
  }

  return {
    manifest: cloned,
    stats: { rasterizedCount },
  };
}

function loadImage(figureRef, imagesManifest, imagesDir) {
  const figure = typeof figureRef === 'string'
    ? imagesManifest[figureRef]
    : (figureRef.figure ? imagesManifest[figureRef.figure] : figureRef);
  if (!figure || !figure.file) return null;

  const imgPath = figure.docxFile || figure.absPath || path.join(imagesDir, figure.file);
  if (!fs.existsSync(imgPath)) return null;

  const ext = path.extname(imgPath).slice(1).toLowerCase();
  const typeMap = { png: 'png', jpg: 'jpg', jpeg: 'jpg', gif: 'gif', bmp: 'bmp' };
  const docxType = typeMap[ext];
  if (!docxType) return null;

  const data = fs.readFileSync(imgPath);
  return {
    data,
    type: docxType,
    alt: figure.alt || '',
    dimensions: getImageDimensions(data, docxType),
  };
}

function getImageDimensions(data, type) {
  try {
    if (type === 'png' && data.length >= 24) {
      return {
        width: data.readUInt32BE(16),
        height: data.readUInt32BE(20),
      };
    }
    if (type === 'gif' && data.length >= 10) {
      return {
        width: data.readUInt16LE(6),
        height: data.readUInt16LE(8),
      };
    }
    if (type === 'bmp' && data.length >= 26) {
      return {
        width: Math.abs(data.readInt32LE(18)),
        height: Math.abs(data.readInt32LE(22)),
      };
    }
    if (type === 'jpg') {
      let offset = 2;
      while (offset < data.length) {
        if (data[offset] !== 0xFF) {
          offset += 1;
          continue;
        }
        const marker = data[offset + 1];
        const size = data.readUInt16BE(offset + 2);
        if ([0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB].includes(marker)) {
          return {
            height: data.readUInt16BE(offset + 5),
            width: data.readUInt16BE(offset + 7),
          };
        }
        offset += 2 + size;
      }
    }
  } catch (error) {
    return null;
  }
  return null;
}

function fitImageSize(image, maxWidth, maxHeight) {
  const fallback = { width: maxWidth, height: maxHeight };
  if (!image || !image.dimensions || !image.dimensions.width || !image.dimensions.height) {
    return fallback;
  }

  const ratio = Math.min(
    maxWidth / image.dimensions.width,
    maxHeight / image.dimensions.height,
    1
  );

  return {
    width: Math.max(1, Math.round(image.dimensions.width * ratio)),
    height: Math.max(1, Math.round(image.dimensions.height * ratio)),
  };
}

function makeImageRun(image, maxWidth, maxHeight, name = 'image') {
  const size = fitImageSize(image, maxWidth, maxHeight);
  return new ImageRun({
    type: image.type,
    data: image.data,
    transformation: size,
    altText: {
      title: image.alt,
      description: image.alt,
      name: image.alt || name,
    },
  });
}

function makeSpacer(after = 120) {
  return new Paragraph({ spacing: { after }, children: [] });
}

function emptyParagraph() {
  return new Paragraph({ children: [new TextRun({ text: '', font: FONT })] });
}

function makeTextParagraph(text, options = {}) {
  const {
    before = 0,
    after = 120,
    alignment,
    size = DOCX_PROFILE.text.bodySize,
    color = ACTIVE_THEME.primary,
    bold = false,
    italics = false,
    heading,
    numbering,
    indent,
    pageBreakBefore = false,
    border: paragraphBorder,
    keepLines = false,
    keepNext = false,
    font = FONT,
    // W27 BODY_LINE_SPACING=1.16 -> docx-js auto (240) * 1.16 ≈ 278.
    line = 280,
  } = options;

  return new Paragraph({
    heading,
    numbering,
    alignment,
    indent,
    pageBreakBefore,
    keepLines,
    keepNext,
    border: paragraphBorder,
    spacing: { before, after, line },
    children: parseTextTokens(text, { size, color, bold, italics, font }),
  });
}

function makeTextParagraphs(text, options = {}) {
  const normalized = String(text ?? '').replace(/\r\n/g, '\n');
  return normalized.split('\n').map((line) => makeTextParagraph(line, options));
}

function normalizeCellChildren(children) {
  const flattened = [];
  for (const child of children || []) {
    if (!child) continue;
    if (Array.isArray(child)) flattened.push(...child);
    else flattened.push(child);
  }
  return flattened.length ? flattened : [emptyParagraph()];
}

function makeCell(children, opts = {}) {
  const width = opts.width || undefined;
  return new TableCell({
    borders: opts.borders || boxBorders(),
    margins: opts.margins || cellMargins(),
    shading: opts.shading,
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    rowSpan: opts.rowSpan,
    columnSpan: opts.columnSpan,
    verticalAlign: opts.verticalAlign || VerticalAlign.TOP,
    children: normalizeCellChildren(children),
  });
}

function makeTextCell(text, opts = {}) {
  // Pick cell margins: warranty > compact > normal.
  let margins;
  if (opts.margins) margins = opts.margins;
  else if (opts.warranty) margins = cellMarginsWarranty();
  else if (opts.compact) margins = cellMarginsCompact();
  else margins = cellMargins();
  return makeCell(makeTextParagraphs(readTextValue(text || ''), {
    after: 0,
    size: opts.size || DOCX_PROFILE.table.bodySize,
    color: opts.color || ACTIVE_THEME.primary,
    bold: opts.bold || false,
    alignment: opts.alignment,
    font: opts.font || FONT,
  }), {
    width: opts.width,
    rowSpan: opts.rowSpan,
    columnSpan: opts.columnSpan,
    shading: opts.shading,
    borders: opts.borders || horizontalBorders(ACTIVE_THEME.tableBorder),
    margins,
    verticalAlign: opts.verticalAlign || VerticalAlign.CENTER,
  });
}

function makeHeaderCell(text, opts = {}) {
  return makeTextCell(text, {
    ...opts,
    shading: { fill: ACTIVE_THEME.tableHeaderFill, type: ShadingType.CLEAR },
    color: ACTIVE_THEME.tableHeaderText,
    bold: true,
    alignment: opts.alignment || AlignmentType.LEFT,
    size: DOCX_PROFILE.table.headerSize,
    borders: opts.borders || horizontalBorders(ACTIVE_THEME.tableBorder),
  });
}

function makeBorderlessCell(children, width) {
  return makeCell(children, {
    width,
    borders: NO_BORDERS,
    margins: { top: 0, bottom: 0, left: 0, right: 0 },
  });
}

function zebraShading(rowIndex) {
  return rowIndex % 2 === 1 ? { fill: ACTIVE_THEME.tableLabelFill, type: ShadingType.CLEAR } : undefined;
}

function isCompactTable(block = {}) {
  const flag = `${block.table_class || ''} ${block.className || ''} ${block.page_class || ''}`.toLowerCase();
  return Boolean(block.compact || flag.includes('compact'));
}

function isCompactLayout(block = {}) {
  const flag = `${block.page_class || ''} ${block.className || ''}`.toLowerCase();
  return Boolean(block.compact || flag.includes('compact'));
}

// W27 'compact_warranty' tables get TALLER cells (52 dxa pad_v vs 36 normal),
// because the chapter 10 (warranty) brand_info/manufacturer_info tables need
// breathing room rather than tighter packing.
function isWarrantyTable(block = {}) {
  const flag = `${block.page_class || ''} ${block.className || ''}`.toLowerCase();
  return flag.includes('compact-warranty');
}

function figureSizePreset(count, variant = 'row', compact = false) {
  if (variant === 'step') {
    if (compact) {
      if (count <= 1) return DOCX_PROFILE.images.stepSingleCompact;
      if (count === 2) return DOCX_PROFILE.images.stepDoubleCompact;
      return DOCX_PROFILE.images.stepTripleCompact;
    }
    if (count <= 1) return DOCX_PROFILE.images.stepSingle;
    if (count === 2) return DOCX_PROFILE.images.stepDouble;
    return DOCX_PROFILE.images.stepTriple;
  }
  if (count <= 1) return DOCX_PROFILE.images.rowSingle;
  if (count === 2) return DOCX_PROFILE.images.rowDouble;
  return DOCX_PROFILE.images.rowTriple;
}

function resolveFigureItem(ref) {
  if (typeof ref === 'string') return { figure: ref };
  return ref || {};
}

function renderFigureGrid(items, ctx, options = {}) {
  const normalized = (items || []).map(resolveFigureItem);
  if (!normalized.length) return [];

  const columns = Math.max(1, Math.min(options.columns || normalized.length, 3));
  const width = options.width || CONTENT_W;
  const colWidth = Math.floor(width / columns);
  const sizePreset = options.sizePreset || figureSizePreset(normalized.length, options.variant);
  const rows = [];

  for (let index = 0; index < normalized.length; index += columns) {
    const slice = normalized.slice(index, index + columns);
    const cells = slice.map((item) => {
      const children = [];
      if (item.label_before) {
        children.push(makeTextParagraph(resolveVars(readTextValue(item.label_before), ctx.vars), {
          after: 20,
          size: DOCX_PROFILE.text.smallSize,
          bold: true,
          alignment: AlignmentType.CENTER,
        }));
      }

      const image = loadImage(item.figure, ctx.images, ctx.imagesDir);
      if (image) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: item.label_after ? 20 : 0 },
          children: [makeImageRun(image, sizePreset.width, sizePreset.height, item.figure)],
        }));
      } else {
        children.push(makeTextParagraph(`[Image: ${item.figure}]`, {
          after: 40,
          italics: true,
          color: ACTIVE_THEME.light,
          alignment: AlignmentType.CENTER,
          size: DOCX_PROFILE.text.smallSize,
        }));
      }

      if (item.label_after) {
        children.push(makeTextParagraph(resolveVars(readTextValue(item.label_after), ctx.vars), {
          after: 0,
          size: DOCX_PROFILE.text.smallSize,
          alignment: AlignmentType.CENTER,
        }));
      }

      return makeBorderlessCell(children, colWidth);
    });

    while (cells.length < columns) {
      cells.push(makeBorderlessCell([emptyParagraph()], colWidth));
    }

    rows.push(new TableRow({ children: cells }));
  }

  return [new Table({
    width: { size: width, type: WidthType.DXA },
    columnWidths: Array.from({ length: columns }, () => colWidth),
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows,
  })];
}

function renderStackedFigures(items, ctx, options = {}) {
  const normalized = (items || []).map(resolveFigureItem);
  const sizePreset = options.sizePreset || DOCX_PROFILE.images.splitPanel;
  const elements = [];

  for (const item of normalized) {
      if (item.label_before) {
        elements.push(makeTextParagraph(resolveVars(readTextValue(item.label_before), ctx.vars), {
        after: 15,
        size: DOCX_PROFILE.text.smallSize,
        bold: true,
        alignment: AlignmentType.CENTER,
      }));
    }

    const image = loadImage(item.figure, ctx.images, ctx.imagesDir);
    if (image) {
      elements.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: item.label_after ? 15 : 45 },
        children: [makeImageRun(image, sizePreset.width, sizePreset.height, item.figure)],
      }));
    } else {
      elements.push(makeTextParagraph(`[Image: ${item.figure}]`, {
        after: 45,
        italics: true,
        color: ACTIVE_THEME.light,
        alignment: AlignmentType.CENTER,
        size: DOCX_PROFILE.text.smallSize,
      }));
    }

    if (item.label_after) {
      elements.push(makeTextParagraph(resolveVars(readTextValue(item.label_after), ctx.vars), {
        after: 45,
        size: DOCX_PROFILE.text.smallSize,
        alignment: AlignmentType.CENTER,
      }));
    }
  }

  return elements.length ? elements : [emptyParagraph()];
}

// ---------------------------------------------------------------------------
// Block renderers 鈫?docx elements
// ---------------------------------------------------------------------------
function renderParagraphBlock(block, ctx) {
  const text = resolveVars(readTextValue(block.text || ''), ctx.vars);
  return makeTextParagraphs(text, {
    after: 55,
    size: DOCX_PROFILE.text.bodySize,
  });
}

function renderSubTitle(block, ctx) {
  // W27 sub_title: 7.5pt bold black, BLACK bottom border thin.
  return [makeTextParagraph(resolveVars(readTextValue(block.text), ctx.vars), {
    before: 70,
    after: 55,
    size: SIZES.subtitleSize,
    bold: true,
    keepNext: true,
    font: TITLE_FONT,
    color: ACTIVE_THEME.sectionTitle,
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 8, color: ACTIVE_THEME.headerBorder },
    },
  })];
}

function renderBulletList(block, ctx) {
  // W27: 3.2mm left indent (~180 DXA), 3.2mm hanging.
  // Bullet = manual leading "•    " run, RED Arial Black 5.8pt (size half-pt 12),
  // body text 7pt (size half-pt 14). Letting docx-js's numbering paint the bullet
  // produces too-small glyphs in LibreOffice; manual prefix renders predictable.
  return (block.items || []).map((item) => {
    const text = resolveVars(readTextValue(item), ctx.vars);
    return new Paragraph({
      spacing: { before: 0, after: 32, line: 270 },
      indent: { left: 180, hanging: 180 },
      children: [
        new TextRun({
          text: '•   ',
          font: TITLE_FONT,
          bold: true,
          size: 14, // 7pt bullet — visibility through LO rendering
          color: ACTIVE_THEME.accent,
        }),
        ...parseTextTokens(text, { size: SIZES.bodySize, font: FONT }),
      ],
    });
  });
}

function getAlertTheme(kind) {
  if (kind === 'warning_box') {
    return { border: ACTIVE_THEME.accent, titleColor: ACTIVE_THEME.accent, icon: '\u25B2', iconColor: ACTIVE_THEME.accent, textColor: ACTIVE_THEME.primary };
  }
  if (kind === 'caution_box') {
    return { border: ACTIVE_THEME.primary, titleColor: ACTIVE_THEME.primary, icon: '\u25B2', iconColor: 'D99A00', textColor: ACTIVE_THEME.primary };
  }
  return { border: ACTIVE_THEME.headerBorder, titleColor: ACTIVE_THEME.primary, icon: '\u258C', iconColor: '1A5276', textColor: ACTIVE_THEME.primary, fill: 'F2F2F7' };
}

function renderAlertBox(block, ctx, kind) {
  // W27 layout:
  //   - warning box: red 1.5pt border (sz=12), title in red 6.5pt bold + ▲ icon left of title
  //   - caution box: black 1pt border (sz=8)
  //   - note box: light gray fill F2F2F7, no border
  //   - cell margins: warning/caution top/bot 46 dxa, left 176, right 110
  //   - note: top/bot 44 dxa, left 205, right 110
  const theme = getAlertTheme(kind);
  const isNote = kind === 'notice_box';
  const isWarning = kind === 'warning_box';
  const isCaution = kind === 'caution_box';
  // W27 compact_safety: title 6.38pt, bullets 6.98pt, line 0.96, after 1.35pt.
  // Only kick in when the box has many items (would otherwise overflow).
  const itemCount = Array.isArray(block.items) ? block.items.length : 0;
  const compactSafety = String(block.page_class || '').includes('compact-safety') && itemCount >= 12;
  const borderSize = isWarning ? 12 : (isCaution ? 8 : 0);
  const cellMargin = isNote ? MARGINS.noteCell : MARGINS.alertCell;
  const elements = [];

  if (block.title) {
    // Only warning_box shows the ▲ icon (and only when no explicit block.icon).
    const showTextIcon = !block.icon && isWarning;
    elements.push(new Paragraph({
      spacing: { after: compactSafety ? 8 : 20, line: 220 },
      children: [
        ...(showTextIcon ? [new TextRun({
          text: theme.icon + ' ',
          font: TITLE_FONT,
          bold: true,
          size: 14,
          color: theme.iconColor,
        })] : []),
        new TextRun({
          text: resolveVars(readTextValue(block.title), ctx.vars),
          font: TITLE_FONT,
          bold: true,
          size: compactSafety ? 12 : 13, // 6.38pt vs 6.5pt
          color: theme.titleColor,
        }),
      ],
    }));
  }
  if (block.icon) {
    const icon = loadImage(block.icon, ctx.images, ctx.imagesDir);
    if (icon) {
      elements.push(new Paragraph({
        spacing: { after: compactSafety ? 6 : 18 },
        indent: { left: -60 }, // pull icon to the left like W27 compact-safety mode
        children: [makeImageRun(icon,
          compactSafety ? Math.round(IMAGES.inlineIcon.width * 0.86) : IMAGES.inlineIcon.width,
          compactSafety ? Math.round(IMAGES.inlineIcon.height * 0.86) : IMAGES.inlineIcon.height,
          'icon')],
      }));
    }
  }
  if (block.items) {
    const bulletLine = compactSafety ? 192 : 250;     // 0.96 vs 1.04 line spacing
    const bulletAfter = compactSafety ? 6 : 12;       // 1.35pt vs 1.2pt
    const bulletSize = compactSafety ? 14 : SIZES.bodySize; // W27 compact_safety uses 6.98pt body = 14
    for (const item of block.items) {
      const itemText = resolveVars(readTextValue(item), ctx.vars);
      elements.push(new Paragraph({
        spacing: { before: 0, after: bulletAfter, line: bulletLine },
        indent: { left: 180, hanging: 180 },
        children: [
          new TextRun({
            text: '•   ',
            font: TITLE_FONT,
            bold: true,
            size: compactSafety ? 11 : 14, // 5.25pt vs 7pt bullet
            color: ACTIVE_THEME.accent,
          }),
          ...parseTextTokens(itemText, { size: bulletSize, font: FONT, color: theme.textColor }),
        ],
      }));
    }
  } else if (block.text) {
    elements.push(...makeTextParagraphs(resolveVars(readTextValue(block.text), ctx.vars), {
      after: 20, color: theme.textColor, size: SIZES.bodySize,
    }));
  }

  const borders = (isWarning || isCaution)
    ? boxBorders(theme.border)
    : (isNote ? NO_BORDERS : boxBorders(theme.border));
  // Override border thickness on warning/caution
  if (isWarning || isCaution) {
    for (const edge of ['top', 'bottom', 'left', 'right']) {
      borders[edge] = { style: BorderStyle.SINGLE, size: borderSize, color: theme.border };
    }
  }

  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows: [new TableRow({
      children: [makeCell(elements, {
        width: CONTENT_W,
        borders,
        shading: (isNote || theme.fill) ? { fill: theme.fill || 'F2F2F7', type: ShadingType.CLEAR } : undefined,
        margins: cellMargin,
      })],
    })],
  }), makeSpacer(40)];
}

function renderStepFlow(block, ctx) {
  // W27 layout (build_b2_docx.py add_step_flow):
  //   - badge: 13.5pt black square, white Arial-Black num, padded with 2 spaces "  n  "
  //   - inline (not table column), badge then gap then text
  //   - line spacing 1.10
  //   - step text: 7pt body
  // We use an inline-shaded run instead of a 2-col table to match the PDF tight
  // inline badge geometry.
  const startAt = Number(block.start_at || 1);
  const compact = isCompactLayout(block);
  const elements = [];
  for (let i = 0; i < (block.steps || []).length; i++) {
    const step = block.steps[i];
    const figureCount = (step.figures || []).length;
    // Inline step text with leading shaded badge run
    const textRuns = parseTextTokens(resolveVars(readTextValue(step.text || step), ctx.vars), {
      size: compact ? SIZES.tableCompactSize : SIZES.bodySize,
      font: FONT,
    });
    const p = new Paragraph({
      spacing: { before: 0, after: figureCount ? 20 : 40, line: 220 },
      children: [
        new TextRun({
          text: `  ${startAt + i}  `,
          font: TITLE_FONT,
          bold: true,
          size: SIZES.bodySize,
          color: 'FFFFFF',
          shading: { type: ShadingType.CLEAR, fill: ACTIVE_THEME.primary, color: 'auto' },
        }),
        new TextRun({
          text: '   ',
          font: FONT,
          size: SIZES.bodySize,
        }),
        ...textRuns,
      ],
    });
    elements.push(p);
    if (figureCount) {
      elements.push(...renderFigureGrid(step.figures, ctx, {
        variant: 'step',
        sizePreset: figureSizePreset(figureCount, 'step', compact),
      }));
    }
  }
  elements.push(makeSpacer(compact ? 25 : 45));
  return elements;
}

function renderFigureBlock(block, ctx) {
  const img = loadImage(block.figure, ctx.images, ctx.imagesDir);
  if (!img) {
    return [makeTextParagraph(`[Image: ${block.figure}]`, {
      italics: true,
      color: ACTIVE_THEME.light,
      alignment: AlignmentType.CENTER,
      size: DOCX_PROFILE.text.smallSize,
    })];
  }

  // Honor block.max_height = "72mm" etc. Default to DOCX_PROFILE.images.figure.
  let maxW = IMAGES.figure.width;
  let maxH = IMAGES.figure.height;
  if (block.max_height) {
    const m = String(block.max_height).match(/^([\d.]+)(mm|pt|in)?$/);
    if (m) {
      const value = parseFloat(m[1]);
      const unit = m[2] || 'mm';
      // docx-js inline ImageRun uses pixels (96 dpi). 1mm = 3.78 px.
      const pxPerUnit = unit === 'mm' ? 3.78 : unit === 'pt' ? 1.333 : 96;
      maxH = Math.round(value * pxPerUnit);
      // Allow image to expand wider too -- target is ~60mm for structure pages.
      maxW = Math.max(maxW, Math.round(value * pxPerUnit * 1.4));
    }
  }

  const elements = [new Paragraph({
    spacing: { after: block.caption ? 24 : 55 },
    alignment: AlignmentType.CENTER,
    children: [makeImageRun(img, maxW, maxH, block.figure)],
  })];
  if (block.caption) {
    elements.push(makeTextParagraph(resolveVars(readTextValue(block.caption), ctx.vars), {
      after: 55,
      italics: true,
      color: ACTIVE_THEME.light,
      alignment: AlignmentType.CENTER,
      size: DOCX_PROFILE.text.smallSize,
    }));
  }
  return elements;
}

function renderFigureRow(block, ctx) {
  const refs = [...(block.figures || []), ...(block.items || [])];
  return [...renderFigureGrid(refs, ctx, { variant: 'row' }), makeSpacer(45)];
}

function renderSplitPanel(block, ctx) {
  const compact = isCompactLayout(block);
  const leftWidth = Math.round(CONTENT_W * (compact ? 0.55 : 0.58));
  const rightWidth = CONTENT_W - leftWidth;
  const leftChildren = [];
  for (const child of block.body_blocks || []) {
    leftChildren.push(...renderBlock({ ...child, page_class: child.page_class || block.page_class || '' }, ctx));
  }
  const rightChildren = renderStackedFigures(block.figures || [], ctx, {
    sizePreset: compact ? DOCX_PROFILE.images.rowDouble : DOCX_PROFILE.images.splitPanel,
  });
  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [leftWidth, rightWidth],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows: [new TableRow({
      children: [
        makeCell(leftChildren, {
          width: leftWidth,
          borders: NO_BORDERS,
          margins: { top: 0, bottom: 0, left: 0, right: compact ? 80 : 120 },
        }),
        makeCell(rightChildren, {
          width: rightWidth,
          borders: NO_BORDERS,
          margins: { top: 20, bottom: 20, left: compact ? 40 : 60, right: 0 },
        }),
      ],
    })],
  }), makeSpacer(compact ? 35 : 60)];
}

function renderTableRef(block, ctx) {
  if (Array.isArray(block.rows)) {
    return [renderCustomTable(block, ctx), makeSpacer(45)];
  }
  switch (block.table) {
    case 'specs': return [renderSpecsTable(ctx, block), makeSpacer(45)];
    case 'parts': return [renderPartsTable(ctx, block), makeSpacer(45)];
    case 'buttons': return [renderButtonsTable(ctx, block), makeSpacer(45)];
    case 'brand_info': return [renderBrandInfoTable(ctx, block), makeSpacer(45)];
    case 'manufacturer_info': return [renderManufacturerTable(ctx, block), makeSpacer(45)];
    default: return [makeTextParagraph(`[Table: ${block.table}]`, { italics: true, color: ACTIVE_THEME.light })];
  }
}

// W27 row heights: normal=215 DXA, compact=225 DXA, warranty-card=242 DXA.
// We disable explicit row heights — letting cells auto-grow gives better
// LO/Word page break behavior and matches target tighter in most pages.
function tableRowHeight(compact) {
  return undefined;
}

function renderCustomTable(block, ctx) {
  const headers = block.headers || [];
  const rows = block.rows || [];
  const compact = isCompactTable(block);

  const colCount = headers.length || (rows[0] ? rows[0].length : 2);
  const colWidths = headers.map((h) => {
    if (typeof h === 'object' && h.width) {
      const pct = parseInt(h.width, 10) / 100;
      return Math.round(CONTENT_W * pct);
    }
    return Math.round(CONTENT_W / colCount);
  });
  if (colWidths.length === 0) {
    for (let i = 0; i < colCount; i++) colWidths.push(Math.round(CONTENT_W / colCount));
  }

  const tableRows = [];

  if (headers.length) {
    tableRows.push(new TableRow({
      height: tableRowHeight(compact),
      children: headers.map((h, i) => {
        const text = typeof h === 'string' ? h : h.text || '';
        return makeHeaderCell(text, { width: colWidths[i], compact });
      }),
    }));
  }

  for (let ri = 0; ri < rows.length; ri++) {
    const row = rows[ri];
    const shading = zebraShading(ri);
    const cells = [];
    for (let i = 0; i < row.length; i++) {
      const cell = typeof row[i] === 'string' ? { text: row[i] } : row[i];
      if (cell === null) continue;
      const rs = cell.rowspan ? parseInt(cell.rowspan, 10) : undefined;
      const cs = cell.colspan ? parseInt(cell.colspan, 10) : undefined;
      cells.push(makeTextCell(
        resolveVars(cell.text || '', ctx.vars),
        {
          width: colWidths[i],
          rowSpan: rs,
          columnSpan: cs,
          compact,
          shading,
          size: compact ? SIZES.tableCompactSize : SIZES.tableBodySize,
        }
      ));
    }
    if (cells.length) tableRows.push(new TableRow({ height: tableRowHeight(compact), children: cells }));
  }

  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colWidths,
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows: tableRows,
  });
}

function renderSpecsTable(ctx, block = {}) {
  const specsRows = ctx.specs.rows;
  const compact = isCompactTable(block);
  const colWidths = [Math.round(CONTENT_W * 0.5), Math.round(CONTENT_W * 0.5)];
  const tableRows = [
    new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeHeaderCell(ctx.labels.specs_col1 || 'Parameter', { width: colWidths[0], compact }),
        makeHeaderCell(ctx.labels.specs_col2 || 'Specification', { width: colWidths[1], compact }),
      ],
    }),
  ];
  for (let ri = 0; ri < specsRows.length; ri++) {
    const r = specsRows[ri];
    const shading = zebraShading(ri);
    tableRows.push(new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeTextCell(r.label, { width: colWidths[0], compact, size: compact ? SIZES.tableCompactSize : SIZES.tableBodySize, shading }),
        makeTextCell(r.value, { width: colWidths[1], compact, size: compact ? SIZES.tableCompactSize : SIZES.tableBodySize, shading }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: colWidths, layout: TableLayoutType.FIXED, borders: NO_BORDERS, rows: tableRows });
}

function renderPartsTable(ctx, block = {}) {
  const parts = ctx.config.parts;
  const compact = isCompactTable(block);
  const half = Math.ceil(parts.length / 2);
  const cw = [Math.round(CONTENT_W * 0.12), Math.round(CONTENT_W * 0.38), Math.round(CONTENT_W * 0.12), Math.round(CONTENT_W * 0.38)];
  const tableRows = [
    new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeHeaderCell(ctx.labels.parts_col_no || 'No.', { width: cw[0], compact }),
        makeHeaderCell(ctx.labels.parts_col_name || 'Part', { width: cw[1], compact }),
        makeHeaderCell(ctx.labels.parts_col_no || 'No.', { width: cw[2], compact }),
        makeHeaderCell(ctx.labels.parts_col_name || 'Part', { width: cw[3], compact }),
      ],
    }),
  ];
  for (let i = 0; i < half; i++) {
    const left = parts[i];
    const right = parts[i + half];
    const shading = zebraShading(i);
    tableRows.push(new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeTextCell(String(left.id), { width: cw[0], compact, shading }),
        makeTextCell(left.name, { width: cw[1], compact, shading }),
        makeTextCell(right ? String(right.id) : '', { width: cw[2], compact, shading }),
        makeTextCell(right ? right.name : '', { width: cw[3], compact, shading }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, borders: NO_BORDERS, rows: tableRows });
}

function renderButtonsTable(ctx, block = {}) {
  const buttons = ctx.config.buttons;
  const compact = isCompactTable(block);
  const cw = [Math.round(CONTENT_W * 0.45), Math.round(CONTENT_W * 0.55)];
  const tableRows = [
    new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeHeaderCell(ctx.labels.buttons_col1 || 'Button', { width: cw[0], compact }),
        makeHeaderCell(ctx.labels.buttons_col2 || 'Description', { width: cw[1], compact }),
      ],
    }),
  ];
  for (let bi = 0; bi < buttons.length; bi++) {
    const b = buttons[bi];
    const shading = zebraShading(bi);
    tableRows.push(new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeTextCell(`${b.id}. [btn:${b.key}] ${b.name}`, { width: cw[0], compact, shading }),
        makeTextCell(b.desc, { width: cw[1], compact, shading }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, borders: NO_BORDERS, rows: tableRows });
}

function localizedInfoHeaders(ctx) {
  if ((ctx.lang || '').startsWith('zh')) return ['项目', '信息'];
  return ['Item', 'Information'];
}

function renderInfoTable(rows, compact = false, headers = null, warranty = false) {
  const cw = [Math.round(CONTENT_W * 0.3), Math.round(CONTENT_W * 0.7)];
  const tableRows = [];
  const cellExtra = { compact, warranty };
  if (headers) {
    tableRows.push(new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeHeaderCell(headers[0], { width: cw[0], ...cellExtra }),
        makeHeaderCell(headers[1], { width: cw[1], ...cellExtra }),
      ],
    }));
  }
  tableRows.push(...rows.map(([label, value], ri) => {
    const shading = zebraShading(ri);
    return new TableRow({
      height: tableRowHeight(compact),
      children: [
        makeTextCell(label, { width: cw[0], ...cellExtra, bold: true, shading }),
        makeTextCell(value, { width: cw[1], ...cellExtra, shading }),
      ],
    });
  }));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: cw,
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows: tableRows,
  });
}

function renderBrandInfoTable(ctx, block = {}) {
  const brand = ctx.brand;
  const isChinese = (ctx.lang || '').startsWith('zh');
  const headers = [
    isChinese ? '项目' : 'Field',
    isChinese ? '信息' : 'Information',
  ];
  return renderInfoTable([
    [ctx.labels.brand_label || 'Brand', brand.name],
    [ctx.labels.address_label || 'Address', brand.address],
    [ctx.labels.website_label || 'Website', brand.website],
    [ctx.labels.email_label || 'Email', brand.support_email],
  ], isCompactTable(block), headers, isWarrantyTable(block));
}

function renderManufacturerTable(ctx, block = {}) {
  const mfr = ctx.mfr;
  const isChinese = (ctx.lang || '').startsWith('zh');
  const headers = [
    isChinese ? '项目' : 'Field',
    isChinese ? '信息' : 'Information',
  ];
  return renderInfoTable([
    [ctx.labels.manufacturer_label || 'Manufacturer', mfr.name_secondary && mfr.name_secondary !== mfr.name_primary ? `${mfr.name_primary}\n${mfr.name_secondary}` : mfr.name_primary],
    [ctx.labels.address_label || 'Address', mfr.address],
    [ctx.labels.website_label || 'Website', mfr.website],
  ], isCompactTable(block), headers, isWarrantyTable(block));
}

function renderQaList(block, ctx) {
  const elements = [];
  for (const item of block.items || []) {
    elements.push(makeTextParagraph(resolveVars(readTextValue(item.question), ctx.vars), {
      before: 80,
      after: 40,
      bold: true,
      size: DOCX_PROFILE.text.subtitleSize - 2,
    }));
    for (const answer of item.answers || []) {
      const answerText = resolveVars(readTextValue(answer), ctx.vars);
      elements.push(new Paragraph({
        spacing: { before: 0, after: 40, line: 240 },
        indent: { left: 180, hanging: 180 },
        children: [
          new TextRun({
            text: '•   ',
            font: TITLE_FONT,
            bold: true,
            size: 14, // 7pt bullet to match W27 visually-large red dot
            color: ACTIVE_THEME.accent,
          }),
          ...parseTextTokens(answerText, { size: SIZES.bodySize, font: FONT }),
        ],
      }));
    }
  }
  return elements;
}

function renderContactBlock(block, ctx) {
  const text = resolveVars(readTextValue(block.text || ''), ctx.vars);
  const email = block.email ? resolveVars(readTextValue(block.email), ctx.vars) : '';
  return [new Paragraph({
    spacing: { after: 120 },
    children: [
      ...parseTextTokens(text),
      ...(email ? [new TextRun({ text: email, bold: true, font: FONT })] : []),
    ],
  })];
}

function renderWarrantyCard(block, ctx) {
  const fields = block.fields || [];
  const cw = [Math.round(CONTENT_W * 0.35), Math.round(CONTENT_W * 0.65)];
  const firstRowBorders = {
    ...horizontalBorders(),
    top: { style: BorderStyle.SINGLE, size: 8, color: ACTIVE_THEME.accent },
  };
  const rows = fields.map((field, fi) => {
    const isFirst = fi === 0;
    const shading = zebraShading(fi);
    return new TableRow({
      children: [
        makeTextCell(resolveVars(readTextValue(field), ctx.vars), {
          width: cw[0],
          bold: true,
          shading,
          borders: isFirst ? firstRowBorders : undefined,
        }),
        makeTextCell('', {
          width: cw[1],
          shading,
          borders: isFirst ? firstRowBorders : undefined,
        }),
      ],
    });
  });
  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: cw,
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows,
  })];
}

// ---------------------------------------------------------------------------
// Master block dispatcher
// ---------------------------------------------------------------------------
function renderBlock(block, ctx) {
  switch (block.type) {
    case 'paragraph': return renderParagraphBlock(block, ctx);
    case 'sub_title': return renderSubTitle(block, ctx);
    case 'bullet_list': return renderBulletList(block, ctx);
    case 'warning_box': return renderAlertBox(block, ctx, 'warning_box');
    case 'caution_box': return renderAlertBox(block, ctx, 'caution_box');
    case 'notice_box': return renderAlertBox(block, ctx, 'notice_box');
    case 'step_flow': return renderStepFlow(block, ctx);
    case 'figure': return renderFigureBlock(block, ctx);
    case 'figure_row': return renderFigureRow(block, ctx);
    case 'split_panel': return renderSplitPanel(block, ctx);
    case 'table_ref': return renderTableRef(block, ctx);
    case 'qa_list': return renderQaList(block, ctx);
    case 'contact_block': return renderContactBlock(block, ctx);
    case 'warranty_card': return renderWarrantyCard(block, ctx);
    default:
      return [new Paragraph({ children: [new TextRun({ text: `[Unknown block: ${block.type}]`, italics: true, font: FONT })] })];
  }
}

// ---------------------------------------------------------------------------
// Document builder
// ---------------------------------------------------------------------------
function sectionDivider() {
  return new Paragraph({
    spacing: { before: 0, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACTIVE_THEME.accent } },
    children: [],
  });
}

function renderChapterHeading(chapter) {
  // W27: left BLACK bar size=18 + space=4, chap num red 13.5pt bold, title 11pt bold.
  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 0, after: 60, line: 320 },
      border: { left: { style: BorderStyle.SINGLE, size: 6, color: ACTIVE_THEME.chapterBar } },
      indent: { left: 160 },
      keepNext: true,
      children: [
        new TextRun({
          text: `${chapter.chapter_no} `,
          font: TITLE_FONT,
          bold: true,
          size: SIZES.chapterNumberSize,
          color: ACTIVE_THEME.chapterNumber,
        }),
        new TextRun({
          text: chapter.title,
          font: TITLE_FONT,
          bold: true,
          size: SIZES.chapterTitleSize,
          color: ACTIVE_THEME.chapterTitle,
        }),
      ],
    }),
  ];
}

function shouldPageBreakBeforePage(page, chapter, pageIndex) {
  if (pageIndex === 0) return false;
  if (page.force_page_break) return true;
  return true;
}

function renderPageSectionTitle(page, chapter, pageIndex) {
  if (page.hide_section_title) return [];
  const title = page.section_title || chapter.title;
  const pageBreakBefore = shouldPageBreakBeforePage(page, chapter, pageIndex);
  if (!title || title === chapter.title) {
    return pageBreakBefore ? [new Paragraph({ pageBreakBefore: true, children: [] })] : [];
  }
  if (pageBreakBefore) {
    return [new Paragraph({
      pageBreakBefore,
      spacing: { before: 0, after: 60, line: 320 },
      border: { left: { style: BorderStyle.SINGLE, size: 6, color: ACTIVE_THEME.chapterBar } },
      indent: { left: 160 },
      keepNext: true,
      children: [
        new TextRun({
          text: `${chapter.chapter_no} `,
          font: TITLE_FONT,
          bold: true,
          size: SIZES.chapterNumberSize,
          color: ACTIVE_THEME.chapterNumber,
        }),
        new TextRun({
          text: title,
          font: TITLE_FONT,
          bold: true,
          size: SIZES.chapterTitleSize,
          color: ACTIVE_THEME.chapterTitle,
        }),
      ],
    })];
  }
  return [makeTextParagraph(title, {
    before: 40,
    after: 90,
    bold: true,
    size: DOCX_PROFILE.text.sectionTitleSize,
    keepNext: true,
    font: TITLE_FONT,
    color: ACTIVE_THEME.sectionTitle,
    pageBreakBefore,
  })];
}

function buildCoverBlock(ctx) {
  const coverImage = ctx.images['cover.main']
    ? loadImage('cover.main', ctx.images, ctx.imagesDir)
    : (ctx.config.product.cover_image
      ? loadImage({ file: ctx.config.product.cover_image, alt: ctx.localized.product_name }, {}, ctx.imagesDir)
      : null);

  const children = [];

  // 1. Brand name as inline "━━ 威富可" (small, top-left like PDF)
  // PDF measurement: red short dash + small bold black "威富可" ~7.5pt, left-aligned, very subtle
  children.push(new Paragraph({
    spacing: { before: 240, after: 0 },
    indent: { right: CONTENT_W - 300 },
    border: { top: { style: BorderStyle.SINGLE, size: 12, color: ACTIVE_THEME.accent } },
    children: [],
  }));
  children.push(new Paragraph({
    spacing: { before: 0, after: 360 },
    indent: { left: 380 },
    children: [
      new TextRun({
        text: '━━━  ',
        font: FONT,
        bold: true,
        size: 1,
        color: 'FFFFFF',
      }),
      new TextRun({
        text: ctx.brand.display_name,
        font: TITLE_FONT,
        bold: true,
        size: DOCX_PROFILE.text.coverBrandSize,
        color: ACTIVE_THEME.primary,
        characterSpacing: 60,
      }),
    ],
  }));

  // 2. Product image (small, left-aligned, like PDF center-left placement)
  if (coverImage) {
    children.push(new Paragraph({
      spacing: { before: 2650, after: 200 },
      alignment: AlignmentType.LEFT,
      children: [makeImageRun(coverImage, DOCX_PROFILE.images.cover.width, DOCX_PROFILE.images.cover.height, 'cover')],
    }));
  }

  // 3. Model + Product name + Document type (bottom area)
  children.push(new Paragraph({
    spacing: { before: 510, after: 18 },
    children: [new TextRun({
      text: `MODEL  ${ctx.model}`,
      font: MONO_FONT,
      size: DOCX_PROFILE.text.coverModelSize,
      color: ACTIVE_THEME.coverModel,
      characterSpacing: 60,
    })],
  }));
  children.push(new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [new TextRun({
      text: ctx.localized.product_name,
      font: TITLE_FONT,
      bold: true,
      size: DOCX_PROFILE.text.coverProductSize,
      color: ACTIVE_THEME.coverTitle,
    })],
  }));
  children.push(new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [new TextRun({
      text: ctx.localized.document_title,
      font: FONT,
      size: DOCX_PROFILE.text.coverTypeSize,
      color: ACTIVE_THEME.coverType,
    })],
  }));
  // Accent divider
  children.push(new Paragraph({
    spacing: { before: 20, after: 2750 },
    indent: { right: CONTENT_W - 420 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACTIVE_THEME.accent } },
    children: [],
  }));

  // 4. Disclaimer at bottom \u2014 PDF has 2-line wrap with subtle black hairline above
  const disclaimerLine1 = ctx.lang && ctx.lang.startsWith('zh')
    ? '\u4F7F\u7528\u4EA7\u54C1\u524D\u8BF7\u4ED4\u7EC6\u9605\u8BFB\u672C\u8BF4\u660E\u4E66\uFF0C\u5E76\u59A5\u5584\u4FDD\u7BA1\u3002'
    : 'Please read this manual carefully before use and keep it for future reference.';
  const disclaimerLine2 = ctx.lang && ctx.lang.startsWith('zh')
    ? '\u8BF4\u660E\u4E66\u4E2D\u7684\u4EA7\u54C1\u3001\u914D\u4EF6\u7B49\u63D2\u56FE\u5747\u4E3A\u793A\u610F\u56FE\uFF0C\u4EC5\u4F9B\u53C2\u8003\u3002\u7531\u4E8E\u4EA7\u54C1\u7684\u66F4\u65B0\u4E0E\u5347\u7EA7\uFF0C\u4EA7\u54C1\u5B9E\u7269\u4E0E\u793A\u610F\u56FE\u53EF\u80FD\u7565\u6709\u5DEE\u5F02\uFF0C\u8BF7\u4EE5\u5B9E\u7269\u4E3A\u51C6\u3002'
    : '';
  // Thin black hairline above disclaimer (PDF has this)
  children.push(new Paragraph({
    spacing: { before: 0, after: 60 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: ACTIVE_THEME.primary } },
    children: [],
  }));
  children.push(new Paragraph({
    spacing: { before: 0, after: 30, line: 200 },
    children: [new TextRun({
      text: disclaimerLine1,
      font: FONT,
      size: DOCX_PROFILE.text.smallSize,
      color: ACTIVE_THEME.muted,
    })],
  }));
  if (disclaimerLine2) {
    children.push(new Paragraph({
      spacing: { before: 0, after: 0, line: 200 },
      children: [new TextRun({
        text: disclaimerLine2,
        font: FONT,
        size: DOCX_PROFILE.text.smallSize,
        color: ACTIVE_THEME.muted,
      })],
    }));
  }

  return children;
}

function buildHeader(ctx, chapter = null) {
  // W27 header: thick BLACK rule (sz=18) on top, brand bold 6.75pt left, mono 5.4pt gray right.
  const rightText = chapter?.header_ref || `${ctx.model}  \u2014  ${ctx.localized.document_title}`;
  return new Header({
    children: [new Paragraph({
      spacing: { after: 60, line: 220 },
      border: { top: { style: BorderStyle.SINGLE, size: 18, color: ACTIVE_THEME.primary } },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
      children: [
        new TextRun({
          text: ctx.brand.display_name,
          font: FONT,
          size: 13, // 6.75pt
          bold: true,
          color: ACTIVE_THEME.primary,
        }),
        new TextRun({
          text: `\t${rightText}`,
          font: MONO_FONT,
          size: SIZES.smallSize,
          color: ACTIVE_THEME.headerText,
        }),
      ],
    })],
  });
}

function buildFooter(ctx) {
  // W27 footer: two-cell table with thin top rule. Left = "<brand> <model> <doc_title>",
  // right = page number (mono gray). Same on every body page.
  const isChinese = (ctx.lang || '').startsWith('zh');
  const leftText = isChinese
    ? `${ctx.brand.display_name} ${ctx.model} ${ctx.localized.document_title}`
    : `${ctx.brand.display_name} ${ctx.model} ${ctx.localized.document_title}`;
  const colLeft = Math.round(CONTENT_W * 0.62);
  const colRight = CONTENT_W - colLeft;
  const footerCellBorders = {
    top: { style: BorderStyle.SINGLE, size: 4, color: 'EEEEEE' },
    left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  };
  return new Footer({
    children: [
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [colLeft, colRight],
        layout: TableLayoutType.FIXED,
        borders: NO_BORDERS,
        rows: [new TableRow({
          children: [
            makeCell([
              new Paragraph({
                spacing: { before: 0, after: 0, line: 200 },
                children: [
                  new TextRun({
                    text: leftText,
                    font: FONT,
                    size: SIZES.smallSize,
                    color: ACTIVE_THEME.footerText,
                  }),
                ],
              }),
            ], {
              width: colLeft,
              borders: footerCellBorders,
              margins: { top: 35, bottom: 0, left: 0, right: 0 },
            }),
            makeCell([
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                spacing: { before: 0, after: 0, line: 200 },
                children: [
                  new TextRun({
                    children: [PageNumber.CURRENT],
                    font: MONO_FONT,
                    size: SIZES.smallSize,
                    color: ACTIVE_THEME.footerText,
                  }),
                ],
              }),
            ], {
              width: colRight,
              borders: footerCellBorders,
              margins: { top: 35, bottom: 0, left: 0, right: 0 },
            }),
          ],
        })],
      }),
    ],
  });
}

function buildStaticTocChildren(chapters, tocTitle) {
  const children = [
    new Paragraph({
      spacing: { before: 0, after: 260 },
      children: [new TextRun({
        text: tocTitle,
        font: TITLE_FONT,
        bold: true,
        size: DOCX_PROFILE.text.tocTitleSize,
        color: ACTIVE_THEME.tocTitle,
      })],
    }),
  ];

  let pageNo = 3;
  const numberWidth = 260;
  const pageWidth = 320;
  const titleWidth = CONTENT_W - numberWidth - pageWidth;
  const rowBorders = {
    top: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    bottom: { style: BorderStyle.SINGLE, size: 3, color: 'E6E6E6' },
    left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  };
  const rows = [];
  for (const chapter of chapters) {
    rows.push(new TableRow({
      children: [
        makeCell([new Paragraph({
          spacing: { before: 0, after: 0, line: 240 },
          children: [new TextRun({
            text: chapter.chapter_no,
            font: MONO_FONT,
            bold: true,
            size: DOCX_PROFILE.text.bodySize,
            color: ACTIVE_THEME.accent,
          })],
        })], {
          width: numberWidth,
          borders: rowBorders,
          margins: { top: 42, bottom: 42, left: 0, right: 0 },
        }),
        makeCell([new Paragraph({
          spacing: { before: 0, after: 0, line: 240 },
          children: [new TextRun({
            text: chapter.toc_title || chapter.title,
            font: TITLE_FONT,
            bold: true,
            size: DOCX_PROFILE.text.bodySize + 1,
            color: ACTIVE_THEME.tocTitle,
          })],
        })], {
          width: titleWidth,
          borders: rowBorders,
          margins: { top: 42, bottom: 42, left: 0, right: 0 },
        }),
        makeCell([new Paragraph({
          alignment: AlignmentType.RIGHT,
          spacing: { before: 0, after: 0, line: 240 },
          children: [new TextRun({
            text: String(pageNo),
            font: MONO_FONT,
            size: DOCX_PROFILE.text.smallSize,
            color: ACTIVE_THEME.muted,
          })],
        })], {
          width: pageWidth,
          borders: rowBorders,
          margins: { top: 42, bottom: 42, left: 0, right: 0 },
        }),
      ],
    }));
    pageNo += Math.max(1, (chapter.pages || []).length);
  }

  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [numberWidth, titleWidth, pageWidth],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows,
  }));

  return children;
}

async function buildDocx(regionCode, brandOverride) {
  const region = config.regions[regionCode];
  if (!region) {
    throw new Error(
      `Unknown region: ${regionCode}. Available: ${Object.keys(config.regions).join(', ')}`
    );
  }

  const activeBrand = brandOverride || config.product.active_brand;
  const activeMarket = region.market;
  const lang = region.lang;
  const model = config.product.model;
  const localeCatalog = loadLocaleCatalog(productDir, lang);
  const localizedRuntime = buildLocalizedRuntimeData(config, localeCatalog, activeBrand, activeMarket, lang);
  const runtimeConfig = localizedRuntime.runtimeConfig;
  const theme = resolveBrandTheme(activeBrand);
  applyDocxTheme(theme.docx || {});

  console.log(`DOCX: ${model} | region=${regionCode} | brand=${activeBrand} | lang=${lang}`);

  const baseImagesManifest = loadImagesManifest(productDir);
  const imagesDir = path.join(productDir, 'images');
  const cacheNamespace = `${path.basename(productDir)}-${regionCode}-${activeBrand}`;
  const preparedImages = await prepareImagesManifestForDocx(baseImagesManifest, imagesDir, cacheNamespace);
  const imagesManifest = preparedImages.manifest;
  const documentSchema = loadContentDocument(productDir, lang);
  const chapters = documentSchema.chapters.filter((ch) => ch.enabled !== false);

  const vars = {
    'brand.display_name': localizedRuntime.brand.display_name,
    'brand.name': localizedRuntime.brand.name,
    'brand.address': localizedRuntime.brand.address,
    'brand.website': localizedRuntime.brand.website,
    'brand.support_email': localizedRuntime.brand.support_email,
    'product.model': model,
    'product.name': localizedRuntime.localized.product_name,
    'product.name_cn': localizedRuntime.localized.product_name,
    'product.name_en': localizedRuntime.localized.product_name,
    'product.name_de': localizedRuntime.localized.product_name,
    'product.name_it': localizedRuntime.localized.product_name,
    'warranty.years': String(config.warranty.years),
    'localized.product_name': localizedRuntime.localized.product_name,
    'localized.document_title': localizedRuntime.localized.document_title,
    'localized.document_title_upper': localizedRuntime.localized.document_title_upper,
  };

  const numberingConfigs = [
    {
      reference: 'bullets',
      // W27 bullet indent: 3.2mm left + 3.2mm hanging (~181 DXA).
      // Bullet glyph: U+2022 in red Arial Black size 11 half-pt (~5.5pt).
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '\u2022',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 220, hanging: 200 } },
          run: { color: ACTIVE_THEME.accent, bold: true, size: 11, font: TITLE_FONT },
        },
      }, {
        level: 1,
        format: LevelFormat.BULLET,
        text: '\u2013',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 420, hanging: 200 } },
        },
      }],
    },
    {
      reference: 'numbers',
      levels: [{
        level: 0,
        format: LevelFormat.DECIMAL,
        text: '%1.',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 280, hanging: 220 } },
          run: { bold: true, color: ACTIVE_THEME.accent },
        },
      }],
    },
  ];

  const ctx = {
    config: runtimeConfig,
    brand: localizedRuntime.brand,
    specs: localizedRuntime.specs,
    mfr: localizedRuntime.manufacturer,
    labels: localizedRuntime.labels,
    localized: localizedRuntime.localized,
    lang,
    model,
    vars,
    images: imagesManifest,
    imagesDir,
  };

  const coverChildren = buildCoverBlock(ctx);
  const tocTitle = langSuffix(lang) === 'cn' ? '目录' : 'Contents';
  const tocChildren = buildStaticTocChildren(chapters, tocTitle);

  const sections = [
    {
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN_Y, right: MARGIN_X, bottom: MARGIN_Y, left: MARGIN_X },
        },
      },
      children: coverChildren,
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN_Y, right: MARGIN_X, bottom: MARGIN_Y, left: MARGIN_X },
        },
      },
      headers: { default: buildHeader(ctx) },
      footers: { default: buildFooter(ctx) },
      children: tocChildren,
    },
  ];

  for (const chapter of chapters) {
    const chapterChildren = [...renderChapterHeading(chapter)];
    for (let pageIndex = 0; pageIndex < (chapter.pages || []).length; pageIndex += 1) {
      const page = chapter.pages[pageIndex];
      chapterChildren.push(...renderPageSectionTitle(page, chapter, pageIndex));
      for (const block of page.blocks || []) {
        chapterChildren.push(...renderBlock({
          ...block,
          page_class: page.page_class || '',
          page_id: page.page_id || '',
          chapter_id: chapter.chapter_id || '',
        }, ctx));
      }
    }
    sections.push({
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN_Y, right: MARGIN_X, bottom: MARGIN_Y, left: MARGIN_X },
        },
      },
      headers: { default: buildHeader(ctx, chapter) },
      footers: { default: buildFooter(ctx) },
      children: chapterChildren,
    });
  }

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: FONT, size: DOCX_PROFILE.text.bodySize },
        },
      },
    },
    numbering: { config: numberingConfigs },
    sections,
  });

  return {
    doc,
    regionCode,
    activeBrand,
    market: activeMarket,
    locale: lang,
    model,
    profile: DOCX_PROFILE,
    templateProfile: DOCX_PROFILE.templateId,
    theme: ACTIVE_THEME,
    assetStats: preparedImages.stats,
  };
}

async function writeBufferWithRetry(outPath, buffer, retries = 5, delayMs = 250) {
  let lastError = null;
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      fs.writeFileSync(outPath, buffer);
      return outPath;
    } catch (error) {
      lastError = error;
      if (error.code !== 'EBUSY' || attempt === retries - 1) {
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  if (lastError && lastError.code === 'EBUSY') {
    const stagedPath = outPath.replace(/\.docx$/i, '.__staged.docx');
    fs.writeFileSync(stagedPath, buffer);
    console.warn(`  ! target locked, wrote staged copy: ${path.basename(stagedPath)}`);
    return stagedPath;
  }

  throw lastError;
}

async function writeDocx(regionCode, brandOverride) {
  const { doc, activeBrand, market, model } = await buildDocx(regionCode, brandOverride);
  const outName = `${model.toLowerCase()}-${activeBrand}-${market}-${regionCode}.docx`;
  const outPath = path.join(outputDir, outName);
  const buffer = await Packer.toBuffer(doc);
  const actualPath = await writeBufferWithRetry(outPath, buffer);
  if (writeBaseTemplateCn && regionCode === 'cn') {
    fs.mkdirSync(path.dirname(baseTemplatePath), { recursive: true });
    fs.copyFileSync(actualPath, baseTemplatePath);
  }
  console.log(`  -> ${path.basename(actualPath)} (${(buffer.length / 1024).toFixed(1)} KB)`);
  return { outName: path.basename(actualPath), outPath: actualPath, activeBrand, market, model, regionCode };
}

async function main() {
  fs.mkdirSync(outputDir, { recursive: true });

  if (buildAll) {
    const allRegions = Object.keys(config.regions);
    const allBrands = Object.keys(config.brands);
    let count = 0;

    for (const r of allRegions) {
      for (const b of allBrands) {
        await writeDocx(r, b);
        count++;
      }
    }
    console.log(`\nDone: ${count} DOCX files generated.`);
  } else {
    await writeDocx(regionKey, brandKey);
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = {
  DOCX_PROFILE,
  buildDocx,
  fitImageSize,
  makeImageRun,
  getImageDimensions,
  writeBufferWithRetry,
  writeDocx,
};
