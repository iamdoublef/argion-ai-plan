const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const swissDir = path.resolve(__dirname, '..');
const templateDir = path.join(swissDir, 'template');
const outputDir = path.join(swissDir, 'output');

function readFile(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function runNodeScript(args) {
  return execFileSync('node', args, {
    cwd: swissDir,
    stdio: 'pipe',
    encoding: 'utf8',
  });
}

function buildHtml(product, region) {
  return runNodeScript(['tools/build-variant.js', '--product', path.join('products', product), '--region', region]);
}

function exportDocx(product, region) {
  return runNodeScript(['tools/export-docx.js', '--product', path.join('products', product), '--region', region]);
}

test('Swiss master templates use AUTO_TOC, DOCUMENT_BODY and theme/localized placeholders', () => {
  const templates = [
    'v23-master-cn.html',
    'v23-master-en.html',
    'v23-master-de.html',
    'v23-master-it.html',
    'imt050-master-cn.html',
    'imt050-master-en.html',
    'imt050-master-de.html',
    'imt050-master-it.html',
  ];

  for (const templateName of templates) {
    const template = readFile(path.join(templateDir, templateName));
    assert.match(template, /\{\{#AUTO_TOC\}\}/);
    assert.match(template, /\{\{#DOCUMENT_BODY\}\}/);
    assert.match(template, /\{\{#THEME_STYLE_OVERRIDES\}\}/);
    assert.match(template, /\{\{localized\.product_name\}\}/);
    assert.match(template, /\{\{localized\.document_title/);
    assert.doesNotMatch(template, /\{\{#CONTENT_BODY\}\}/);
  }

  const documentStart = readFile(path.join(templateDir, 'shared', 'cn', 'document-start.html'));
  assert.match(documentStart, /\{\{localized\.product_name\}\}/);
  assert.match(documentStart, /\{\{localized\.document_title\}\}/);
  assert.doesNotMatch(documentStart, /\{\{product\.name_/);
});

test('products use structure source, locale catalogs and translation workbooks', () => {
  const products = ['imt050', 'v23'];
  const locales = ['zh-CN', 'zh-HK', 'zh-TW', 'en', 'de', 'it'];

  for (const product of products) {
    const productDir = path.join(swissDir, 'products', product);
    assert.ok(fs.existsSync(path.join(productDir, 'product.json')));
    assert.ok(fs.existsSync(path.join(productDir, 'images.json')));
    assert.ok(fs.existsSync(path.join(productDir, 'content', 'source', 'manifest.json')));
    assert.ok(fs.existsSync(path.join(productDir, 'content', 'source', 'chapters')));
    assert.ok(!fs.existsSync(path.join(productDir, 'config.json')), `${product} still has legacy config.json`);

    const chaptersDir = path.join(productDir, 'content', 'source', 'chapters');
    assert.ok(fs.readdirSync(chaptersDir).length > 0, `${product} source chapters missing`);

    for (const locale of locales) {
      assert.ok(fs.existsSync(path.join(productDir, 'i18n', 'compiled', `${locale}.json`)), `${product} missing compiled ${locale}`);
      assert.ok(fs.existsSync(path.join(productDir, 'i18n', 'workbooks', `${locale}.xlsx`)), `${product} missing workbook ${locale}`);
    }

    for (const chapterFile of fs.readdirSync(chaptersDir)) {
      const chapterText = readFile(path.join(chaptersDir, chapterFile));
      assert.doesNotMatch(chapterText, /"type"\s*:\s*"html_fragment"/, `${product}/${chapterFile} still contains html_fragment`);
      assert.doesNotMatch(chapterText, /<[A-Za-z/][^>]*>/, `${product}/${chapterFile} still contains raw HTML`);
    }
  }
});

test('build-variant and docx exporter use locale catalogs and theme-driven output without runtime traditional conversion', () => {
  const buildVariantSource = readFile(path.join(swissDir, 'tools', 'build-variant.js'));
  const exportDocxSource = readFile(path.join(swissDir, 'tools', 'export-docx.js'));

  assert.match(buildVariantSource, /loadLocaleCatalog/);
  assert.match(buildVariantSource, /buildLocalizedRuntimeData/);
  assert.match(buildVariantSource, /THEME_STYLE_OVERRIDES/);
  assert.doesNotMatch(buildVariantSource, /region\.convert\s*===\s*['"]traditional['"]/);
  assert.doesNotMatch(buildVariantSource, /content\.\$\{templateLang\}\.json/);
  assert.doesNotMatch(buildVariantSource, /CONTENT_BODY/);

  assert.match(exportDocxSource, /loadLocaleCatalog/);
  assert.match(exportDocxSource, /buildLocalizedRuntimeData/);
  assert.match(exportDocxSource, /resolveBrandTheme/);
});

test('independent zh-HK and zh-TW locale catalogs exist and differ from zh-CN seeds', () => {
  const productDir = path.join(swissDir, 'products', 'imt050', 'i18n', 'compiled');
  const cn = JSON.parse(readFile(path.join(productDir, 'zh-CN.json')));
  const hk = JSON.parse(readFile(path.join(productDir, 'zh-HK.json')));
  const tw = JSON.parse(readFile(path.join(productDir, 'zh-TW.json')));

  assert.equal(hk.locale, 'zh-HK');
  assert.equal(tw.locale, 'zh-TW');
  assert.notDeepEqual(hk.strings, cn.strings);
  assert.notDeepEqual(tw.strings, cn.strings);
  assert.notEqual(
    hk.strings['content.chapter.10-warranty.title'],
    tw.strings['content.chapter.10-warranty.title']
  );
});

test('HTML builds use localized catalogs with no unresolved placeholders', () => {
  buildHtml('imt050', 'cn');
  buildHtml('imt050', 'hk');
  buildHtml('imt050', 'tw');
  buildHtml('v23', 'gb');

  const imtCn = readFile(path.join(outputDir, 'imt050-wevac-eu-cn.html'));
  const imtHk = readFile(path.join(outputDir, 'imt050-wevac-eu-hk.html'));
  const imtTw = readFile(path.join(outputDir, 'imt050-wevac-us-tw.html'));
  const v23Gb = readFile(path.join(outputDir, 'v23-wevac-eu-gb.html'));

  for (const html of [imtCn, imtHk, imtTw, v23Gb]) {
    assert.doesNotMatch(html, /\{\{[^}]+\}\}/);
    assert.match(html, /toc-item/);
  }

  assert.notEqual(imtCn, imtHk);
  assert.notEqual(imtCn, imtTw);
});

test('ODM DOCX export works from the same source content', () => {
  exportDocx('imt050', 'hk');
  exportDocx('v23', 'gb');

  const imtDocx = path.join(outputDir, 'imt050-wevac-eu-hk.docx');
  const v23Docx = path.join(outputDir, 'v23-wevac-eu-gb.docx');

  assert.ok(fs.existsSync(imtDocx));
  assert.ok(fs.existsSync(v23Docx));
  assert.ok(fs.statSync(imtDocx).size > 0);
  assert.ok(fs.statSync(v23Docx).size > 0);
});
