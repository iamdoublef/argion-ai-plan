# iter-03: 修复 iter-02 的 bug，采用 run-级精确处理
# 方法: 把 document.xml 按 <w:r> ... </w:r> 切片，对每个 run 看其文本，按文本特征做精确编辑

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

# ===== 通用 transform: 字体、灰色 =====
# 字号在这里只做大概批量，最后封面/章节按精确表格指定
def transform_basic(src: str) -> str:
    # 字体: 宋体/黑体 → Microsoft YaHei
    src = src.replace('w:eastAsia="宋体"', 'w:eastAsia="Microsoft YaHei"')
    src = src.replace('w:eastAsia="黑体"', 'w:eastAsia="Microsoft YaHei"')
    # 灰色统一
    src = src.replace('w:color w:val="8A8A8A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="9A9A9A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="666666"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="7A7A7A"', 'w:color w:val="8E8E93"')
    return src

# ===== 按 run 精确处理 =====
# 找到每一个 <w:r>...</w:r>，根据 <w:t> 内容决定该 run 的字号/字体/颜色
def transform_runs(src: str) -> str:
    # pattern matches one <w:r>...</w:r>
    run_pattern = re.compile(r'<w:r>(\s*<w:rPr>.*?</w:rPr>)?\s*(<w:t[^>]*>([^<]*)</w:t>|<w:drawing>.*?</w:drawing>|<w:tab/>|<w:br/>)\s*</w:r>', re.DOTALL)

    def process_run(m):
        full = m.group(0)
        rpr = m.group(1) or ''
        inner = m.group(2)
        text = m.group(3)
        if text is None:
            return full  # 不是文字 run，跳过

        # ===== 文本特征匹配 =====
        # 1. "威富可" 封面（不是 footer 里那个）：第一个出现的、size 大于 etc 的需要 sz=15 (7.5pt)
        # 2. "MODEL  IMT050"：sz=12 (6pt), color 红
        # 3. "制冰机"（封面）：sz=36 (18pt)
        # 4. "说明书"（封面）：sz=15 (7.5pt)
        # 5. "目录"：sz=24 (12pt)
        # 6. 章节大数字 "01"-"10"（颜色红+加粗 sz=27）：改 ascii 为 Arial Black
        # 7. 章节小标签 "CH.01 — SAFETY"：sz=11 (5.5pt)

        if text == '威富可':
            # 这是封面那个（带 spacing 80, sz=28/15/36 都可能）
            # 改 sz=15 (7.5pt), color 黑
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="15"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="15"', rpr_new)
            rpr_new = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', '<w:color w:val="1A1A1A"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        if 'MODEL' in text and 'IMT050' in text:
            # MODEL IMT050: sz=12 (6pt), color 红
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="12"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="12"', rpr_new)
            rpr_new = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', '<w:color w:val="E63946"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        if text == '制冰机':
            # sz=36 (18pt), color 1A1A1A，加粗
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="36"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="36"', rpr_new)
            rpr_new = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', '<w:color w:val="1A1A1A"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        if text == '说明书':
            # 封面那个说明书: sz=15 (7.5pt), gray 8E8E93
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="15"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="15"', rpr_new)
            rpr_new = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', '<w:color w:val="8E8E93"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        if text == '目录':
            # sz=24 (12pt) - 目录大标题
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="24"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="24"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 章节大数字 01-10
        if re.match(r'^0[0-9]$|^10$', text.strip()):
            # 改 ascii 为 Arial Black, sz=27 (13.5pt)
            rpr_new = rpr
            rpr_new = re.sub(r'w:ascii="Arial"', 'w:ascii="Arial Black"', rpr_new)
            rpr_new = re.sub(r'w:cs="Arial"', 'w:cs="Arial Black"', rpr_new)
            rpr_new = re.sub(r'w:hAnsi="Arial"', 'w:hAnsi="Arial Black"', rpr_new)
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="27"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="27"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # disclaimer (使用产品前请...)
        if text.startswith('使用产品前请') or text.startswith('说明书中的产品'):
            # sz=11 (5.5pt), gray 8E8E93
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="11"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="11"', rpr_new)
            rpr_new = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"', '<w:color w:val="8E8E93"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # CH.XX — XXX 章节小标签
        if re.match(r'^CH\.\d+', text.strip()):
            # sz=11 (5.5pt), gray 8E8E93
            rpr_new = rpr
            rpr_new = re.sub(r'w:sz w:val="[0-9]+"', 'w:sz w:val="11"', rpr_new)
            rpr_new = re.sub(r'w:szCs w:val="[0-9]+"', 'w:szCs w:val="11"', rpr_new)
            return f'<w:r>{rpr_new}{inner}</w:r>'

        # 默认: 不动
        return full

    return run_pattern.sub(process_run, src)


# ===== 全局字号下调 =====
# DESIGN_BRIEF 目标：正文 7pt(sz=14), 章节小标题 7pt(sz=14), 章节大数字 13.5(sz=27)，制冰机 18pt(sz=36)
# 已经由 run-level 处理处理了封面。其余批量 sz 缩小。
def transform_sizes(src: str) -> str:
    # 先用 placeholder
    placeholders = {
        '16': '__SZ16__',
        '17': '__SZ17__',
        '18': '__SZ18__',
        '19': '__SZ19__',
        '20': '__SZ20__',
        # 24/27/28/36 都已经在 run-level 处理过封面/章节，这里保留
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


# ====== 处理主文档 ======
doc_path = ROOT / 'document.xml'
src = doc_path.read_text(encoding='utf-8')
orig_len = len(src)

src = transform_basic(src)
src = transform_runs(src)
src = transform_sizes(src)

doc_path.write_text(src, encoding='utf-8')

# ====== 处理 headers / footers ======
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
        s2 = transform_sizes(s2)
        if s != s2:
            p.write_text(s2, encoding='utf-8')

# ====== 统计 ======
src = doc_path.read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('document sizes:', Counter(sizes).most_common())
colors = re.findall(r'w:color w:val="([0-9A-Fa-f]+)"', src)
print('document colors:', Counter(colors).most_common())
print(f'YaHei count: {src.count("Microsoft YaHei")}')
print(f'Arial Black count: {src.count("Arial Black")}')
print(f'Bytes: {orig_len} -> {len(src)}')
