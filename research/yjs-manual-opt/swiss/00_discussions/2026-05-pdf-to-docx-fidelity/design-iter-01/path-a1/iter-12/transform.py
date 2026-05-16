# iter-12: 折中方案 - 只做字体修复 + 颜色统一 + 封面修复，**保持字号不变**
# 目标：保留原 winner 的 layout（最接近 target 像素），但应用所有非破坏性的设计修复

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

CHAPTER_TITLES = {'安全须知', '产品参数', '产品结构', '产品功能', '技术参数',
                  '操作使用', '故障排除', '清洁保养', '存储运输', '保修信息',
                  '保修信息（续）'}


def transform_basic(src: str) -> str:
    # 字体修复
    src = src.replace('w:eastAsia="宋体"', 'w:eastAsia="Microsoft YaHei"')
    src = src.replace('w:eastAsia="黑体"', 'w:eastAsia="Microsoft YaHei"')
    # 灰色统一
    src = src.replace('w:color w:val="8A8A8A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="9A9A9A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="666666"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="7A7A7A"', 'w:color w:val="8E8E93"')
    return src


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
    """只改封面颜色 + 章节大数字字体（Arial Black）"""
    run_pattern = re.compile(r'<w:r>(\s*<w:rPr>.*?</w:rPr>)?\s*(<w:t[^>]*>([^<]*)</w:t>|<w:drawing>.*?</w:drawing>|<w:tab/>|<w:br/>)\s*</w:r>', re.DOTALL)

    def process_run(m):
        full = m.group(0)
        rpr = m.group(1) or ''
        inner = m.group(2)
        text = m.group(3)
        if text is None:
            return full

        t = text.strip()

        # 封面 威富可: 红→黑
        if t == '威富可' and 'w:spacing w:val="80"' in rpr:
            rpr_new = set_color(rpr, '1A1A1A')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # MODEL IMT050: 灰→红
        if 'MODEL' in t and 'IMT050' in t:
            rpr_new = set_color(rpr, 'E63946')
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 章节大数字 01-10 sz=24: 改 Arial Black
        if re.match(r'^(0[0-9]|10)\s*$', text):
            if 'w:sz w:val="24"' in rpr:
                rpr_new = set_ascii_font(rpr, 'Arial Black')
                return f'<w:r>{rpr_new}{inner}</w:r>'

        return full

    return run_pattern.sub(process_run, src)


# 主文档
doc_path = ROOT / 'document.xml'
src = doc_path.read_text(encoding='utf-8')
orig_len = len(src)

src = transform_basic(src)
src = transform_runs(src)

doc_path.write_text(src, encoding='utf-8')

# 添加封面短红线
src = doc_path.read_text(encoding='utf-8')
old = '''      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="1A1A1A"/>
          <w:spacing w:val="80"/>
          <w:sz w:val="28"/>
          <w:szCs w:val="28"/>
        </w:rPr><w:t xml:space="preserve">威富可</w:t></w:r>'''
new = '''      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="E63946"/>
          <w:sz w:val="22"/>
          <w:szCs w:val="22"/>
        </w:rPr><w:t xml:space="preserve">──── </w:t></w:r>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="1A1A1A"/>
          <w:spacing w:val="80"/>
          <w:sz w:val="28"/>
          <w:szCs w:val="28"/>
        </w:rPr><w:t xml:space="preserve">威富可</w:t></w:r>'''
if old in src:
    src = src.replace(old, new, 1)
    print('封面短红线 OK')
else:
    print('WARN: 未找到封面')
doc_path.write_text(src, encoding='utf-8')

# headers / footers / etc
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
        if s != s2:
            p.write_text(s2, encoding='utf-8')

# 统计
src = doc_path.read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('document sizes:', Counter(sizes).most_common())
colors = re.findall(r'w:color w:val="([0-9A-Fa-f]+)"', src)
print('document colors:', Counter(colors).most_common())
print(f'YaHei: {src.count("Microsoft YaHei")}')
print(f'Arial Black: {src.count("Arial Black")}')
print(f'Bytes: {orig_len} -> {len(src)}')
