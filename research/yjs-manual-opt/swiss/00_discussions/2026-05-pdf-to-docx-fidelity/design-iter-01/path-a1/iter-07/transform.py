# iter-07: 修正章节标题 in TOC vs 章节首页
# 关键: 章节标题在 rpr 含 sz=24 才改 sz=27（章节首页）；sz=17 的是目录，保持 sz=14

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

CHAPTER_TITLES = {'安全须知', '产品参数', '产品结构', '产品功能', '技术参数',
                  '操作使用', '故障排除', '清洁保养', '存储运输', '保修信息',
                  '保修信息（续）'}

WARNING_LABELS = {'警告', '注意', '提示', '危险', 'WARNING', 'CAUTION', 'NOTICE', 'DANGER'}


def transform_basic(src: str) -> str:
    src = src.replace('w:eastAsia="宋体"', 'w:eastAsia="Microsoft YaHei"')
    src = src.replace('w:eastAsia="黑体"', 'w:eastAsia="Microsoft YaHei"')
    src = src.replace('w:color w:val="8A8A8A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="9A9A9A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="666666"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="7A7A7A"', 'w:color w:val="8E8E93"')
    return src


def set_size(rpr: str, sz: str) -> str:
    rpr = re.sub(r'w:sz w:val="[0-9]+"', f'w:sz w:val="{sz}"', rpr)
    rpr = re.sub(r'w:szCs w:val="[0-9]+"', f'w:szCs w:val="{sz}"', rpr)
    return rpr


def set_color(rpr: str, color: str) -> str:
    if '<w:color' in rpr:
        return re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', f'<w:color w:val="{color}"', rpr)
    return rpr.replace('</w:rPr>', f'<w:color w:val="{color}"/></w:rPr>', 1)


def set_ascii_font(rpr: str, font: str) -> str:
    if 'w:ascii=' in rpr:
        rpr = re.sub(r'w:ascii="[^"]+"', f'w:ascii="{font}"', rpr)
    if 'w:cs=' in rpr:
        rpr = re.sub(r'w:cs="[^"]+"', f'w:cs="{font}"', rpr)
    if 'w:hAnsi=' in rpr:
        rpr = re.sub(r'w:hAnsi="[^"]+"', f'w:hAnsi="{font}"', rpr)
    return rpr


def transform_runs(src: str) -> str:
    run_pattern = re.compile(r'<w:r>(\s*<w:rPr>.*?</w:rPr>)?\s*(<w:t[^>]*>([^<]*)</w:t>|<w:drawing>.*?</w:drawing>|<w:tab/>|<w:br/>)\s*</w:r>', re.DOTALL)

    def process_run(m):
        full = m.group(0)
        rpr = m.group(1) or ''
        inner = m.group(2)
        text = m.group(3)
        if text is None:
            return full

        t = text.strip()

        # 封面 威富可
        if t == '威富可' and 'w:spacing w:val="80"' in rpr:
            rpr_new = set_size(rpr, '15')
            rpr_new = set_color(rpr_new, '1A1A1A')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # MODEL IMT050
        if 'MODEL' in t and 'IMT050' in t:
            rpr_new = set_size(rpr, '12')
            rpr_new = set_color(rpr_new, 'E63946')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 制冰机 cover
        if t == '制冰机' and ('w:sz w:val="24"' in rpr or 'w:sz w:val="28"' in rpr):
            rpr_new = set_size(rpr, '36')
            rpr_new = set_color(rpr_new, '1A1A1A')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 说明书 cover
        if t == '说明书' and '<w:b/>' not in rpr:
            rpr_new = set_size(rpr, '15')
            rpr_new = set_color(rpr_new, '8E8E93')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 目录
        if t == '目录':
            rpr_new = set_size(rpr, '24')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 章节数字 01-10 根据 sz 区分
        if re.match(r'^(0[0-9]|10)\s*$', text):
            if 'w:sz w:val="24"' in rpr:
                # 章节首页 → sz=27 + Arial Black
                rpr_new = set_ascii_font(rpr, 'Arial Black')
                rpr_new = set_size(rpr_new, '27')
                return f'<w:r>{rpr_new}{inner}</w:r>'
            elif 'w:sz w:val="16"' in rpr or 'w:sz w:val="17"' in rpr:
                # 目录 → sz=14 (7pt)
                rpr_new = set_size(rpr, '14')
                return f'<w:r>{rpr_new}{inner}</w:r>'

        # 章节标题: 仅在 sz=24（章节首页）情况下改 sz=27
        if t in CHAPTER_TITLES:
            if 'w:sz w:val="24"' in rpr:
                rpr_new = set_size(rpr, '27')
                rpr_new = set_color(rpr_new, '1A1A1A')
                return f'<w:r>{rpr_new}{inner}</w:r>'
            elif 'w:sz w:val="20"' in rpr:
                # 保修信息（续）的 sz=20 处理 - 也是首页章节标题
                rpr_new = set_size(rpr, '27')
                rpr_new = set_color(rpr_new, '1A1A1A')
                return f'<w:r>{rpr_new}{inner}</w:r>'
            # 其他 sz（如 sz=17）保持 sz=14（目录里的）

        # CH.XX 标签
        if re.match(r'^CH\.\d+', t):
            rpr_new = set_size(rpr, '11')
            rpr_new = set_color(rpr_new, '8E8E93')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # WARNING/CAUTION 等
        if t in WARNING_LABELS:
            rpr_new = set_size(rpr, '13')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # disclaimer
        if t.startswith('使用产品前请') or t.startswith('说明书中的产品'):
            rpr_new = set_size(rpr, '11')
            rpr_new = set_color(rpr_new, '8E8E93')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        return full

    return run_pattern.sub(process_run, src)


def transform_sizes_global(src: str) -> str:
    placeholders = {
        '16': '__SZ16__',
        '17': '__SZ17__',
        '18': '__SZ18__',
        '19': '__SZ19__',
        '20': '__SZ20__',
    }
    targets = {
        '__SZ16__': '14',
        '__SZ17__': '14',
        '__SZ18__': '14',
        '__SZ19__': '14',
        '__SZ20__': '15',
    }
    for v, p in placeholders.items():
        src = re.sub(r'w:sz w:val="' + v + r'"', f'w:sz w:val="{p}"', src)
        src = re.sub(r'w:szCs w:val="' + v + r'"', f'w:szCs w:val="{p}"', src)
    for p, t in targets.items():
        src = src.replace(p, t)
    return src


def add_cover_red_dash(src: str) -> str:
    # 关键：威富可段落已被 transform_runs 改过，匹配新的格式
    old = '''      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="1A1A1A"/>
          <w:spacing w:val="80"/>
          <w:sz w:val="15"/>
          <w:szCs w:val="15"/>
        </w:rPr>
        <w:t xml:space="preserve">威富可</w:t>
      </w:r>'''
    new = '''      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="E63946"/>
          <w:sz w:val="15"/>
          <w:szCs w:val="15"/>
        </w:rPr>
        <w:t xml:space="preserve">──── </w:t>
      </w:r>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="1A1A1A"/>
          <w:spacing w:val="80"/>
          <w:sz w:val="15"/>
          <w:szCs w:val="15"/>
        </w:rPr>
        <w:t xml:space="preserve">威富可</w:t>
      </w:r>'''
    if old in src:
        src = src.replace(old, new, 1)
        print('封面短红线已加')
    else:
        print('WARN: 未找到封面段落')
    return src


# 主文档
doc_path = ROOT / 'document.xml'
src = doc_path.read_text(encoding='utf-8')
orig_len = len(src)

src = transform_basic(src)
src = transform_runs(src)
src = transform_sizes_global(src)
src = add_cover_red_dash(src)

doc_path.write_text(src, encoding='utf-8')

# headers / footers
for sub in ['header1.xml', 'header2.xml', 'header3.xml', 'header4.xml', 'header5.xml',
            'header6.xml', 'header7.xml', 'header8.xml', 'header9.xml', 'header10.xml', 'header11.xml',
            'footer1.xml', 'footer2.xml', 'footer3.xml', 'footer4.xml', 'footer5.xml',
            'footer6.xml', 'footer7.xml', 'footer8.xml', 'footer9.xml', 'footer10.xml', 'footer11.xml',
            'comments.xml', 'endnotes.xml', 'footnotes.xml']:
    p = ROOT / sub
    if p.exists():
        s = p.read_text(encoding='utf-8')
        s2 = transform_basic(s)
        s2 = transform_runs(s2)
        s2 = transform_sizes_global(s2)
        if s != s2:
            p.write_text(s2, encoding='utf-8')

# 统计
src = doc_path.read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('document sizes:', Counter(sizes).most_common())
print(f'Arial Black: {src.count("Arial Black")}')

# 检查各种章节标题
for t in ['安全须知', '产品结构', '技术参数']:
    for m in re.finditer(t, src):
        pos = m.start()
        rpr_start = src.rfind('<w:rPr>', 0, pos)
        rpr_end = src.find('</w:rPr>', rpr_start)
        rpr = src[rpr_start:rpr_end]
        sz = re.search(r'w:sz w:val="([0-9]+)"', rpr)
        print(f'  {t} sz={sz.group(1) if sz else "?"}')

print(f'Bytes: {orig_len} -> {len(src)}')
