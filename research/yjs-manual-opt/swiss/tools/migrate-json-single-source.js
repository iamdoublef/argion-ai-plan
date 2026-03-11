#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const swissRoot = path.resolve(__dirname, '..');
const sourceRoot = path.resolve(__dirname, '..', '..', 'source');
const products = ['imt050', 'v23'];
const langs = ['cn', 'en', 'de', 'it'];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function decodeHtml(value = '') {
  return value
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

function stripTags(value = '') {
  return decodeHtml(value.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
}

function slugify(value = '') {
  return value
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

function findMatchingDivEnd(source, startIndex) {
  let depth = 0;
  let index = startIndex;

  while (index < source.length) {
    const openIndex = source.indexOf('<div', index);
    const closeIndex = source.indexOf('</div>', index);

    if (closeIndex === -1) {
      throw new Error(`Unclosed <div> starting at ${startIndex}`);
    }

    if (openIndex !== -1 && openIndex < closeIndex) {
      depth += 1;
      index = openIndex + 4;
      continue;
    }

    depth -= 1;
    index = closeIndex + 6;
    if (depth === 0) {
      return index;
    }
  }

  throw new Error(`Unable to resolve </div> for page block at ${startIndex}`);
}

function splitPages(bodyHtml) {
  const pages = [];
  let cursor = 0;

  while (true) {
    const startIndex = bodyHtml.indexOf('<div class="page', cursor);
    if (startIndex === -1) {
      break;
    }
    const endIndex = findMatchingDivEnd(bodyHtml, startIndex);
    pages.push(bodyHtml.slice(startIndex, endIndex));
    cursor = endIndex;
  }

  return pages;
}

function extractDivByClass(source, className) {
  const start = source.indexOf(`<div class="${className}"`);
  if (start === -1) {
    return '';
  }
  const end = findMatchingDivEnd(source, start);
  return source.slice(start, end);
}

function parsePage(pageHtml) {
  const openingMatch = pageHtml.match(/^<div class="([^"]+)"/);
  if (!openingMatch) {
    throw new Error(`Invalid page block: ${pageHtml.slice(0, 80)}`);
  }

  const headerStart = pageHtml.indexOf('<div class="header-strip"');
  const headerEnd = findMatchingDivEnd(pageHtml, headerStart);
  const titleMatch = pageHtml.match(/<h2 class="section-title"><span class="chapter-num">(\d+)<\/span>([\s\S]*?)<\/h2>/);
  const footerStart = pageHtml.lastIndexOf('<div class="page-footer"');
  if (footerStart === -1) {
    throw new Error(`Missing page footer in page: ${pageHtml.slice(0, 140)}`);
  }

  const headerRefMatch = pageHtml.match(/<div class="header-ref">([\s\S]*?)<\/div>/);
  const derivedChapterNo = titleMatch
    ? titleMatch[1]
    : ((headerRefMatch ? headerRefMatch[1] : '').match(/CH\.(\d+)/i) || [])[1];
  if (!derivedChapterNo) {
    throw new Error(`Unable to derive chapter number from page: ${pageHtml.slice(0, 140)}`);
  }

  let contentStart = headerEnd;
  let sectionTitle = '';
  if (titleMatch) {
    const titleStart = pageHtml.indexOf(titleMatch[0], headerEnd);
    contentStart = titleStart + titleMatch[0].length;
    sectionTitle = stripTags(titleMatch[2]);
  }

  return {
    page_class: openingMatch[1].split(/\s+/).filter((token) => token && token !== 'page').join(' '),
    chapter_no: derivedChapterNo,
    section_title: sectionTitle,
    header_ref: stripTags(headerRefMatch ? headerRefMatch[1] : ''),
    body_html: pageHtml.slice(contentStart, footerStart).trim(),
  };
}

function chapterIdFromPage(pageMeta) {
  const refSlug = slugify(pageMeta.header_ref.replace(/^CH\.\d+\s+[—-]\s+/i, ''));
  const titleSlug = slugify(pageMeta.section_title.replace(/\s*[（(].*?[)）]\s*$/, ''));
  return `${pageMeta.chapter_no}-${refSlug || titleSlug || `chapter-${pageMeta.chapter_no}`}`;
}

function normalizeTocTitle(sectionTitle) {
  return sectionTitle
    .replace(/\s*[（(](续|續|cont\.?|cont|forts\.?|fortsetzung|seguito)[)）]\s*$/i, '')
    .trim();
}

function parseListItems(boxHtml) {
  return [...boxHtml.matchAll(/<li>([\s\S]*?)<\/li>/g)].map((match) => match[1].trim());
}

function parseBox(pageBody, className) {
  const boxHtml = extractDivByClass(pageBody, className);
  if (!boxHtml) {
    return null;
  }

  const titleMatch = boxHtml.match(/<div class="box-title">([\s\S]*?)<\/div>/);
  const iconMatch = boxHtml.match(/src="\.\/\{\{images_dir\}\}\/([^"]+)"/);

  return {
    title: titleMatch ? stripTags(titleMatch[1]) : '',
    items: parseListItems(boxHtml),
    icon_file: iconMatch ? iconMatch[1] : null,
  };
}

function buildLegacyChapter(pages) {
  const firstPage = pages[0];
  return {
    chapter_id: chapterIdFromPage(firstPage),
    chapter_no: firstPage.chapter_no,
    title: normalizeTocTitle(firstPage.section_title),
    toc_title: normalizeTocTitle(firstPage.section_title),
    header_ref: firstPage.header_ref,
    pages: pages.map((page) => ({
      page_class: page.page_class,
      section_title: page.section_title,
      hide_section_title: !page.section_title,
      blocks: [
        {
          type: 'html_fragment',
          html: page.body_html,
        },
      ],
    })),
  };
}

function chunkPagesIntoChapters(pageMetas) {
  const chapters = [];
  let current = [];
  let currentChapterNo = null;

  for (const pageMeta of pageMetas) {
    if (currentChapterNo && pageMeta.chapter_no !== currentChapterNo) {
      chapters.push(buildLegacyChapter(current));
      current = [];
    }
    currentChapterNo = pageMeta.chapter_no;
    current.push(pageMeta);
  }

  if (current.length) {
    chapters.push(buildLegacyChapter(current));
  }

  return chapters;
}

function buildImt050SafetyChapter(lang, legacyChapter) {
  const [page1, page2] = legacyChapter.pages;
  const introMatch = page1.blocks[0].html.match(/<p>([\s\S]*?)<\/p>/);
  const warningBox = parseBox(page1.blocks[0].html, 'warning-box');
  const cautionBox = parseBox(page2.blocks[0].html, 'caution-box');
  const noticeBox = parseBox(page2.blocks[0].html, 'note-box');

  return {
    ...legacyChapter,
    pages: [
      {
        page_class: page1.page_class,
        section_title: page1.section_title,
        blocks: [
          {
            type: 'paragraph',
            text: introMatch ? introMatch[1].trim() : '',
          },
          {
            type: 'warning_box',
            title: warningBox.title,
            icon: 'safety.warning_icon',
            items: warningBox.items,
          },
        ],
      },
      {
        page_class: page2.page_class,
        section_title: page2.section_title,
        blocks: [
          {
            type: 'caution_box',
            title: cautionBox.title,
            items: cautionBox.items,
          },
          {
            type: 'notice_box',
            title: noticeBox.title,
            items: noticeBox.items,
          },
        ],
      },
    ],
  };
}

const imt050OperationData = {
  cn: {
    title: '操作指引',
    continuation: '操作指引（续）',
    prep_title: '工作前准备',
    prep_items: [
      '务必将产品放置在平整稳固的平面，且产品背部和右侧散热孔处不能放置任何东西，以免阻挡散热。产品与墙或物品之间距离必须 ≥ 120 mm（4.7 in），以确保通风良好。',
      '若第一次使用产品，或距离上一次很长时间没有使用产品，请先运行一次清洁程序。请参阅 CH.08 维护保养中的清洁说明。',
    ],
    power_title: '产品开机',
    power_items: [
      '给产品接通电源，产品发出“滴”一声，所有按键点亮后再熄灭，表示已经接通电源。',
      '然后点击 <b>Power</b> 按键，按键显示白灯，产品已处于开机状态。',
    ],
    make_title: '如何制作子弹冰',
    steps_page_1: [
      { id: 'open_lid', text: '打开腔盖，并取出子弹冰篮和水箱。' },
      { id: 'fill_tank', text: '给子弹冰水箱中注满水，注水至水位刻度处。', figures: ['operation.make_ice.fill_tank', 'operation.make_ice.max_mark'] },
      { id: 'seat_tank', text: '然后将水箱放入子弹冰内腔，请用手按压下水箱，确保已经装到位。水箱松动可能导致产品无法工作。', figures: ['operation.make_ice.seat_tank'] },
    ],
    steps_page_2: [
      { id: 'return_basket', text: '然后放入子弹冰篮，并关闭腔盖。', figures: ['operation.make_ice.return_basket', 'operation.make_ice.close_lid', 'operation.make_ice.closed_unit'], gap: '3mm', max_height: '28mm', max_width: '30%' },
      { id: 'select_size', text: '点击 <b>Make Ice</b> 按键，切换点亮按键上方的 S / M / L 指示灯，选择需要制作的子弹冰尺寸。', figures: ['operation.make_ice.select_size'], max_height: '28mm', max_width: '55%' },
      { id: 'start_cycle', text: '选择完尺寸后，产品自动开始制作子弹冰。' },
    ],
    notice_title: '提示 NOTICE',
    notice_items: [
      '制冰中途可点击 <b>Make Ice</b> 按键切换制冰尺寸。',
      '制冰中途可点击 <b>Power</b> 按键终止，子弹冰制冰按键灯熄灭，产品停止子弹冰制冰。',
      '当产品检测到子弹冰冰篮装满后，<b>ICE FULL</b> 警示灯点亮为绿灯，产品停止制冰。待冰融解，或取走后，产品会自动恢复制冰。',
      '请留意，制冰期间若 <b>ADD WATER</b> 警示灯点亮红灯，产品会停止制冰，请及时给水箱补充水。',
    ],
  },
  en: {
    title: 'Operation Guide',
    continuation: 'Operation Guide (Cont.)',
    prep_title: 'Preparation Before Use',
    prep_items: [
      'Place the unit on a stable, level surface. Keep the rear side and right-side ventilation openings clear. Maintain at least 120 mm (4.7 in) of clearance from walls or other objects for proper airflow.',
      'Before first use, or if the unit has not been used for a long time, run one cleaning cycle first. Refer to CH.08 Maintenance for the cleaning procedure.',
    ],
    power_title: 'Powering On',
    power_items: [
      'Connect the power supply. The unit emits one beep, all indicators light up and then turn off, which means the unit is powered.',
      'Press the <b>Power</b> button. The indicator lights white, which means the unit is on.',
    ],
    make_title: 'Making Bullet Ice',
    steps_page_1: [
      { id: 'open_lid', text: 'Open the lid and remove the ice basket and water tank.' },
      { id: 'fill_tank', text: 'Fill the bullet-ice water tank with drinking water up to the water level line.', figures: ['operation.make_ice.fill_tank', 'operation.make_ice.max_mark'] },
      { id: 'seat_tank', text: 'Place the water tank back into the bullet-ice chamber. Press down on the tank by hand to make sure it is fully seated. A loose tank may prevent the unit from operating.', figures: ['operation.make_ice.seat_tank'] },
    ],
    steps_page_2: [
      { id: 'return_basket', text: 'Place the ice basket back in and close the lid.', figures: ['operation.make_ice.return_basket', 'operation.make_ice.close_lid', 'operation.make_ice.closed_unit'], gap: '3mm', max_height: '28mm', max_width: '30%' },
      { id: 'select_size', text: 'Press the <b>Make Ice</b> button. Switch the S / M / L indicator above the button to select the desired bullet-ice size.', figures: ['operation.make_ice.select_size'], max_height: '28mm', max_width: '55%' },
      { id: 'start_cycle', text: 'After the size is selected, the unit starts making bullet ice automatically.' },
    ],
    notice_title: 'NOTICE',
    notice_items: [
      'During ice-making, press <b>Make Ice</b> to switch the ice size.',
      'During ice-making, press <b>Power</b> to stop the bullet-ice cycle. The ice-making indicator turns off and the unit stops making bullet ice.',
      'When the basket is full, the <b>ICE FULL</b> indicator lights green and the unit stops making ice. After the ice melts or is removed, the unit resumes automatically.',
      'If the <b>ADD WATER</b> indicator lights red during ice-making, the unit stops. Refill the water tank promptly.',
    ],
  },
  de: {
    title: 'Bedienungsanleitung',
    continuation: 'Bedienungsanleitung (Forts.)',
    prep_title: 'Vorbereitung vor dem Betrieb',
    prep_items: [
      'Stellen Sie das Gerät auf eine stabile, ebene Fläche. Halten Sie die Rückseite und die rechten Lüftungsöffnungen frei. Der Abstand zu Wänden oder Gegenständen muss mindestens 120 mm betragen, damit die Belüftung gewährleistet ist.',
      'Vor der ersten Verwendung oder nach längerer Nichtbenutzung führen Sie bitte zuerst einen Reinigungszyklus durch. Siehe CH.08 Wartung und Pflege.',
    ],
    power_title: 'Gerät einschalten',
    power_items: [
      'Schließen Sie die Stromversorgung an. Das Gerät gibt einen Signalton aus, alle Tasten leuchten kurz auf und erlöschen wieder. Damit ist die Stromversorgung aktiv.',
      'Drücken Sie die <b>Power</b>-Taste. Die Anzeige leuchtet weiß und das Gerät ist eingeschaltet.',
    ],
    make_title: 'Bullet-Eis herstellen',
    steps_page_1: [
      { id: 'open_lid', text: 'Öffnen Sie den Deckel und nehmen Sie den Eiskorb und den Wassertank heraus.' },
      { id: 'fill_tank', text: 'Füllen Sie den Bullet-Eis-Wassertank mit Trinkwasser bis zur Wasserstandslinie.', figures: ['operation.make_ice.fill_tank', 'operation.make_ice.max_mark'] },
      { id: 'seat_tank', text: 'Setzen Sie den Wassertank wieder in den Innenraum ein. Drücken Sie den Tank von Hand nach unten, damit er sicher sitzt. Ein lockerer Tank kann den Betrieb verhindern.', figures: ['operation.make_ice.seat_tank'] },
    ],
    steps_page_2: [
      { id: 'return_basket', text: 'Setzen Sie den Eiskorb wieder ein und schließen Sie den Deckel.', figures: ['operation.make_ice.return_basket', 'operation.make_ice.close_lid', 'operation.make_ice.closed_unit'], gap: '3mm', max_height: '28mm', max_width: '30%' },
      { id: 'select_size', text: 'Drücken Sie die Taste <b>Make Ice</b>. Schalten Sie die Anzeige S / M / L oberhalb der Taste um, um die gewünschte Bullet-Eis-Größe zu wählen.', figures: ['operation.make_ice.select_size'], max_height: '28mm', max_width: '55%' },
      { id: 'start_cycle', text: 'Nach der Größenauswahl beginnt das Gerät automatisch mit der Herstellung von Bullet-Eis.' },
    ],
    notice_title: 'HINWEIS',
    notice_items: [
      'Während des Betriebs können Sie mit <b>Make Ice</b> die Eisgröße wechseln.',
      'Während des Betriebs können Sie mit <b>Power</b> den Bullet-Eis-Zyklus beenden. Die Anzeige erlischt und das Gerät stoppt die Eisherstellung.',
      'Wenn der Korb voll ist, leuchtet die Anzeige <b>ICE FULL</b> grün und das Gerät stoppt. Nachdem das Eis geschmolzen oder entnommen wurde, setzt das Gerät den Betrieb automatisch fort.',
      'Leuchtet während der Eisherstellung die Anzeige <b>ADD WATER</b> rot, stoppt das Gerät. Füllen Sie den Wassertank rechtzeitig nach.',
    ],
  },
  it: {
    title: 'Guida al funzionamento',
    continuation: 'Guida al funzionamento (seguito)',
    prep_title: 'Preparazione prima dell’uso',
    prep_items: [
      'Posizionare l’unità su una superficie stabile e piana. Lasciare libere la parte posteriore e le aperture di ventilazione sul lato destro. La distanza da pareti o altri oggetti deve essere di almeno 120 mm per garantire una ventilazione adeguata.',
      'Prima del primo utilizzo, o se l’unità non è stata usata per molto tempo, eseguire un ciclo di pulizia. Fare riferimento al CH.08 Manutenzione.',
    ],
    power_title: 'Accensione del prodotto',
    power_items: [
      'Collegare l’alimentazione. L’unità emette un segnale acustico, tutti i pulsanti si illuminano e poi si spengono: questo indica che l’alimentazione è attiva.',
      'Premere il pulsante <b>Power</b>. L’indicatore si illumina di bianco e l’unità è accesa.',
    ],
    make_title: 'Produzione del ghiaccio bullet',
    steps_page_1: [
      { id: 'open_lid', text: 'Aprire il coperchio e rimuovere il cestello del ghiaccio e il serbatoio dell’acqua.' },
      { id: 'fill_tank', text: 'Riempire il serbatoio dell’acqua per il ghiaccio bullet con acqua potabile fino alla linea del livello.', figures: ['operation.make_ice.fill_tank', 'operation.make_ice.max_mark'] },
      { id: 'seat_tank', text: 'Riposizionare il serbatoio nella camera interna. Premere il serbatoio verso il basso con la mano per assicurarsi che sia correttamente in sede. Un serbatoio non ben posizionato può impedire il funzionamento dell’unità.', figures: ['operation.make_ice.seat_tank'] },
    ],
    steps_page_2: [
      { id: 'return_basket', text: 'Riposizionare il cestello del ghiaccio e chiudere il coperchio.', figures: ['operation.make_ice.return_basket', 'operation.make_ice.close_lid', 'operation.make_ice.closed_unit'], gap: '3mm', max_height: '28mm', max_width: '30%' },
      { id: 'select_size', text: 'Premere il pulsante <b>Make Ice</b>. Selezionare l’indicatore S / M / L sopra il pulsante per scegliere la dimensione desiderata del ghiaccio bullet.', figures: ['operation.make_ice.select_size'], max_height: '28mm', max_width: '55%' },
      { id: 'start_cycle', text: 'Dopo la selezione della dimensione, l’unità avvia automaticamente la produzione del ghiaccio bullet.' },
    ],
    notice_title: 'AVVISO',
    notice_items: [
      'Durante la produzione del ghiaccio è possibile premere <b>Make Ice</b> per cambiare la dimensione.',
      'Durante la produzione del ghiaccio è possibile premere <b>Power</b> per interrompere il ciclo del ghiaccio bullet. L’indicatore si spegne e l’unità interrompe la produzione.',
      'Quando il cestello è pieno, l’indicatore <b>ICE FULL</b> si illumina in verde e l’unità si arresta. Dopo che il ghiaccio si è sciolto o è stato rimosso, l’unità riprende automaticamente.',
      'Se durante la produzione del ghiaccio l’indicatore <b>ADD WATER</b> si illumina in rosso, l’unità si arresta. Riempire tempestivamente il serbatoio dell’acqua.',
    ],
  },
};

function buildImt050OperationChapter(lang, legacyChapter) {
  const data = imt050OperationData[lang];
  const [page1, page2] = legacyChapter.pages;

  return {
    ...legacyChapter,
    title: data.title,
    toc_title: data.title,
    pages: [
      {
        page_class: page1.page_class,
        section_title: data.title,
        blocks: [
          { type: 'sub_title', text: data.prep_title },
          { type: 'bullet_list', items: data.prep_items },
          { type: 'sub_title', text: data.power_title },
          { type: 'bullet_list', items: data.power_items },
          { type: 'sub_title', text: data.make_title },
          {
            type: 'step_flow',
            start_at: 1,
            figure_margin: '4px 0 6px',
            max_height: '24mm',
            max_width: '35%',
            steps: data.steps_page_1,
          },
        ],
      },
      {
        page_class: page2.page_class,
        section_title: data.continuation,
        blocks: [
          {
            type: 'step_flow',
            start_at: 4,
            figure_margin: '4px 0 6px',
            max_height: '24mm',
            max_width: '35%',
            steps: data.steps_page_2,
          },
          {
            type: 'figure_row',
            className: 'status-indicator-row',
            gap: '4mm',
            align: 'center',
            justify: 'center',
            margin: '8px 0 4px',
            font_size: '9px',
            items: [
              { label_before: 'ICE FULL → ', figure: 'operation.make_ice.ice_full_status', height: '14px' },
              { label_before: 'ADD WATER → ', figure: 'operation.make_ice.add_water_status', height: '14px' },
            ],
          },
          {
            type: 'notice_box',
            title: data.notice_title,
            items: data.notice_items,
          },
        ],
      },
    ],
  };
}

function buildImagesManifest(product) {
  if (product === 'imt050') {
    return {
      'cover.main': { file: 'image1.png', alt: 'Product cover image' },
      'safety.warning_icon': { file: 'image3.png', alt: 'Warning icon' },
      'structure.main': { file: 'image5.png', alt: 'Product structure diagram' },
      'structure.legend': { file: 'image7.png', alt: 'Structure legend' },
      'control_panel.main': { file: 'image9.png', alt: 'Control panel diagram' },
      'cleaning.drain_plug': { file: 'image10.png', alt: 'Drain plug' },
      'cleaning.drain_container': { file: 'image12.png', alt: 'Drain container' },
      'operation.make_ice.fill_tank': { file: 'image14.png', alt: 'Fill water tank', kind: 'procedural' },
      'operation.make_ice.max_mark': { file: 'image16.png', alt: 'Water level mark', kind: 'procedural' },
      'operation.make_ice.seat_tank': { file: 'image18.png', alt: 'Seat tank inside chamber', kind: 'procedural' },
      'operation.make_ice.return_basket': { file: 'image20.png', alt: 'Return ice basket', kind: 'procedural' },
      'operation.make_ice.close_lid': { file: 'image22.png', alt: 'Close lid', kind: 'procedural' },
      'operation.make_ice.closed_unit': { file: 'image24.png', alt: 'Unit closed', kind: 'procedural' },
      'operation.make_ice.select_size': { file: 'image26.png', alt: 'Select ice size', kind: 'procedural' },
      'operation.make_ice.ice_full_status': { file: 'image28.png', alt: 'Ice full indicator', kind: 'procedural' },
      'operation.make_ice.add_water_status': { file: 'image30.png', alt: 'Add water indicator', kind: 'procedural' },
      'warranty.separator.primary': { file: 'image31.png', alt: 'Warranty separator', kind: 'shared' },
      'warranty.separator.secondary': { file: 'image32.png', alt: 'Warranty separator', kind: 'shared' },
    };
  }

  return {
    'cover.main': { file: 'cover-image.png', alt: 'Product cover image' },
    'safety.warning_icon': { file: 'image3.png', alt: 'Warning icon' },
    'structure.main': { file: 'image5.svg', alt: 'Product structure diagram' },
    'control_panel.main': { file: 'image10.svg', alt: 'Control panel diagram' },
    'warranty.separator.primary': { file: 'image31.png', alt: 'Warranty separator', kind: 'shared' },
  };
}

function buildManifest(chapters) {
  return {
    chapters: chapters.map((chapter) => ({
      chapter_id: chapter.chapter_id,
      chapter_no: chapter.chapter_no,
      title: chapter.title,
      toc_title: chapter.toc_title,
      header_ref: chapter.header_ref,
      enabled: true,
      file: `${chapter.chapter_id}.json`,
    })),
  };
}

function migrateProduct(product) {
  const productDir = path.join(swissRoot, 'products', product);
  const configPath = path.join(productDir, 'config.json');
  const productPath = path.join(productDir, 'product.json');

  fs.copyFileSync(configPath, productPath);
  writeJson(path.join(productDir, 'images.json'), buildImagesManifest(product));

  for (const lang of langs) {
    const legacyPath = path.join(productDir, `content.${lang}.json`);
    if (!fs.existsSync(legacyPath)) {
      continue;
    }

    const legacy = readJson(legacyPath);
    const bodyHtml = legacy.blocks ? legacy.blocks.CONTENT_BODY : legacy.CONTENT_BODY;
    if (typeof bodyHtml !== 'string') {
      throw new Error(`Legacy content missing CONTENT_BODY: ${legacyPath}`);
    }

    const pageMetas = splitPages(bodyHtml).map(parsePage);
    const legacyChapters = chunkPagesIntoChapters(pageMetas);
    const chapters = legacyChapters.map((chapter) => {
      if (product === 'imt050' && chapter.chapter_no === '01') {
        return buildImt050SafetyChapter(lang, chapter);
      }
      if (product === 'imt050' && chapter.chapter_no === '06') {
        return buildImt050OperationChapter(lang, chapter);
      }
      return chapter;
    });

    const contentRoot = path.join(productDir, 'content', lang);
    const chaptersDir = path.join(contentRoot, 'chapters');
    fs.rmSync(contentRoot, { recursive: true, force: true });
    fs.mkdirSync(chaptersDir, { recursive: true });

    writeJson(path.join(contentRoot, 'manifest.json'), buildManifest(chapters));
    for (const chapter of chapters) {
      writeJson(path.join(chaptersDir, `${chapter.chapter_id}.json`), chapter);
    }
  }
}

for (const product of products) {
  migrateProduct(product);
  console.log(`Migrated ${product} -> JSON single-source schema`);
}
