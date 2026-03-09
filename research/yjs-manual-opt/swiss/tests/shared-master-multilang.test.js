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

test('V23 and IMT050 EN/DE/IT outputs share the same A5 base shell and shared components', () => {
  const cases = [
    { product: 'v23', region: 'gb', file: 'v23-wevac-eu-gb.html' },
    { product: 'imt050', region: 'gb', file: 'imt050-wevac-eu-gb.html' },
    { product: 'v23', region: 'de', file: 'v23-wevac-eu-de.html' },
    { product: 'imt050', region: 'de', file: 'imt050-wevac-eu-de.html' },
    { product: 'v23', region: 'it', file: 'v23-wevac-eu-it.html' },
    { product: 'imt050', region: 'it', file: 'imt050-wevac-eu-it.html' },
  ];

  for (const { product, region, file } of cases) {
    buildVariant(product, region);
    const html = readOutput(file);

    assert.match(html, /SHARED SWISS BASE MASTER/);
    assert.match(html, /@page\s*\{\s*size:\s*148mm 210mm;\s*margin:\s*0;/);
    assert.match(html, /--page-width:\s*148mm;/);
    assert.match(html, /--page-height:\s*210mm;/);
    assert.match(html, /--page-margin:\s*10mm;/);
    assert.match(html, /\.page\s*\{[^}]*width:\s*var\(--page-width\);[^}]*min-height:\s*var\(--page-height\);/);
    assert.match(html, /class="cover-bottom"/);
    assert.match(html, /<div class="toc-item">/);

    if (product === 'imt050') {
      assert.doesNotMatch(html, /size:\s*210mm 297mm/);
      assert.doesNotMatch(html, /class="toc-list"/);
      assert.doesNotMatch(html, /class="step-row"/);
    }
  }
});
