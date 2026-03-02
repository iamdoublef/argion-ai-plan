const fs = require('fs');
const path = require('path');
const { chromium } = require(path.resolve(__dirname, '../../output/node_modules/playwright'));

const root = __dirname;
const outDir = path.resolve(root, 'docs-pdf');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const jobs = [
  {
    src: path.resolve(__dirname, '../../../../.claude/agents/manual-auditor.md'),
    out: path.resolve(outDir, 'manual-auditor.pdf'),
    title: 'manual-auditor.md',
  },
  {
    src: path.resolve(__dirname, '../../../../.claude/agents/manual-writer.md'),
    out: path.resolve(outDir, 'manual-writer.pdf'),
    title: 'manual-writer.md',
  },
  {
    src: path.resolve(__dirname, '../../data/d5-manual-standard.md'),
    out: path.resolve(outDir, 'd5-manual-standard.pdf'),
    title: 'd5-manual-standard.md',
  },
  {
    src: path.resolve(__dirname, '../../INDEX.md'),
    out: path.resolve(outDir, 'INDEX.pdf'),
    title: 'INDEX.md',
  },
  {
    src: path.resolve(__dirname, '../../research-log.md'),
    out: path.resolve(outDir, 'research-log.pdf'),
    title: 'research-log.md',
  },
  {
    src: path.resolve(outDir, 'leader-brief.md'),
    out: path.resolve(outDir, 'leader-brief.pdf'),
    title: 'leader-brief.md',
  },
];

const esc = (s) => s
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;');

function makeHtml(title, body) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>${title}</title>
<style>
  @page { size: A4; margin: 14mm; }
  body {
    font-family: "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
    color: #111;
    line-height: 1.45;
    font-size: 12px;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .meta { font-size: 11px; color: #666; margin-bottom: 8px; border-bottom: 1px solid #ddd; padding-bottom: 6px; }
  pre { margin: 0; font: inherit; white-space: pre-wrap; }
</style>
</head>
<body>
  <div class="meta">Source: ${title}</div>
  <pre>${esc(body)}</pre>
</body>
</html>`;
}

(async () => {
  const browser = await chromium.launch();
  for (const job of jobs) {
    const content = fs.readFileSync(job.src, 'utf8');
    const page = await browser.newPage();
    await page.setContent(makeHtml(job.title, content), { waitUntil: 'load' });
    await page.pdf({ path: job.out, format: 'A4', printBackground: true, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
    await page.close();
    console.log('generated', path.basename(job.out));
  }
  await browser.close();
})();
