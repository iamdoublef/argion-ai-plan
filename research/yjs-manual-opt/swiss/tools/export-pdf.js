#!/usr/bin/env node
/**
 * export-pdf.js — Playwright-based PDF exporter with image validation
 *
 * Usage:
 *   node export-pdf.js output/v23-wevac-eu-cn.html
 *   node export-pdf.js output/*.html          (batch)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function exportPdf(htmlPath) {
  const abs = path.resolve(htmlPath);
  if (!fs.existsSync(abs)) {
    console.error(`File not found: ${abs}`);
    return false;
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  const failedRequests = [];
  page.on('requestfailed', req => failedRequests.push(req.url()));

  const fileUrl = `file:///${abs.replace(/\\/g, '/')}`;
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  const imageReport = await page.evaluate(() => {
    const imgs = Array.from(document.images);
    return {
      total: imgs.length,
      failed: imgs.filter(i => !i.complete).length,
      zeroWidth: imgs.filter(i => i.naturalWidth === 0).length,
      details: imgs.map(i => ({
        src: i.src.split('/').pop(),
        complete: i.complete,
        naturalWidth: i.naturalWidth,
        renderWidth: i.getBoundingClientRect().width
      }))
    };
  });

  const pageCount = await page.evaluate(() => document.querySelectorAll('.page').length);

  console.log(`\n=== ${path.basename(htmlPath)} ===`);
  console.log(`Pages: ${pageCount}`);
  console.log(`Images: total=${imageReport.total}, failed=${imageReport.failed}, zeroWidth=${imageReport.zeroWidth}`);
  console.log(`Failed requests: ${failedRequests.length}`);

  if (failedRequests.length > 0) {
    console.log('  Failed URLs:', failedRequests);
  }

  const pdfPath = abs.replace(/\.html$/, '.pdf');
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  console.log(`PDF: ${pdfPath}`);

  await browser.close();

  const pass = failedRequests.length === 0
    && imageReport.failed === 0
    && imageReport.zeroWidth === 0;

  console.log(`Status: ${pass ? 'PASS' : 'FAIL'}`);

  const reportPath = abs.replace(/\.html$/, '-image-report.json');
  fs.writeFileSync(reportPath, JSON.stringify({ pageCount, imageReport, failedRequests, pass }, null, 2));

  return pass;
}

(async () => {
  const files = process.argv.slice(2);
  if (files.length === 0) {
    console.log('Usage: node export-pdf.js <html-file> [html-file...]');
    process.exit(1);
  }

  let allPass = true;
  for (const f of files) {
    const ok = await exportPdf(f);
    if (!ok) allPass = false;
  }

  console.log(`\n${'='.repeat(40)}`);
  console.log(`Overall: ${allPass ? 'ALL PASS' : 'SOME FAILED'}`);
  process.exit(allPass ? 0 : 1);
})();
