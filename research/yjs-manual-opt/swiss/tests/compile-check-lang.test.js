const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');

const toolPath = path.resolve(__dirname, '..', 'tools', 'compile-translation-workbook.js');

// ---------------------------------------------------------------------------
// Unit tests: checkLanguage
// ---------------------------------------------------------------------------

test('checkLanguage: Chinese text in EN locale → warnings', () => {
  const { checkLanguage } = require(toolPath);
  const strings = {
    'chapter.01.title': 'Safety',
    'chapter.07.row.14': '未达到设定真空度',
    'chapter.07.row.15': '检查密封胶条',
  };
  const warnings = checkLanguage(strings, 'en');
  assert.equal(warnings.length, 2);
  assert.ok(warnings[0].text_id.includes('row.14'));
  assert.ok(warnings[1].text_id.includes('row.15'));
});

test('checkLanguage: clean EN strings → no warnings', () => {
  const { checkLanguage } = require(toolPath);
  const strings = {
    'chapter.01.title': 'Safety',
    'chapter.02.title': 'Tips',
  };
  const warnings = checkLanguage(strings, 'en');
  assert.equal(warnings.length, 0);
});

test('checkLanguage: Chinese text in zh-CN locale → no warnings (source lang)', () => {
  const { checkLanguage } = require(toolPath);
  const strings = {
    'chapter.01.title': '安全信息',
    'chapter.02.title': '使用提示',
  };
  const warnings = checkLanguage(strings, 'zh-CN');
  assert.equal(warnings.length, 0);
});

test('checkLanguage: mixed EN+CN in DE locale → warns for CJK only', () => {
  const { checkLanguage } = require(toolPath);
  const strings = {
    'title': 'Sicherheit',
    'mixed': 'German text 但有中文',
  };
  const warnings = checkLanguage(strings, 'de');
  assert.equal(warnings.length, 1);
  assert.ok(warnings[0].text_id === 'mixed');
});

test('checkLanguage: strict mode returns isError=true', () => {
  const { checkLanguage } = require(toolPath);
  const strings = { 'key': '中文内容' };
  const warnings = checkLanguage(strings, 'en', { strict: true });
  assert.equal(warnings.length, 1);
  assert.equal(warnings[0].isError, true);
});

test('checkLanguage: non-strict mode returns isError=false', () => {
  const { checkLanguage } = require(toolPath);
  const strings = { 'key': '中文内容' };
  const warnings = checkLanguage(strings, 'en', { strict: false });
  assert.equal(warnings.length, 1);
  assert.equal(warnings[0].isError, false);
});
