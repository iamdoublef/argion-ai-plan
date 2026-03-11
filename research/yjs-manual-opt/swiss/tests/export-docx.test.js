const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { Packer } = require('docx');

const swissDir = path.resolve(__dirname, '..');
const exportDocxModulePath = path.join(swissDir, 'tools', 'export-docx.js');

function loadExportDocxModule(productName) {
  const prevArgv = process.argv.slice();
  delete require.cache[exportDocxModulePath];
  process.argv = [
    process.argv[0],
    exportDocxModulePath,
    '--product',
    path.join(swissDir, 'products', productName),
  ];
  const mod = require(exportDocxModulePath);
  process.argv = prevArgv;
  return mod;
}

test('buildDocx returns A5 Word profile and themed document for IMT050 ACT CN', async () => {
  const { buildDocx, DOCX_PROFILE } = loadExportDocxModule('imt050');
  const result = buildDocx('cn', 'act');

  assert.equal(result.model, 'IMT050');
  assert.equal(result.activeBrand, 'act');
  assert.equal(result.locale, 'zh-CN');
  assert.equal(result.profile.page.width, DOCX_PROFILE.page.width);
  assert.equal(result.profile.page.height, DOCX_PROFILE.page.height);
  assert.equal(result.theme.accent, 'C76A1B');
  assert.equal(result.theme.tableHeaderFill, 'C76A1B');

  const buffer = await Packer.toBuffer(result.doc);
  assert.ok(buffer.length > 50_000);
});

test('buildDocx returns A5 Word profile and themed document for V23 Vesta GB', async () => {
  const { buildDocx } = loadExportDocxModule('v23');
  const result = buildDocx('gb', 'vesta');

  assert.equal(result.model, 'V23');
  assert.equal(result.activeBrand, 'vesta');
  assert.equal(result.locale, 'en');
  assert.equal(result.theme.accent, '2E75B6');
  assert.equal(result.theme.tableHeaderFill, '2E75B6');

  const buffer = await Packer.toBuffer(result.doc);
  assert.ok(buffer.length > 50_000);
});

test('writeDocx creates a DOCX output from the shared JSON single source', async () => {
  const { writeDocx } = loadExportDocxModule('imt050');
  const result = await writeDocx('gb', 'wevac');

  assert.match(result.outName, /^imt050-wevac-eu-gb(\.__staged)?\.docx$/);
  assert.ok(fs.existsSync(result.outPath));
});
