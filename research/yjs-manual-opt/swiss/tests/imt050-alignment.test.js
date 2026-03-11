const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const swissDir = path.resolve(__dirname, '..');
const outputDir = path.join(swissDir, 'output');

function buildVariant(region) {
  execFileSync(
    'node',
    ['tools/build-variant.js', '--product', 'products/imt050', '--region', region],
    {
      cwd: swissDir,
      stdio: 'pipe',
      encoding: 'utf8',
    }
  );
}

function readOutput(filename) {
  return fs.readFileSync(path.join(outputDir, filename), 'utf8');
}

function readCatalog(locale) {
  return JSON.parse(
    fs.readFileSync(
      path.join(swissDir, 'products', 'imt050', 'i18n', 'compiled', `${locale}.json`),
      'utf8'
    )
  );
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test('CN output uses the V23-style 10-chapter skeleton', () => {
  buildVariant('cn');
  const html = readOutput('imt050-wevac-eu-cn.html');
  const catalog = readCatalog('zh-CN');

  const tocMatches = html.match(/class="toc-item"/g) ?? [];
  assert.equal(tocMatches.length, 10, 'expected 10 TOC items');

  assert.match(
    html,
    new RegExp(`<span class="toc-chapter">02<\\/span><span class="toc-name">${escapeRegExp(catalog.strings['content.chapter.02-usage-tips.toc_title'])}<\\/span>`)
  );
  assert.match(
    html,
    new RegExp(`<h2 class="section-title"><span class="chapter-num">04<\\/span>${escapeRegExp(catalog.strings['content.chapter.04-features.title'])}<\\/h2>`)
  );
  assert.match(
    html,
    new RegExp(`<span class="toc-chapter">09<\\/span><span class="toc-name">${escapeRegExp(catalog.strings['content.chapter.09-installation-storage-disposal.toc_title'])}<\\/span>`)
  );
  assert.match(
    html,
    new RegExp(`<h2 class="section-title"><span class="chapter-num">10<\\/span>${escapeRegExp(catalog.strings['content.chapter.10-warranty.title'])}<\\/h2>`)
  );
  assert.match(html, /src="\.\/images_imt050\/image31\.png"/);
});

test('EN output mirrors the same chapter skeleton', () => {
  buildVariant('gb');
  const html = readOutput('imt050-wevac-eu-gb.html');
  const catalog = readCatalog('en');

  const tocMatches = html.match(/class="toc-item"/g) ?? [];
  assert.equal(tocMatches.length, 10, 'expected 10 TOC items');

  assert.match(
    html,
    new RegExp(`<span class="toc-chapter">02<\\/span><span class="toc-name">${escapeRegExp(catalog.strings['content.chapter.02-usage-tips.toc_title'])}<\\/span>`)
  );
  assert.match(
    html,
    new RegExp(`<h2 class="section-title"><span class="chapter-num">04<\\/span>${escapeRegExp(catalog.strings['content.chapter.04-features.title'])}<\\/h2>`)
  );
  assert.match(
    html,
    new RegExp(`<span class="toc-chapter">09<\\/span><span class="toc-name">${escapeRegExp(catalog.strings['content.chapter.09-installation-storage-disposal.toc_title'])}<\\/span>`)
  );
  assert.match(
    html,
    new RegExp(`<h2 class="section-title"><span class="chapter-num">10<\\/span>${escapeRegExp(catalog.strings['content.chapter.10-warranty.title'])}<\\/h2>`)
  );
  assert.match(html, /src="\.\/images_imt050\/image31\.png"/);
});
