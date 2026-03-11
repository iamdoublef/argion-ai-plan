#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

/**
 * Compare compiled JSON strings with workbook target_text values.
 * @param {Record<string,string>} compiled - text_id → translated text from compiled JSON
 * @param {Record<string,string>} workbook - text_id → target_text from workbook
 * @returns {Array<{ text_id: string, newValue: string, oldValue: string|undefined }>}
 */
function diffStrings(compiled, workbook) {
  const changes = [];
  for (const [text_id, newValue] of Object.entries(compiled)) {
    const oldValue = workbook[text_id];
    if (oldValue !== newValue) {
      changes.push({ text_id, newValue, oldValue });
    }
  }
  return changes;
}

/**
 * Sync compiled JSON strings back into an xlsx workbook's target_text column.
 * @param {Record<string,string>} compiled - text_id → translated text
 * @param {string} workbookPath - path to .xlsx file
 * @param {{ dryRun?: boolean }} options
 * @returns {{ updated: number, unchanged: number, added: number, diff: Array }}
 */
function syncToWorkbook(compiled, workbookPath, options = {}) {
  const { dryRun = false } = options;

  const wb = XLSX.readFile(workbookPath);
  const sheet = wb.Sheets.strings;
  if (!sheet) throw new Error(`Workbook missing "strings" sheet: ${workbookPath}`);

  const rows = XLSX.utils.sheet_to_json(sheet, { defval: '' });
  const wbMap = {};
  for (const row of rows) {
    if (row.text_id) wbMap[row.text_id] = String(row.target_text ?? '');
  }

  const diff = diffStrings(compiled, wbMap);
  const existingIds = new Set(rows.map(r => r.text_id));
  let updated = 0;
  let added = 0;

  if (!dryRun && diff.length > 0) {
    // Update existing rows
    for (const row of rows) {
      if (!row.text_id) continue;
      if (compiled[row.text_id] !== undefined && String(row.target_text ?? '') !== compiled[row.text_id]) {
        row.target_text = compiled[row.text_id];
        updated++;
      }
    }

    // Add new rows for keys not in workbook
    for (const change of diff) {
      if (!existingIds.has(change.text_id)) {
        rows.push({ text_id: change.text_id, source_text: '', target_text: change.newValue });
        added++;
      }
    }

    // Write back
    const newSheet = XLSX.utils.json_to_sheet(rows);
    wb.Sheets.strings = newSheet;
    XLSX.writeFile(wb, workbookPath);
  } else if (dryRun) {
    updated = diff.filter(d => existingIds.has(d.text_id)).length;
    added = diff.filter(d => !existingIds.has(d.text_id)).length;
  }

  return {
    updated,
    unchanged: Object.keys(wbMap).length - diff.filter(d => existingIds.has(d.text_id)).length,
    added,
    diff,
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const args = process.argv.slice(2);
  function getArg(name, fallback = null) {
    const idx = args.indexOf(`--${name}`);
    return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
  }

  const jsonPath = getArg('json');
  const wbPath = getArg('workbook');
  const dryRun = args.includes('--dry-run');

  if (!jsonPath || !wbPath) {
    console.log('Usage: node sync-json-to-workbook.js --json <compiled.json> --workbook <locale.xlsx> [--dry-run]');
    process.exit(1);
  }

  const compiled = JSON.parse(fs.readFileSync(path.resolve(jsonPath), 'utf8'));
  const strings = compiled.strings || compiled;
  const result = syncToWorkbook(strings, path.resolve(wbPath), { dryRun });

  console.log(`Sync ${dryRun ? '(dry-run) ' : ''}complete: ${result.updated} updated, ${result.added} added, ${result.unchanged} unchanged`);
  if (result.diff.length > 0) {
    console.log('\nChanges:');
    for (const d of result.diff) {
      console.log(`  ${d.text_id}: "${d.oldValue ?? '(new)'}" → "${d.newValue}"`);
    }
  }
}

if (require.main === module) main();

module.exports = { diffStrings, syncToWorkbook };
