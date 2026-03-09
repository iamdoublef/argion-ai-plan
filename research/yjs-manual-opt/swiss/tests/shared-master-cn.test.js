const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const swissDir = path.resolve(__dirname, '..');
const outputDir = path.join(swissDir, 'output');

function buildVariant(product, region) {
  execFileSync(
    'node',
    ['tools/build-variant.js', '--product', `products/${product}`, '--region', region],
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

test('V23 CN and IMT050 CN share the same A5 CN master geometry and shared shell markers', () => {
  buildVariant('v23', 'cn');
  buildVariant('imt050', 'cn');

  const v23Html = readOutput('v23-wevac-eu-cn.html');
  const imt050Html = readOutput('imt050-wevac-eu-cn.html');

  for (const html of [v23Html, imt050Html]) {
    assert.match(html, /SHARED SWISS CN MASTER/);
    assert.match(html, /@page\s*\{\s*size:\s*148mm 210mm;\s*margin:\s*0;/);
    assert.match(html, /--page-width:\s*148mm;/);
    assert.match(html, /--page-height:\s*210mm;/);
    assert.match(html, /--page-margin:\s*10mm;/);
    assert.match(html, /\.page\s*\{[^}]*width:\s*var\(--page-width\);[^}]*min-height:\s*var\(--page-height\);/);
    assert.match(html, /<div class="cover-divider"><\/div>/);
    assert.match(html, /class="cover-bottom"/);
    assert.match(html, /<div class="toc-item">/);
  }

  assert.doesNotMatch(imt050Html, /size:\s*210mm 297mm/);
  assert.doesNotMatch(imt050Html, /class="toc-list"/);
});
