const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');

const toolPath = path.resolve(__dirname, '..', 'tools', 'build-all.js');

// ---------------------------------------------------------------------------
// Unit tests: enumerateProducts
// ---------------------------------------------------------------------------
test('enumerateProducts: finds v23 and imt050', () => {
  const { enumerateProducts } = require(toolPath);
  const productsDir = path.resolve(__dirname, '..', 'products');
  const products = enumerateProducts(productsDir);
  assert.ok(products.length >= 2);
  const names = products.map(p => path.basename(p));
  assert.ok(names.includes('v23'));
  assert.ok(names.includes('imt050'));
});

// ---------------------------------------------------------------------------
// Unit tests: enumerateVariants
// ---------------------------------------------------------------------------
test('enumerateVariants: returns region×brand pairs from product config', () => {
  const { enumerateVariants } = require(toolPath);
  const productDir = path.resolve(__dirname, '..', 'products', 'v23');
  const variants = enumerateVariants(productDir);
  assert.ok(variants.length >= 6, `Expected ≥6 variants, got ${variants.length}`);
  // Each variant should have region and brand
  for (const v of variants) {
    assert.ok(v.region, 'variant must have region');
    assert.ok(v.brand, 'variant must have brand');
  }
});

// ---------------------------------------------------------------------------
// Unit tests: buildReport
// ---------------------------------------------------------------------------
test('buildReport: aggregates variant results correctly', () => {
  const { buildReport } = require(toolPath);
  const variantResults = [
    { product: 'v23', region: 'cn', brand: 'wevac', htmlFile: 'v23-wevac-eu-cn.html',
      audit: { summary: { errors: 0, warnings: 0, infos: 0, pages: 14 } } },
    { product: 'v23', region: 'gb', brand: 'wevac', htmlFile: 'v23-wevac-eu-gb.html',
      audit: { summary: { errors: 1, warnings: 0, infos: 0, pages: 23 } } },
  ];
  const report = buildReport(variantResults);
  assert.equal(report.total, 2);
  assert.equal(report.passed, 1);
  assert.equal(report.failed, 1);
});

test('buildReport: all pass → overall PASS', () => {
  const { buildReport } = require(toolPath);
  const variantResults = [
    { product: 'v23', region: 'cn', brand: 'wevac', htmlFile: 'a.html',
      audit: { summary: { errors: 0, warnings: 1, infos: 0, pages: 14 } } },
  ];
  const report = buildReport(variantResults);
  assert.equal(report.overall, 'PASS');
});

test('buildReport: any error → overall FAIL', () => {
  const { buildReport } = require(toolPath);
  const variantResults = [
    { product: 'v23', region: 'cn', brand: 'wevac', htmlFile: 'a.html',
      audit: { summary: { errors: 0, warnings: 0, infos: 0, pages: 14 } } },
    { product: 'v23', region: 'gb', brand: 'wevac', htmlFile: 'b.html',
      audit: { summary: { errors: 2, warnings: 0, infos: 0, pages: 23 } } },
  ];
  const report = buildReport(variantResults);
  assert.equal(report.overall, 'FAIL');
});
