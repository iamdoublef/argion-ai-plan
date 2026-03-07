#!/usr/bin/env node
/**
 * export-pdf-batch.js — Export all HTML files in output/ to PDF using a single browser
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const outputDir = path.resolve(__dirname, '..', 'output');

async function main() {
  const htmlFiles = fs.readdirSync(outputDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  if (htmlFiles.length === 0) {
    console.log('No HTML files found in output/');
    process.exit(1);
  }

  console.log(`Found ${htmlFiles.length} HTML files to export.\n`);

  const browser = await chromium.launch();
  const results = [];

  for (const file of htmlFiles) {
    const abs = path.join(outputDir, file);
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
      };
    });

    const pageCount = await page.evaluate(() => document.querySelectorAll('.page').length);

    const pdfPath = abs.replace(/\.html$/, '.pdf');
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });

    await page.close();

    const pass = failedRequests.length === 0
      && imageReport.failed === 0
      && imageReport.zeroWidth === 0;

    const pdfSize = (fs.statSync(pdfPath).size / 1024).toFixed(0);

    results.push({
      file,
      pages: pageCount,
      images: imageReport.total,
      failedImg: imageReport.failed,
      zeroWidth: imageReport.zeroWidth,
      failedReq: failedRequests.length,
      pdfKB: pdfSize,
      pass,
    });

    const status = pass ? 'PASS' : 'FAIL';
    console.log(`[${status}] ${file} — ${pageCount} pages, ${imageReport.total} imgs, PDF ${pdfSize} KB`);
  }

  await browser.close();

  const passCount = results.filter(r => r.pass).length;
  const failCount = results.filter(r => !r.pass).length;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`TOTAL: ${results.length} | PASS: ${passCount} | FAIL: ${failCount}`);
  console.log('='.repeat(60));

  if (failCount > 0) {
    console.log('\nFailed variants:');
    results.filter(r => !r.pass).forEach(r => {
      console.log(`  ${r.file}: failedImg=${r.failedImg} zeroWidth=${r.zeroWidth} failedReq=${r.failedReq}`);
    });
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
