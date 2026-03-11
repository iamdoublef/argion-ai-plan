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
const productDir = path.isAbsolute(productArg) ? productArg : path.resolve(swissRoot, productArg);

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
}

main();
