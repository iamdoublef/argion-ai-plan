#!/usr/bin/env node
/**
 * build-variant.js — Config-driven manual variant builder (multi-language)
 *
 * Usage:
 *   node build-variant.js --region cn                     # China mainland / zh-CN / EU
 *   node build-variant.js --region gb --brand vesta       # UK English / Vesta / EU
 *   node build-variant.js --region de --brand act         # German / ACT / EU
 *   node build-variant.js --region tw --brand wevac       # Taiwan / Traditional CN / US
 *   node build-variant.js --region hk                     # Hong Kong / Traditional CN / EU
 *   node build-variant.js --all                           # Build all 21 variants
 */
const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// CLI args
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}
const buildAll = args.includes('--all');

const productDir = path.resolve(getArg('product', path.resolve(__dirname, '..', 'products', 'v23')));
const regionKey  = getArg('region', 'cn');
const brandKey   = getArg('brand', null);
const outputDir  = path.resolve(__dirname, '..', 'output');

// ---------------------------------------------------------------------------
// Load product data
// ---------------------------------------------------------------------------
function loadProductConfig(dir) {
  const configPath = path.join(dir, 'product.json');
  if (!fs.existsSync(configPath)) {
    throw new Error(`Product data not found: ${configPath}`);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

const config = loadProductConfig(productDir);

// ---------------------------------------------------------------------------
// Language helpers — pick the right field suffix for the target language
// ---------------------------------------------------------------------------
function langSuffix(lang) {
  if (lang.startsWith('zh')) return 'cn';
  if (lang.startsWith('de')) return 'de';
  if (lang.startsWith('it')) return 'it';
  return 'en';
}

function pickField(obj, base, suffix) {
  const key = `${base}_${suffix}`;
  return obj[key] !== undefined ? obj[key] : (obj[base] || '');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function resolveTemplateIncludes(entryPath, templateRoot, stack = []) {
  const normalizedEntry = path.resolve(entryPath);
  const normalizedRoot = path.resolve(templateRoot);
  const includePattern = /\{\{>\s*([^}\s]+)\s*\}\}/g;

  if (!normalizedEntry.startsWith(normalizedRoot)) {
    throw new Error(`Template include escapes template root: ${normalizedEntry}`);
  }
  if (stack.includes(normalizedEntry)) {
    throw new Error(`Template include cycle detected: ${[...stack, normalizedEntry].join(' -> ')}`);
  }
  if (!fs.existsSync(normalizedEntry)) {
    throw new Error(`Template include not found: ${normalizedEntry}`);
  }

  const source = fs.readFileSync(normalizedEntry, 'utf8');
  return source.replace(includePattern, (_, includeRef) => {
    const includePath = path.resolve(normalizedRoot, includeRef);
    return resolveTemplateIncludes(includePath, normalizedRoot, [...stack, normalizedEntry]);
  });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function replaceTemplateSlots(html, blocks) {
  let rendered = html;

  for (const [key, value] of Object.entries(blocks)) {
    if (typeof value !== 'string') {
      throw new Error(`Template slot "${key}" must be a string`);
    }

    const pattern = new RegExp(`{{#${escapeRegExp(key)}}}`, 'g');
    rendered = rendered.replace(pattern, value);
  }

  return rendered;
}

function stripTags(value = '') {
  return value.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function escapeHtml(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttribute(value = '') {
  return escapeHtml(value).replace(/`/g, '&#96;');
}

const RAW_HTML_PATTERN = /<\/?[a-z][^>]*>/i;

function validateTextTokenValue(value, label = 'text field') {
  const normalized = String(value ?? '');
  if (RAW_HTML_PATTERN.test(normalized)) {
    throw new Error(`Raw HTML is not allowed in ${label}: ${normalized}`);
  }
}

function renderTextTokens(value = '') {
  validateTextTokenValue(value, 'text token field');
  const normalized = String(value).replace(/\r\n/g, '\n');
  const escaped = escapeHtml(normalized);
  return escaped
    .replace(/\[btn:([^\]]+)\]/g, '<span class="btn-name">$1</span>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/\n/g, '<br>');
}

function loadImagesManifest(productDir) {
  const imagesPath = path.join(productDir, 'images.json');
  if (!fs.existsSync(imagesPath)) {
    return {};
  }

  const manifest = readJson(imagesPath);
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    throw new Error(`Invalid images manifest: ${imagesPath}`);
  }
  return manifest;
}

function normalizeChapterEntry(entry, chapter) {
  return {
    chapter_id: entry.chapter_id,
    chapter_no: entry.chapter_no,
    title: chapter.title || entry.title,
    title_id: chapter.title_id || entry.title_id,
    toc_title: chapter.toc_title || entry.toc_title || chapter.title || entry.title,
    toc_title_id: chapter.toc_title_id || entry.toc_title_id,
    header_ref: chapter.header_ref || entry.header_ref,
    header_ref_id: chapter.header_ref_id || entry.header_ref_id,
    enabled: entry.enabled !== false,
    file: entry.file,
    pages: chapter.pages || [],
  };
}

function validateManifestEntry(entry, contentRoot) {
  const requiredFields = ['chapter_id', 'chapter_no', 'title', 'toc_title', 'header_ref', 'file'];
  for (const field of requiredFields) {
    if (!entry[field]) {
      throw new Error(`Manifest entry missing "${field}" in ${path.join(contentRoot, 'manifest.json')}`);
    }
  }
}

function validateManifest(manifest, contentRoot) {
  let expectedChapterNo = 1;
  for (const entry of manifest.chapters) {
    validateManifestEntry(entry, contentRoot);
    const actualChapterNo = Number(entry.chapter_no);
    if (!Number.isInteger(actualChapterNo) || actualChapterNo !== expectedChapterNo) {
      throw new Error(`Manifest chapter numbering must be continuous in ${path.join(contentRoot, 'manifest.json')}: expected ${String(expectedChapterNo).padStart(2, '0')} got ${entry.chapter_no}`);
    }
    expectedChapterNo += 1;
  }
}

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function loadStructuredDocumentFromRoot(contentRoot) {
  const manifestPath = path.join(contentRoot, 'manifest.json');

  if (!fs.existsSync(manifestPath)) {
    throw new Error(`Structured content manifest not found: ${manifestPath}`);
  }

  const manifest = readJson(manifestPath);
  if (!manifest || !Array.isArray(manifest.chapters)) {
    throw new Error(`Invalid manifest file: ${manifestPath}`);
  }

  validateManifest(manifest, contentRoot);

  const chapters = manifest.chapters.map((entry) => {
    const chapterPath = path.join(contentRoot, 'chapters', entry.file);
    if (!fs.existsSync(chapterPath)) {
      throw new Error(`Chapter file not found: ${chapterPath}`);
    }

    const chapter = readJson(chapterPath);
    if (chapter.chapter_id && chapter.chapter_id !== entry.chapter_id) {
      throw new Error(`Chapter id mismatch: manifest=${entry.chapter_id} chapter=${chapter.chapter_id}`);
    }
    if (!Array.isArray(chapter.pages)) {
      throw new Error(`Chapter pages must be an array: ${chapterPath}`);
    }

    return normalizeChapterEntry(entry, chapter);
  });

  return {
    kind: 'structured',
    manifest,
    chapters,
  };
}

function loadSourceDocument(productDir) {
  return loadStructuredDocumentFromRoot(path.join(productDir, 'content', 'source'));
}

function loadLocaleCatalog(productDir, locale) {
  const catalogPath = path.join(productDir, 'i18n', 'compiled', `${locale}.json`);
  if (!fs.existsSync(catalogPath)) {
    throw new Error(`Locale catalog not found: ${catalogPath}`);
  }

  const catalog = readJson(catalogPath);
  if (!catalog || typeof catalog !== 'object' || Array.isArray(catalog)) {
    throw new Error(`Invalid locale catalog: ${catalogPath}`);
  }

  if (!catalog.strings || typeof catalog.strings !== 'object' || Array.isArray(catalog.strings)) {
    throw new Error(`Locale catalog missing strings map: ${catalogPath}`);
  }

  return catalog;
}

function translateCatalogString(catalog, textId, fallback = '') {
  if (!textId) {
    return fallback;
  }
  if (Object.prototype.hasOwnProperty.call(catalog.strings, textId)) {
    return catalog.strings[textId];
  }
  return fallback;
}

function localizeStructuredNode(node, catalog) {
  if (Array.isArray(node)) {
    node.forEach((item) => localizeStructuredNode(item, catalog));
    return node;
  }

  if (!node || typeof node !== 'object') {
    return node;
  }

  Object.entries(node).forEach(([key, value]) => {
    if (key.endsWith('_id')) {
      const baseKey = key.slice(0, -3);
      if (typeof node[baseKey] === 'string') {
        node[baseKey] = translateCatalogString(catalog, value, node[baseKey]);
      }
      return;
    }

    if (Array.isArray(value) || (value && typeof value === 'object')) {
      localizeStructuredNode(value, catalog);
    }
  });

  return node;
}

function loadContentDocument(productDir, locale) {
  const sourceDocument = loadSourceDocument(productDir);
  const catalog = loadLocaleCatalog(productDir, locale);
  const localizedDocument = deepClone(sourceDocument);
  localizeStructuredNode(localizedDocument, catalog);
  return localizedDocument;
}

const DOCUMENT_TITLE_BY_SUFFIX = {
  cn: '使用说明书',
  en: 'User Manual',
  de: 'Bedienungsanleitung',
  it: "Manuale d'uso",
};

function documentTitleForLocale(locale) {
  const suffix = langSuffix(locale);
  return DOCUMENT_TITLE_BY_SUFFIX[suffix] || DOCUMENT_TITLE_BY_SUFFIX.en;
}

let themeRegistryCache = null;

function loadBrandThemes() {
  if (themeRegistryCache) {
    return themeRegistryCache;
  }

  const themesPath = path.resolve(__dirname, '..', 'template', 'shared', 'base', 'brand-themes.json');
  themeRegistryCache = readJson(themesPath);
  return themeRegistryCache;
}

function resolveBrandTheme(brandKey) {
  const themes = loadBrandThemes();
  return themes[brandKey] || themes.default || { html: {}, docx: {} };
}

function buildThemeStyleOverrides(brandKey) {
  const theme = resolveBrandTheme(brandKey);
  const htmlVars = theme.html || {};
  const entries = Object.entries(htmlVars);
  if (!entries.length) {
    return '';
  }

  const declarations = entries.map(([key, value]) => `  ${key}: ${value};`).join('\n');
  return `:root {\n${declarations}\n}`;
}

function getBrandDisplayName(brandData, locale) {
  const suffix = langSuffix(locale);
  if (suffix === 'cn' && brandData.display_name_cn) {
    return brandData.display_name_cn;
  }
  return brandData.display_name;
}

function getBrandAddress(brandData, locale) {
  const suffix = langSuffix(locale);
  if (suffix === 'cn' && brandData.address_cn) {
    return brandData.address_cn;
  }
  return brandData.address;
}

function getManufacturerName(config, locale) {
  const suffix = langSuffix(locale);
  if (suffix === 'cn' && config.manufacturer.name_cn) {
    return config.manufacturer.name_cn;
  }
  return config.manufacturer.name_en;
}

function getManufacturerAddress(config, locale) {
  const suffix = langSuffix(locale);
  if (suffix === 'cn' && config.manufacturer.address_cn) {
    return config.manufacturer.address_cn;
  }
  return config.manufacturer.address_en;
}

function buildLocalizedUiLabels(config, catalog, locale) {
  const suffix = langSuffix(locale);
  const baseLabels = config.ui_labels[suffix] || config.ui_labels.en || {};
  const localized = {};

  for (const [key, value] of Object.entries(baseLabels)) {
    localized[key] = translateCatalogString(catalog, `product.ui_labels.${key}`, value);
  }

  if (!localized.cover_subtitle) {
    localized.cover_subtitle = translateCatalogString(catalog, 'system.document_title', documentTitleForLocale(locale));
  }

  return localized;
}

function buildLocalizedRuntimeData(config, catalog, brandKey, marketKey, locale) {
  const suffix = langSuffix(locale);
  const rawBrand = config.brands[brandKey];
  const rawManufacturer = config.manufacturer;
  const rawSpecs = config.specs[marketKey];

  const brand = {
    display_name: translateCatalogString(catalog, `product.brands.${brandKey}.display_name`, getBrandDisplayName(rawBrand, locale)),
    name: translateCatalogString(catalog, `product.brands.${brandKey}.name`, rawBrand.name),
    address: translateCatalogString(catalog, `product.brands.${brandKey}.address`, getBrandAddress(rawBrand, locale)),
    website: rawBrand.website,
    support_email: rawBrand.support_email,
  };

  const manufacturer = {
    name_primary: translateCatalogString(catalog, 'product.manufacturer.name', getManufacturerName(config, locale)),
    name_secondary: rawManufacturer.name_en,
    address: translateCatalogString(catalog, 'product.manufacturer.address', getManufacturerAddress(config, locale)),
    website: rawManufacturer.website,
  };

  const labels = buildLocalizedUiLabels(config, catalog, locale);
  const productName = translateCatalogString(catalog, 'product.product.name', pickField(config.product, 'name', suffix));
  const documentTitle = translateCatalogString(catalog, 'system.document_title', documentTitleForLocale(locale));

  const specs = {
    rows: (rawSpecs.rows || []).map((row, index) => ({
      label: translateCatalogString(catalog, `product.specs.${marketKey}.rows.${index}.label`, pickField(row, 'label', suffix)),
      value: translateCatalogString(catalog, `product.specs.${marketKey}.rows.${index}.value`, pickField(row, 'value', suffix) || row.value),
    })),
  };

  const parts = (config.parts || []).map((part) => ({
    id: part.id,
    name: translateCatalogString(catalog, `product.parts.${part.id}.name`, pickField(part, 'name', suffix)),
  }));

  const buttons = (config.buttons || []).map((button) => ({
    id: button.id,
    key: button.key,
    name: translateCatalogString(catalog, `product.buttons.${button.id}.name`, pickField(button, 'name', suffix)),
    desc: translateCatalogString(catalog, `product.buttons.${button.id}.desc`, pickField(button, 'desc', suffix)),
  }));

  return {
    localized: {
      product_name: productName,
      document_title: documentTitle,
      document_title_upper: suffix === 'cn' ? documentTitle : documentTitle.toUpperCase(),
    },
    labels,
    brand,
    manufacturer,
    specs,
    parts,
    buttons,
    runtimeConfig: {
      ...config,
      parts,
      buttons,
    },
  };
}

function styleAttr(styleMap = {}) {
  const entries = Object.entries(styleMap).filter(([, value]) => value !== undefined && value !== null && value !== '');
  if (!entries.length) {
    return '';
  }
  const css = entries.map(([key, value]) => `${key}:${value}`).join(';');
  return ` style="${escapeAttribute(css)}"`;
}

function resolveFigure(figureRef, context) {
  if (typeof figureRef === 'string') {
    const figure = context.images[figureRef];
    if (!figure) {
      throw new Error(`Missing image id: ${figureRef}`);
    }
    return {
      id: figureRef,
      ...figure,
    };
  }

  if (figureRef && typeof figureRef === 'object') {
    if (figureRef.figure) {
      return {
        ...resolveFigure(figureRef.figure, context),
        ...figureRef,
      };
    }
    if (figureRef.file) {
      return figureRef;
    }
  }

  throw new Error(`Invalid figure reference: ${JSON.stringify(figureRef)}`);
}

function renderFigureImage(figureRef, context, defaults = {}) {
  const figure = resolveFigure(figureRef, context);
  const style = {
    'max-height': figure.max_height || defaults.max_height || defaults['max-height'],
    'max-width': figure.max_width || defaults.max_width || defaults['max-width'],
    width: figure.width || defaults.width,
    height: figure.height || defaults.height,
    'object-fit': figure.object_fit || defaults.object_fit || defaults['object-fit'] || 'contain',
    display: figure.display || defaults.display,
    'vertical-align': figure.vertical_align || defaults.vertical_align || defaults['vertical-align'],
  };

  return `<img src="./${context.config.images_dir}/${figure.file}" alt="${escapeAttribute(figure.alt || '')}"${styleAttr(style)}>`;
}

function readTextValue(value) {
  if (typeof value === 'string') {
    return value;
  }
  if (value && typeof value === 'object' && typeof value.text === 'string') {
    return value.text;
  }
  return '';
}

function renderBlockListItems(items = []) {
  return items.map((item) => `<li>${renderTextTokens(readTextValue(item))}</li>`).join('\n');
}

function renderTableRef(block, context) {
  const tableLabels = {
    cn: {
      specs: ['参数', '规格'],
      parts: ['编号', '名称', '编号', '名称'],
      buttons: ['No. / 按键', '功能说明'],
      brand: ['项目', '信息'],
      brand_info: ['项目', '信息'],
      manufacturer: ['项目', '信息'],
      manufacturer_info: ['项目', '信息'],
    },
    en: {
      specs: ['Parameter', 'Specification'],
      parts: ['No.', 'Part', 'No.', 'Part'],
      buttons: ['No. / Button', 'Description'],
      brand: ['Field', 'Information'],
      brand_info: ['Field', 'Information'],
      manufacturer: ['Field', 'Information'],
      manufacturer_info: ['Field', 'Information'],
    },
    de: {
      specs: ['Parameter', 'Spezifikation'],
      parts: ['Nr.', 'Teil', 'Nr.', 'Teil'],
      buttons: ['Nr. / Taste', 'Beschreibung'],
      brand: ['Feld', 'Information'],
      brand_info: ['Feld', 'Information'],
      manufacturer: ['Feld', 'Information'],
      manufacturer_info: ['Feld', 'Information'],
    },
    it: {
      specs: ['Parametro', 'Specifica'],
      parts: ['N.', 'Parte', 'N.', 'Parte'],
      buttons: ['N. / Pulsante', 'Descrizione'],
      brand: ['Campo', 'Informazione'],
      brand_info: ['Campo', 'Informazione'],
      manufacturer: ['Campo', 'Informazione'],
      manufacturer_info: ['Campo', 'Informazione'],
    },
  };

  const labels = tableLabels[context.suffix] || tableLabels.en;
  const headers = block.headers || labels[block.table];
  const tableClasses = ['structured-table'];
  if (block.table_class) tableClasses.push(block.table_class);
  const tableClassAttr = ` class="${tableClasses.join(' ')}"`;

  if (Array.isArray(block.rows)) {
    const renderCell = (cell, isHeader = false) => {
      const normalized = typeof cell === 'string' ? { text: cell } : cell;
      const attrs = [];
      if (normalized.width) attrs.push(` style="width:${escapeAttribute(normalized.width)};"`);
      if (normalized.rowspan) attrs.push(` rowspan="${escapeAttribute(normalized.rowspan)}"`);
      if (normalized.colspan) attrs.push(` colspan="${escapeAttribute(normalized.colspan)}"`);
      const tag = isHeader ? 'th' : 'td';
      return `<${tag}${attrs.join('')}>${renderTextTokens(normalized.text || '')}</${tag}>`;
    };

    const headerHtml = headers
      ? `<thead><tr>${headers.map((header) => renderCell(header, true)).join('')}</tr></thead>`
      : '';
    const rowsHtml = block.rows
      .map((row) => `<tr>${row.map((cell) => renderCell(cell)).join('')}</tr>`)
      .join('\n');

    return `<table${tableClassAttr}>
    ${headerHtml}
    <tbody>
${rowsHtml}
    </tbody>
  </table>`;
  }

  switch (block.table) {
    case 'specs':
      return `<table${tableClassAttr}>
    <thead><tr><th>${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildSpecsRows(context.specs)}
    </tbody>
  </table>`;
    case 'parts':
      return `<table${tableClassAttr}>
    <thead><tr><th style="width:15%;">${headers[0]}</th><th>${headers[1]}</th><th style="width:15%;">${headers[2]}</th><th>${headers[3]}</th></tr></thead>
    <tbody>
${context.builders.buildPartsRows(context.config.parts)}
    </tbody>
  </table>`;
    case 'buttons':
      return `<table${tableClassAttr}>
    <thead><tr><th style="width:45%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildButtonsRows(context.config.buttons)}
    </tbody>
  </table>`;
    case 'brand_info':
      return `<table${tableClassAttr}>
    <thead><tr><th style="width:30%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildBrandInfoRows(context.brand)}
    </tbody>
  </table>`;
    case 'manufacturer_info':
      return `<table${tableClassAttr}>
    <thead><tr><th style="width:30%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildManufacturerRows(context.mfr)}
    </tbody>
  </table>`;
    default:
      throw new Error(`Unknown table ref: ${block.table}`);
  }
}

function renderFigure(block, context) {
  const image = renderFigureImage(block.figure, context, {
    'max-height': block.max_height,
    'max-width': block.max_width,
  });
  const caption = block.caption ? `<div class="fig-caption">${renderTextTokens(block.caption)}</div>` : '';
  const className = block.className ? ` ${block.className}` : '';

  return `<div class="fig-wrap${className}">
    ${image}
    ${caption}
  </div>`;
}

function renderSplitPanel(block, context) {
  const className = block.className ? ` ${block.className}` : '';
  const style = {
    gap: block.gap || '16px',
    'align-items': block.align || 'flex-start',
    'margin-bottom': block.margin_bottom,
    margin: block.margin,
  };

  const bodyBlocks = (block.body_blocks || []).map((childBlock) => renderBlock(childBlock, context)).join('\n');
  const figures = (block.figures || []).map((figureRef) => {
    const figure = typeof figureRef === 'string' ? { figure: figureRef } : figureRef;
    return renderFigureImage(figure, context, {
      width: figure.width || block.figure_width,
      'max-height': figure.max_height || block.max_height,
      'max-width': figure.max_width || block.max_width,
      display: 'block',
    });
  }).join('\n');

  return `<div class="split-panel${className}"${styleAttr(style)}>
    <div class="split-panel-body">
      ${bodyBlocks}
    </div>
    <div class="split-panel-figures">
      ${figures}
    </div>
  </div>`;
}

function renderFigureRow(block, context) {
  const className = block.className ? ` ${block.className}` : '';
  const style = {
    display: 'flex',
    gap: block.gap || '3mm',
    'justify-content': block.justify || 'center',
    'align-items': block.align || 'flex-start',
    margin: block.margin || '4px 0 6px',
    'font-size': block.font_size,
  };

  const items = (block.items || []).map((item) => {
    const labelBefore = item.label_before ? `<span>${renderTextTokens(item.label_before)}</span>` : '';
    const labelAfter = item.label_after ? `<span>${renderTextTokens(item.label_after)}</span>` : '';
    return `${labelBefore}${renderFigureImage(item.figure || item, context, {
      'max-height': item.max_height || block.max_height,
      'max-width': item.max_width || block.max_width,
      height: item.height,
      width: item.width,
      display: item.display || 'inline-block',
      'vertical-align': item.vertical_align || 'middle',
    })}${labelAfter}`;
  });

  const figures = (block.figures || []).map((figureRef) => {
    const figure = typeof figureRef === 'string' ? { figure: figureRef } : figureRef;
    return renderFigureImage(figure, context, {
      'max-height': figure.max_height || block.max_height,
      'max-width': figure.max_width || block.max_width,
    });
  });

  return `<div class="figure-row${className}"${styleAttr(style)}>
    ${[...figures, ...items].join('\n')}
  </div>`;
}

function renderStepFlow(block, context) {
  const startAt = Number(block.start_at || 1);
  const className = block.className ? ` ${block.className}` : '';
  const steps = (block.steps || []).map((step, index) => {
    const stepNo = startAt + index;
    const figures = step.figures && step.figures.length
      ? renderFigureRow({
          figures: step.figures,
          items: step.items,
          gap: step.gap || block.gap,
          justify: step.justify || block.justify,
          align: step.align || block.align,
          margin: step.margin || block.figure_margin,
          className: 'step-figures',
          max_height: step.max_height || block.max_height,
          max_width: step.max_width || block.max_width,
          font_size: step.font_size || block.font_size,
        }, context)
      : '';

    return `<div class="step-flow-step">
      <div class="step-flow-row">
        <span class="step-num">${stepNo}</span>
        <div class="step-text">${renderTextTokens(step.text)}</div>
      </div>
      ${figures}
    </div>`;
  }).join('\n');

  return `<div class="step-flow${className}">
    ${steps}
  </div>`;
}

function renderQaList(block) {
  return `<div class="qa-list">
    ${(block.items || []).map((item) => `<div class="qa-item">
      <div class="sub-title">${renderTextTokens(readTextValue(item.question || item.question_text || ''))}</div>
      <ul class="bullet-list">
        ${renderBlockListItems(item.answers || [])}
      </ul>
    </div>`).join('\n')}
  </div>`;
}

function renderContactBlock(block) {
  const email = block.email ? `<b>${renderTextTokens(readTextValue(block.email))}</b>` : '';
  const text = renderTextTokens(readTextValue(block.text || ''));
  const cutLine = block.cut_line ? `<div class="contact-cut-line">${renderTextTokens(readTextValue(block.cut_line))}</div>` : '';
  return `<div class="contact-block">
    <p>${text}${email}</p>
    ${cutLine}
  </div>`;
}

function renderWarrantyCard(block, context) {
  const fields = block.fields || [];
  return `<table class="warranty-card">
    <tbody>
      ${fields.map((field) => `<tr><td>${renderTextTokens(readTextValue(field))}</td><td></td></tr>`).join('\n')}
    </tbody>
  </table>`;
}

function renderBlock(block, context) {
  switch (block.type) {
    case 'paragraph':
      return `<p>${renderTextTokens(block.text)}</p>`;
    case 'bullet_list':
      return `<ul class="bullet-list">
        ${renderBlockListItems(block.items)}
      </ul>`;
    case 'warning_box':
    case 'caution_box':
    case 'notice_box': {
      const classNameMap = {
        warning_box: 'warning-box',
        caution_box: 'caution-box',
        notice_box: 'note-box',
      };
      const className = classNameMap[block.type];
      const icon = block.icon
        ? `<div style="margin:6px 0 8px;">${renderFigureImage(block.icon, context, { width: '22px', 'max-height': '22px' })}</div>`
        : '';
      const body = block.items
        ? `<ul class="box-list">
            ${renderBlockListItems(block.items)}
          </ul>`
        : renderTextTokens(block.text || '');
      const title = block.title
        ? `<div class="box-title">${renderTextTokens(block.title)}</div>`
        : '';
      return `<div class="${className}">
        ${title}
        ${icon}
        ${body}
      </div>`;
    }
    case 'sub_title':
      return `<div class="sub-title">${renderTextTokens(block.text)}</div>`;
    case 'figure':
      return renderFigure(block, context);
    case 'figure_row':
      return renderFigureRow(block, context);
    case 'step_flow':
      return renderStepFlow(block, context);
    case 'split_panel':
      return renderSplitPanel(block, context);
    case 'table_ref':
      return renderTableRef(block, context);
    case 'qa_list':
      return renderQaList(block, context);
    case 'contact_block':
      return renderContactBlock(block, context);
    case 'warranty_card':
      return renderWarrantyCard(block, context);
    default:
      throw new Error(`Unknown block type: ${block.type}`);
  }
}

function collectBlockFigureIds(block) {
  const ids = [];
  if (!block || typeof block !== 'object') {
    return ids;
  }

  if ((block.type === 'warning_box' || block.type === 'caution_box' || block.type === 'notice_box') && block.icon) {
    if (typeof block.icon === 'string') ids.push(block.icon);
    else if (block.icon && typeof block.icon.figure === 'string') ids.push(block.icon.figure);
  }
  if (block.type === 'figure' && typeof block.figure === 'string') {
    ids.push(block.figure);
  }
  if (block.type === 'figure_row') {
    for (const figure of block.figures || []) {
      if (typeof figure === 'string') ids.push(figure);
      else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
    }
    for (const item of block.items || []) {
      if (item && typeof item.figure === 'string') ids.push(item.figure);
    }
  }
  if (block.type === 'step_flow') {
    for (const step of block.steps || []) {
      for (const figure of step.figures || []) {
        if (typeof figure === 'string') ids.push(figure);
        else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
      }
      for (const item of step.items || []) {
        if (item && typeof item.figure === 'string') ids.push(item.figure);
      }
    }
  }
  if (block.type === 'split_panel') {
    for (const figure of block.figures || []) {
      if (typeof figure === 'string') ids.push(figure);
      else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
    }
  }

  return ids;
}

function collectProceduralImageUsage(chapters, imagesManifest) {
  const seen = new Map();

  function visitBlock(block, chapterId, pageKey, blockIndex) {
    if (!block || typeof block !== 'object') return;

    if (block.type === 'step_flow') {
      (block.steps || []).forEach((step, stepIndex) => {
        const usageRef = `${chapterId}.${pageKey}.${step.id || `step${stepIndex + 1}`}`;
        for (const figureRef of step.figures || []) {
          const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
          const meta = imagesManifest[imageId];
          if (!meta) throw new Error(`Missing image id: ${imageId}`);
          if (meta.kind === 'procedural') {
            if (seen.has(imageId)) {
              throw new Error(`Procedural image reused across steps: ${imageId}`);
            }
            seen.set(imageId, usageRef);
          }
        }
      });
    }

    if (block.type === 'split_panel') {
      (block.figures || []).forEach((figureRef, figureIndex) => {
        const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
        const meta = imagesManifest[imageId];
        if (!meta) throw new Error(`Missing image id: ${imageId}`);
        if (meta.kind === 'procedural') {
          const usageRef = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}.figure${figureIndex + 1}`;
          if (seen.has(imageId)) {
            throw new Error(`Procedural image reused across blocks: ${imageId}`);
          }
          seen.set(imageId, usageRef);
        }
      });
      (block.body_blocks || []).forEach((childBlock, childIndex) => {
        visitBlock(childBlock, chapterId, pageKey, `${blockIndex}-split-${childIndex}`);
      });
    }

    if (block.type !== 'step_flow' && block.type !== 'split_panel') {
      for (const imageId of collectBlockFigureIds(block)) {
        const meta = imagesManifest[imageId];
        if (!meta) {
          throw new Error(`Missing image id: ${imageId}`);
        }
        if (meta.kind === 'procedural') {
          const usageRef = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}`;
          if (seen.has(imageId)) {
            throw new Error(`Procedural image reused across steps: ${imageId}`);
          }
          seen.set(imageId, usageRef);
        }
      }
    }
  }

  for (const chapter of chapters) {
    for (let pageIndex = 0; pageIndex < (chapter.pages || []).length; pageIndex += 1) {
      const page = chapter.pages[pageIndex];
      const pageKey = page.page_id || `page${pageIndex + 1}`;
      (page.blocks || []).forEach((block, blockIndex) => {
        visitBlock(block, chapter.chapter_id, pageKey, blockIndex);
      });
    }
  }

  return seen;
}

function validateProceduralImageUsage(chapters, imagesManifest) {
  const seen = collectProceduralImageUsage(chapters, imagesManifest);

  for (const [imageId, meta] of Object.entries(imagesManifest)) {
    if (meta.kind !== 'procedural') continue;
    if (!meta.usage_ref) {
      throw new Error(`Procedural image missing usage_ref: ${imageId}`);
    }
    const actualUsageRef = seen.get(imageId);
    if (!actualUsageRef) {
      throw new Error(`Procedural image not used in content: ${imageId}`);
    }
    if (meta.usage_ref !== actualUsageRef) {
      throw new Error(`Procedural image usage_ref mismatch: ${imageId} expected ${meta.usage_ref} actual ${actualUsageRef}`);
    }
  }
}

function renderStructuredDocument(documentSchema, context) {
  const chapters = documentSchema.chapters.filter((chapter) => chapter.enabled !== false);
  validateProceduralImageUsage(chapters, context.images);

  let pageNo = 3;
  const tocEntries = [];
  const pages = [];

  for (const chapter of chapters) {
    tocEntries.push({
      chapter_no: chapter.chapter_no,
      toc_title: chapter.toc_title || chapter.title,
      page_no: pageNo,
    });

    for (const page of chapter.pages) {
      const pageClass = page.page_class ? ` ${page.page_class}` : '';
      const headerRef = page.header_ref || chapter.header_ref;
      const sectionTitle = page.hide_section_title
        ? ''
        : `<h2 class="section-title"><span class="chapter-num">${chapter.chapter_no}</span>${page.section_title || chapter.title}</h2>`;
      const blocks = (page.blocks || []).map((block) => renderBlock(block, context)).join('\n');

      pages.push(`<div class="page${pageClass}">
  <div class="header-strip">
    <div class="header-brand">{{brand.display_name}}</div>
    <div class="header-ref">${headerRef}</div>
  </div>
  ${sectionTitle}
  ${blocks}
  <div class="page-footer"><span>{{brand.display_name}} {{product.model}} ${context.localized.document_title}</span><span>${pageNo}</span></div>
</div>`);
      pageNo += 1;
    }
  }

  const tocHtml = tocEntries.map((entry) => `<div class="toc-item"><span><span class="toc-chapter">${entry.chapter_no}</span><span class="toc-name">${entry.toc_title}</span></span><span class="toc-page">${entry.page_no}</span></div>`).join('\n');

  return {
    tocHtml,
    documentHtml: pages.join('\n\n'),
  };
}

function renderDocument(documentSchema, context) {
  if (documentSchema.kind !== 'structured') {
    throw new Error(`Unsupported document schema kind: ${documentSchema.kind}`);
  }

  return renderStructuredDocument(documentSchema, context);
}

// ---------------------------------------------------------------------------
// Build a single variant
// ---------------------------------------------------------------------------
function buildVariant(regionCode, brandOverride) {
  const region = config.regions[regionCode];
  if (!region) {
    console.error(`Unknown region: ${regionCode}. Available: ${Object.keys(config.regions).join(', ')}`);
    process.exit(1);
  }

  const activeBrand  = brandOverride || config.product.active_brand;
  const activeMarket = region.market;
  const lang         = region.lang;
  const suffix       = langSuffix(lang);

  if (!config.brands[activeBrand]) {
    console.error(`Unknown brand: ${activeBrand}. Available: ${Object.keys(config.brands).join(', ')}`);
    process.exit(1);
  }
  if (!config.specs[activeMarket]) {
    console.error(`Unknown market: ${activeMarket}. Available: ${Object.keys(config.specs).join(', ')}`);
    process.exit(1);
  }

  const model = config.product.model;
  const themeStyleOverrides = buildThemeStyleOverrides(activeBrand);
  const localeCatalog = loadLocaleCatalog(productDir, lang);
  const localizedRuntime = buildLocalizedRuntimeData(config, localeCatalog, activeBrand, activeMarket, lang);
  const brand = localizedRuntime.brand;
  const specs = localizedRuntime.specs;
  const mfr   = localizedRuntime.manufacturer;
  const labels = localizedRuntime.labels;
  const runtimeConfig = localizedRuntime.runtimeConfig;

  console.log(`Building: ${model} | region=${regionCode} | brand=${activeBrand} (${brand.display_name}) | market=${activeMarket} | lang=${lang}`);

  // Load template
  const templateLang = region.template_lang || langSuffix(region.lang);
  const templatePrefix = config.product.template_prefix || 'v23';
  const templatePath = path.resolve(__dirname, '..', 'template', `${templatePrefix}-master-${templateLang}.html`);
  if (!fs.existsSync(templatePath)) {
    console.error(`Template not found: ${templatePath}`);
    process.exit(1);
  }
  let html = resolveTemplateIncludes(templatePath, path.resolve(__dirname, '..', 'template'));

  // Update <html lang="...">
  html = html.replace(/<html lang="[^"]*">/, `<html lang="${lang}">`);

  // Simple variable replacements
  const vars = {
    'brand.display_name':      brand.display_name,
    'brand.name':              brand.name,
    'brand.address':           brand.address,
    'brand.website':           brand.website,
    'brand.support_email':     brand.support_email,
    'product.model':           model,
    'product.name':            localizedRuntime.localized.product_name,
    'product.name_cn':         localizedRuntime.localized.product_name,
    'product.name_en':         localizedRuntime.localized.product_name,
    'product.name_de':         localizedRuntime.localized.product_name,
    'product.name_it':         localizedRuntime.localized.product_name,
    'product.cover_image':     config.product.cover_image || '',
    'manufacturer.website':    mfr.website,
    'warranty.years':          String(config.warranty.years),
    'images_dir':              config.images_dir,
    'localized.product_name':  localizedRuntime.localized.product_name,
    'localized.document_title': localizedRuntime.localized.document_title,
    'localized.document_title_upper': localizedRuntime.localized.document_title_upper,
  };

  for (const [key, value] of Object.entries(vars)) {
    const pattern = new RegExp(`\\{\\{${key.replace(/\./g, '\\.')}\\}\\}`, 'g');
    html = html.replace(pattern, value);
  }

  // Block replacements — language-aware
  function buildSpecsRows(specsData) {
    return specsData.rows
      .map(r => {
        return `      <tr><td>${r.label}</td><td>${r.value}</td></tr>`;
      })
      .join('\n');
  }

  function buildPartsRows(parts) {
    const rows = [];
    const half = Math.ceil(parts.length / 2);
    for (let i = 0; i < half; i++) {
      const left = parts[i];
      const right = parts[i + half];
      const leftName  = left.name;
      const rightId   = right ? right.id : '';
      const rightName = right ? right.name : '';
      rows.push(`      <tr><td>${left.id}</td><td>${leftName}</td><td>${rightId}</td><td>${rightName}</td></tr>`);
    }
    return rows.join('\n');
  }

  function buildButtonsRows(buttons) {
    return buttons
      .map(b => {
        const keyEscaped = b.key.replace(/&/g, '&amp;');
        const bName = b.name;
        const bDesc = b.desc;
        return `      <tr><td><span class="callout-no">${b.id}</span> <span class="btn-name">${keyEscaped}</span>\u3000${bName}</td><td>${bDesc}</td></tr>`;
      })
      .join('\n');
  }

  function buildBrandInfoRows(brandData) {
    return [
      `      <tr><td style="width:30%">${labels.brand_label}</td><td><b>${brandData.name}</b></td></tr>`,
      `      <tr><td>${labels.address_label}</td><td>${brandData.address}</td></tr>`,
      `      <tr><td>${labels.website_label}</td><td>${brandData.website}</td></tr>`,
      `      <tr><td>${labels.email_label}</td><td>${brandData.support_email}</td></tr>`,
    ].join('\n');
  }

  function buildManufacturerRows(mfrData) {
    return [
      `      <tr><td style="width:30%">${labels.manufacturer_label}</td><td><b>${mfrData.name_primary}</b>${mfrData.name_secondary && mfrData.name_secondary !== mfrData.name_primary ? `<br><span style="font-weight:400;font-size:12px;color:#666">${mfrData.name_secondary}</span>` : ''}</td></tr>`,
      `      <tr><td>${labels.address_label}</td><td>${mfrData.address}</td></tr>`,
      `      <tr><td>${labels.website_label}</td><td>${mfrData.website}</td></tr>`,
    ].join('\n');
  }

  const imagesManifest = loadImagesManifest(productDir);
  const documentSchema = loadContentDocument(productDir, lang);
  const renderedDocument = renderDocument(documentSchema, {
    config: runtimeConfig,
    brand,
    specs,
    mfr,
    model,
    suffix,
    labels,
    localized: localizedRuntime.localized,
    images: imagesManifest,
    builders: {
      buildSpecsRows,
      buildPartsRows,
      buildButtonsRows,
      buildBrandInfoRows,
      buildManufacturerRows,
    },
  });

  html = replaceTemplateSlots(html, {
    THEME_STYLE_OVERRIDES: themeStyleOverrides,
    AUTO_TOC: renderedDocument.tocHtml,
    DOCUMENT_BODY: renderedDocument.documentHtml,
  });

  for (const [key, value] of Object.entries(vars)) {
    const pattern = new RegExp(`\{\{${key.replace(/\./g, '\\.')}\}\}`, 'g');
    html = html.replace(pattern, value);
  }

  const blocks = {
    'SPECS_TABLE_ROWS':        buildSpecsRows(specs),
    'PARTS_TABLE_ROWS':        buildPartsRows(runtimeConfig.parts),
    'BUTTONS_TABLE_ROWS':      buildButtonsRows(runtimeConfig.buttons),
    'BRAND_INFO_ROWS':         buildBrandInfoRows(brand),
    'MANUFACTURER_INFO_ROWS':  buildManufacturerRows(mfr),
  };

  for (const [key, value] of Object.entries(blocks)) {
    const pattern = new RegExp(`{{#${key}}}`, 'g');
    html = html.replace(pattern, value);
  }

  // Validate — no remaining placeholders
  const remaining = html.match(/\{\{[^}]+\}\}/g);
  if (remaining) {
    console.warn(`  WARNING: ${remaining.length} unresolved placeholder(s):`);
    const unique = [...new Set(remaining)];
    unique.forEach(p => console.warn(`    ${p}`));
  }

  // Copy images to output
  fs.mkdirSync(outputDir, { recursive: true });
  const imgSrc = path.join(productDir, 'images');
  const imgDst = path.join(outputDir, config.images_dir);
  if (fs.existsSync(imgSrc)) {
    fs.mkdirSync(imgDst, { recursive: true });
    for (const f of fs.readdirSync(imgSrc)) {
      fs.copyFileSync(path.join(imgSrc, f), path.join(imgDst, f));
    }
    console.log(`  Copied ${fs.readdirSync(imgSrc).length} images → ${imgDst}`);
  }

  // Write output
  const outName = `${model.toLowerCase()}-${activeBrand}-${activeMarket}-${regionCode}.html`;
  const outPath = path.join(outputDir, outName);
  fs.writeFileSync(outPath, html, 'utf8');

  const sizeKB = (Buffer.byteLength(html, 'utf8') / 1024).toFixed(1);
  const status = remaining ? 'WARNING' : 'OK';
  console.log(`  Output: ${outName} (${sizeKB} KB) — ${status}`);

  return { outName, sizeKB, status, region: regionCode, brand: activeBrand, market: activeMarket };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  if (buildAll) {
    const allRegions = Object.keys(config.regions);
    const allBrands  = Object.keys(config.brands);
    const results = [];

    for (const r of allRegions) {
      for (const b of allBrands) {
        results.push(buildVariant(r, b));
      }
    }

    console.log('\n========== BUILD MATRIX SUMMARY ==========');
    console.log(`Total: ${results.length} variants`);
    const ok = results.filter(r => r.status === 'OK').length;
    const warn = results.filter(r => r.status === 'WARNING').length;
    console.log(`OK: ${ok} | WARNING: ${warn}`);
    console.log('');
    results.forEach(r => {
      console.log(`  [${r.status}] ${r.outName} (${r.sizeKB} KB)`);
    });

    if (warn > 0) process.exit(1);
  } else {
    const result = buildVariant(regionKey, brandKey);
    if (result.status !== 'OK') process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  buildVariant,
  langSuffix,
  pickField,
  loadProductConfig,
  loadImagesManifest,
  loadSourceDocument,
  loadLocaleCatalog,
  loadContentDocument,
  buildLocalizedRuntimeData,
  buildThemeStyleOverrides,
  resolveBrandTheme,
  renderDocument,
  replaceTemplateSlots,
  renderTextTokens,
  resolveTemplateIncludes,
};
