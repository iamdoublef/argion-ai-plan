const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const buildVariantModulePath = path.resolve(__dirname, '..', 'tools', 'build-variant.js');

function makeTempProductDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'swiss-product-'));
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function writeMinimalProduct(productDir) {
  writeJson(path.join(productDir, 'product.json'), {
    product: {
      model: 'IMT050',
      name_cn: '制冰机',
      name_en: 'Ice Maker',
      active_brand: 'wevac',
      active_market: 'eu',
      template_prefix: 'imt050',
      cover_image: 'image1.png',
    },
    images_dir: 'images_test',
    specs: {
      eu: {
        rows: [
          { label: '功率', label_en: 'Power', value: '110 W', value_en: '110 W' },
        ],
      },
    },
    parts: [
      { id: 1, name_cn: '水箱', name_en: 'Water Tank' },
    ],
    buttons: [
      { id: 1, key: 'Power', name_cn: '电源', name_en: 'Power', desc_cn: '开机', desc_en: 'Turn on' },
    ],
    brands: {
      wevac: {
        display_name: 'WEVAC',
        display_name_cn: '威富克',
        name: 'WEVAC TECHNOLOGY CO., LIMITED',
        address: 'HK Address',
        address_cn: '香港地址',
        website: 'www.example.com',
        support_email: 'support@example.com',
      },
    },
    manufacturer: {
      name_cn: '广州亚俊氏真空科技股份有限公司',
      name_en: 'Guangzhou Argion Electric Appliance Co., Ltd.',
      address_cn: '广州地址',
      address_en: 'Guangzhou Address',
      website: 'www.argion.com',
    },
    ui_labels: {
      cn: { cover_subtitle: '使用说明书' },
      en: { cover_subtitle: 'User Manual' },
    },
  });
}

function writeMinimalCatalog(productDir, locale, overrides = {}) {
  writeJson(path.join(productDir, 'i18n', 'compiled', `${locale}.json`), {
    locale,
    strings: overrides,
  });
}

function writeMinimalSourceChapter(productDir, chapterNo = '01') {
  writeJson(path.join(productDir, 'content', 'source', 'manifest.json'), {
    chapters: [
      {
        chapter_id: `${chapterNo}-safety`,
        chapter_no: chapterNo,
        title: 'Safety',
        title_id: `content.chapter.${chapterNo}-safety.title`,
        toc_title: 'Safety',
        toc_title_id: `content.chapter.${chapterNo}-safety.toc_title`,
        header_ref: `CH.${chapterNo} - SAFETY`,
        header_ref_id: `content.chapter.${chapterNo}-safety.header_ref`,
        enabled: true,
        file: `${chapterNo}-safety.json`,
      },
    ],
  });

  writeJson(path.join(productDir, 'content', 'source', 'chapters', `${chapterNo}-safety.json`), {
    chapter_id: `${chapterNo}-safety`,
    pages: [
      {
        page_id: 'page1',
        page_class: 'compact-safety',
        section_title: 'Safety',
        section_title_id: `content.chapter.${chapterNo}-safety.page.page1.section_title`,
        blocks: [
          {
            type: 'paragraph',
            text: 'Read before use.',
            text_id: `content.chapter.${chapterNo}-safety.page.page1.block.1.text`,
          },
        ],
      },
    ],
  });
}

function makeRenderContext(images = {}) {
  return {
    config: {
      product: { model: 'IMT050' },
      images_dir: 'images_test',
      parts: [],
      buttons: [],
    },
    brand: {
      display_name: 'WEVAC',
      name: 'WEVAC',
      address: 'Address',
      website: 'example.com',
      support_email: 'support@example.com',
    },
    specs: { rows: [] },
    mfr: {
      name_primary: 'Factory CN',
      name_secondary: 'Factory EN',
      address: 'Address CN',
      website: 'factory.example.com',
    },
    suffix: 'en',
    labels: {},
    localized: {
      document_title: 'User Manual',
      document_title_upper: 'USER MANUAL',
      product_name: 'Ice Maker',
    },
    images,
    builders: {
      buildSpecsRows: () => '',
      buildPartsRows: () => '',
      buildButtonsRows: () => '',
      buildBrandInfoRows: () => '',
      buildManufacturerRows: () => '',
    },
  };
}

test('loadProductConfig requires product.json', () => {
  const { loadProductConfig } = require(buildVariantModulePath);
  const productDir = makeTempProductDir();

  assert.throws(() => loadProductConfig(productDir), /Product data not found:/);

  writeMinimalProduct(productDir);
  assert.equal(loadProductConfig(productDir).product.model, 'IMT050');
});

test('loadLocaleCatalog requires compiled locale file with strings map', () => {
  const { loadLocaleCatalog } = require(buildVariantModulePath);
  const productDir = makeTempProductDir();

  assert.throws(() => loadLocaleCatalog(productDir, 'en'), /Locale catalog not found:/);

  writeJson(path.join(productDir, 'i18n', 'compiled', 'en.json'), { locale: 'en' });
  assert.throws(() => loadLocaleCatalog(productDir, 'en'), /missing strings map/i);
});

test('loadContentDocument reads source chapters and localizes by text_id', () => {
  const { loadContentDocument } = require(buildVariantModulePath);
  const productDir = makeTempProductDir();

  writeMinimalSourceChapter(productDir);
  writeMinimalCatalog(productDir, 'en', {
    'content.chapter.01-safety.title': 'Safety',
    'content.chapter.01-safety.toc_title': 'Safety',
    'content.chapter.01-safety.header_ref': 'CH.01 - SAFETY',
    'content.chapter.01-safety.page.page1.section_title': 'Safety',
    'content.chapter.01-safety.page.page1.block.1.text': 'Read before first use.',
  });

  const document = loadContentDocument(productDir, 'en');
  assert.equal(document.kind, 'structured');
  assert.equal(document.chapters.length, 1);
  assert.equal(document.chapters[0].chapter_id, '01-safety');
  assert.equal(document.chapters[0].title, 'Safety');
  assert.equal(document.chapters[0].pages[0].section_title, 'Safety');
  assert.equal(document.chapters[0].pages[0].blocks[0].text, 'Read before first use.');
});

test('loadContentDocument rejects numbering gaps and missing chapter files', () => {
  const { loadContentDocument } = require(buildVariantModulePath);
  const productDir = makeTempProductDir();

  writeJson(path.join(productDir, 'content', 'source', 'manifest.json'), {
    chapters: [
      {
        chapter_id: '01-safety',
        chapter_no: '02',
        title: 'Safety',
        toc_title: 'Safety',
        header_ref: 'CH.01 - SAFETY',
        enabled: true,
        file: '01-safety.json',
      },
    ],
  });
  writeMinimalCatalog(productDir, 'en', {});

  assert.throws(() => loadContentDocument(productDir, 'en'), /chapter numbering must be continuous/i);

  writeJson(path.join(productDir, 'content', 'source', 'manifest.json'), {
    chapters: [
      {
        chapter_id: '01-safety',
        chapter_no: '01',
        title: 'Safety',
        toc_title: 'Safety',
        header_ref: 'CH.01 - SAFETY',
        enabled: true,
        file: '01-safety.json',
      },
    ],
  });

  assert.throws(() => loadContentDocument(productDir, 'en'), /Chapter file not found:/);
});

test('buildLocalizedRuntimeData localizes facts, labels and product name from catalog', () => {
  const { buildLocalizedRuntimeData } = require(buildVariantModulePath);

  const config = {
    product: {
      model: 'IMT050',
      name_cn: '制冰机',
      name_en: 'Ice Maker',
    },
    specs: {
      eu: {
        rows: [
          { label: '功率', label_en: 'Power', value: '110 W', value_en: '110 W' },
        ],
      },
    },
    parts: [
      { id: 1, name_cn: '水箱', name_en: 'Water Tank' },
    ],
    buttons: [
      { id: 1, key: 'Power', name_cn: '电源', name_en: 'Power', desc_cn: '开机', desc_en: 'Turn on' },
    ],
    brands: {
      wevac: {
        display_name: 'WEVAC',
        display_name_cn: '威富克',
        name: 'WEVAC TECHNOLOGY CO., LIMITED',
        address: 'HK Address',
        address_cn: '香港地址',
        website: 'www.example.com',
        support_email: 'support@example.com',
      },
    },
    manufacturer: {
      name_cn: '广州亚俊氏真空科技股份有限公司',
      name_en: 'Guangzhou Argion Electric Appliance Co., Ltd.',
      address_cn: '广州地址',
      address_en: 'Guangzhou Address',
      website: 'www.argion.com',
    },
    ui_labels: {
      en: {
        cover_subtitle: 'User Manual',
      },
    },
  };

  const catalog = {
    strings: {
      'product.product.name': 'Ice Maker Pro',
      'product.brands.wevac.display_name': 'WEVAC PRO',
      'product.specs.eu.rows.0.label': 'Power',
      'product.buttons.1.desc': 'Press to power on.',
      'product.ui_labels.cover_subtitle': 'User Guide',
      'system.document_title': 'User Manual',
    },
  };

  const runtime = buildLocalizedRuntimeData(config, catalog, 'wevac', 'eu', 'en');
  assert.equal(runtime.localized.product_name, 'Ice Maker Pro');
  assert.equal(runtime.brand.display_name, 'WEVAC PRO');
  assert.equal(runtime.specs.rows[0].label, 'Power');
  assert.equal(runtime.buttons[0].desc, 'Press to power on.');
  assert.equal(runtime.labels.cover_subtitle, 'User Guide');
});

test('renderTextTokens supports lightweight tokens and rejects raw HTML', () => {
  const { renderTextTokens } = require(buildVariantModulePath);

  assert.equal(
    renderTextTokens('Press [btn:Power] and read **Warning**.\nLine 2'),
    'Press <span class="btn-name">Power</span> and read <b>Warning</b>.<br>Line 2'
  );

  assert.throws(
    () => renderTextTokens('Press <b>Power</b>'),
    /Raw HTML is not allowed in text token field/
  );
});

test('renderDocument rejects unknown block types including legacy html_fragment', () => {
  const { renderDocument } = require(buildVariantModulePath);
  const documentSchema = {
    kind: 'structured',
    chapters: [
      {
        chapter_id: '01-safety',
        chapter_no: '01',
        title: 'Safety',
        toc_title: 'Safety',
        header_ref: 'CH.01 - SAFETY',
        pages: [
          {
            section_title: 'Safety',
            blocks: [{ type: 'html_fragment', html: '<p>legacy</p>' }],
          },
        ],
      },
    ],
  };

  assert.throws(
    () => renderDocument(documentSchema, makeRenderContext()),
    /Unknown block type: html_fragment/
  );
});

test('renderDocument validates procedural image usage_ref', () => {
  const { renderDocument } = require(buildVariantModulePath);

  const schema = {
    kind: 'structured',
    chapters: [
      {
        chapter_id: '06-operation',
        chapter_no: '06',
        title: 'Operation',
        toc_title: 'Operation',
        header_ref: 'CH.06 - OPERATION',
        pages: [
          {
            page_id: 'page1',
            section_title: 'Operation',
            blocks: [
              {
                type: 'step_flow',
                steps: [{ id: 'fill_tank', text: 'Fill tank.', figures: ['operation.fill_tank'] }],
              },
            ],
          },
        ],
      },
    ],
  };

  assert.throws(
    () => renderDocument(schema, makeRenderContext({
      'operation.fill_tank': { file: 'fill.png', alt: 'Fill tank', kind: 'procedural' },
    })),
    /Procedural image missing usage_ref: operation\.fill_tank/
  );

  assert.throws(
    () => renderDocument(schema, makeRenderContext({
      'operation.fill_tank': {
        file: 'fill.png',
        alt: 'Fill tank',
        kind: 'procedural',
        usage_ref: '06-operation.page1.other_step',
      },
    })),
    /usage_ref mismatch/
  );
});

test('renderDocument renders split_panel, tokens and TOC from structured content', () => {
  const { renderDocument } = require(buildVariantModulePath);

  const result = renderDocument({
    kind: 'structured',
    chapters: [
      {
        chapter_id: '01-safety',
        chapter_no: '01',
        title: 'Safety',
        toc_title: 'Safety',
        header_ref: 'CH.01 - SAFETY',
        pages: [
          {
            page_id: 'page1',
            page_class: 'compact-safety',
            section_title: 'Safety',
            blocks: [{ type: 'paragraph', text: 'Read before use.' }],
          },
        ],
      },
      {
        chapter_id: '06-operation',
        chapter_no: '06',
        title: 'Operation',
        toc_title: 'Operation',
        header_ref: 'CH.06 - OPERATION',
        pages: [
          {
            page_id: 'page1',
            section_title: 'Operation',
            blocks: [
              {
                type: 'split_panel',
                body_blocks: [
                  { type: 'sub_title', text: 'Quick start' },
                  { type: 'paragraph', text: 'Press [btn:Power] to start.' },
                ],
                figures: ['operation.panel'],
              },
            ],
          },
        ],
      },
    ],
  }, makeRenderContext({
    'operation.panel': {
      file: 'panel.png',
      alt: 'Control panel',
      kind: 'procedural',
      usage_ref: '06-operation.page1.block1.figure1',
    },
  }));

  assert.match(result.tocHtml, /toc-chapter">01/);
  assert.match(result.tocHtml, /toc-chapter">06/);
  assert.match(result.documentHtml, /class="split-panel"/);
  assert.match(result.documentHtml, /<span class="btn-name">Power<\/span>/);
  assert.match(result.documentHtml, /panel\.png/);
});
