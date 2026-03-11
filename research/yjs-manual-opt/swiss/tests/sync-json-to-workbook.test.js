const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const XLSX = require('xlsx');

const toolPath = path.resolve(__dirname, '..', 'tools', 'sync-json-to-workbook.js');

function makeTmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'sync-wb-'));
}

function createTestWorkbook(filePath, rows) {
  const ws = XLSX.utils.json_to_sheet(rows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'strings');
  XLSX.writeFile(wb, filePath);
}

function readWorkbookRows(filePath) {
  const wb = XLSX.readFile(filePath);
  return XLSX.utils.sheet_to_json(wb.Sheets.strings, { defval: '' });
}

// ---------------------------------------------------------------------------
// Unit test: diffStrings
// ---------------------------------------------------------------------------
test('diffStrings: detects changed values', () => {
  const { diffStrings } = require(toolPath);
  const compiled = { 'key.1': 'English text', 'key.2': 'Same' };
  const workbook = { 'key.1': '中文原文', 'key.2': 'Same' };
  const diff = diffStrings(compiled, workbook);
  assert.equal(diff.length, 1);
  assert.equal(diff[0].text_id, 'key.1');
  assert.equal(diff[0].newValue, 'English text');
  assert.equal(diff[0].oldValue, '中文原文');
});

test('diffStrings: no changes → empty diff', () => {
  const { diffStrings } = require(toolPath);
  const compiled = { 'a': 'hello', 'b': 'world' };
  const workbook = { 'a': 'hello', 'b': 'world' };
  const diff = diffStrings(compiled, workbook);
  assert.equal(diff.length, 0);
});

test('diffStrings: new key in compiled (not in workbook) → included', () => {
  const { diffStrings } = require(toolPath);
  const compiled = { 'a': 'hello', 'new.key': 'brand new' };
  const workbook = { 'a': 'hello' };
  const diff = diffStrings(compiled, workbook);
  assert.equal(diff.length, 1);
  assert.equal(diff[0].text_id, 'new.key');
  assert.equal(diff[0].oldValue, undefined);
});

// ---------------------------------------------------------------------------
// Integration test: syncToWorkbook updates xlsx
// ---------------------------------------------------------------------------
test('syncToWorkbook: updates changed target_text in xlsx', () => {
  const { syncToWorkbook } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const wbPath = path.join(tmpDir, 'en.xlsx');
    createTestWorkbook(wbPath, [
      { text_id: 'key.1', source_text: '中文', target_text: '中文' },
      { text_id: 'key.2', source_text: '保持', target_text: 'Keep' },
    ]);

    const compiled = { 'key.1': 'English translation', 'key.2': 'Keep' };
    const result = syncToWorkbook(compiled, wbPath);

    assert.equal(result.updated, 1);
    assert.equal(result.unchanged, 1);

    // Verify the workbook was actually updated
    const rows = readWorkbookRows(wbPath);
    assert.equal(rows[0].target_text, 'English translation');
    assert.equal(rows[1].target_text, 'Keep');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

test('syncToWorkbook: preserves other columns', () => {
  const { syncToWorkbook } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const wbPath = path.join(tmpDir, 'en.xlsx');
    createTestWorkbook(wbPath, [
      { text_id: 'key.1', source_text: '原文', target_text: '旧翻译', context: 'header' },
    ]);

    const compiled = { 'key.1': 'New translation' };
    syncToWorkbook(compiled, wbPath);

    const rows = readWorkbookRows(wbPath);
    assert.equal(rows[0].target_text, 'New translation');
    assert.equal(rows[0].source_text, '原文');
    assert.equal(rows[0].context, 'header');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

test('syncToWorkbook: dry-run does not modify file', () => {
  const { syncToWorkbook } = require(toolPath);
  const tmpDir = makeTmpDir();
  try {
    const wbPath = path.join(tmpDir, 'en.xlsx');
    createTestWorkbook(wbPath, [
      { text_id: 'key.1', source_text: '中文', target_text: '中文' },
    ]);

    const statBefore = fs.statSync(wbPath).mtimeMs;
    const compiled = { 'key.1': 'English' };
    const result = syncToWorkbook(compiled, wbPath, { dryRun: true });

    assert.equal(result.updated, 1);
    // File should not be modified
    const rowsAfter = readWorkbookRows(wbPath);
    assert.equal(rowsAfter[0].target_text, '中文');
  } finally {
    fs.rmSync(tmpDir, { recursive: true });
  }
});
