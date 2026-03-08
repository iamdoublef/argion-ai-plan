#!/usr/bin/env node
/**
 * _audit-visual.js — Playwright visual audit for manual HTML outputs
 * Takes screenshots of each page and checks image aspect ratios.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2] || 'output/imt050-wevac-eu-cn.html';
const outDir = 'output/_audit';

(async () => {
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  // Viewport approximates A5 at 96dpi: 148mm * 3.78px/mm ≈ 560px, 210mm * 3.78 ≈ 794px
  const page = await browser.newPage({ viewport: { width: 560, height: 794 } });
  const abs = path.resolve(htmlFile);
  const url = 'file:///' + abs.replace(/\\/g, '/');
  await page.goto(url, { waitUntil: 'networkidle' });

  // Screenshot each .page div
  const pageEls = await page.$$('.page');
  console.log('Total pages:', pageEls.length);

  for (let i = 0; i < pageEls.length; i++) {
    const box = await pageEls[i].boundingBox();
    await pageEls[i].screenshot({ path: path.join(outDir, 'page-' + (i + 1) + '.png') });
    console.log('Page ' + (i + 1) + ': w=' + Math.round(box.width) + ' h=' + Math.round(box.height));
  }

  // Check image aspect ratios
  const imgs = await page.evaluate(() => {
    return Array.from(document.images).map(img => {
      const rect = img.getBoundingClientRect();
      const natRatio = img.naturalWidth / img.naturalHeight;
      const renRatio = rect.width / rect.height;
      return {
        src: img.src.split('/').pop(),
        naturalW: img.naturalWidth,
        naturalH: img.naturalHeight,
        renderW: Math.round(rect.width),
        renderH: Math.round(rect.height),
        naturalRatio: natRatio.toFixed(3),
        renderRatio: renRatio.toFixed(3),
        stretched: Math.abs(natRatio - renRatio) > 0.02
      };
    });
  });

  console.log('\nImage Audit:');
  let hasIssue = false;
  imgs.forEach(i => {
    const status = i.stretched ? 'STRETCHED!' : 'OK';
    if (i.stretched) hasIssue = true;
    console.log(`  ${i.src}: natural=${i.naturalW}x${i.naturalH} render=${i.renderW}x${i.renderH} ratio=${i.naturalRatio}/${i.renderRatio} ${status}`);
  });

  // Check page overflow
  const overflows = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.page')).map((p, i) => ({
      page: i + 1,
      scrollH: p.scrollHeight,
      clientH: p.clientHeight,
      overflow: p.scrollHeight > p.clientHeight + 2
    }));
  });

  console.log('\nPage Overflow Check:');
  overflows.forEach(o => {
    const status = o.overflow ? `OVERFLOW (content=${o.scrollH}px > page=${o.clientH}px)` : 'OK';
    if (o.overflow) hasIssue = true;
    console.log(`  Page ${o.page}: ${status}`);
  });

  console.log('\n' + (hasIssue ? 'ISSUES FOUND' : 'ALL CHECKS PASSED'));
  await browser.close();
  process.exit(hasIssue ? 1 : 0);
})();
