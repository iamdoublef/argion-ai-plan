#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

const swissRoot = path.resolve(__dirname, '..');
const args = process.argv.slice(2);

function getArg(name, fallback = null) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const workbookArg = getArg('workbook', null);
const productArg = getArg('product', path.join('products', 'v23'));
const localeArg = getArg('locale', null);
const checkLangFlag = args.includes('--check-lang');
const strictFlag = args.includes('--strict');
const productDir = path.isAbsolute(productArg) ? productArg : path.resolve(swissRoot, productArg);

/**
 * Check for source language residuals in target locale strings.
 * @param {Record<string,string>} strings - compiled text_id → text map
 * @param {string} locale - target locale (e.g. 'en', 'de')
 * @param {{ strict?: boolean }} options
 * @returns {Array<{ text_id: string, value: string, isError: boolean }>}
 */
function checkLanguage(strings, locale, options = {}) {
  const { strict = false } = options;
  if (locale.startsWith('zh')) return []; // source language, skip
  const cjkRe = /[\u4e00-\u9fff]/;
  const warnings = [];
  for (const [text_id, value] of Object.entries(strings)) {
    if (cjkRe.test(value)) {
      warnings.push({ text_id, value, isError: strict });
    }
  }
  return warnings;
}

function compileWorkbook(workbookPath, locale) {
  const wb = XLSX.readFile(workbookPath);
  const sheet = wb.Sheets.strings;
  if (!sheet) {
    throw new Error(`Workbook missing "strings" sheet: ${workbookPath}`);
  }

  const rows = XLSX.utils.sheet_to_json(sheet, { defval: '' });
  const strings = {};

  rows.forEach((row) => {
    if (!row.text_id) {
      return;
    }
    strings[row.text_id] = String(row.target_text || row.source_text || '');
  });

  const outPath = path.join(productDir, 'i18n', 'compiled', `${locale}.json`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, `${JSON.stringify({ locale, strings }, null, 2)}\n`, 'utf8');
  return outPath;
}

function main() {
  const workbookPath = workbookArg
    ? (path.isAbsolute(workbookArg) ? workbookArg : path.resolve(swissRoot, workbookArg))
    : path.join(productDir, 'i18n', 'workbooks', `${localeArg}.xlsx`);

  const locale = localeArg || path.basename(workbookPath, path.extname(workbookPath));
  const outPath = compileWorkbook(workbookPath, locale);
  console.log(`Compiled locale catalog: ${outPath}`);

  if (checkLangFlag) {
    const compiled = JSON.parse(fs.readFileSync(outPath, 'utf8'));
    const warnings = checkLanguage(compiled.strings, locale, { strict: strictFlag });
    if (warnings.length > 0) {
      console.log(`\nLanguage check: ${warnings.length} issue(s) found in ${locale}:`);
      for (const w of warnings) {
        const level = w.isError ? 'ERROR' : 'WARNING';
        console.log(`  [${level}] ${w.text_id}: "${w.value.substring(0, 60)}"`);
      }
      if (strictFlag) {
        console.log('\n--strict mode: aborting due to language issues.');
        process.exit(1);
      }
    } else {
      console.log(`\nLanguage check: PASS (0 issues)`);
    }
  }
}

if (require.main === module) {
  main();
}

module.exports = { compileWorkbook, checkLanguage };
