# iter-15: 表格内 sz=14 → sz=15（拉宽行高一点）
# 不动表格外正文（保持 sz=14）

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'


def transform_table_sizes(src: str) -> str:
    """在 <w:tbl>...</w:tbl> 内的 w:sz=14 改成 w:sz=15"""
    # 把 <w:tbl>...</w:tbl> 块找出来，逐块替换
    def process_tbl(m):
        block = m.group(0)
        block = re.sub(r'w:sz w:val="14"', 'w:sz w:val="15"', block)
        block = re.sub(r'w:szCs w:val="14"', 'w:szCs w:val="15"', block)
        return block

    src = re.sub(r'<w:tbl>.*?</w:tbl>', process_tbl, src, flags=re.DOTALL)
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform_table_sizes(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

src = (ROOT / 'document.xml').read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('sizes after:', Counter(sizes).most_common())
