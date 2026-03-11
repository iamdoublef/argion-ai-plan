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
  WidthType, ShadingType, PageNumber, TableOfContents,
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

const DOCX_PROFILE = {
  templateId: 'A5_CN_BASE_V1',
  page: {
    width: PAGE_W,
    height: PAGE_H,
    marginX: MARGIN_X,
    marginY: MARGIN_Y,
  },
  images: {
    cover: { width: 360, height: 255 },
    figure: { width: 340, height: 230 },
    splitPanel: { width: 180, height: 150 },
    stepSingle: { width: 300, height: 190 },
    stepDouble: { width: 185, height: 145 },
    stepTriple: { width: 125, height: 110 },
    stepSingleCompact: { width: 250, height: 155 },
    stepDoubleCompact: { width: 160, height: 120 },
    stepTripleCompact: { width: 110, height: 92 },
    rowSingle: { width: 260, height: 170 },
    rowDouble: { width: 170, height: 125 },
    rowTriple: { width: 120, height: 100 },
    inlineIcon: { width: 28, height: 28 },
  },
  table: {
    bodySize: 19,
    compactSize: 17,
    headerSize: 18,
  },
  text: {
    bodySize: 21,
    subtitleSize: 24,
    sectionTitleSize: 26,
    chapterNumberSize: 38,
    chapterTitleSize: 36,
    coverBrandSize: 28,
    coverTypeSize: 19,
    coverProductSize: 34,
    coverModelSize: 18,
    coverCompanySize: 16,
    tocTitleSize: 30,
    smallSize: 16,
  },
};

// ---------------------------------------------------------------------------
// Styling constants
// ---------------------------------------------------------------------------
const DEFAULT_DOCX_THEME = {
  primary: '1A1A1A',
  accent: 'E63946',
  light: '666666',
  muted: '9A9A9A',
  font: 'Arial Narrow',
  latinFont: 'Arial Narrow',
  cjkFont: '宋体',
  titleLatinFont: 'Arial Black',
  titleCjkFont: '黑体',
  coverDivider: 'E63946',
  coverModel: 'E63946',
  coverType: '666666',
  coverTitle: '1A1A1A',
  coverCompany: '8A8A8A',
  chapterBar: '000000',
  chapterNumber: 'E63946',
  chapterTitle: '1A1A1A',
  chapterHeaderRef: '8A8A8A',
  tocTitle: '1A1A1A',
  tocText: '666666',
  sectionTitle: '1A1A1A',
  tableHeaderFill: '1A1A1A',
  tableHeaderText: 'FFFFFF',
  tableLabelFill: 'F4F4F4',
  tableBorder: 'D4D4D4',
  warningFill: 'FFF3D6',
  cautionFill: 'F7D9DD',
  noticeFill: 'DCECF8',
  warningBorder: 'E2C55A',
  cautionBorder: 'D9A7B3',
  noticeBorder: '9FC4DA',
  boxBorder: 'D4D4D4',
  headerBorder: 'D9D9D9',
  headerText: '7A7A7A',
  footerText: '8A8A8A',
};

let ACTIVE_THEME = { ...DEFAULT_DOCX_THEME };
let FONT = buildFontBundle(DEFAULT_DOCX_THEME.latinFont, DEFAULT_DOCX_THEME.cjkFont);
let TITLE_FONT = buildFontBundle(DEFAULT_DOCX_THEME.titleLatinFont, DEFAULT_DOCX_THEME.titleCjkFont);

function buildFontBundle(latin, cjk) {
  return {
    ascii: latin,
    hAnsi: latin,
    cs: latin,
    eastAsia: cjk,
  };
}

function applyDocxTheme(docxTheme = {}) {
  ACTIVE_THEME = { ...DEFAULT_DOCX_THEME, ...docxTheme };
  FONT = buildFontBundle(ACTIVE_THEME.latinFont, ACTIVE_THEME.cjkFont);
  TITLE_FONT = buildFontBundle(ACTIVE_THEME.titleLatinFont, ACTIVE_THEME.titleCjkFont);
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
};
function boxBorders(color = ACTIVE_THEME.boxBorder) {
  return { top: border(color), bottom: border(color), left: border(color), right: border(color) };
}
const CELL_MARGINS = { top: 70, bottom: 70, left: 90, right: 90 };
const CELL_MARGINS_COMPACT = { top: 40, bottom: 40, left: 70, right: 70 };
const DOCX_IMAGE_CACHE_DIR = path.resolve(outputDir, '_docx_raster_cache');

// ---------------------------------------------------------------------------
// Text token parsing: [btn:XXX] and **bold**
// ---------------------------------------------------------------------------
function parseTextTokens(text, base = {}) {
  const runFont = base.font || FONT;
  const { font: _font, ...runBase } = base;
  if (!text) return [new TextRun({ text: '', font: runFont, ...runBase })];
  const runs = [];
  const regex = /(\[btn:([^\]]+)\]|\*\*([^*]+)\*\*)/g;
  let lastIndex = 0;
  let match;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      runs.push(new TextRun({ text: text.slice(lastIndex, match.index), font: runFont, ...runBase }));
    }
    if (match[2]) {
      runs.push(new TextRun({
        text: match[2],
        bold: true,
        font: runFont,
        color: ACTIVE_THEME.accent,
        ...runBase,
      }));
    } else if (match[3]) {
      runs.push(new TextRun({ text: match[3], bold: true, font: runFont, ...runBase }));
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
    spacing: { before, after, line: 320 },
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
    margins: opts.margins || CELL_MARGINS,
    shading: opts.shading,
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    rowSpan: opts.rowSpan,
    columnSpan: opts.columnSpan,
    verticalAlign: opts.verticalAlign || VerticalAlign.TOP,
    children: normalizeCellChildren(children),
  });
}

function makeTextCell(text, opts = {}) {
  return makeCell(makeTextParagraphs(readTextValue(text || ''), {
    after: 0,
    size: opts.size || DOCX_PROFILE.table.bodySize,
    color: opts.color || ACTIVE_THEME.primary,
    bold: opts.bold || false,
    alignment: opts.alignment,
  }), {
    width: opts.width,
    rowSpan: opts.rowSpan,
    columnSpan: opts.columnSpan,
    shading: opts.shading,
    borders: opts.borders || boxBorders(),
    margins: opts.compact ? CELL_MARGINS_COMPACT : (opts.margins || CELL_MARGINS),
    verticalAlign: opts.verticalAlign || VerticalAlign.CENTER,
  });
}

function makeHeaderCell(text, opts = {}) {
  return makeTextCell(text, {
    ...opts,
    shading: { fill: ACTIVE_THEME.tableHeaderFill, type: ShadingType.CLEAR },
    color: ACTIVE_THEME.tableHeaderText,
    bold: true,
    alignment: AlignmentType.CENTER,
    size: DOCX_PROFILE.table.headerSize,
  });
}

function makeBorderlessCell(children, width) {
  return makeCell(children, {
    width,
    borders: NO_BORDERS,
    margins: { top: 0, bottom: 0, left: 0, right: 0 },
  });
}

function isCompactTable(block = {}) {
  const flag = `${block.table_class || ''} ${block.className || ''} ${block.page_class || ''}`.toLowerCase();
  return Boolean(block.compact || flag.includes('compact'));
}

function isCompactLayout(block = {}) {
  const flag = `${block.page_class || ''} ${block.className || ''}`.toLowerCase();
  return Boolean(block.compact || flag.includes('compact'));
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
          after: 40,
          size: DOCX_PROFILE.text.smallSize,
          bold: true,
          alignment: AlignmentType.CENTER,
        }));
      }

      const image = loadImage(item.figure, ctx.images, ctx.imagesDir);
      if (image) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: item.label_after ? 40 : 0 },
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
        after: 30,
        size: DOCX_PROFILE.text.smallSize,
        bold: true,
        alignment: AlignmentType.CENTER,
      }));
    }

    const image = loadImage(item.figure, ctx.images, ctx.imagesDir);
    if (image) {
      elements.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: item.label_after ? 30 : 90 },
        children: [makeImageRun(image, sizePreset.width, sizePreset.height, item.figure)],
      }));
    } else {
      elements.push(makeTextParagraph(`[Image: ${item.figure}]`, {
        after: 90,
        italics: true,
        color: ACTIVE_THEME.light,
        alignment: AlignmentType.CENTER,
        size: DOCX_PROFILE.text.smallSize,
      }));
    }

    if (item.label_after) {
      elements.push(makeTextParagraph(resolveVars(readTextValue(item.label_after), ctx.vars), {
        after: 90,
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
    after: 110,
    size: DOCX_PROFILE.text.bodySize,
  });
}

function renderSubTitle(block, ctx) {
  return [makeTextParagraph(resolveVars(readTextValue(block.text), ctx.vars), {
    before: 120,
    after: 100,
    size: DOCX_PROFILE.text.sectionTitleSize,
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
  return (block.items || []).map((item) => makeTextParagraph(resolveVars(readTextValue(item), ctx.vars), {
    after: 50,
    numbering: { reference: 'bullets', level: 0 },
    size: DOCX_PROFILE.text.bodySize,
  }));
}

function getAlertTheme(kind) {
  if (kind === 'warning_box') return { fill: ACTIVE_THEME.warningFill, border: ACTIVE_THEME.warningBorder };
  if (kind === 'caution_box') return { fill: ACTIVE_THEME.cautionFill, border: ACTIVE_THEME.cautionBorder };
  return { fill: ACTIVE_THEME.noticeFill, border: ACTIVE_THEME.noticeBorder };
}

function renderAlertBox(block, ctx, kind) {
  const theme = getAlertTheme(kind);
  const elements = [];
  if (block.title) {
    elements.push(makeTextParagraph(resolveVars(readTextValue(block.title), ctx.vars), {
      after: 60,
      bold: true,
      size: DOCX_PROFILE.text.subtitleSize - 2,
      font: TITLE_FONT,
      color: ACTIVE_THEME.primary,
    }));
  }
  if (block.icon) {
    const icon = loadImage(block.icon, ctx.images, ctx.imagesDir);
    if (icon) {
      elements.push(new Paragraph({
        spacing: { after: 70 },
        children: [makeImageRun(icon, DOCX_PROFILE.images.inlineIcon.width, DOCX_PROFILE.images.inlineIcon.height, 'icon')],
      }));
    }
  }
  if (block.items) {
    for (const item of block.items) {
      elements.push(makeTextParagraph(resolveVars(readTextValue(item), ctx.vars), {
        after: 50,
        numbering: { reference: 'bullets', level: 0 },
        size: DOCX_PROFILE.text.bodySize,
      }));
    }
  } else if (block.text) {
    elements.push(...makeTextParagraphs(resolveVars(readTextValue(block.text), ctx.vars), {
      after: 60,
    }));
  }

  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows: [new TableRow({
      children: [makeCell(elements, {
        width: CONTENT_W,
        borders: boxBorders(theme.border),
        shading: { fill: theme.fill, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 150, right: 150 },
      })],
    })],
  }), makeSpacer(80)];
}

function renderStepFlow(block, ctx) {
  const startAt = Number(block.start_at || 1);
  const compact = isCompactLayout(block);
  const numberWidth = Math.round(CONTENT_W * (compact ? 0.08 : 0.09));
  const textWidth = CONTENT_W - numberWidth;
  const rows = [];
  for (let i = 0; i < (block.steps || []).length; i++) {
    const step = block.steps[i];
    const figureCount = (step.figures || []).length;
    const body = [
      ...makeTextParagraphs(resolveVars(readTextValue(step.text || step), ctx.vars), {
        after: figureCount ? (compact ? 45 : 70) : 10,
        size: compact ? DOCX_PROFILE.table.compactSize : DOCX_PROFILE.text.bodySize,
      }),
    ];
    if (figureCount) {
      body.push(...renderFigureGrid(step.figures, ctx, {
        variant: 'step',
        sizePreset: figureSizePreset(figureCount, 'step', compact),
      }));
    }
    rows.push(new TableRow({
      cantSplit: true,
      children: [
        makeCell([
          makeTextParagraph(String(startAt + i), {
            after: 0,
            bold: true,
            size: compact ? DOCX_PROFILE.table.headerSize : DOCX_PROFILE.text.subtitleSize,
            color: 'FFFFFF',
            alignment: AlignmentType.CENTER,
          }),
        ], {
          width: numberWidth,
          borders: NO_BORDERS,
          shading: { fill: ACTIVE_THEME.accent, type: ShadingType.CLEAR },
          margins: { top: compact ? 80 : 120, bottom: compact ? 80 : 120, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
        }),
        makeCell(body, {
          width: textWidth,
          borders: boxBorders(ACTIVE_THEME.boxBorder),
          margins: { top: compact ? 80 : 100, bottom: compact ? 80 : 100, left: 120, right: 120 },
        }),
      ],
    }));
  }
  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [numberWidth, textWidth],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDERS,
    rows,
  }), makeSpacer(compact ? 50 : 80)];
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

  const elements = [new Paragraph({
    spacing: { after: block.caption ? 40 : 100 },
    alignment: AlignmentType.CENTER,
    children: [makeImageRun(img, DOCX_PROFILE.images.figure.width, DOCX_PROFILE.images.figure.height, block.figure)],
  })];
  if (block.caption) {
    elements.push(makeTextParagraph(resolveVars(readTextValue(block.caption), ctx.vars), {
      after: 100,
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
  return [...renderFigureGrid(refs, ctx, { variant: 'row' }), makeSpacer(90)];
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
  }), makeSpacer(compact ? 60 : 100)];
}

function renderTableRef(block, ctx) {
  if (Array.isArray(block.rows)) {
    return [renderCustomTable(block, ctx), makeSpacer(90)];
  }
  switch (block.table) {
    case 'specs': return [renderSpecsTable(ctx, block), makeSpacer(90)];
    case 'parts': return [renderPartsTable(ctx, block), makeSpacer(90)];
    case 'buttons': return [renderButtonsTable(ctx, block), makeSpacer(90)];
    case 'brand_info': return [renderBrandInfoTable(ctx, block), makeSpacer(90)];
    case 'manufacturer_info': return [renderManufacturerTable(ctx, block), makeSpacer(90)];
    default: return [makeTextParagraph(`[Table: ${block.table}]`, { italics: true, color: ACTIVE_THEME.light })];
  }
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
      children: headers.map((h, i) => {
        const text = typeof h === 'string' ? h : h.text || '';
        return makeHeaderCell(text, { width: colWidths[i], compact });
      }),
    }));
  }

  for (const row of rows) {
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
          size: compact ? DOCX_PROFILE.table.compactSize : DOCX_PROFILE.table.bodySize,
        }
      ));
    }
    if (cells.length) tableRows.push(new TableRow({ children: cells }));
  }

  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colWidths,
    layout: TableLayoutType.FIXED,
    rows: tableRows,
  });
}

function renderSpecsTable(ctx, block = {}) {
  const specsRows = ctx.specs.rows;
  const compact = isCompactTable(block);
  const colWidths = [Math.round(CONTENT_W * 0.45), Math.round(CONTENT_W * 0.55)];
  const tableRows = [
    new TableRow({
      children: [
        makeHeaderCell(ctx.labels.specs_col1 || 'Parameter', { width: colWidths[0], compact }),
        makeHeaderCell(ctx.labels.specs_col2 || 'Specification', { width: colWidths[1], compact }),
      ],
    }),
  ];
  for (const r of specsRows) {
    tableRows.push(new TableRow({
      children: [
        makeTextCell(r.label, { width: colWidths[0], compact, size: compact ? DOCX_PROFILE.table.compactSize : DOCX_PROFILE.table.bodySize }),
        makeTextCell(r.value, { width: colWidths[1], compact, size: compact ? DOCX_PROFILE.table.compactSize : DOCX_PROFILE.table.bodySize }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: colWidths, layout: TableLayoutType.FIXED, rows: tableRows });
}

function renderPartsTable(ctx, block = {}) {
  const parts = ctx.config.parts;
  const compact = isCompactTable(block);
  const half = Math.ceil(parts.length / 2);
  const cw = [Math.round(CONTENT_W * 0.12), Math.round(CONTENT_W * 0.38), Math.round(CONTENT_W * 0.12), Math.round(CONTENT_W * 0.38)];
  const tableRows = [
    new TableRow({
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
    tableRows.push(new TableRow({
      children: [
        makeTextCell(String(left.id), { width: cw[0], compact }),
        makeTextCell(left.name, { width: cw[1], compact }),
        makeTextCell(right ? String(right.id) : '', { width: cw[2], compact }),
        makeTextCell(right ? right.name : '', { width: cw[3], compact }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, rows: tableRows });
}

function renderButtonsTable(ctx, block = {}) {
  const buttons = ctx.config.buttons;
  const compact = isCompactTable(block);
  const cw = [Math.round(CONTENT_W * 0.45), Math.round(CONTENT_W * 0.55)];
  const tableRows = [
    new TableRow({
      children: [
        makeHeaderCell(ctx.labels.buttons_col1 || 'Button', { width: cw[0], compact }),
        makeHeaderCell(ctx.labels.buttons_col2 || 'Description', { width: cw[1], compact }),
      ],
    }),
  ];
  for (const b of buttons) {
    tableRows.push(new TableRow({
      children: [
        makeTextCell(`${b.id}. [btn:${b.key}] ${b.name}`, { width: cw[0], compact }),
        makeTextCell(b.desc, { width: cw[1], compact }),
      ],
    }));
  }
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, rows: tableRows });
}

function renderInfoTable(rows, compact = false) {
  const cw = [Math.round(CONTENT_W * 0.3), Math.round(CONTENT_W * 0.7)];
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: cw,
    layout: TableLayoutType.FIXED,
    rows: rows.map(([label, value]) => new TableRow({
      children: [
        makeTextCell(label, {
          width: cw[0],
          compact,
          bold: true,
          shading: { fill: ACTIVE_THEME.tableLabelFill, type: ShadingType.CLEAR },
        }),
        makeTextCell(value, { width: cw[1], compact }),
      ],
    })),
  });
}

function renderBrandInfoTable(ctx, block = {}) {
  const brand = ctx.brand;
  return renderInfoTable([
    [ctx.labels.brand_label || 'Brand', brand.name],
    [ctx.labels.address_label || 'Address', brand.address],
    [ctx.labels.website_label || 'Website', brand.website],
    [ctx.labels.email_label || 'Email', brand.support_email],
  ], isCompactTable(block));
}

function renderManufacturerTable(ctx, block = {}) {
  const mfr = ctx.mfr;
  return renderInfoTable([
    [ctx.labels.manufacturer_label || 'Manufacturer', mfr.name_secondary && mfr.name_secondary !== mfr.name_primary ? `${mfr.name_primary}\n${mfr.name_secondary}` : mfr.name_primary],
    [ctx.labels.address_label || 'Address', mfr.address],
    [ctx.labels.website_label || 'Website', mfr.website],
  ], isCompactTable(block));
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
      elements.push(makeTextParagraph(resolveVars(readTextValue(answer), ctx.vars), {
        after: 40,
        numbering: { reference: 'bullets', level: 0 },
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
  const rows = fields.map((field) => new TableRow({
    children: [
      makeTextCell(resolveVars(readTextValue(field), ctx.vars), {
        width: cw[0],
        bold: true,
        shading: { fill: ACTIVE_THEME.tableLabelFill, type: ShadingType.CLEAR },
      }),
      makeTextCell('', { width: cw[1] }),
    ],
  }));
  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: cw,
    layout: TableLayoutType.FIXED,
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
function renderChapterHeading(chapter) {
  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 0, after: 60, line: 320 },
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: ACTIVE_THEME.chapterBar } },
      indent: { left: 160 },
      keepNext: true,
      children: [
        new TextRun({
          text: `${chapter.chapter_no} `,
          font: TITLE_FONT,
          bold: true,
          size: DOCX_PROFILE.text.chapterNumberSize,
          color: ACTIVE_THEME.chapterNumber,
        }),
        new TextRun({
          text: chapter.title,
          font: TITLE_FONT,
          bold: true,
          size: DOCX_PROFILE.text.chapterTitleSize,
          color: ACTIVE_THEME.chapterTitle,
        }),
      ],
    }),
    new Paragraph({
      spacing: { after: 120 },
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({
        text: chapter.header_ref,
        font: FONT,
        size: DOCX_PROFILE.text.smallSize,
        color: ACTIVE_THEME.chapterHeaderRef,
      })],
    }),
  ];
}

function shouldPageBreakBeforePage(page, chapter, pageIndex) {
  if (pageIndex === 0) return false;
  if (page.force_page_break) return true;
  const title = `${page.section_title || ''}`.toLowerCase();
  const pageKey = `${page.page_key || ''}`.toLowerCase();
  if (title.includes('\u7eed') || title.includes('continued')) return true;
  if (pageKey.includes('continued') || pageKey.includes('warranty') || pageKey.includes('appendix')) return true;
  if ((page.blocks || []).some((block) => block.type === 'warranty_card')) return true;
  return false;
}

function renderPageSectionTitle(page, chapter, pageIndex) {
  if (page.hide_section_title) return [];
  const title = page.section_title || chapter.title;
  const pageBreakBefore = shouldPageBreakBeforePage(page, chapter, pageIndex);
  if (!title || title === chapter.title) {
    return pageBreakBefore ? [new Paragraph({ pageBreakBefore: true, children: [] })] : [];
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

  const children = [
    new Paragraph({
      spacing: { before: 220, after: 35 },
      children: [new TextRun({
        text: ctx.brand.display_name,
        font: TITLE_FONT,
        bold: true,
        size: DOCX_PROFILE.text.coverBrandSize,
        color: ACTIVE_THEME.primary,
      })],
    }),
    new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({
        text: ctx.localized.document_title,
        font: FONT,
        size: DOCX_PROFILE.text.coverTypeSize,
        color: ACTIVE_THEME.coverType,
      })],
    }),
    new Paragraph({
      spacing: { after: 24 },
      children: [new TextRun({
        text: ctx.localized.product_name,
        font: TITLE_FONT,
        bold: true,
        size: DOCX_PROFILE.text.coverProductSize,
        color: ACTIVE_THEME.coverTitle,
      })],
    }),
    new Paragraph({
      spacing: { after: 120 },
      children: [new TextRun({
        text: ctx.model,
        font: FONT,
        bold: true,
        size: DOCX_PROFILE.text.coverModelSize,
        color: ACTIVE_THEME.coverModel,
      })],
    }),
    new Paragraph({
      spacing: { after: 160 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACTIVE_THEME.coverDivider } },
      children: [],
    }),
  ];

  if (coverImage) {
    children.push(new Paragraph({
      spacing: { before: 180, after: 180 },
      alignment: AlignmentType.CENTER,
      children: [makeImageRun(coverImage, DOCX_PROFILE.images.cover.width, DOCX_PROFILE.images.cover.height, 'cover')],
    }));
  }

  children.push(
    new Paragraph({
      spacing: { before: 140, after: 0 },
      children: [new TextRun({
        text: ctx.brand.website || ctx.brand.name,
        font: FONT,
        size: DOCX_PROFILE.text.coverCompanySize,
        color: ACTIVE_THEME.coverCompany,
      })],
    })
  );

  return children;
}

function buildHeader(ctx, chapter = null) {
  const rightText = chapter?.header_ref || `${ctx.model}  ${ctx.localized.document_title}`;
  return new Header({
    children: [new Paragraph({
      spacing: { after: 40 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACTIVE_THEME.headerBorder } },
      tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      children: [
        new TextRun({ text: ctx.brand.display_name, font: FONT, size: DOCX_PROFILE.text.smallSize, color: ACTIVE_THEME.headerText }),
        new TextRun({ text: `\t${rightText}`, font: FONT, size: DOCX_PROFILE.text.smallSize, color: ACTIVE_THEME.headerText }),
      ],
    })],
  });
}

function buildFooter(ctx) {
  return new Footer({
    children: [new Paragraph({
      spacing: { before: 40 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: ACTIVE_THEME.headerBorder } },
      tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      children: [
        new TextRun({ text: `${ctx.brand.display_name} ${ctx.model}`, font: FONT, size: DOCX_PROFILE.text.smallSize, color: ACTIVE_THEME.footerText }),
        new TextRun({ text: '\t', font: FONT, size: DOCX_PROFILE.text.smallSize, color: ACTIVE_THEME.footerText }),
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: DOCX_PROFILE.text.smallSize, color: ACTIVE_THEME.footerText }),
      ],
    })],
  });
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
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '\u2022',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 420, hanging: 210 } } },
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
    model,
    vars,
    images: imagesManifest,
    imagesDir,
  };

  const coverChildren = buildCoverBlock(ctx);
  const tocTitle = langSuffix(lang) === 'cn' ? '目录' : 'Contents';
  const tocChildren = [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 0, after: 120 },
      children: [new TextRun({
        text: tocTitle,
        font: TITLE_FONT,
        bold: true,
        size: DOCX_PROFILE.text.tocTitleSize,
        color: ACTIVE_THEME.tocTitle,
      })],
    }),
    new TableOfContents(tocTitle, {
      hyperlink: true,
      headingStyleRange: '1-2',
      rightTabStop: TabStopPosition.MAX,
    }),
  ];

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
      paragraphStyles: [
        {
          id: 'Heading1',
          name: 'Heading 1',
          basedOn: 'Normal',
          next: 'Normal',
          quickFormat: true,
          run: {
            size: DOCX_PROFILE.text.chapterTitleSize,
            bold: true,
            font: TITLE_FONT,
            color: ACTIVE_THEME.chapterTitle,
          },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 0 },
        },
        {
          id: 'Heading2',
          name: 'Heading 2',
          basedOn: 'Normal',
          next: 'Normal',
          quickFormat: true,
          run: {
            size: DOCX_PROFILE.text.sectionTitleSize,
            bold: true,
            font: TITLE_FONT,
            color: ACTIVE_THEME.sectionTitle,
          },
          paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 1 },
        },
      ],
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
