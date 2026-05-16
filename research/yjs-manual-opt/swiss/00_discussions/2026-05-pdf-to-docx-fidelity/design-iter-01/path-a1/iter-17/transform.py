# iter-17: 选择性扩张 - 仅给大表格（多于 5 行）的表加 trHeight=320
# 目标: 让 page 8 / 11 表格行高拉宽，但不动小表

import re
from pathlib import Path

ROOT = Path(__file__).parent / 'unpacked' / 'word'


def transform(src: str) -> str:
    def process_tbl(m):
        block = m.group(0)
        n_tr = block.count('<w:tr>')
        if n_tr < 5:
            return block
        # 大表格，给每行加 trHeight=320 (default ~280)
        def add_trheight(mm):
            full = mm.group(0)
            if '<w:trPr>' in full[:120]:
                return full
            return mm.group(0).replace('<w:tr>', '<w:tr>\n        <w:trPr><w:trHeight w:val="320" w:hRule="atLeast"/></w:trPr>', 1)
        block = re.sub(r'<w:tr>\s*<w:tc>', add_trheight, block)
        return block

    src = re.sub(r'<w:tbl>.*?</w:tbl>', process_tbl, src, flags=re.DOTALL)
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

src = (ROOT / 'document.xml').read_text(encoding='utf-8')
n_trh = src.count('w:trHeight')
print(f'trHeight count: {n_trh}')
