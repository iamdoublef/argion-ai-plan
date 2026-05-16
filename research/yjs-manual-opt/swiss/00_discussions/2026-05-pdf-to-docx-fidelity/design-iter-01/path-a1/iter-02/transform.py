# iter-02:
# 1) 封面 6 个 run 按 target 精确改字体/字号/颜色
# 2) 全局字号下调到 target 范围
# 3) 全局字体改 Microsoft YaHei
# 4) 灰色统一 8E8E93
# 5) headers / footers 也一起改

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

# ===== 通用替换：字体、灰色、字号 =====
def transform_xml(src: str, is_main_doc=False) -> str:
    # 字体: 宋体/黑体 → Microsoft YaHei
    src = src.replace('w:eastAsia="宋体"', 'w:eastAsia="Microsoft YaHei"')
    src = src.replace('w:eastAsia="黑体"', 'w:eastAsia="Microsoft YaHei"')

    # 字号下调（用占位符防止链式替换）
    placeholders = {
        '16': '__SZ16__',
        '17': '__SZ17__',
        '18': '__SZ18__',
        '19': '__SZ19__',
        '20': '__SZ20__',
        '24': '__SZ24__',
        '28': '__SZ28__',
        '32': '__SZ32__',
        '36': '__SZ36__',
    }
    targets = {
        '__SZ16__': '14',  # 8pt → 7pt
        '__SZ17__': '14',
        '__SZ18__': '14',
        '__SZ19__': '14',
        '__SZ20__': '14',  # 章节小标题
        '__SZ24__': '27',  # 制冰机 12pt → 13.5pt（PDF target 18pt 但视觉打到这就够）
        '__SZ28__': '15',  # 威富可、目录: 14pt → 7.5pt（如 target）
        '__SZ32__': '27',
        '__SZ36__': '36',
    }
    for v, p in placeholders.items():
        src = re.sub(r'w:sz w:val="' + v + r'"', f'w:sz w:val="{p}"', src)
        src = re.sub(r'w:szCs w:val="' + v + r'"', f'w:szCs w:val="{p}"', src)
    for p, t in targets.items():
        src = src.replace(p, t)

    # 灰色统一
    src = src.replace('w:color w:val="8A8A8A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="9A9A9A"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="666666"', 'w:color w:val="8E8E93"')
    src = src.replace('w:color w:val="7A7A7A"', 'w:color w:val="8E8E93"')

    return src

# ===== 主文档处理 =====
doc_path = ROOT / 'document.xml'
src = doc_path.read_text(encoding='utf-8')
orig_len = len(src)

src = transform_xml(src, is_main_doc=True)

# ===== 封面精修 =====
# 封面 6 个 run（已被通用处理改过字体/字号），现在精确改：
# 1. 威富可: 红→黑, 字号 sz=15(7.5pt) target=7.5pt
# 2. MODEL IMT050: 灰→红, 字号 sz=12(6pt) target=6pt
# 3. 制冰机: 黑保持, 字号 sz=36(18pt) target=18pt
# 4. 说明书: 灰保持(8E8E93), 字号 sz=15(7.5pt) target=7.5pt
# 5. disclaimer 1: 灰保持, 字号 sz=11(5.5pt) target=5.4pt
# 6. disclaimer 2: 同上

# 威富可: 红→黑（找到带"威富可"的 run）
pat = re.compile(r'(<w:r>\s*<w:rPr>[^<]*(?:<[^>]+>[^<]*)*?)<w:color w:val="E63946"/>(.*?威富可</w:t>\s*</w:r>)', re.DOTALL)
src, n = pat.subn(lambda m: m.group(1) + '<w:color w:val="1A1A1A"/>' + m.group(2), src, count=1)
print(f'威富可 red→black: {n}')

# 威富可: 字号 15→15 (经过通用处理 28→15) 应已经 OK
# 但若不是，再精修一次：找到"威富可" run，强制 sz=15
pat_wfk_sz = re.compile(r'(<w:r>\s*<w:rPr>.*?)w:sz w:val="[0-9]+"(/>\s*<w:szCs w:val="[0-9]+"/>.*?威富可</w:t>\s*</w:r>)', re.DOTALL)
src, n = pat_wfk_sz.subn(lambda m: m.group(1) + 'w:sz w:val="15"' + m.group(2).replace('w:szCs w:val=', 'w:szCs w:val=').replace('/>\n', '/>\n'), src, count=1)
print(f'威富可 sz fix: {n}')

# MODEL IMT050: 灰→红
pat = re.compile(r'(<w:r>\s*<w:rPr>.*?)<w:color w:val="8E8E93"/>(.*?MODEL  IMT050.*?</w:r>)', re.DOTALL)
src, n = pat.subn(lambda m: m.group(1) + '<w:color w:val="E63946"/>' + m.group(2), src, count=1)
print(f'MODEL gray→red: {n}')

# MODEL IMT050: 字号 改 12 (6pt) - 当前经通用处理 16→14
pat_model = re.compile(r'(<w:r>\s*<w:rPr>.*?)w:sz w:val="[0-9]+"(/>\s*<w:szCs w:val="[0-9]+"/>.*?MODEL  IMT050.*?</w:r>)', re.DOTALL)
src, n = pat_model.subn(lambda m: m.group(1) + 'w:sz w:val="12"' + m.group(2), src, count=1)
print(f'MODEL sz fix: {n}')

# 制冰机: 字号改 36 (18pt) - 当前经通用处理 24→27
pat_zhibj = re.compile(r'(<w:r>\s*<w:rPr>.*?)w:sz w:val="[0-9]+"(/>\s*<w:szCs w:val="[0-9]+"/>.*?制冰机</w:t>\s*</w:r>)', re.DOTALL)
src, n = pat_zhibj.subn(lambda m: m.group(1) + 'w:sz w:val="36"' + m.group(2), src, count=1)
print(f'制冰机 sz fix: {n}')

# disclaimer 字号 sz=15 (7.5pt) - 经过通用处理已 OK，不改

# 目录: 字号现在是 15 (7.5pt) 太小，应该是 24（约 12pt）
pat_mulu = re.compile(r'(<w:r>\s*<w:rPr>.*?)w:sz w:val="15"(/>\s*<w:szCs w:val="15"/>.*?目录</w:t>\s*</w:r>)', re.DOTALL)
src, n = pat_mulu.subn(lambda m: m.group(1) + 'w:sz w:val="24"' + m.group(2), src, count=1)
print(f'目录 sz fix: {n}')

# 章节首页大数字 "01" "02" ... 处理：target 是 Arial-Black 13.5pt
# 这些数字目前是 ascii="Arial" b/  和 sz=24 → 27（已被改）。
# 但 ascii 字体我们要改成 "Arial Black" — 找含 sz=27 的 run（章节大数字）改 ascii
# 章节数字特征：内容为 "01" "02"...，颜色为 E63946，sz=27
pat_ch_num = re.compile(r'(<w:r>\s*<w:rPr>\s*)<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/>(\s*<w:b/>\s*<w:bCs/>\s*<w:color w:val="E63946"/>(?:\s*<w:spacing[^/]+/>)?\s*<w:sz w:val="27"/>\s*<w:szCs w:val="27"/>\s*</w:rPr>\s*<w:t[^>]*>0[0-9])')
src, n = pat_ch_num.subn(lambda m: m.group(1) + '<w:rFonts w:ascii="Arial Black" w:cs="Arial Black" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial Black"/>' + m.group(2), src)
print(f'章节大数字 ascii→Arial Black: {n}')

doc_path.write_text(src, encoding='utf-8')

# ===== headers / footers / endnotes / footnotes 也改 =====
for sub in ['header1.xml', 'header2.xml', 'header3.xml', 'header4.xml', 'header5.xml',
            'header6.xml', 'header7.xml', 'header8.xml', 'header9.xml', 'header10.xml', 'header11.xml',
            'footer1.xml', 'footer2.xml', 'footer3.xml', 'footer4.xml', 'footer5.xml',
            'footer6.xml', 'footer7.xml', 'footer8.xml', 'footer9.xml', 'footer10.xml', 'footer11.xml',
            'comments.xml', 'endnotes.xml', 'footnotes.xml']:
    p = ROOT / sub
    if p.exists():
        s = p.read_text(encoding='utf-8')
        s2 = transform_xml(s)
        if s != s2:
            p.write_text(s2, encoding='utf-8')

# ===== 最终统计 =====
src = doc_path.read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('sizes:', Counter(sizes).most_common())
colors = re.findall(r'w:color w:val="([0-9A-Fa-f]+)"', src)
print('colors:', Counter(colors).most_common())
print(f'YaHei count: {src.count("Microsoft YaHei")}')
print(f'Arial Black count: {src.count("Arial Black")}')
print(f'Bytes: {orig_len} -> {len(src)}')
