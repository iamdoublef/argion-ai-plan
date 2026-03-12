#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const swissRoot = path.resolve(__dirname, '..');
const products = ['imt050', 'v23'];
const langs = ['cn', 'en', 'de', 'it'];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function decodeEntities(value = '') {
  return value
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function normalizeText(value = '') {
  return decodeEntities(String(value))
    .replace(/\u00a0/g, ' ')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.replace(/\s+/g, ' ').trim())
    .join('\n')
    .replace(/\n{2,}/g, '\n')
    .trim();
}

function sanitizeTokenString(value = '') {
  return normalizeText(
    String(value)
      .replace(/<span[^>]*class=["'][^"']*btn-name[^"']*["'][^>]*>(.*?)<\/span>/gi, '[btn:$1]')
      .replace(/<(b|strong)>(.*?)<\/\1>/gi, '**$2**')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, '')
  );
}

function stripLeadingStepNumber(value = '') {
  return normalizeText(value).replace(/^\d+\s*/, '');
}

function parseStyle(style = '') {
  return style.split(';').reduce((acc, declaration) => {
    const [rawKey, rawValue] = declaration.split(':');
    if (!rawKey || !rawValue) return acc;
    acc[rawKey.trim().toLowerCase()] = rawValue.trim();
    return acc;
  }, {});
}

function hasClass(node, className) {
  const classValue = node?.attrs?.class || '';
  return classValue.split(/\s+/).includes(className);
}

function elementChildren(node) {
  return (node.children || []).filter((child) => child.type === 'element');
}

function textChildren(node) {
  return (node.children || []).filter((child) => child.type === 'text' && child.text.trim());
}

function filenameFromSrc(src = '') {
  return path.basename(src.replace(/^\.\/\{\{images_dir\}\}\//, ''));
}

function createImageRegistry(imagesManifest) {
  const idByFile = new Map();
  let counter = 1;

  for (const [id, meta] of Object.entries(imagesManifest)) {
    idByFile.set(meta.file, id);
  }

  function nextId(chapterId, pageIndex) {
    const id = `${chapterId}.page${String(pageIndex + 1).padStart(2, '0')}.image${String(counter).padStart(2, '0')}`;
    counter += 1;
    return id;
  }

  function ensureImageId(imageNode, chapterId, pageIndex, kind = 'reference') {
    const src = imageNode?.attrs?.src || '';
    const file = filenameFromSrc(src);
    if (!file) {
      throw new Error(`Missing image src for ${chapterId} page ${pageIndex + 1}`);
    }

    if (idByFile.has(file)) {
      return idByFile.get(file);
    }

    const id = nextId(chapterId, pageIndex);
    imagesManifest[id] = {
      file,
      alt: normalizeText(imageNode.attrs?.alt || id),
      kind,
    };
    idByFile.set(file, id);
    return id;
  }

  return {
    ensureImageId,
    idByFile,
  };
}

function inlineToTokens(node) {
  if (!node) return '';
  if (node.type === 'text') {
    return node.text;
  }
  if (node.type !== 'element') {
    return '';
  }

  const children = (node.children || []).map((child) => inlineToTokens(child)).join('');

  switch (node.tag) {
    case 'br':
      return '\n';
    case 'b':
    case 'strong':
      return `**${children}**`;
    case 'span':
      if (hasClass(node, 'btn-name')) {
        return `[btn:${normalizeText(children)}]`;
      }
      return children;
    default:
      return children;
  }
}

function extractText(node) {
  return normalizeText(inlineToTokens(node));
}

function parseList(node) {
  return elementChildren(node)
    .filter((child) => child.tag === 'li')
    .map((child) => extractText(child))
    .filter(Boolean);
}

function parseInlineTable(node) {
  const headers = elementChildren(node).find((child) => child.tag === 'thead');
  const body = elementChildren(node).find((child) => child.tag === 'tbody') || node;

  const headerRow = headers
    ? elementChildren(headers).find((child) => child.tag === 'tr')
    : null;

  const parsedHeaders = headerRow
    ? elementChildren(headerRow)
        .filter((child) => child.tag === 'th' || child.tag === 'td')
        .map((cell) => {
          const styles = parseStyle(cell.attrs?.style || '');
          const header = { text: extractText(cell) };
          if (styles.width) header.width = styles.width;
          return header;
        })
    : null;

  const rows = elementChildren(body)
    .filter((child) => child.tag === 'tr')
    .map((row) => elementChildren(row)
      .filter((cell) => cell.tag === 'th' || cell.tag === 'td')
      .map((cell) => {
        const styles = parseStyle(cell.attrs?.style || '');
        const parsedCell = { text: extractText(cell) };
        if (styles.width) parsedCell.width = styles.width;
        if (cell.attrs?.rowspan) parsedCell.rowspan = Number(cell.attrs.rowspan);
        if (cell.attrs?.colspan) parsedCell.colspan = Number(cell.attrs.colspan);
        return parsedCell;
      }));

  const allTwoColumnAndSecondEmpty = rows.length > 0 && rows.every((row) => row.length === 2 && !row[1].text);
  if (!parsedHeaders && allTwoColumnAndSecondEmpty) {
    return {
      type: 'warranty_card',
      fields: rows.map((row) => row[0].text),
    };
  }

  return {
    type: 'table_ref',
    headers: parsedHeaders,
    rows,
  };
}

function parseTable(node) {
  const innerHtml = node.html || '';
  if (innerHtml.includes('{{#SPECS_TABLE_ROWS}}')) return { type: 'table_ref', table: 'specs' };
  if (innerHtml.includes('{{#PARTS_TABLE_ROWS}}')) return { type: 'table_ref', table: 'parts' };
  if (innerHtml.includes('{{#BUTTONS_TABLE_ROWS}}')) return { type: 'table_ref', table: 'buttons' };
  if (innerHtml.includes('{{#BRAND_INFO_ROWS}}')) return { type: 'table_ref', table: 'brand_info' };
  if (innerHtml.includes('{{#MANUFACTURER_INFO_ROWS}}')) return { type: 'table_ref', table: 'manufacturer_info' };
  return parseInlineTable(node);
}

function onlyFigureNodes(nodes) {
  return nodes.length > 0 && nodes.every((node) => {
    if (node.tag === 'img') return true;
    const children = elementChildren(node);
    return children.length > 0 && onlyFigureNodes(children);
  });
}

function collectFiguresFromNode(node, ctx, chapterId, pageIndex, kind = 'reference') {
  const figures = [];

  function walk(current) {
    if (!current || current.type !== 'element') return;
    if (current.tag === 'img') {
      const imageId = ctx.imageRegistry.ensureImageId(current, chapterId, pageIndex, kind);
      const styles = parseStyle(current.attrs?.style || '');
      const figure = { figure: imageId };
      if (styles.width) figure.width = styles.width;
      if (styles.height) figure.height = styles.height;
      if (styles['max-width']) figure.max_width = styles['max-width'];
      if (styles['max-height']) figure.max_height = styles['max-height'];
      figures.push(figure);
      return;
    }
    for (const child of elementChildren(current)) walk(child);
  }

  walk(node);
  return figures;
}

function parseBox(node, ctx, chapterId, pageIndex, type) {
  const titleNode = elementChildren(node).find((child) => hasClass(child, 'box-title'));
  const iconNode = elementChildren(node).find((child) => child.tag === 'img')
    || elementChildren(node).flatMap((child) => elementChildren(child)).find((child) => child.tag === 'img');
  const listNode = elementChildren(node).find((child) => child.tag === 'ul');

  const block = {
    type,
    title: extractText(titleNode),
  };
  if (iconNode) {
    block.icon = ctx.imageRegistry.ensureImageId(iconNode, chapterId, pageIndex, 'reference');
  }
  if (listNode) {
    block.items = parseList(listNode);
  } else {
    const bodyNodes = (node.children || []).filter((child) => child !== titleNode);
    block.text = normalizeText(bodyNodes.map((child) => inlineToTokens(child)).join(''));
  }
  return block;
}

function parseFigureBlock(node, ctx, chapterId, pageIndex) {
  const imageNode = elementChildren(node).find((child) => child.tag === 'img');
  if (!imageNode) return null;
  const imageId = ctx.imageRegistry.ensureImageId(imageNode, chapterId, pageIndex, 'reference');
  const styles = parseStyle(imageNode.attrs?.style || '');
  const block = {
    type: 'figure',
    figure: imageId,
  };
  if (styles.width) block.width = styles.width;
  if (styles['max-width']) block.max_width = styles['max-width'];
  if (styles['max-height']) block.max_height = styles['max-height'];
  if (node.attrs?.class && node.attrs.class !== 'fig-wrap') block.className = node.attrs.class.replace(/\bfig-wrap\b/g, '').trim();
  return block;
}

function parseStepFlow(node, chapterId, pageIndex) {
  const steps = elementChildren(node)
    .filter((child) => child.tag === 'li')
    .map((child, index) => ({
      id: `step${index + 1}`,
      text: stripLeadingStepNumber(extractText(child)),
    }))
    .filter((step) => step.text);

  return {
    type: 'step_flow',
    steps,
  };
}

function parseFlex(node, ctx, chapterId, pageIndex) {
  const children = elementChildren(node);
  if (!children.length) return [];

  if (onlyFigureNodes(children)) {
    return [{
      type: 'figure_row',
      figures: children.flatMap((child) => collectFiguresFromNode(child, ctx, chapterId, pageIndex, 'reference')),
    }];
  }

  const left = children[0];
  const right = children[children.length - 1];
  const rightFigures = collectFiguresFromNode(right, ctx, chapterId, pageIndex, 'procedural');

  if (rightFigures.length) {
    return [{
      type: 'split_panel',
      body_blocks: parseNodes(left.children || [left], ctx, chapterId, pageIndex),
      figures: rightFigures,
    }];
  }

  return children.flatMap((child) => parseNode(child, ctx, chapterId, pageIndex));
}

function parseNode(node, ctx, chapterId, pageIndex) {
  if (!node) return [];
  if (node.type === 'text') {
    return [];
  }

  if (node.tag === 'div' && hasClass(node, 'sub-title')) {
    return [{ type: 'sub_title', text: extractText(node) }];
  }
  if (node.tag === 'div' && hasClass(node, 'warning-box')) {
    return [parseBox(node, ctx, chapterId, pageIndex, 'warning_box')];
  }
  if (node.tag === 'div' && hasClass(node, 'caution-box')) {
    return [parseBox(node, ctx, chapterId, pageIndex, 'caution_box')];
  }
  if (node.tag === 'div' && hasClass(node, 'note-box')) {
    return [parseBox(node, ctx, chapterId, pageIndex, 'notice_box')];
  }
  if (node.tag === 'div' && hasClass(node, 'fig-wrap')) {
    const figureBlock = parseFigureBlock(node, ctx, chapterId, pageIndex);
    return figureBlock ? [figureBlock] : [];
  }
  if (node.tag === 'div' && parseStyle(node.attrs?.style || '').display === 'flex') {
    return parseFlex(node, ctx, chapterId, pageIndex);
  }
  if (node.tag === 'div' && hasClass(node, 'rollbag-stack')) {
    return [{
      type: 'figure_row',
      figures: collectFiguresFromNode(node, ctx, chapterId, pageIndex, 'reference'),
    }];
  }
  if (node.tag === 'div') {
    return parseNodes(node.children || [], ctx, chapterId, pageIndex);
  }
  if (node.tag === 'p') {
    const text = extractText(node);
    return text ? [{ type: 'paragraph', text }] : [];
  }
  if (node.tag === 'ul') {
    const items = parseList(node);
    return items.length ? [{ type: 'bullet_list', items }] : [];
  }
  if (node.tag === 'ol' && hasClass(node, 'steps')) {
    return [parseStepFlow(node, chapterId, pageIndex)];
  }
  if (node.tag === 'table') {
    return [parseTable(node)];
  }
  if (node.tag === 'img') {
    return [{
      type: 'figure',
      figure: ctx.imageRegistry.ensureImageId(node, chapterId, pageIndex, 'reference'),
    }];
  }

  return [];
}

function parseNodes(nodes, ctx, chapterId, pageIndex) {
  return nodes.flatMap((node) => parseNode(node, ctx, chapterId, pageIndex));
}

async function buildAst(page, html) {
  return page.evaluate((fragment) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(`<div id="root">${fragment}</div>`, 'text/html');
    const root = doc.querySelector('#root');

    function walk(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        return { type: 'text', text: node.textContent || '' };
      }
      if (node.nodeType !== Node.ELEMENT_NODE) {
        return null;
      }

      const attrs = {};
      for (const attr of node.attributes) {
        attrs[attr.name] = attr.value;
      }

      return {
        type: 'element',
        tag: node.tagName.toLowerCase(),
        attrs,
        html: node.outerHTML,
        children: Array.from(node.childNodes).map(walk).filter(Boolean),
      };
    }

    return Array.from(root.childNodes).map(walk).filter(Boolean);
  }, html);
}

function postProcessBlocks(blocks) {
  return blocks.map((block) => {
    if (block.type === 'step_flow') {
      return {
        ...block,
        steps: block.steps.map((step, index) => ({
          ...step,
          id: step.id || `step${index + 1}`,
        })),
      };
    }
    if (block.type === 'split_panel') {
      return {
        ...block,
        body_blocks: postProcessBlocks(block.body_blocks || []),
      };
    }
    return block;
  });
}

function sanitizeFigureRef(figureRef) {
  if (!figureRef || typeof figureRef !== 'object' || Array.isArray(figureRef)) {
    return figureRef;
  }

  const nextFigureRef = { ...figureRef };
  for (const key of ['label', 'label_before', 'label_after', 'caption']) {
    if (typeof nextFigureRef[key] === 'string') {
      nextFigureRef[key] = sanitizeTokenString(nextFigureRef[key]);
    }
  }
  return nextFigureRef;
}

function sanitizeTableCells(cells = []) {
  return cells.map((cell) => {
    if (typeof cell === 'string') {
      return sanitizeTokenString(cell);
    }
    if (!cell || typeof cell !== 'object' || Array.isArray(cell)) {
      return cell;
    }
    return {
      ...cell,
      text: typeof cell.text === 'string' ? sanitizeTokenString(cell.text) : cell.text,
    };
  });
}

function sanitizeBlockText(block) {
  if (!block || typeof block !== 'object') {
    return block;
  }

  const nextBlock = { ...block };

  for (const key of ['text', 'title', 'caption', 'label', 'label_before', 'label_after']) {
    if (typeof nextBlock[key] === 'string') {
      nextBlock[key] = sanitizeTokenString(nextBlock[key]);
    }
  }

  if (Array.isArray(nextBlock.items)) {
    nextBlock.items = nextBlock.items.map((item) => {
      if (typeof item === 'string') {
        return sanitizeTokenString(item);
      }
      if (!item || typeof item !== 'object' || Array.isArray(item)) {
        return item;
      }
      return Object.fromEntries(Object.entries(item).map(([key, value]) => {
        if (typeof value === 'string' && ['text', 'label', 'label_before', 'label_after', 'caption'].includes(key)) {
          return [key, sanitizeTokenString(value)];
        }
        if (key === 'figure') {
          return [key, sanitizeFigureRef(value)];
        }
        return [key, value];
      }));
    });
  }

  if (Array.isArray(nextBlock.fields)) {
    nextBlock.fields = nextBlock.fields.map((field) => sanitizeTokenString(field));
  }

  if (Array.isArray(nextBlock.steps)) {
    nextBlock.steps = nextBlock.steps.map((step) => ({
      ...step,
      text: typeof step.text === 'string' ? sanitizeTokenString(step.text) : step.text,
    }));
  }

  if (Array.isArray(nextBlock.headers)) {
    nextBlock.headers = sanitizeTableCells(nextBlock.headers);
  }

  if (Array.isArray(nextBlock.rows)) {
    nextBlock.rows = nextBlock.rows.map((row) => sanitizeTableCells(row));
  }

  if (Array.isArray(nextBlock.figures)) {
    nextBlock.figures = nextBlock.figures.map((figureRef) => sanitizeFigureRef(figureRef));
  }

  if (nextBlock.type === 'split_panel') {
    nextBlock.body_blocks = (nextBlock.body_blocks || []).map((childBlock) => sanitizeBlockText(childBlock));
  }

  return nextBlock;
}

function sanitizeChapterContent(chapter) {
  return {
    ...chapter,
    title: typeof chapter.title === 'string' ? sanitizeTokenString(chapter.title) : chapter.title,
    toc_title: typeof chapter.toc_title === 'string' ? sanitizeTokenString(chapter.toc_title) : chapter.toc_title,
    header_ref: typeof chapter.header_ref === 'string' ? sanitizeTokenString(chapter.header_ref) : chapter.header_ref,
    pages: (chapter.pages || []).map((page) => ({
      ...page,
      section_title: typeof page.section_title === 'string' ? sanitizeTokenString(page.section_title) : page.section_title,
      blocks: (page.blocks || []).map((block) => sanitizeBlockText(block)),
    })),
  };
}

function finalizePageBlocks(chapterNo, blocks) {
  let warrantyTableIndex = 0;

  return blocks.map((block) => {
    if (block.type === 'split_panel') {
      return {
        ...block,
        body_blocks: finalizePageBlocks(chapterNo, block.body_blocks || []),
      };
    }

    if ((block.type === 'warning_box' || block.type === 'caution_box' || block.type === 'notice_box') && !block.title) {
      const nextBlock = { ...block };
      delete nextBlock.title;
      return nextBlock;
    }

    if (block.type === 'table_ref' && Array.isArray(block.rows) && block.rows.length === 0) {
      if (chapterNo === '03' && Array.isArray(block.headers) && block.headers.length === 4) {
        return { type: 'table_ref', table: 'parts' };
      }
      if (chapterNo === '04' && Array.isArray(block.headers) && block.headers.length === 2) {
        return { type: 'table_ref', table: 'buttons' };
      }
      if (chapterNo === '05' && Array.isArray(block.headers) && block.headers.length === 2) {
        return { type: 'table_ref', table: 'specs' };
      }
      if (chapterNo === '10' && !block.headers) {
        warrantyTableIndex += 1;
        return { type: 'table_ref', table: warrantyTableIndex === 1 ? 'brand_info' : 'manufacturer_info' };
      }
    }

    return block;
  });
}

function assignUsageRefs(productDir, imagesManifest) {
  function directImageIds(block) {
    const ids = [];
    if (!block || typeof block !== 'object') return ids;
    if (block.icon && typeof block.icon === 'string') ids.push(block.icon);
    if (typeof block.figure === 'string') ids.push(block.figure);
    (block.figures || []).forEach((figureRef) => {
      ids.push(typeof figureRef === 'string' ? figureRef : figureRef.figure);
    });
    (block.items || []).forEach((item) => {
      if (item?.figure) ids.push(item.figure);
    });
    return ids.filter(Boolean);
  }

  function visitBlock(block, chapterId, pageKey, blockIndex) {
    if (!block || typeof block !== 'object') return;

    if (block.type === 'step_flow') {
      (block.steps || []).forEach((step, stepIndex) => {
        for (const figureRef of step.figures || []) {
          const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
          if (!imagesManifest[imageId]) continue;
          if (imagesManifest[imageId].kind === 'shared') continue;
          imagesManifest[imageId].kind = 'procedural';
          imagesManifest[imageId].usage_ref = `${chapterId}.${pageKey}.${step.id || `step${stepIndex + 1}`}`;
        }
      });
    }

    for (const imageId of directImageIds(block)) {
      if (!imagesManifest[imageId] || imagesManifest[imageId].kind === 'shared') continue;
      if (imagesManifest[imageId].kind === 'procedural') {
        imagesManifest[imageId].usage_ref = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}`;
      }
    }

    if (block.type === 'split_panel') {
      (block.figures || []).forEach((figureRef, figureIndex) => {
        const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
        if (!imagesManifest[imageId] || imagesManifest[imageId].kind === 'shared') return;
        imagesManifest[imageId].kind = 'procedural';
        imagesManifest[imageId].usage_ref = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}.figure${figureIndex + 1}`;
      });
      (block.body_blocks || []).forEach((childBlock, childIndex) => {
        visitBlock(childBlock, chapterId, pageKey, `${blockIndex}-${childIndex}`);
      });
    }
  }

  for (const lang of langs) {
    const manifestPath = path.join(productDir, 'content', lang, 'manifest.json');
    if (!fs.existsSync(manifestPath)) continue;
    const manifest = readJson(manifestPath);
    for (const chapterEntry of manifest.chapters) {
      const chapter = readJson(path.join(productDir, 'content', lang, 'chapters', chapterEntry.file));
      (chapter.pages || []).forEach((page, pageIndex) => {
        const pageKey = page.page_id || `page${pageIndex + 1}`;
        (page.blocks || []).forEach((block, blockIndex) => {
          visitBlock(block, chapter.chapter_id, pageKey, blockIndex);
        });
      });
    }
  }
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    for (const product of products) {
      const productDir = path.join(swissRoot, 'products', product);
      const imagesManifest = readJson(path.join(productDir, 'images.json'));
      const imageRegistry = createImageRegistry(imagesManifest);

      for (const lang of langs) {
        const contentRoot = path.join(productDir, 'content', lang);
        const manifestPath = path.join(contentRoot, 'manifest.json');
        if (!fs.existsSync(manifestPath)) continue;

        const manifest = readJson(manifestPath);
        for (const chapterEntry of manifest.chapters) {
          const chapterPath = path.join(contentRoot, 'chapters', chapterEntry.file);
          let chapter = readJson(chapterPath);
          let chapterChanged = false;

          chapter.pages = await Promise.all((chapter.pages || []).map(async (chapterPage, pageIndex) => {
            const pageId = chapterPage.page_id || `page${pageIndex + 1}`;
            const blocks = [];

            for (const block of chapterPage.blocks || []) {
              if (block.type !== 'html_fragment') {
                blocks.push(block);
                continue;
              }

              const ast = await buildAst(page, block.html || '');
              const parsedBlocks = finalizePageBlocks(
                chapter.chapter_no,
                postProcessBlocks(parseNodes(ast, { imageRegistry }, chapter.chapter_id, pageIndex))
              );
              blocks.push(...parsedBlocks);
              chapterChanged = true;
            }

            return {
              ...chapterPage,
              page_id: pageId,
              blocks,
            };
          }));

          chapter = sanitizeChapterContent(chapter);

          writeJson(chapterPath, chapter);
          if (chapterChanged) {
            console.log(`Normalized ${product}/${lang}/${chapterEntry.file}`);
          }
        }
      }

      assignUsageRefs(productDir, imagesManifest);
      writeJson(path.join(productDir, 'images.json'), imagesManifest);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
