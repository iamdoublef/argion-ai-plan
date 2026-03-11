#!/usr/bin/env node
/**
 * build-all.js — Build all variants for one or more products, with optional audit.
 *
 * Usage:
 *   node tools/build-all.js --product products/v23         # All variants for v23
 *   node tools/build-all.js --all                          # All products, all variants
 *   node tools/build-all.js --product products/v23 --audit # Build + audit each variant
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const swissRoot = path.resolve(__dirname, '..');
const productsRoot = path.join(swissRoot, 'products');
const outputDir = path.join(swissRoot, 'output');

// ---------------------------------------------------------------------------
// Enumerate products
// ---------------------------------------------------------------------------
function enumerateProducts(productsDir) {
  return fs.readdirSync(productsDir)
    .map(name => path.join(productsDir, name))
    .filter(p => fs.statSync(p).isDirectory() && fs.existsSync(path.join(p, 'product.json')));
}

// ---------------------------------------------------------------------------
// Enumerate variants for a product
// ---------------------------------------------------------------------------
function enumerateVariants(productDir) {
  const config = JSON.parse(fs.readFileSync(path.join(productDir, 'product.json'), 'utf8'));
  const regions = Object.keys(config.regions || {});
  const brands = Object.keys(config.brands || {});
  const variants = [];
  for (const region of regions) {
    for (const brand of brands) {
      variants.push({ region, brand });
    }
  }
  return variants;
}

// ---------------------------------------------------------------------------
// Build report
// ---------------------------------------------------------------------------
function buildReport(variantResults) {
  const passed = variantResults.filter(r => r.audit.summary.errors === 0).length;
  const failed = variantResults.length - passed;
  return {
    total: variantResults.length,
    passed,
    failed,
    overall: failed === 0 ? 'PASS' : 'FAIL',
    variants: variantResults,
  };
}

// ---------------------------------------------------------------------------
// Build a single variant (calls build-variant.js as subprocess)
// ---------------------------------------------------------------------------
function buildOneVariant(productDir, region, brand) {
  const buildScript = path.join(swissRoot, 'tools', 'build-variant.js');
  const args = ['--product', productDir, '--region', region, '--brand', brand];
  try {
    const stdout = execFileSync('node', [buildScript, ...args], {
      cwd: swissRoot,
      encoding: 'utf8',
      timeout: 30000,
    });
    const match = stdout.match(/Output:\s+(\S+)/);
    return match ? match[1] : null;
  } catch (err) {
    console.error(`  Build failed: ${path.basename(productDir)} ${region} ${brand}`);
    return null;
  }
}

// ---------------------------------------------------------------------------
// Audit a single HTML file
// ---------------------------------------------------------------------------
async function auditOne(htmlFile, locale) {
  const { auditVisual } = require(path.join(swissRoot, 'tools', 'audit-visual.js'));
  const htmlPath = path.join(outputDir, htmlFile);
  return auditVisual(htmlPath, { locale });
}

// ---------------------------------------------------------------------------
// Region → locale mapping
// ---------------------------------------------------------------------------
function regionToLocale(region) {
  const map = { cn: 'zh-CN', gb: 'en', de: 'de', it: 'it', hk: 'zh-HK', tw: 'zh-TW', za: 'en' };
  return map[region] || 'en';
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
async function main() {
  const args = process.argv.slice(2);
  const getArg = (name, fb) => {
    const idx = args.indexOf(`--${name}`);
    return idx !== -1 && args[idx + 1] ? args[idx + 1] : fb;
  };
  const doAll = args.includes('--all');
  const doAudit = args.includes('--audit');
  const productArg = getArg('product', null);

  let productDirs;
  if (doAll) {
    productDirs = enumerateProducts(productsRoot);
  } else if (productArg) {
    productDirs = [path.isAbsolute(productArg) ? productArg : path.resolve(swissRoot, productArg)];
  } else {
    console.error('Usage: --product <path> or --all');
    process.exit(1);
  }

  const allResults = [];

  for (const productDir of productDirs) {
    const productName = path.basename(productDir);
    const variants = enumerateVariants(productDir);
    console.log(`\n=== ${productName.toUpperCase()} (${variants.length} variants) ===`);

    for (const { region, brand } of variants) {
      const htmlFile = buildOneVariant(productDir, region, brand);
      if (!htmlFile) {
        allResults.push({
          product: productName, region, brand, htmlFile: null,
          audit: { summary: { errors: 1, warnings: 0, infos: 0, pages: 0 }, issues: [{ type: 'BUILD_FAILURE', severity: 'ERROR', message: 'Build failed' }] },
        });
        continue;
      }

      let audit;
      if (doAudit) {
        const locale = regionToLocale(region);
        audit = await auditOne(htmlFile, locale);
      } else {
        audit = { summary: { errors: 0, warnings: 0, infos: 0, pages: 0 }, issues: [] };
      }

      const status = audit.summary.errors === 0 ? 'PASS' : 'FAIL';
      console.log(`  [${status}] ${htmlFile} (${audit.summary.errors}E ${audit.summary.warnings}W)`);
      allResults.push({ product: productName, region, brand, htmlFile, audit });
    }
  }

  const report = buildReport(allResults);
  console.log(`\n========== SUMMARY ==========`);
  console.log(`Total: ${report.total} | Passed: ${report.passed} | Failed: ${report.failed}`);
  console.log(`Overall: ${report.overall}`);

  if (args.includes('--json')) {
    const jsonPath = path.join(outputDir, '_audit', 'build-all-report.json');
    fs.mkdirSync(path.dirname(jsonPath), { recursive: true });
    fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2), 'utf8');
    console.log(`Report: ${jsonPath}`);
  }

  process.exit(report.overall === 'PASS' ? 0 : 1);
}

if (require.main === module) {
  main();
}

module.exports = { enumerateProducts, enumerateVariants, buildReport };
