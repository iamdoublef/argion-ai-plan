const path = require('path');
const fs = require('fs');
const { chromium } = require(path.resolve(__dirname, '../../output/node_modules/playwright'));

const ROOT = __dirname;
const manuals = [
  { html: 'v23-cn-main.html', pdf: 'v23-cn-main-fixed.pdf' },
  { html: 'v23-en-main.html', pdf: 'v23-en-main-fixed.pdf' },
  { html: 'v23-mi-style.html', pdf: 'v23-mi-style-fixed.pdf' },
  { html: 'v23-lifestyle-style.html', pdf: 'v23-lifestyle-style-fixed.pdf' },
  { html: 'v23-swiss-style.html', pdf: 'v23-swiss-style-fixed.pdf' },
];

async function waitForAssets(page) {
  await page.waitForLoadState('networkidle');
  await page.waitForFunction(() => {
    if (!document.fonts) return true;
    return document.fonts.status === 'loaded';
  }, { timeout: 15000 });

  await page.waitForFunction(() => {
    const imgs = Array.from(document.images || []);
    if (!imgs.length) return true;
    return imgs.every((img) => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0);
  }, { timeout: 30000 });
}

async function inspectImages(page) {
  return page.evaluate(() => {
    const imgs = Array.from(document.images || []);
    const stats = {
      total: imgs.length,
      complete: 0,
      nonzeroNatural: 0,
      zeroNatural: 0,
      failed: 0,
      src: [],
    };
    for (const img of imgs) {
      const rec = {
        src: img.getAttribute('src') || '',
        complete: !!img.complete,
        nw: img.naturalWidth || 0,
        nh: img.naturalHeight || 0,
      };
      stats.src.push(rec);
      if (rec.complete) stats.complete += 1;
      if (rec.nw > 0 && rec.nh > 0) stats.nonzeroNatural += 1;
      if (rec.nw === 0 || rec.nh === 0) stats.zeroNatural += 1;
      if (!rec.complete || rec.nw === 0 || rec.nh === 0) stats.failed += 1;
    }
    return stats;
  });
}

(async () => {
  const browser = await chromium.launch();
  const report = [];

  for (const job of manuals) {
    const page = await browser.newPage();
    const htmlPath = path.resolve(ROOT, job.html);
    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

    console.log(`rendering: ${job.html}`);
    await page.goto(fileUrl, { waitUntil: 'networkidle' });
    await waitForAssets(page);

    const imgStats = await inspectImages(page);

    const outPath = path.resolve(ROOT, job.pdf);
    await page.pdf({
      path: outPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });

    report.push({ html: job.html, pdf: job.pdf, images: imgStats });
    await page.close();
    console.log(`  -> ${job.pdf}`);
  }

  await browser.close();
  fs.writeFileSync(path.resolve(ROOT, 'audit', 'image-load-report.json'), JSON.stringify(report, null, 2), 'utf8');
  console.log('done');
})();
