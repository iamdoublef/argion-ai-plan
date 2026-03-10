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

test('CN output uses the V23-style 10-chapter skeleton', () => {
  buildVariant('cn');
  const html = readOutput('imt050-wevac-eu-cn.html');

  const tocMatches = html.match(/class="toc-item"/g) ?? [];
  assert.equal(tocMatches.length, 10, 'expected 10 TOC items');

  assert.match(html, /<span class="toc-chapter">02<\/span><span class="toc-name">产品及使用提示<\/span>/);
  assert.match(html, /<h2 class="section-title"><span class="chapter-num">04<\/span>产品功能<\/h2>/);
  assert.match(html, /<span class="toc-chapter">09<\/span><span class="toc-name">安装运输、存储与拆除<\/span>/);
  assert.match(html, /<h2 class="section-title"><span class="chapter-num">10<\/span>品牌与保修信息<\/h2>/);
  assert.match(html, /src="\.\/images_imt050\/image31\.png"/);
});

test('EN output mirrors the same chapter skeleton', () => {
  buildVariant('gb');
  const html = readOutput('imt050-wevac-eu-gb.html');

  const tocMatches = html.match(/class="toc-item"/g) ?? [];
  assert.equal(tocMatches.length, 10, 'expected 10 TOC items');

  assert.match(html, /<span class="toc-chapter">02<\/span><span class="toc-name">Product Usage Tips<\/span>/);
  assert.match(html, /<h2 class="section-title"><span class="chapter-num">04<\/span>Product Features<\/h2>/);
  assert.match(html, /<span class="toc-chapter">09<\/span><span class="toc-name">Installation, Transport, Storage & Disposal<\/span>/);
  assert.match(html, /<h2 class="section-title"><span class="chapter-num">10<\/span>Brand & Warranty Information<\/h2>/);
  assert.match(html, /src="\.\/images_imt050\/image31\.png"/);
});
