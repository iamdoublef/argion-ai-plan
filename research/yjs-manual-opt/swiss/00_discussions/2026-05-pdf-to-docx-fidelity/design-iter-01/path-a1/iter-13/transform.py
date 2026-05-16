# iter-13: 在 iter-08 基础上，为所有表行加 trHeight 拉宽
# 目标: 让 page 11 故障排除表行高变宽，匹配 target

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'


def transform(src: str) -> str:
    # 在每个 <w:tr> 后面加 <w:trPr><w:trHeight w:hRule="atLeast" w:val="380"/></w:trPr>
    # 但只在 <w:tr> 后没有 <w:trPr> 时添加（避免重复）

    # pattern: <w:tr>\s*<w:tc>  → <w:tr>\n  <w:trPr><w:trHeight ...></w:trPr>\n  <w:tc>
    # 注意: 不能动有现有 trPr 的（如表头）
    def add_trheight(m):
        full = m.group(0)
        if '<w:trPr>' in full[:100]:  # 已有 trPr
            return full
        # 加 trPr
        return m.group(0).replace('<w:tr>', '<w:tr>\n        <w:trPr><w:trHeight w:val="380" w:hRule="atLeast"/></w:trPr>', 1)

    # 匹配 <w:tr>\n      <w:tc>
    src = re.sub(r'<w:tr>\s*<w:tc>', add_trheight, src)
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

src = (ROOT / 'document.xml').read_text(encoding='utf-8')
n_tr = src.count('<w:tr>')
n_trh = src.count('w:trHeight')
print(f'<w:tr> count: {n_tr}')
print(f'w:trHeight count: {n_trh}')
