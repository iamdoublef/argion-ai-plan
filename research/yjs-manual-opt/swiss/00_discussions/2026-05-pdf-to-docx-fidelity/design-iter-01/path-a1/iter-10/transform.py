# iter-10: 在 iter-08 基础上略调字号
# 尝试: sz=14 → sz=15（更接近 target 7.5pt 主字）
# 但保持 sz=13 (6.5pt) 不动（表格紧凑）

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

def transform(src: str) -> str:
    # 占位符
    src = re.sub(r'w:sz w:val="14"', 'w:sz w:val="__SZ14__"', src)
    src = re.sub(r'w:szCs w:val="14"', 'w:szCs w:val="__SZ14__"', src)
    src = src.replace('__SZ14__', '15')
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

# 统计
src = (ROOT / 'document.xml').read_text(encoding='utf-8')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
print('document sizes:', Counter(sizes).most_common())
