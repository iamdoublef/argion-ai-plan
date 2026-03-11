#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

const swissRoot = path.resolve(__dirname, '..');
const standardsRoot = path.join(swissRoot, 'standards');
const localeGuides = JSON.parse(fs.readFileSync(path.join(standardsRoot, 'locale-guides.json'), 'utf8'));
const glossary = JSON.parse(fs.readFileSync(path.join(standardsRoot, 'terminology-glossary.json'), 'utf8'));

const args = process.argv.slice(2);
function getArg(name, fallback = null) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const productArg = getArg('product', path.join('products', 'v23'));
const localeArg = getArg('locale', null);
const exportAll = args.includes('--all');
const productDir = path.isAbsolute(productArg) ? productArg : path.resolve(swissRoot, productArg);

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function workbookLocales(dir) {
  const compiledDir = path.join(dir, 'i18n', 'compiled');
  return fs.readdirSync(compiledDir)
    .filter((file) => file.endsWith('.json'))
    .map((file) => path.basename(file, '.json'))
    .sort();
}

function buildWorkbook(productDir, locale) {
  const metadata = readJson(path.join(productDir, 'i18n', 'strings.json'));
  const catalog = readJson(path.join(productDir, 'i18n', 'compiled', `${locale}.json`));

  const stringsRows = metadata.map((entry) => ({
    text_id: entry.text_id,
    scope: entry.scope,
    context: entry.context,
    source_text: entry.source_text,
    target_text: catalog.strings[entry.text_id] || '',
    status: 'review',
    review_note: '',
  }));

  const termsRows = (glossary.global || []).map((entry) => ({
    term_id: entry.term_id,
    source_term: entry.source_term,
    target_term: entry.targets?.[locale] || '',
    note: entry.note || '',
  }));

  const forbiddenRows = (glossary.forbidden_wording || [])
    .filter((entry) => entry.locale === locale || entry.locale === 'en' || entry.locale === locale.toLowerCase())
    .map((entry) => ({
      source_term: entry.source_term,
      preferred: entry.preferred,
    }));

  const localeRulesRows = (localeGuides[locale]?.rules || []).map((rule, index) => ({
    no: index + 1,
    rule,
  }));

  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(stringsRows), 'strings');
  XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(termsRows), 'terms');
  XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(localeRulesRows), 'locale_rules');
  if (forbiddenRows.length) {
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(forbiddenRows), 'forbidden_words');
  }

  const outPath = path.join(productDir, 'i18n', 'workbooks', `${locale}.xlsx`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  XLSX.writeFile(wb, outPath);
  return outPath;
}

function main() {
  const locales = exportAll ? workbookLocales(productDir) : [localeArg || 'en'];
  locales.forEach((locale) => {
    const outPath = buildWorkbook(productDir, locale);
    console.log(`Workbook exported: ${outPath}`);
  });
}

main();
