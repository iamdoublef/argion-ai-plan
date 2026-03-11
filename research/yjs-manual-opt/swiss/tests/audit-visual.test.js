const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const toolPath = path.resolve(__dirname, '..', 'tools', 'audit-visual.js');

// ---------------------------------------------------------------------------
// Helper: create minimal HTML fixture for testing
// ---------------------------------------------------------------------------
function createTestHtml(tmpDir, content, { styles = '' } = {}) {
  const html = `<!DOCTYPE html>
<html><head>
<style>
.page {
  width: 148mm; height: 210mm; padding: 10mm;
  position: relative; overflow: hidden; background: #fff;
  page-break-after: always;
}
img { max-width: 100%; height: auto; }
${styles}
</style>
</head><body>
${content}
</body></html>`;
  const filePath = path.join(tmpDir, 'test.html');
  fs.writeFileSync(filePath, html, 'utf8');
  return filePath;
}

function makeTmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'audit-visual-'));
}

// ---------------------------------------------------------------------------
// Unit tests: classifyOverlap (cover page absolute elements)
// ---------------------------------------------------------------------------
test('classifyOverlap: absolute-positioned cover element → INFO not ERROR', async () => {
  const { classifyOverlap } = require(toolPath);
  const result = classifyOverlap({
    pageIndex: 0,
    childA: { position: 'static', tag: 'DIV' },
    childB: { position: 'absolute', tag: 'DIV', className: 'cover-bottom' },
    overlapPx: 58,
  });
  assert.equal(result.severity, 'INFO');
});

test('classifyOverlap: non-cover page overlap → ERROR', async () => {
  const { classifyOverlap } = require(toolPath);
  const result = classifyOverlap({
    pageIndex: 5,
    childA: { position: 'static', tag: 'DIV' },
    childB: { position: 'static', tag: 'DIV' },
    overlapPx: 30,
  });
  assert.equal(result.severity, 'ERROR');
});

// ---------------------------------------------------------------------------
// Unit tests: classifyImageOverflow
// ---------------------------------------------------------------------------
test('classifyImageOverflow: image exceeds page right → ERROR', async () => {
  const { classifyImageOverflow } = require(toolPath);
  const result = classifyImageOverflow({
    src: 'image30.svg',
    imgRight: 769,
    pageRight: 560,
  });
  assert.equal(result.severity, 'ERROR');
  assert.ok(result.overflowPx > 0);
});

test('classifyImageOverflow: image within page → null', async () => {
  const { classifyImageOverflow } = require(toolPath);
  const result = classifyImageOverflow({
    src: 'image28.svg',
    imgRight: 274,
    pageRight: 560,
  });
  assert.equal(result, null);
});

// ---------------------------------------------------------------------------
// Unit tests: classifyDataResidual
// ---------------------------------------------------------------------------
test('classifyDataResidual: detects {{}} template variable residual', async () => {
  const { classifyDataResidual } = require(toolPath);
  const results = classifyDataResidual('Hello {{brand.name}} world');
  assert.ok(results.length > 0);
  assert.equal(results[0].severity, 'ERROR');
  assert.ok(results[0].match.includes('brand.name'));
});

test('classifyDataResidual: detects undefined literal', async () => {
  const { classifyDataResidual } = require(toolPath);
  const results = classifyDataResidual('Value is undefined here');
  assert.ok(results.length > 0);
});

test('classifyDataResidual: clean text → empty', async () => {
  const { classifyDataResidual } = require(toolPath);
  const results = classifyDataResidual('This is normal text with no issues');
  assert.equal(results.length, 0);
});

// ---------------------------------------------------------------------------
// Unit tests: classifySourceLangResidual
// ---------------------------------------------------------------------------
test('classifySourceLangResidual: Chinese chars in EN locale → ERROR', async () => {
  const { classifySourceLangResidual } = require(toolPath);
  const results = classifySourceLangResidual('en', '未达到设定真空度');
  assert.ok(results.length > 0);
  assert.equal(results[0].severity, 'ERROR');
});

test('classifySourceLangResidual: no Chinese in EN → empty', async () => {
  const { classifySourceLangResidual } = require(toolPath);
  const results = classifySourceLangResidual('en', 'Target vacuum not reached');
  assert.equal(results.length, 0);
});

test('classifySourceLangResidual: Chinese in zh-CN → empty (source lang)', async () => {
  const { classifySourceLangResidual } = require(toolPath);
  const results = classifySourceLangResidual('zh-CN', '未达到设定真空度');
  assert.equal(results.length, 0);
});

// ---------------------------------------------------------------------------
// Integration test: auditVisual with clean HTML
// ---------------------------------------------------------------------------
test('auditVisual: clean single-page HTML → no errors', async () => {
  const { auditVisual } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const htmlPath = createTestHtml(tmpDir,
      '<div class="page"><p>Hello world</p></div>');
    const result = await auditVisual(htmlPath);
    assert.equal(result.summary.errors, 0);
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

// ---------------------------------------------------------------------------
// Integration test: auditVisual detects horizontal overflow
// ---------------------------------------------------------------------------
test('auditVisual: wide image → detects overflow', async () => {
  const { auditVisual } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    // Create an oversized inline element
    const htmlPath = createTestHtml(tmpDir,
      `<div class="page">
        <div style="width:200mm;height:10mm;background:red;"></div>
      </div>`);
    const result = await auditVisual(htmlPath);
    assert.ok(result.summary.errors > 0 || result.summary.warnings > 0,
      'Should detect overflow for 200mm element in 148mm page');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

// ---------------------------------------------------------------------------
// Integration test: auditVisual returns structured JSON
// ---------------------------------------------------------------------------
test('auditVisual: returns proper structure', async () => {
  const { auditVisual } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const htmlPath = createTestHtml(tmpDir,
      '<div class="page"><p>Test</p></div>');
    const result = await auditVisual(htmlPath);
    assert.ok('issues' in result);
    assert.ok('summary' in result);
    assert.ok(Array.isArray(result.issues));
    assert.equal(typeof result.summary.errors, 'number');
    assert.equal(typeof result.summary.warnings, 'number');
    assert.equal(typeof result.summary.infos, 'number');
    assert.equal(typeof result.summary.pages, 'number');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

// ---------------------------------------------------------------------------
// Integration test: auditVisual detects data residuals
// ---------------------------------------------------------------------------
test('auditVisual: detects {{}} residual in rendered text', async () => {
  const { auditVisual } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const htmlPath = createTestHtml(tmpDir,
      '<div class="page"><p>Brand: {{brand.name}}</p></div>');
    const result = await auditVisual(htmlPath);
    const residualIssues = result.issues.filter(i => i.type === 'DATA_RESIDUAL');
    assert.ok(residualIssues.length > 0, 'Should detect unreplaced template variable');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});
