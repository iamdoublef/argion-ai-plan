#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const {
  loadProductConfig,
  langSuffix,
  pickField,
} = require('./build-variant.js');

const swissRoot = path.resolve(__dirname, '..');
const standardsRoot = path.join(swissRoot, 'standards');
const localeGuides = JSON.parse(fs.readFileSync(path.join(standardsRoot, 'locale-guides.json'), 'utf8'));
const glossary = JSON.parse(fs.readFileSync(path.join(standardsRoot, 'terminology-glossary.json'), 'utf8'));

const args = process.argv.slice(2);
const productArgIndex = args.indexOf('--product');
const requestedProduct = productArgIndex !== -1 ? args[productArgIndex + 1] : null;

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function resolveProducts() {
  if (!requestedProduct) {
    return ['imt050', 'v23'];
  }
  const absolute = path.isAbsolute(requestedProduct)
    ? requestedProduct
    : path.resolve(swissRoot, requestedProduct);
  return [absolute];
}

function productDirFromInput(input) {
  if (path.isAbsolute(input)) {
    return input;
  }
  return path.join(swissRoot, 'products', input);
}

function loadStructuredLanguageDocument(productDir, lang) {
  const contentRoot = path.join(productDir, 'content', lang);
  const manifestPath = path.join(contentRoot, 'manifest.json');
  const manifest = readJson(manifestPath);

  return {
    manifest,
    chapters: manifest.chapters.map((entry) => {
      const chapterPath = path.join(contentRoot, 'chapters', entry.file);
      return readJson(chapterPath);
    }),
  };
}

function annotateTextNode(value, textId) {
  if (typeof value === 'string') {
    return { text: value, text_id: textId };
  }
  if (value && typeof value === 'object') {
    return {
      ...value,
      text_id: value.text_id || textId,
    };
  }
  return { text: '', text_id: textId };
}

function annotateCell(cell, textId) {
  if (typeof cell === 'string') {
    return { text: cell, text_id: textId };
  }
  return {
    ...cell,
    text_id: cell.text_id || textId,
  };
}

function annotateArrayItems(items = [], baseId) {
  return items.map((item, index) => annotateTextNode(item, `${baseId}.${index + 1}`));
}

function annotateBlock(block, baseId) {
  const next = { ...block };

  if (typeof next.text === 'string') {
    next.text_id = next.text_id || `${baseId}.text`;
  }
  if (typeof next.title === 'string') {
    next.title_id = next.title_id || `${baseId}.title`;
  }
  if (typeof next.caption === 'string') {
    next.caption_id = next.caption_id || `${baseId}.caption`;
  }
  if (typeof next.email === 'string') {
    next.email_id = next.email_id || `${baseId}.email`;
  }
  if (typeof next.cut_line === 'string') {
    next.cut_line_id = next.cut_line_id || `${baseId}.cut_line`;
  }

  if (Array.isArray(next.items)) {
    if (next.type === 'qa_list') {
      next.items = next.items.map((item, index) => ({
        ...item,
        question: annotateTextNode(item.question, `${baseId}.qa.${index + 1}.question`),
        answers: annotateArrayItems(item.answers || [], `${baseId}.qa.${index + 1}.answer`),
      }));
    } else {
      next.items = annotateArrayItems(next.items, `${baseId}.item`);
    }
  }

  if (Array.isArray(next.fields)) {
    next.fields = annotateArrayItems(next.fields, `${baseId}.field`);
  }

  if (Array.isArray(next.steps)) {
    next.steps = next.steps.map((step, index) => ({
      ...step,
      text_id: step.text_id || `${baseId}.step.${step.id || `step${index + 1}`}.text`,
    }));
  }

  if (Array.isArray(next.body_blocks)) {
    next.body_blocks = next.body_blocks.map((child, index) => annotateBlock(child, `${baseId}.body.${index + 1}`));
  }

  if (Array.isArray(next.headers)) {
    next.headers = next.headers.map((header, index) => annotateCell(header, `${baseId}.header.${index + 1}`));
  }

  if (Array.isArray(next.rows)) {
    next.rows = next.rows.map((row, rowIndex) =>
      row.map((cell, cellIndex) => annotateCell(cell, `${baseId}.row.${rowIndex + 1}.cell.${cellIndex + 1}`)));
  }

  if (Array.isArray(next.items) && next.type === 'figure_row') {
    next.items = next.items.map((item, index) => ({
      ...item,
      ...(typeof item.label_before === 'string'
        ? { label_before_id: item.label_before_id || `${baseId}.item.${index + 1}.label_before` }
        : {}),
      ...(typeof item.label_after === 'string'
        ? { label_after_id: item.label_after_id || `${baseId}.item.${index + 1}.label_after` }
        : {}),
    }));
  }

  return next;
}

function annotateSourceDocument(sourceDocument) {
  const annotatedManifest = {
    chapters: sourceDocument.manifest.chapters.map((entry) => ({
      ...entry,
      title_id: entry.title_id || `content.chapter.${entry.chapter_id}.title`,
      toc_title_id: entry.toc_title_id || `content.chapter.${entry.chapter_id}.toc_title`,
      header_ref_id: entry.header_ref_id || `content.chapter.${entry.chapter_id}.header_ref`,
    })),
  };

  const annotatedChapters = sourceDocument.chapters.map((chapter, chapterIndex) => {
    const manifestEntry = annotatedManifest.chapters[chapterIndex];
    return {
      ...clone(chapter),
      title_id: chapter.title_id || manifestEntry.title_id,
      toc_title_id: chapter.toc_title_id || manifestEntry.toc_title_id,
      header_ref_id: chapter.header_ref_id || manifestEntry.header_ref_id,
      pages: (chapter.pages || []).map((page, pageIndex) => ({
        ...page,
        ...(typeof page.section_title === 'string'
          ? { section_title_id: page.section_title_id || `content.chapter.${chapter.chapter_id}.page.${page.page_id || `page${pageIndex + 1}`}.section_title` }
          : {}),
        blocks: (page.blocks || []).map((block, blockIndex) =>
          annotateBlock(block, `content.chapter.${chapter.chapter_id}.page.${page.page_id || `page${pageIndex + 1}`}.block.${block.id || blockIndex + 1}`)),
      })),
    };
  });

  return { manifest: annotatedManifest, chapters: annotatedChapters };
}

function collectTextMetadata(node, scope, context, results) {
  if (Array.isArray(node)) {
    node.forEach((item, index) => collectTextMetadata(item, scope, `${context}[${index}]`, results));
    return;
  }

  if (!node || typeof node !== 'object') {
    return;
  }

  for (const [key, value] of Object.entries(node)) {
    if (key.endsWith('_id')) {
      const baseKey = key.slice(0, -3);
      const sourceValue = node[baseKey];
      if (typeof sourceValue === 'string') {
        results.push({
          text_id: value,
          scope,
          context: `${context}.${baseKey}`,
          source_text: sourceValue,
        });
      }
      continue;
    }

    if (Array.isArray(value) || (value && typeof value === 'object')) {
      collectTextMetadata(value, scope, `${context}.${key}`, results);
    }
  }
}

function buildGlossaryMap(locale) {
  const replacements = [];

  for (const entry of glossary.global || []) {
    if (entry.targets && entry.targets[locale] && entry.source_term) {
      replacements.push([entry.source_term, entry.targets[locale]]);
    }
  }

  for (const entry of glossary.forbidden_wording || []) {
    if (entry.locale === locale && entry.source_term && entry.preferred) {
      replacements.push([entry.source_term, entry.preferred]);
    }
  }

  return replacements;
}

function applyGlossary(text, locale) {
  let output = String(text ?? '');
  for (const [from, to] of buildGlossaryMap(locale)) {
    output = output.split(from).join(to);
  }
  return output;
}

function seedLocaleText(text, locale) {
  if (locale === 'zh-CN') {
    return String(text ?? '');
  }

  if (locale === 'zh-HK' || locale === 'zh-TW') {
    return applyGlossary(String(text ?? ''), locale);
  }

  return String(text ?? '');
}

function extractTargetValue(targetNode, baseKey, locale, sourceValue) {
  if (typeof targetNode === 'string' && baseKey === 'text') {
    return targetNode;
  }

  if (targetNode && typeof targetNode === 'object') {
    const value = targetNode[baseKey];
    if (typeof value === 'string') {
      return value;
    }
    if (value && typeof value === 'object' && typeof value.text === 'string') {
      return value.text;
    }
  }

  return seedLocaleText(sourceValue, locale);
}

function collectCatalogStrings(sourceNode, targetNode, locale, strings) {
  if (Array.isArray(sourceNode)) {
    sourceNode.forEach((item, index) => collectCatalogStrings(item, Array.isArray(targetNode) ? targetNode[index] : undefined, locale, strings));
    return;
  }

  if (!sourceNode || typeof sourceNode !== 'object') {
    return;
  }

  Object.entries(sourceNode).forEach(([key, value]) => {
    if (key.endsWith('_id')) {
      const baseKey = key.slice(0, -3);
      if (typeof sourceNode[baseKey] === 'string') {
        strings[value] = extractTargetValue(targetNode, baseKey, locale, sourceNode[baseKey]);
      }
      return;
    }

    if (Array.isArray(value) || (value && typeof value === 'object')) {
      const nextTarget = targetNode && typeof targetNode === 'object' ? targetNode[key] : undefined;
      collectCatalogStrings(value, nextTarget, locale, strings);
    }
  });
}

function buildProductStringEntries(config) {
  const entries = [];

  entries.push({
    text_id: 'product.product.name',
    scope: 'product',
    context: 'product.name',
    source_text: config.product.name_cn,
    targets: {
      'zh-CN': config.product.name_cn,
      en: config.product.name_en,
      de: config.product.name_de,
      it: config.product.name_it,
    },
  });

  Object.entries(config.brands || {}).forEach(([brandKey, brand]) => {
    entries.push({
      text_id: `product.brands.${brandKey}.display_name`,
      scope: 'product',
      context: `brands.${brandKey}.display_name`,
      source_text: brand.display_name_cn || brand.display_name,
      targets: {
        'zh-CN': brand.display_name_cn || brand.display_name,
        en: brand.display_name,
        de: brand.display_name,
        it: brand.display_name,
      },
    });
    entries.push({
      text_id: `product.brands.${brandKey}.name`,
      scope: 'product',
      context: `brands.${brandKey}.name`,
      source_text: brand.name,
      targets: { 'zh-CN': brand.name, en: brand.name, de: brand.name, it: brand.name },
    });
    entries.push({
      text_id: `product.brands.${brandKey}.address`,
      scope: 'product',
      context: `brands.${brandKey}.address`,
      source_text: brand.address_cn || brand.address,
      targets: {
        'zh-CN': brand.address_cn || brand.address,
        en: brand.address,
        de: brand.address,
        it: brand.address,
      },
    });
  });

  entries.push({
    text_id: 'product.manufacturer.name',
    scope: 'product',
    context: 'manufacturer.name',
    source_text: config.manufacturer.name_cn,
    targets: {
      'zh-CN': config.manufacturer.name_cn,
      en: config.manufacturer.name_en,
      de: config.manufacturer.name_en,
      it: config.manufacturer.name_en,
    },
  });
  entries.push({
    text_id: 'product.manufacturer.address',
    scope: 'product',
    context: 'manufacturer.address',
    source_text: config.manufacturer.address_cn,
    targets: {
      'zh-CN': config.manufacturer.address_cn,
      en: config.manufacturer.address_en,
      de: config.manufacturer.address_en,
      it: config.manufacturer.address_en,
    },
  });

  Object.entries(config.specs || {}).forEach(([marketKey, market]) => {
    (market.rows || []).forEach((row, index) => {
      entries.push({
        text_id: `product.specs.${marketKey}.rows.${index}.label`,
        scope: 'product',
        context: `specs.${marketKey}.rows.${index}.label`,
        source_text: row.label,
        targets: {
          'zh-CN': row.label,
          en: row.label_en || row.label,
          de: row.label_de || row.label_en || row.label,
          it: row.label_it || row.label_en || row.label,
        },
      });
      entries.push({
        text_id: `product.specs.${marketKey}.rows.${index}.value`,
        scope: 'product',
        context: `specs.${marketKey}.rows.${index}.value`,
        source_text: row.value,
        targets: {
          'zh-CN': row.value,
          en: row.value_en || row.value,
          de: row.value_de || row.value_en || row.value,
          it: row.value_it || row.value_en || row.value,
        },
      });
    });
  });

  (config.parts || []).forEach((part) => {
    entries.push({
      text_id: `product.parts.${part.id}.name`,
      scope: 'product',
      context: `parts.${part.id}.name`,
      source_text: part.name_cn,
      targets: {
        'zh-CN': part.name_cn,
        en: part.name_en,
        de: part.name_de,
        it: part.name_it,
      },
    });
  });

  (config.buttons || []).forEach((button) => {
    entries.push({
      text_id: `product.buttons.${button.id}.name`,
      scope: 'product',
      context: `buttons.${button.id}.name`,
      source_text: button.name_cn,
      targets: {
        'zh-CN': button.name_cn,
        en: button.name_en,
        de: button.name_de,
        it: button.name_it,
      },
    });
    entries.push({
      text_id: `product.buttons.${button.id}.desc`,
      scope: 'product',
      context: `buttons.${button.id}.desc`,
      source_text: button.desc_cn,
      targets: {
        'zh-CN': button.desc_cn,
        en: button.desc_en,
        de: button.desc_de,
        it: button.desc_it,
      },
    });
  });

  const cnLabels = config.ui_labels.cn || {};
  for (const key of Object.keys(cnLabels)) {
    entries.push({
      text_id: `product.ui_labels.${key}`,
      scope: 'product',
      context: `ui_labels.${key}`,
      source_text: cnLabels[key],
      targets: {
        'zh-CN': cnLabels[key],
        en: (config.ui_labels.en || {})[key] || cnLabels[key],
        de: (config.ui_labels.de || {})[key] || (config.ui_labels.en || {})[key] || cnLabels[key],
        it: (config.ui_labels.it || {})[key] || (config.ui_labels.en || {})[key] || cnLabels[key],
      },
    });
  }

  const manualTerm = (glossary.global || []).find((entry) => entry.term_id === 'manual');
  entries.push({
    text_id: 'system.document_title',
    scope: 'system',
    context: 'system.document_title',
    source_text: manualTerm?.targets?.['zh-CN'] || '使用说明书',
    targets: {
      'zh-CN': manualTerm?.targets?.['zh-CN'] || '使用说明书',
      'zh-HK': manualTerm?.targets?.['zh-HK'] || '說明書',
      'zh-TW': manualTerm?.targets?.['zh-TW'] || '使用說明書',
      en: manualTerm?.targets?.en || 'User Manual',
      de: manualTerm?.targets?.de || 'Bedienungsanleitung',
      it: manualTerm?.targets?.it || "Manuale d'uso",
    },
  });

  return entries;
}

function buildLocaleCatalog(locale, annotatedSource, targetDocument, productEntries) {
  const strings = {};

  collectCatalogStrings(annotatedSource.manifest, targetDocument?.manifest, locale, strings);
  annotatedSource.chapters.forEach((sourceChapter, index) => {
    collectCatalogStrings(sourceChapter, targetDocument?.chapters?.[index], locale, strings);
  });

  productEntries.forEach((entry) => {
    strings[entry.text_id] = entry.targets[locale] || seedLocaleText(entry.source_text, locale);
  });

  return { locale, strings };
}

function buildSourceAndCatalogs(productDir) {
  const config = loadProductConfig(productDir);
  const sourceDocument = loadStructuredLanguageDocument(productDir, 'cn');
  const annotatedSource = annotateSourceDocument(sourceDocument);
  const productEntries = buildProductStringEntries(config);

  const sourceRoot = path.join(productDir, 'content', 'source');
  writeJson(path.join(sourceRoot, 'manifest.json'), annotatedSource.manifest);
  annotatedSource.chapters.forEach((chapter, index) => {
    writeJson(path.join(sourceRoot, 'chapters', annotatedSource.manifest.chapters[index].file), chapter);
  });

  const metadata = [];
  collectTextMetadata(annotatedSource.manifest, 'content', 'content.manifest', metadata);
  annotatedSource.chapters.forEach((chapter) => {
    collectTextMetadata(chapter, 'content', `content.chapter.${chapter.chapter_id}`, metadata);
  });
  metadata.push(...productEntries.map((entry) => ({
    text_id: entry.text_id,
    scope: entry.scope,
    context: entry.context,
    source_text: entry.source_text,
  })));

  writeJson(path.join(productDir, 'i18n', 'strings.json'), metadata.sort((a, b) => a.text_id.localeCompare(b.text_id)));

  const targets = {
    'zh-CN': loadStructuredLanguageDocument(productDir, 'cn'),
    en: loadStructuredLanguageDocument(productDir, 'en'),
    de: loadStructuredLanguageDocument(productDir, 'de'),
    it: loadStructuredLanguageDocument(productDir, 'it'),
    'zh-HK': null,
    'zh-TW': null,
  };

  Object.keys(targets).forEach((locale) => {
    const catalog = buildLocaleCatalog(locale, annotatedSource, targets[locale], productEntries);
    writeJson(path.join(productDir, 'i18n', 'compiled', `${locale}.json`), catalog);
  });

  return {
    productDir,
    strings: metadata.length,
    locales: Object.keys(targets).length,
    localeGuideCount: Object.keys(localeGuides).length,
  };
}

function main() {
  const inputs = resolveProducts();
  const results = [];

  for (const input of inputs) {
    const productDir = productDirFromInput(input);
    results.push(buildSourceAndCatalogs(productDir));
  }

  results.forEach((result) => {
    console.log(`Migrated ${path.basename(result.productDir)} -> source + i18n (${result.strings} strings, ${result.locales} locales)`);
  });
}

main();
