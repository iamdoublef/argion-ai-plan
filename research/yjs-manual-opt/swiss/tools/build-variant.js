#!/usr/bin/env node
/**
 * build-variant.js — Config-driven manual variant builder (multi-language)
 *
 * Usage:
 *   node build-variant.js --region cn                     # China mainland / zh-CN / EU
 *   node build-variant.js --region gb --brand vesta       # UK English / Vesta / EU
 *   node build-variant.js --region de --brand act         # German / ACT / EU
 *   node build-variant.js --region tw --brand wevac       # Taiwan / Traditional CN / US
 *   node build-variant.js --region hk                     # Hong Kong / Traditional CN / EU
 *   node build-variant.js --all                           # Build all 21 variants
 */
const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// CLI args
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}
const buildAll = args.includes('--all');

const productDir = path.resolve(getArg('product', path.resolve(__dirname, '..', 'products', 'v23')));
const regionKey  = getArg('region', 'cn');
const brandKey   = getArg('brand', null);
const outputDir  = path.resolve(__dirname, '..', 'output');

// ---------------------------------------------------------------------------
// Load product data
// ---------------------------------------------------------------------------
function loadProductConfig(dir) {
  const configPath = path.join(dir, 'product.json');
  if (!fs.existsSync(configPath)) {
    throw new Error(`Product data not found: ${configPath}`);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

const config = loadProductConfig(productDir);

// ---------------------------------------------------------------------------
// Simplified → Traditional Chinese mapping (covers all characters in the manual)
// ---------------------------------------------------------------------------
const S2T_MAP = {
  '让':'讓','儿':'兒','动':'動','认':'認','应':'應','监':'監','督':'督','间':'間','请':'請',
  '留':'留','发':'發','开':'開','关':'關','连':'連','线':'線','损':'損','坏':'壞','联':'聯',
  '维':'維','护':'護','对':'對','尖':'尖','针':'針','纸':'紙','张':'張','须':'須','纹':'紋',
  '热':'熱','储':'儲','鲜':'鮮','过':'過','质':'質','选':'選','择':'擇','冻':'凍','压':'壓',
  '机':'機','产':'產','结':'結','构':'構','图':'圖','编':'編','号':'號','称':'稱','锁':'鎖',
  '扣':'扣','控':'控','制':'製','抽':'抽','气':'氣','盖':'蓋','密':'密','封':'封','圈':'圈',
  '卷':'卷','袋':'袋','仓':'倉','撑':'撐','管':'管','体':'體','刀':'刀','液':'液','槽':'槽',
  '腔':'腔','温':'溫','胶':'膠','布':'布','单':'單','独':'獨','长':'長','键':'鍵','灯':'燈',
  '亮':'亮','恢':'恢','复':'復','默':'默','认':'認','设':'設','置':'置','禁':'禁','智':'智',
  '能':'能','调':'調','节':'節','续':'續','工':'工','作':'作','隔':'隔','散':'散','实':'實',
  '固':'固','启':'啟','终':'終','止':'止','柔':'柔','贵':'貴','碎':'碎','满':'滿','直':'直',
  '确':'確','保':'保','面':'面','松':'鬆','暂':'暫','达':'達','释':'釋','退':'退','出':'出',
  '闭':'閉','罐':'罐','拧':'擰','适':'適','配':'配','装':'裝','软':'軟','覆':'覆','盖':'蓋',
  '轻':'輕','微':'微','兼':'兼','容':'容','阀':'閥','将':'將','食':'食','物':'物','酱':'醬',
  '料':'料','两':'兩','则':'則','宽':'寬','专':'專','用':'用','电':'電','源':'源','插':'插',
  '入':'入','破':'破','裂':'裂','板':'板','排':'排','脱':'脫','咨':'諮','询':'詢','专':'專',
  '业':'業','修':'修','全':'全','部':'部','内':'內','翻':'翻','起':'起','正':'正','异':'異',
  '无':'無','法':'法','拉':'拉','链':'鏈','方':'方','向':'向','标':'標','可':'可','示':'示',
  '参':'參','考':'考','升':'升','级':'級','略':'略','差':'差','阅':'閱','读':'讀','说':'說',
  '明':'明','书':'書','妥':'妥','善':'善','购':'購','买':'買','凭':'憑','证':'證','享':'享',
  '受':'受','服':'服','务':'務','清':'清','洁':'潔','拔':'拔','毛':'毛','刷':'刷','避':'避',
  '免':'免','硬':'硬','残':'殘','碎':'碎','屑':'屑','尘':'塵','检':'檢','查':'查','严':'嚴',
  '重':'重','变':'變','形':'形','脱':'脫','落':'落','时':'時','替':'替','换':'換','支':'支',
  '持':'持','高':'高','霉':'霉','菌':'菌','氧':'氧','环':'環','境':'境','繁':'繁','殖':'殖',
  '抑':'抑','酵':'酵','母':'母','水':'水','糖':'糖','中':'中','等':'等','存':'存','减':'減',
  '缓':'緩','生':'生','冷':'冷','藏':'藏','有':'有','效':'效','细':'細','导':'導','难':'難',
  '闻':'聞','味':'味','道':'道','适':'適','当':'當','条':'條','件':'件','肉':'肉','毒':'毒',
  '梭':'梭','前':'前','是':'是','否':'否','非':'非','常':'常','规':'規','运':'運','输':'輸',
  '经':'經','销':'銷','商':'商','零':'零','售':'售','合':'合','伙':'夥','伴':'伴','须':'須',
  '提':'提','供':'供','原':'原','始':'始','收':'收','据':'據','副':'副','本':'本','客':'客',
  '户':'戶','城':'城','州':'州','邮':'郵','政':'政','邮':'郵','箱':'箱','日':'日','期':'期',
  '型':'型','序':'序','列':'列','商':'商','蔬':'蔬','菜':'菜','焯':'焯','沸':'沸','煮':'煮',
  '熟':'熟','浸':'浸','吸':'吸','干':'乾','十':'十','字':'字','花':'花','科':'科','芽':'芽',
  '卷':'卷','心':'心','排':'排','放':'放','存':'存','冰':'冰','箱':'箱','切':'切','忌':'忌',
  '大':'大','蒜':'蒜','蘑':'蘑','菇':'菇','菌':'菌','品':'品','害':'害','影':'影','响':'響',
  '健':'健','康':'康','类':'類','海':'海','月':'月','天':'天','鱼':'魚','干':'乾','果':'果',
  '咖':'咖','啡':'啡','豆':'豆','蛋':'蛋','面':'麵','包':'包','饼':'餅','粉':'粉','米':'米',
  '货':'貨','茶':'茶','叶':'葉','奶':'奶','总':'總','寿':'壽','命':'命','风':'風','帮':'幫',
  '助':'助','量':'量','个':'個','执':'執','行':'行','进':'進','预':'預','扁':'扁','嘴':'嘴',
  '圆':'圓','瓶':'瓶','塞':'塞','腌':'醃','网':'網','址':'址','邮':'郵','制':'製','造':'造',
  '厂':'廠','地':'地','信':'信','息':'息','年':'年','限':'限','数':'數','量':'量','获':'獲',
  '得':'得','资':'資','格':'格','程':'程','点':'點','击':'擊','运':'運','电':'電','仅':'僅',
  '烫':'燙','伤':'傷','断':'斷','拆':'拆','悬':'懸','挂':'掛','台':'臺','绊':'絆','倒':'倒',
  '润':'潤','滑':'滑','剂':'劑','有':'有','丢':'丟','弃':'棄','垃':'垃','圾':'圾','回':'回',
  '或':'或','处':'處','份':'份','系':'繫','权':'權','整':'整','齐':'齊','割':'割','端':'端',
  '制':'製','从':'從','拉':'拉','扯':'扯','移':'移','至':'至','刀':'刀','架':'架','滑':'滑',
  '划':'劃','功':'功','指':'指','引':'引','操':'操','如':'如','何':'何','使':'使','打':'打',
  '卷':'卷','拉':'拉','所':'所','需':'需','度':'度','最':'最','左':'左','右':'右','边':'邊',
  '下':'下','着':'著','以':'以','平':'平','放':'放','并':'並','把':'把','手':'手','向':'向',
  '等':'等','待':'待','完':'完','成':'成','步':'步','骤':'驟','份':'份','需':'需','在':'在',
  '和':'和','之':'之','建':'建','议':'議','留':'留','间':'間','空':'空','模':'模','式':'式',
  '若':'若','终':'終','止':'止','采':'採','尝':'嘗','试':'試','后':'後','否':'否','足':'足',
  '状':'狀','态':'態','配':'配','可':'可','处':'處','于':'於','旋':'旋','转':'轉','力':'力',
  '挡':'擋','当':'當','段':'段','分':'分','钟':'鐘','底':'底','垫':'墊','厨':'廚','房':'房',
  '纸':'紙','盘':'盤','通':'通','电':'電','合':'合','上':'上','次':'次','复':'復','倒':'倒',
  '小':'小','凉':'涼','汁':'汁','弄':'弄','湿':'濕','擦':'擦','容':'容','纳':'納','还':'還',
  '看':'看','几':'幾','问':'問','题':'題','方':'方','案':'案','解':'解','决':'決','按':'按',
  '报':'報','警':'警','蜂':'蜂','鸣':'鳴','声':'聲','鸣':'鳴','闪':'閃','目':'目','录':'錄',
  '须':'須','知':'知','技':'技','术':'術','故':'故','障':'障','养':'養','特':'特','性':'性',
  '怎':'怎','样':'樣','安':'安','全':'全','为':'為','其':'其','他':'他','设':'設','计':'計',
  '途':'途','成':'成','人':'人','期':'期','意':'意','外':'外','造':'造','窒':'窒','息':'息',
  '危':'危','险':'險','接':'接','触':'觸','湿':'濕','严':'嚴','燃':'燃','爆':'爆','炸':'炸',
  '确':'確','铭':'銘','牌':'牌','离':'離','区':'區','域':'域','勿':'勿','主':'主','浸':'浸',
  '符':'符','合':'合','范':'範','停':'停','授':'授','自':'自','供':'供','添':'添','加':'加',
  '任':'任','何':'何','溶':'溶','受':'受','丝':'絲','参':'參','规':'規','规':'規','格':'格',
  '泵':'泵','宽':'寬','尺':'尺','寸':'寸',
};

function toTraditional(text) {
  let result = '';
  for (const ch of text) {
    result += S2T_MAP[ch] || ch;
  }
  return result;
}

// ---------------------------------------------------------------------------
// Language helpers — pick the right field suffix for the target language
// ---------------------------------------------------------------------------
function langSuffix(lang) {
  if (lang.startsWith('zh')) return 'cn';
  if (lang.startsWith('de')) return 'de';
  if (lang.startsWith('it')) return 'it';
  return 'en';
}

function pickField(obj, base, suffix) {
  const key = `${base}_${suffix}`;
  return obj[key] !== undefined ? obj[key] : (obj[base] || '');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function resolveTemplateIncludes(entryPath, templateRoot, stack = []) {
  const normalizedEntry = path.resolve(entryPath);
  const normalizedRoot = path.resolve(templateRoot);
  const includePattern = /\{\{>\s*([^}\s]+)\s*\}\}/g;

  if (!normalizedEntry.startsWith(normalizedRoot)) {
    throw new Error(`Template include escapes template root: ${normalizedEntry}`);
  }
  if (stack.includes(normalizedEntry)) {
    throw new Error(`Template include cycle detected: ${[...stack, normalizedEntry].join(' -> ')}`);
  }
  if (!fs.existsSync(normalizedEntry)) {
    throw new Error(`Template include not found: ${normalizedEntry}`);
  }

  const source = fs.readFileSync(normalizedEntry, 'utf8');
  return source.replace(includePattern, (_, includeRef) => {
    const includePath = path.resolve(normalizedRoot, includeRef);
    return resolveTemplateIncludes(includePath, normalizedRoot, [...stack, normalizedEntry]);
  });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function replaceTemplateSlots(html, blocks) {
  let rendered = html;

  for (const [key, value] of Object.entries(blocks)) {
    if (typeof value !== 'string') {
      throw new Error(`Template slot "${key}" must be a string`);
    }

    const pattern = new RegExp(`{{#${escapeRegExp(key)}}}`, 'g');
    rendered = rendered.replace(pattern, value);
  }

  return rendered;
}

function stripTags(value = '') {
  return value.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function escapeHtml(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttribute(value = '') {
  return escapeHtml(value).replace(/`/g, '&#96;');
}

const RAW_HTML_PATTERN = /<\/?[a-z][^>]*>/i;

function validateTextTokenValue(value, label = 'text field') {
  const normalized = String(value ?? '');
  if (RAW_HTML_PATTERN.test(normalized)) {
    throw new Error(`Raw HTML is not allowed in ${label}: ${normalized}`);
  }
}

function renderTextTokens(value = '') {
  validateTextTokenValue(value, 'text token field');
  const normalized = String(value).replace(/\r\n/g, '\n');
  const escaped = escapeHtml(normalized);
  return escaped
    .replace(/\[btn:([^\]]+)\]/g, '<span class="btn-name">$1</span>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/\n/g, '<br>');
}

function loadImagesManifest(productDir) {
  const imagesPath = path.join(productDir, 'images.json');
  if (!fs.existsSync(imagesPath)) {
    return {};
  }

  const manifest = readJson(imagesPath);
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    throw new Error(`Invalid images manifest: ${imagesPath}`);
  }
  return manifest;
}

function normalizeChapterEntry(entry, chapter) {
  return {
    chapter_id: entry.chapter_id,
    chapter_no: entry.chapter_no,
    title: chapter.title || entry.title,
    toc_title: chapter.toc_title || entry.toc_title || chapter.title || entry.title,
    header_ref: chapter.header_ref || entry.header_ref,
    enabled: entry.enabled !== false,
    file: entry.file,
    pages: chapter.pages || [],
  };
}

function validateManifestEntry(entry, contentRoot) {
  const requiredFields = ['chapter_id', 'chapter_no', 'title', 'toc_title', 'header_ref', 'file'];
  for (const field of requiredFields) {
    if (!entry[field]) {
      throw new Error(`Manifest entry missing "${field}" in ${path.join(contentRoot, 'manifest.json')}`);
    }
  }
}

function validateManifest(manifest, contentRoot) {
  let expectedChapterNo = 1;
  for (const entry of manifest.chapters) {
    validateManifestEntry(entry, contentRoot);
    const actualChapterNo = Number(entry.chapter_no);
    if (!Number.isInteger(actualChapterNo) || actualChapterNo !== expectedChapterNo) {
      throw new Error(`Manifest chapter numbering must be continuous in ${path.join(contentRoot, 'manifest.json')}: expected ${String(expectedChapterNo).padStart(2, '0')} got ${entry.chapter_no}`);
    }
    expectedChapterNo += 1;
  }
}

function loadContentDocument(productDir, templateLang) {
  const contentRoot = path.join(productDir, 'content', templateLang);
  const manifestPath = path.join(contentRoot, 'manifest.json');

  if (!fs.existsSync(manifestPath)) {
    throw new Error(`Structured content manifest not found: ${manifestPath}`);
  }

  const manifest = readJson(manifestPath);
  if (!manifest || !Array.isArray(manifest.chapters)) {
    throw new Error(`Invalid manifest file: ${manifestPath}`);
  }

  validateManifest(manifest, contentRoot);

  const chapters = manifest.chapters.map((entry) => {
    const chapterPath = path.join(contentRoot, 'chapters', entry.file);
    if (!fs.existsSync(chapterPath)) {
      throw new Error(`Chapter file not found: ${chapterPath}`);
    }

    const chapter = readJson(chapterPath);
    if (chapter.chapter_id && chapter.chapter_id !== entry.chapter_id) {
      throw new Error(`Chapter id mismatch: manifest=${entry.chapter_id} chapter=${chapter.chapter_id}`);
    }
    if (!Array.isArray(chapter.pages)) {
      throw new Error(`Chapter pages must be an array: ${chapterPath}`);
    }

    return normalizeChapterEntry(entry, chapter);
  });

  return {
    kind: 'structured',
    manifest,
    chapters,
  };
}

function styleAttr(styleMap = {}) {
  const entries = Object.entries(styleMap).filter(([, value]) => value !== undefined && value !== null && value !== '');
  if (!entries.length) {
    return '';
  }
  const css = entries.map(([key, value]) => `${key}:${value}`).join(';');
  return ` style="${escapeAttribute(css)}"`;
}

function resolveFigure(figureRef, context) {
  if (typeof figureRef === 'string') {
    const figure = context.images[figureRef];
    if (!figure) {
      throw new Error(`Missing image id: ${figureRef}`);
    }
    return {
      id: figureRef,
      ...figure,
    };
  }

  if (figureRef && typeof figureRef === 'object') {
    if (figureRef.figure) {
      return {
        ...resolveFigure(figureRef.figure, context),
        ...figureRef,
      };
    }
    if (figureRef.file) {
      return figureRef;
    }
  }

  throw new Error(`Invalid figure reference: ${JSON.stringify(figureRef)}`);
}

function renderFigureImage(figureRef, context, defaults = {}) {
  const figure = resolveFigure(figureRef, context);
  const style = {
    'max-height': figure.max_height || defaults.max_height || defaults['max-height'],
    'max-width': figure.max_width || defaults.max_width || defaults['max-width'],
    width: figure.width || defaults.width,
    height: figure.height || defaults.height,
    'object-fit': figure.object_fit || defaults.object_fit || defaults['object-fit'] || 'contain',
    display: figure.display || defaults.display,
    'vertical-align': figure.vertical_align || defaults.vertical_align || defaults['vertical-align'],
  };

  return `<img src="./${context.config.images_dir}/${figure.file}" alt="${escapeAttribute(figure.alt || '')}"${styleAttr(style)}>`;
}

function renderBlockListItems(items = []) {
  return items.map((item) => `<li>${renderTextTokens(item)}</li>`).join('\n');
}

function renderTableRef(block, context) {
  const tableLabels = {
    cn: {
      specs: ['参数', '规格'],
      parts: ['编号', '名称', '编号', '名称'],
      buttons: ['No. / 按键', '功能说明'],
      brand: ['项目', '信息'],
      brand_info: ['项目', '信息'],
      manufacturer: ['项目', '信息'],
      manufacturer_info: ['项目', '信息'],
    },
    en: {
      specs: ['Parameter', 'Specification'],
      parts: ['No.', 'Part', 'No.', 'Part'],
      buttons: ['No. / Button', 'Description'],
      brand: ['Field', 'Information'],
      brand_info: ['Field', 'Information'],
      manufacturer: ['Field', 'Information'],
      manufacturer_info: ['Field', 'Information'],
    },
    de: {
      specs: ['Parameter', 'Spezifikation'],
      parts: ['Nr.', 'Teil', 'Nr.', 'Teil'],
      buttons: ['Nr. / Taste', 'Beschreibung'],
      brand: ['Feld', 'Information'],
      brand_info: ['Feld', 'Information'],
      manufacturer: ['Feld', 'Information'],
      manufacturer_info: ['Feld', 'Information'],
    },
    it: {
      specs: ['Parametro', 'Specifica'],
      parts: ['N.', 'Parte', 'N.', 'Parte'],
      buttons: ['N. / Pulsante', 'Descrizione'],
      brand: ['Campo', 'Informazione'],
      brand_info: ['Campo', 'Informazione'],
      manufacturer: ['Campo', 'Informazione'],
      manufacturer_info: ['Campo', 'Informazione'],
    },
  };

  const labels = tableLabels[context.suffix] || tableLabels.en;
  const headers = block.headers || labels[block.table];

  if (Array.isArray(block.rows)) {
    const renderCell = (cell, isHeader = false) => {
      const normalized = typeof cell === 'string' ? { text: cell } : cell;
      const attrs = [];
      if (normalized.width) attrs.push(` style="width:${escapeAttribute(normalized.width)};"`);
      if (normalized.rowspan) attrs.push(` rowspan="${escapeAttribute(normalized.rowspan)}"`);
      if (normalized.colspan) attrs.push(` colspan="${escapeAttribute(normalized.colspan)}"`);
      const tag = isHeader ? 'th' : 'td';
      return `<${tag}${attrs.join('')}>${renderTextTokens(normalized.text || '')}</${tag}>`;
    };

    const headerHtml = headers
      ? `<thead><tr>${headers.map((header) => renderCell(header, true)).join('')}</tr></thead>`
      : '';
    const rowsHtml = block.rows
      .map((row) => `<tr>${row.map((cell) => renderCell(cell)).join('')}</tr>`)
      .join('\n');

    return `<table>
    ${headerHtml}
    <tbody>
${rowsHtml}
    </tbody>
  </table>`;
  }

  switch (block.table) {
    case 'specs':
      return `<table>
    <thead><tr><th>${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildSpecsRows(context.specs)}
    </tbody>
  </table>`;
    case 'parts':
      return `<table>
    <thead><tr><th style="width:15%;">${headers[0]}</th><th>${headers[1]}</th><th style="width:15%;">${headers[2]}</th><th>${headers[3]}</th></tr></thead>
    <tbody>
${context.builders.buildPartsRows(context.config.parts)}
    </tbody>
  </table>`;
    case 'buttons':
      return `<table>
    <thead><tr><th style="width:45%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildButtonsRows(context.config.buttons)}
    </tbody>
  </table>`;
    case 'brand_info':
      return `<table>
    <thead><tr><th style="width:30%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildBrandInfoRows(context.brand)}
    </tbody>
  </table>`;
    case 'manufacturer_info':
      return `<table>
    <thead><tr><th style="width:30%;">${headers[0]}</th><th>${headers[1]}</th></tr></thead>
    <tbody>
${context.builders.buildManufacturerRows(context.mfr)}
    </tbody>
  </table>`;
    default:
      throw new Error(`Unknown table ref: ${block.table}`);
  }
}

function renderFigure(block, context) {
  const image = renderFigureImage(block.figure, context, {
    'max-height': block.max_height,
    'max-width': block.max_width,
  });
  const caption = block.caption ? `<div class="fig-caption">${renderTextTokens(block.caption)}</div>` : '';
  const className = block.className ? ` ${block.className}` : '';

  return `<div class="fig-wrap${className}">
    ${image}
    ${caption}
  </div>`;
}

function renderSplitPanel(block, context) {
  const className = block.className ? ` ${block.className}` : '';
  const style = {
    gap: block.gap || '16px',
    'align-items': block.align || 'flex-start',
    'margin-bottom': block.margin_bottom,
    margin: block.margin,
  };

  const bodyBlocks = (block.body_blocks || []).map((childBlock) => renderBlock(childBlock, context)).join('\n');
  const figures = (block.figures || []).map((figureRef) => {
    const figure = typeof figureRef === 'string' ? { figure: figureRef } : figureRef;
    return renderFigureImage(figure, context, {
      width: figure.width || block.figure_width,
      'max-height': figure.max_height || block.max_height,
      'max-width': figure.max_width || block.max_width,
      display: 'block',
    });
  }).join('\n');

  return `<div class="split-panel${className}"${styleAttr(style)}>
    <div class="split-panel-body">
      ${bodyBlocks}
    </div>
    <div class="split-panel-figures">
      ${figures}
    </div>
  </div>`;
}

function renderFigureRow(block, context) {
  const className = block.className ? ` ${block.className}` : '';
  const style = {
    display: 'flex',
    gap: block.gap || '3mm',
    'justify-content': block.justify || 'center',
    'align-items': block.align || 'flex-start',
    margin: block.margin || '4px 0 6px',
    'font-size': block.font_size,
  };

  const items = (block.items || []).map((item) => {
    const labelBefore = item.label_before ? `<span>${renderTextTokens(item.label_before)}</span>` : '';
    const labelAfter = item.label_after ? `<span>${renderTextTokens(item.label_after)}</span>` : '';
    return `${labelBefore}${renderFigureImage(item.figure || item, context, {
      'max-height': item.max_height || block.max_height,
      'max-width': item.max_width || block.max_width,
      height: item.height,
      width: item.width,
      display: item.display || 'inline-block',
      'vertical-align': item.vertical_align || 'middle',
    })}${labelAfter}`;
  });

  const figures = (block.figures || []).map((figureRef) => {
    const figure = typeof figureRef === 'string' ? { figure: figureRef } : figureRef;
    return renderFigureImage(figure, context, {
      'max-height': figure.max_height || block.max_height,
      'max-width': figure.max_width || block.max_width,
    });
  });

  return `<div class="figure-row${className}"${styleAttr(style)}>
    ${[...figures, ...items].join('\n')}
  </div>`;
}

function renderStepFlow(block, context) {
  const startAt = Number(block.start_at || 1);
  const className = block.className ? ` ${block.className}` : '';
  const steps = (block.steps || []).map((step, index) => {
    const stepNo = startAt + index;
    const figures = step.figures && step.figures.length
      ? renderFigureRow({
          figures: step.figures,
          items: step.items,
          gap: step.gap || block.gap,
          justify: step.justify || block.justify,
          align: step.align || block.align,
          margin: step.margin || block.figure_margin,
          className: 'step-figures',
          max_height: step.max_height || block.max_height,
          max_width: step.max_width || block.max_width,
          font_size: step.font_size || block.font_size,
        }, context)
      : '';

    return `<div class="step-flow-step">
      <div class="step-flow-row">
        <span class="step-num">${stepNo}</span>
        <div class="step-text">${renderTextTokens(step.text)}</div>
      </div>
      ${figures}
    </div>`;
  }).join('\n');

  return `<div class="step-flow${className}">
    ${steps}
  </div>`;
}

function renderQaList(block) {
  return `<div class="qa-list">
    ${(block.items || []).map((item) => `<div class="qa-item">
      <div class="sub-title">${renderTextTokens(item.question)}</div>
      <ul class="bullet-list">
        ${renderBlockListItems(item.answers || [])}
      </ul>
    </div>`).join('\n')}
  </div>`;
}

function renderContactBlock(block) {
  const email = block.email ? `<b>${renderTextTokens(block.email)}</b>` : '';
  const text = renderTextTokens(block.text || '');
  const cutLine = block.cut_line ? `<div class="contact-cut-line">${renderTextTokens(block.cut_line)}</div>` : '';
  return `<div class="contact-block">
    <p>${text}${email}</p>
    ${cutLine}
  </div>`;
}

function renderWarrantyCard(block, context) {
  const fields = block.fields || [];
  return `<table class="warranty-card">
    <tbody>
      ${fields.map((field) => `<tr><td>${renderTextTokens(field)}</td><td></td></tr>`).join('\n')}
    </tbody>
  </table>`;
}

function renderBlock(block, context) {
  switch (block.type) {
    case 'paragraph':
      return `<p>${renderTextTokens(block.text)}</p>`;
    case 'bullet_list':
      return `<ul class="bullet-list">
        ${renderBlockListItems(block.items)}
      </ul>`;
    case 'warning_box':
    case 'caution_box':
    case 'notice_box': {
      const classNameMap = {
        warning_box: 'warning-box',
        caution_box: 'caution-box',
        notice_box: 'note-box',
      };
      const className = classNameMap[block.type];
      const icon = block.icon
        ? `<div style="margin:6px 0 8px;">${renderFigureImage(block.icon, context, { width: '22px', 'max-height': '22px' })}</div>`
        : '';
      const body = block.items
        ? `<ul class="box-list">
            ${renderBlockListItems(block.items)}
          </ul>`
        : renderTextTokens(block.text || '');
      const title = block.title
        ? `<div class="box-title">${renderTextTokens(block.title)}</div>`
        : '';
      return `<div class="${className}">
        ${title}
        ${icon}
        ${body}
      </div>`;
    }
    case 'sub_title':
      return `<div class="sub-title">${renderTextTokens(block.text)}</div>`;
    case 'figure':
      return renderFigure(block, context);
    case 'figure_row':
      return renderFigureRow(block, context);
    case 'step_flow':
      return renderStepFlow(block, context);
    case 'split_panel':
      return renderSplitPanel(block, context);
    case 'table_ref':
      return renderTableRef(block, context);
    case 'qa_list':
      return renderQaList(block, context);
    case 'contact_block':
      return renderContactBlock(block, context);
    case 'warranty_card':
      return renderWarrantyCard(block, context);
    default:
      throw new Error(`Unknown block type: ${block.type}`);
  }
}

function collectBlockFigureIds(block) {
  const ids = [];
  if (!block || typeof block !== 'object') {
    return ids;
  }

  if ((block.type === 'warning_box' || block.type === 'caution_box' || block.type === 'notice_box') && block.icon) {
    if (typeof block.icon === 'string') ids.push(block.icon);
    else if (block.icon && typeof block.icon.figure === 'string') ids.push(block.icon.figure);
  }
  if (block.type === 'figure' && typeof block.figure === 'string') {
    ids.push(block.figure);
  }
  if (block.type === 'figure_row') {
    for (const figure of block.figures || []) {
      if (typeof figure === 'string') ids.push(figure);
      else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
    }
    for (const item of block.items || []) {
      if (item && typeof item.figure === 'string') ids.push(item.figure);
    }
  }
  if (block.type === 'step_flow') {
    for (const step of block.steps || []) {
      for (const figure of step.figures || []) {
        if (typeof figure === 'string') ids.push(figure);
        else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
      }
      for (const item of step.items || []) {
        if (item && typeof item.figure === 'string') ids.push(item.figure);
      }
    }
  }
  if (block.type === 'split_panel') {
    for (const figure of block.figures || []) {
      if (typeof figure === 'string') ids.push(figure);
      else if (figure && typeof figure === 'object' && typeof figure.figure === 'string') ids.push(figure.figure);
    }
  }

  return ids;
}

function collectProceduralImageUsage(chapters, imagesManifest) {
  const seen = new Map();

  function visitBlock(block, chapterId, pageKey, blockIndex) {
    if (!block || typeof block !== 'object') return;

    if (block.type === 'step_flow') {
      (block.steps || []).forEach((step, stepIndex) => {
        const usageRef = `${chapterId}.${pageKey}.${step.id || `step${stepIndex + 1}`}`;
        for (const figureRef of step.figures || []) {
          const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
          const meta = imagesManifest[imageId];
          if (!meta) throw new Error(`Missing image id: ${imageId}`);
          if (meta.kind === 'procedural') {
            if (seen.has(imageId)) {
              throw new Error(`Procedural image reused across steps: ${imageId}`);
            }
            seen.set(imageId, usageRef);
          }
        }
      });
    }

    if (block.type === 'split_panel') {
      (block.figures || []).forEach((figureRef, figureIndex) => {
        const imageId = typeof figureRef === 'string' ? figureRef : figureRef.figure;
        const meta = imagesManifest[imageId];
        if (!meta) throw new Error(`Missing image id: ${imageId}`);
        if (meta.kind === 'procedural') {
          const usageRef = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}.figure${figureIndex + 1}`;
          if (seen.has(imageId)) {
            throw new Error(`Procedural image reused across blocks: ${imageId}`);
          }
          seen.set(imageId, usageRef);
        }
      });
      (block.body_blocks || []).forEach((childBlock, childIndex) => {
        visitBlock(childBlock, chapterId, pageKey, `${blockIndex}-split-${childIndex}`);
      });
    }

    if (block.type !== 'step_flow' && block.type !== 'split_panel') {
      for (const imageId of collectBlockFigureIds(block)) {
        const meta = imagesManifest[imageId];
        if (!meta) {
          throw new Error(`Missing image id: ${imageId}`);
        }
        if (meta.kind === 'procedural') {
          const usageRef = `${chapterId}.${pageKey}.${block.id || `block${blockIndex + 1}`}`;
          if (seen.has(imageId)) {
            throw new Error(`Procedural image reused across steps: ${imageId}`);
          }
          seen.set(imageId, usageRef);
        }
      }
    }
  }

  for (const chapter of chapters) {
    for (let pageIndex = 0; pageIndex < (chapter.pages || []).length; pageIndex += 1) {
      const page = chapter.pages[pageIndex];
      const pageKey = page.page_id || `page${pageIndex + 1}`;
      (page.blocks || []).forEach((block, blockIndex) => {
        visitBlock(block, chapter.chapter_id, pageKey, blockIndex);
      });
    }
  }

  return seen;
}

function validateProceduralImageUsage(chapters, imagesManifest) {
  const seen = collectProceduralImageUsage(chapters, imagesManifest);

  for (const [imageId, meta] of Object.entries(imagesManifest)) {
    if (meta.kind !== 'procedural') continue;
    if (!meta.usage_ref) {
      throw new Error(`Procedural image missing usage_ref: ${imageId}`);
    }
    const actualUsageRef = seen.get(imageId);
    if (!actualUsageRef) {
      throw new Error(`Procedural image not used in content: ${imageId}`);
    }
    if (meta.usage_ref !== actualUsageRef) {
      throw new Error(`Procedural image usage_ref mismatch: ${imageId} expected ${meta.usage_ref} actual ${actualUsageRef}`);
    }
  }
}

function docTypeLabel(suffix) {
  const labels = {
    cn: '使用说明书',
    en: 'User Manual',
    de: 'Bedienungsanleitung',
    it: "Manuale d'uso",
  };
  return labels[suffix] || labels.en;
}

function renderStructuredDocument(documentSchema, context) {
  const chapters = documentSchema.chapters.filter((chapter) => chapter.enabled !== false);
  validateProceduralImageUsage(chapters, context.images);

  let pageNo = 3;
  const tocEntries = [];
  const pages = [];

  for (const chapter of chapters) {
    tocEntries.push({
      chapter_no: chapter.chapter_no,
      toc_title: chapter.toc_title || chapter.title,
      page_no: pageNo,
    });

    for (const page of chapter.pages) {
      const pageClass = page.page_class ? ` ${page.page_class}` : '';
      const headerRef = page.header_ref || chapter.header_ref;
      const sectionTitle = page.hide_section_title
        ? ''
        : `<h2 class="section-title"><span class="chapter-num">${chapter.chapter_no}</span>${page.section_title || chapter.title}</h2>`;
      const blocks = (page.blocks || []).map((block) => renderBlock(block, context)).join('\n');

      pages.push(`<div class="page${pageClass}">
  <div class="header-strip">
    <div class="header-brand">{{brand.display_name}}</div>
    <div class="header-ref">${headerRef}</div>
  </div>
  ${sectionTitle}
  ${blocks}
  <div class="page-footer"><span>{{brand.display_name}} {{product.model}} ${docTypeLabel(context.suffix)}</span><span>${pageNo}</span></div>
</div>`);
      pageNo += 1;
    }
  }

  const tocHtml = tocEntries.map((entry) => `<div class="toc-item"><span><span class="toc-chapter">${entry.chapter_no}</span><span class="toc-name">${entry.toc_title}</span></span><span class="toc-page">${entry.page_no}</span></div>`).join('\n');

  return {
    tocHtml,
    documentHtml: pages.join('\n\n'),
  };
}

function renderDocument(documentSchema, context) {
  if (documentSchema.kind !== 'structured') {
    throw new Error(`Unsupported document schema kind: ${documentSchema.kind}`);
  }

  return renderStructuredDocument(documentSchema, context);
}

// ---------------------------------------------------------------------------
// Build a single variant
// ---------------------------------------------------------------------------
function buildVariant(regionCode, brandOverride) {
  const region = config.regions[regionCode];
  if (!region) {
    console.error(`Unknown region: ${regionCode}. Available: ${Object.keys(config.regions).join(', ')}`);
    process.exit(1);
  }

  const activeBrand  = brandOverride || config.product.active_brand;
  const activeMarket = region.market;
  const lang         = region.lang;
  const suffix       = langSuffix(lang);

  if (!config.brands[activeBrand]) {
    console.error(`Unknown brand: ${activeBrand}. Available: ${Object.keys(config.brands).join(', ')}`);
    process.exit(1);
  }
  if (!config.specs[activeMarket]) {
    console.error(`Unknown market: ${activeMarket}. Available: ${Object.keys(config.specs).join(', ')}`);
    process.exit(1);
  }

  const brand = config.brands[activeBrand];
  const specs = config.specs[activeMarket];
  const mfr   = config.manufacturer;
  const model = config.product.model;

  console.log(`Building: ${model} | region=${regionCode} | brand=${activeBrand} (${brand.display_name}) | market=${activeMarket} | lang=${lang}`);

  // Load template
  const templateLang = region.template_lang || langSuffix(region.lang);
  const templatePrefix = config.product.template_prefix || 'v23';
  const templatePath = path.resolve(__dirname, '..', 'template', `${templatePrefix}-master-${templateLang}.html`);
  if (!fs.existsSync(templatePath)) {
    console.error(`Template not found: ${templatePath}`);
    process.exit(1);
  }
  let html = resolveTemplateIncludes(templatePath, path.resolve(__dirname, '..', 'template'));

  // Update <html lang="...">
  html = html.replace(/<html lang="[^"]*">/, `<html lang="${lang}">`);

  // Simple variable replacements
  const vars = {
    'brand.display_name':      brand.display_name,
    'brand.name':              brand.name,
    'brand.address':           brand.address,
    'brand.website':           brand.website,
    'brand.support_email':     brand.support_email,
    'product.model':           model,
    'product.name_cn':         config.product.name_cn,
    'product.name_en':         config.product.name_en,
    'product.name_de':         config.product.name_de,
    'product.name_it':         config.product.name_it,
    'product.cover_image':     config.product.cover_image || '',
    'manufacturer.name_cn':    mfr.name_cn,
    'manufacturer.name_en':    mfr.name_en,
    'manufacturer.address_cn': mfr.address_cn,
    'manufacturer.address_en': mfr.address_en,
    'manufacturer.website':    mfr.website,
    'warranty.years':          String(config.warranty.years),
    'images_dir':              config.images_dir,
  };

  for (const [key, value] of Object.entries(vars)) {
    const pattern = new RegExp(`\\{\\{${key.replace(/\./g, '\\.')}\\}\\}`, 'g');
    html = html.replace(pattern, value);
  }

  // Block replacements — language-aware
  function buildSpecsRows(specsData) {
    return specsData.rows
      .map(r => {
        const label = pickField(r, 'label', suffix);
        const value = pickField(r, 'value', suffix) || r.value;
        return `      <tr><td>${label}</td><td>${value}</td></tr>`;
      })
      .join('\n');
  }

  function buildPartsRows(parts) {
    const rows = [];
    const half = Math.ceil(parts.length / 2);
    for (let i = 0; i < half; i++) {
      const left = parts[i];
      const right = parts[i + half];
      const leftName  = pickField(left, 'name', suffix);
      const rightId   = right ? right.id : '';
      const rightName = right ? pickField(right, 'name', suffix) : '';
      rows.push(`      <tr><td>${left.id}</td><td>${leftName}</td><td>${rightId}</td><td>${rightName}</td></tr>`);
    }
    return rows.join('\n');
  }

  function buildButtonsRows(buttons) {
    return buttons
      .map(b => {
        const keyEscaped = b.key.replace(/&/g, '&amp;');
        const bName = pickField(b, 'name', suffix);
        const bDesc = pickField(b, 'desc', suffix);
        return `      <tr><td><span class="callout-no">${b.id}</span> <span class="btn-name">${keyEscaped}</span>\u3000${bName}</td><td>${bDesc}</td></tr>`;
      })
      .join('\n');
  }

  const labels = config.ui_labels[suffix] || config.ui_labels.en;

  function buildBrandInfoRows(brandData) {
    return [
      `      <tr><td style="width:30%">${labels.brand_label}</td><td><b>${brandData.name}</b></td></tr>`,
      `      <tr><td>${labels.address_label}</td><td>${brandData.address}</td></tr>`,
      `      <tr><td>${labels.website_label}</td><td>${brandData.website}</td></tr>`,
      `      <tr><td>${labels.email_label}</td><td>${brandData.support_email}</td></tr>`,
    ].join('\n');
  }

  function buildManufacturerRows(mfrData) {
    return [
      `      <tr><td style="width:30%">${labels.manufacturer_label}</td><td><b>${mfrData.name_cn}</b><br><span style="font-weight:400;font-size:12px;color:#666">${mfrData.name_en}</span></td></tr>`,
      `      <tr><td>${labels.address_label}</td><td>${suffix === 'cn' ? mfrData.address_cn : mfrData.address_en}</td></tr>`,
      `      <tr><td>${labels.website_label}</td><td>${mfrData.website}</td></tr>`,
    ].join('\n');
  }

  const imagesManifest = loadImagesManifest(productDir);
  const documentSchema = loadContentDocument(productDir, templateLang);
  const renderedDocument = renderDocument(documentSchema, {
    config,
    brand,
    specs,
    mfr,
    model,
    suffix,
    labels,
    images: imagesManifest,
    builders: {
      buildSpecsRows,
      buildPartsRows,
      buildButtonsRows,
      buildBrandInfoRows,
      buildManufacturerRows,
    },
  });

  html = replaceTemplateSlots(html, {
    AUTO_TOC: renderedDocument.tocHtml,
    DOCUMENT_BODY: renderedDocument.documentHtml,
  });

  for (const [key, value] of Object.entries(vars)) {
    const pattern = new RegExp(`\{\{${key.replace(/\./g, '\\.')}\}\}`, 'g');
    html = html.replace(pattern, value);
  }

  const blocks = {
    'SPECS_TABLE_ROWS':        buildSpecsRows(specs),
    'PARTS_TABLE_ROWS':        buildPartsRows(config.parts),
    'BUTTONS_TABLE_ROWS':      buildButtonsRows(config.buttons),
    'BRAND_INFO_ROWS':         buildBrandInfoRows(brand),
    'MANUFACTURER_INFO_ROWS':  buildManufacturerRows(mfr),
  };

  for (const [key, value] of Object.entries(blocks)) {
    const pattern = new RegExp(`{{#${key}}}`, 'g');
    html = html.replace(pattern, value);
  }

  // Traditional Chinese conversion for HK/TW
  if (region.convert === 'traditional') {
    html = toTraditional(html);
  }

  // Validate — no remaining placeholders
  const remaining = html.match(/\{\{[^}]+\}\}/g);
  if (remaining) {
    console.warn(`  WARNING: ${remaining.length} unresolved placeholder(s):`);
    const unique = [...new Set(remaining)];
    unique.forEach(p => console.warn(`    ${p}`));
  }

  // Copy images to output
  fs.mkdirSync(outputDir, { recursive: true });
  const imgSrc = path.join(productDir, 'images');
  const imgDst = path.join(outputDir, config.images_dir);
  if (fs.existsSync(imgSrc)) {
    fs.mkdirSync(imgDst, { recursive: true });
    for (const f of fs.readdirSync(imgSrc)) {
      fs.copyFileSync(path.join(imgSrc, f), path.join(imgDst, f));
    }
    console.log(`  Copied ${fs.readdirSync(imgSrc).length} images → ${imgDst}`);
  }

  // Write output
  const outName = `${model.toLowerCase()}-${activeBrand}-${activeMarket}-${regionCode}.html`;
  const outPath = path.join(outputDir, outName);
  fs.writeFileSync(outPath, html, 'utf8');

  const sizeKB = (Buffer.byteLength(html, 'utf8') / 1024).toFixed(1);
  const status = remaining ? 'WARNING' : 'OK';
  console.log(`  Output: ${outName} (${sizeKB} KB) — ${status}`);

  return { outName, sizeKB, status, region: regionCode, brand: activeBrand, market: activeMarket };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  if (buildAll) {
    const allRegions = Object.keys(config.regions);
    const allBrands  = Object.keys(config.brands);
    const results = [];

    for (const r of allRegions) {
      for (const b of allBrands) {
        results.push(buildVariant(r, b));
      }
    }

    console.log('\n========== BUILD MATRIX SUMMARY ==========');
    console.log(`Total: ${results.length} variants`);
    const ok = results.filter(r => r.status === 'OK').length;
    const warn = results.filter(r => r.status === 'WARNING').length;
    console.log(`OK: ${ok} | WARNING: ${warn}`);
    console.log('');
    results.forEach(r => {
      console.log(`  [${r.status}] ${r.outName} (${r.sizeKB} KB)`);
    });

    if (warn > 0) process.exit(1);
  } else {
    const result = buildVariant(regionKey, brandKey);
    if (result.status !== 'OK') process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  buildVariant,
  langSuffix,
  pickField,
  loadProductConfig,
  loadImagesManifest,
  loadContentDocument,
  renderDocument,
  replaceTemplateSlots,
  renderTextTokens,
  resolveTemplateIncludes,
};
