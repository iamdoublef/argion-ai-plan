const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const buildVariantModulePath = path.resolve(__dirname, '..', 'tools', 'build-variant.js');

function makeTempTemplateTree() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'swiss-template-'));
}

test('resolveTemplateIncludes expands nested partials and leaves variables for later replacement', () => {
  const { resolveTemplateIncludes } = require(buildVariantModulePath);
  const templateRoot = makeTempTemplateTree();

  fs.mkdirSync(path.join(templateRoot, 'shared', 'layout'), { recursive: true });
  fs.writeFileSync(
    path.join(templateRoot, 'master.html'),
    '<html>{{> shared/layout/head.html}}<body>{{product.model}}</body></html>',
    'utf8'
  );
  fs.writeFileSync(
    path.join(templateRoot, 'shared', 'layout', 'head.html'),
    '<head>{{> shared/layout/meta.html}}</head>',
    'utf8'
  );
  fs.writeFileSync(
    path.join(templateRoot, 'shared', 'layout', 'meta.html'),
    '<meta name="manual" content="{{product.model}}">',
    'utf8'
  );

  const html = resolveTemplateIncludes(path.join(templateRoot, 'master.html'), templateRoot);

  assert.equal(
    html,
    '<html><head><meta name="manual" content="{{product.model}}"></head><body>{{product.model}}</body></html>'
  );
});

test('resolveTemplateIncludes throws a clear error when a partial is missing', () => {
  const { resolveTemplateIncludes } = require(buildVariantModulePath);
  const templateRoot = makeTempTemplateTree();

  fs.writeFileSync(
    path.join(templateRoot, 'master.html'),
    '<html>{{> shared/missing.html}}</html>',
    'utf8'
  );

  assert.throws(
    () => resolveTemplateIncludes(path.join(templateRoot, 'master.html'), templateRoot),
    /Template include not found: .*shared[\\\/]missing\.html/
  );
});
