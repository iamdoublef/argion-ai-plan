#!/usr/bin/env node
/**
 * audit-visual.js — Playwright-based visual audit for Swiss manual HTML outputs.
 *
 * Usage (CLI):
 *   node tools/audit-visual.js output/v23-wevac-eu-gb.html [--json] [--locale en]
 *
 * Usage (API):
 *   const { auditVisual, classifyOverlap, ... } = require('./tools/audit-visual.js');
 *   const result = await auditVisual('output/file.html', { locale: 'en' });
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// ---------------------------------------------------------------------------
// Classification helpers (unit-testable without Playwright)
// ---------------------------------------------------------------------------

/**
 * Classify overlap between two sibling elements on a page.
 * Cover page (index 0) with absolute-positioned elements → INFO.
 */
function classifyOverlap({ pageIndex, childA, childB, overlapPx }) {
  const isAbsolute = childA.position === 'absolute' || childB.position === 'absolute';
  if (pageIndex === 0 && isAbsolute) {
    return {
      type: 'OVERLAP',
      severity: 'INFO',
      message: `Cover page: absolute-positioned element overlap (${overlapPx}px) — design behavior`,
    };
  }
  return {
    type: 'OVERLAP',
    severity: 'ERROR',
    message: `Children overlap by ${overlapPx}px (${childA.tag} vs ${childB.tag})`,
  };
}

/**
 * Classify image overflow beyond page boundary.
 */
function classifyImageOverflow({ src, imgRight, pageRight }) {
  const overflow = Math.round(imgRight - pageRight);
  if (overflow <= 2) return null; // tolerance
  return {
    type: 'IMG_OVERFLOW',
    severity: 'ERROR',
    message: `${src} exceeds page right by ${overflow}px`,
    overflowPx: overflow,
  };
}

/**
 * Detect data residuals in rendered text.
 */
function classifyDataResidual(text) {
  const issues = [];
  const patterns = [
    { re: /\{\{([^}]+)\}\}/g, label: 'template variable' },
    { re: /\bundefined\b/gi, label: 'undefined literal' },
    { re: /\bnull\b/gi, label: 'null literal' },
    { re: /\bNaN\b/g, label: 'NaN literal' },
    { re: /\bTODO\b/gi, label: 'TODO marker' },
  ];
  for (const { re, label } of patterns) {
    let m;
    while ((m = re.exec(text)) !== null) {
      issues.push({
        type: 'DATA_RESIDUAL',
        severity: 'ERROR',
        message: `${label}: "${m[0]}"`,
        match: m[0],
      });
    }
  }
  return issues;
}

/**
 * Detect source language residual in target locale text.
 */
function classifySourceLangResidual(locale, text) {
  if (locale.startsWith('zh')) return []; // source language, skip
  const cjkRe = /[\u4e00-\u9fff]/g;
  const matches = text.match(cjkRe);
  if (!matches || matches.length === 0) return [];
  return [{
    type: 'SOURCE_LANG_RESIDUAL',
    severity: 'ERROR',
    message: `${matches.length} CJK characters found in ${locale} locale text`,
    count: matches.length,
  }];
}

// ---------------------------------------------------------------------------
// Main audit function (Playwright-based)
// ---------------------------------------------------------------------------

async function auditVisual(htmlPath, options = {}) {
  const { locale = null, screenshotDir = null } = options;
  const issues = [];

  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 560, height: 794 } });
    const absPath = path.resolve(htmlPath);
    await page.goto('file:///' + absPath.replace(/\\/g, '/'), { waitUntil: 'networkidle' });

    const pageCount = await page.evaluate(() => document.querySelectorAll('.page').length);

    // --- Check each page ---
    const pageIssues = await page.evaluate(() => {
      const results = [];
      const pages = document.querySelectorAll('.page');

      pages.forEach((p, pi) => {
        const pageRect = p.getBoundingClientRect();

        // Horizontal overflow
        if (p.scrollWidth > p.clientWidth + 2) {
          results.push({
            page: pi + 1, type: 'HORIZONTAL_OVERFLOW', severity: 'ERROR',
            message: `scrollW=${p.scrollWidth} > clientW=${p.clientWidth}`,
          });
        }

        // Overlapping siblings
        const children = Array.from(p.children);
        for (let i = 0; i < children.length - 1; i++) {
          const a = children[i];
          const b = children[i + 1];
          const aRect = a.getBoundingClientRect();
          const bRect = b.getBoundingClientRect();
          const overlap = Math.round(aRect.bottom - bRect.top);
          if (overlap > 5) {
            results.push({
              page: pi + 1, type: 'OVERLAP_RAW',
              childA: { position: getComputedStyle(a).position, tag: a.tagName, className: a.className },
              childB: { position: getComputedStyle(b).position, tag: b.tagName, className: b.className },
              overlapPx: overlap,
              pageIndex: pi,
            });
          }
        }

        // Image overflow
        const imgs = p.querySelectorAll('img');
        imgs.forEach(img => {
          const ir = img.getBoundingClientRect();
          if (ir.right > pageRect.right + 2) {
            results.push({
              page: pi + 1, type: 'IMG_OVERFLOW_RAW',
              src: img.src.split('/').pop(),
              imgRight: Math.round(ir.right),
              pageRight: Math.round(pageRect.right),
            });
          }
          // Zero-size image
          if (ir.width < 1 || ir.height < 1) {
            results.push({
              page: pi + 1, type: 'ZERO_SIZE_IMG', severity: 'ERROR',
              message: `${img.src.split('/').pop()} has zero dimensions (${Math.round(ir.width)}x${Math.round(ir.height)})`,
            });
          }
        });

        // Empty page
        const contentH = Array.from(p.children).reduce((h, c) => {
          const r = c.getBoundingClientRect();
          return Math.max(h, r.bottom - pageRect.top);
        }, 0);
        if (contentH < pageRect.height * 0.1 && children.length > 0) {
          results.push({
            page: pi + 1, type: 'EMPTY_PAGE', severity: 'WARNING',
            message: `Content height ${Math.round(contentH)}px < 10% of page height`,
          });
        }
      });

      return results;
    });

    // Classify raw issues
    for (const raw of pageIssues) {
      if (raw.type === 'OVERLAP_RAW') {
        const classified = classifyOverlap(raw);
        issues.push({ page: raw.page, ...classified });
      } else if (raw.type === 'IMG_OVERFLOW_RAW') {
        const classified = classifyImageOverflow(raw);
        if (classified) issues.push({ page: raw.page, ...classified });
      } else {
        issues.push(raw);
      }
    }

    // Data residual check
    const allText = await page.evaluate(() => document.body.innerText);
    const residuals = classifyDataResidual(allText);
    residuals.forEach(r => issues.push({ page: 0, ...r }));

    // Source language residual check
    if (locale) {
      const langIssues = classifySourceLangResidual(locale, allText);
      langIssues.forEach(r => issues.push({ page: 0, ...r }));
    }

    // Screenshots (if requested)
    if (screenshotDir) {
      if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
      const pageEls = await page.$$('.page');
      const errorPages = new Set(issues.filter(i => i.severity === 'ERROR').map(i => i.page));
      for (const ep of errorPages) {
        if (ep > 0 && ep <= pageEls.length) {
          await pageEls[ep - 1].screenshot({
            path: path.join(screenshotDir, `issue-page-${ep}.png`),
          });
        }
      }
    }

    // Build summary
    const summary = {
      pages: pageCount,
      errors: issues.filter(i => i.severity === 'ERROR').length,
      warnings: issues.filter(i => i.severity === 'WARNING').length,
      infos: issues.filter(i => i.severity === 'INFO').length,
    };

    return { issues, summary };
  } finally {
    await browser.close();
  }
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------
if (require.main === module) {
  const args = process.argv.slice(2);
  const htmlFile = args.find(a => !a.startsWith('--')) || 'output/v23-wevac-eu-cn.html';
  const jsonOutput = args.includes('--json');
  const localeIdx = args.indexOf('--locale');
  const locale = localeIdx !== -1 ? args[localeIdx + 1] : null;

  (async () => {
    const result = await auditVisual(htmlFile, {
      locale,
      screenshotDir: 'output/_audit',
    });

    if (jsonOutput) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      const name = path.basename(htmlFile);
      console.log(`=== Visual Audit: ${name} ===`);
      console.log(`Pages: ${result.summary.pages}`);
      console.log(`Errors: ${result.summary.errors} | Warnings: ${result.summary.warnings} | Info: ${result.summary.infos}`);
      if (result.issues.length > 0) {
        console.log('\nIssues:');
        for (const issue of result.issues) {
          const loc = issue.page > 0 ? `Page ${issue.page}` : 'Global';
          console.log(`  [${issue.severity}] ${loc}: ${issue.message} (${issue.type})`);
        }
      }
      console.log('\n' + (result.summary.errors === 0 ? 'ALL CHECKS PASSED' : 'ISSUES FOUND'));
    }
    process.exit(result.summary.errors > 0 ? 1 : 0);
  })();
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------
module.exports = {
  auditVisual,
  classifyOverlap,
  classifyImageOverflow,
  classifyDataResidual,
  classifySourceLangResidual,
};
