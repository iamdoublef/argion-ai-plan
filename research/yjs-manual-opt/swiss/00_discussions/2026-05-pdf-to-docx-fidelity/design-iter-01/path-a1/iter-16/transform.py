# iter-16: 表格内 sz=13/14 → sz=16（恢复 winner 表格紧凑的原 sz）
# 目标: 让 page 8/11 表格 layout 回归 winner，降低视觉差

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'


def transform_table_sizes(src: str) -> str:
    def process_tbl(m):
        block = m.group(0)
        block = re.sub(r'w:sz w:val="13"', 'w:sz w:val="16"', block)
        block = re.sub(r'w:szCs w:val="13"', 'w:szCs w:val="16"', block)
        block = re.sub(r'w:sz w:val="14"', 'w:sz w:val="16"', block)
        block = re.sub(r'w:szCs w:val="14"', 'w:szCs w:val="16"', block)
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
