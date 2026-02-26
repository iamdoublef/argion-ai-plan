/**
 * V23 Manual PDF Generator
 * Uses Playwright to render HTML manuals and export as A4 PDF.
 *
 * Usage:
 *   npm install playwright   (if not already installed)
 *   node generate-pdf.js
 *
 * Output:
 *   V23-Manual-CN-Wevac.pdf
 *   V23-Manual-EN-Wevac.pdf
 */

const { chromium } = require('playwright');
const path = require('path');

const MANUALS = [
  { html: 'v23-manual-cn.html', pdf: 'V23-Manual-CN-Wevac.pdf' },
  { html: 'v23-manual-en.html', pdf: 'V23-Manual-EN-Wevac.pdf' },
];

async function generatePDF(browser, htmlFile, pdfFile) {
  const page = await browser.newPage();
  const filePath = path.resolve(__dirname, htmlFile);
  const fileUrl = 'file:///' + filePath.replace(/\\/g, '/');

  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  await page.pdf({
    path: path.resolve(__dirname, pdfFile),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });

  console.log(`  -> ${pdfFile}`);
  await page.close();
}

(async () => {
  console.log('Launching browser...');
  const browser = await chromium.launch();

  for (const { html, pdf } of MANUALS) {
    const htmlPath = path.resolve(__dirname, html);
    try {
      require('fs').accessSync(htmlPath);
      await generatePDF(browser, html, pdf);
    } catch {
      console.log(`  !! Skipped ${html} (file not found)`);
    }
  }

  await browser.close();
  console.log('Done.');
})();
