# iter-09: 基于 iter-08，把 w:color 1A1A1A → 000000（文本部分）
# 注意：不动表格/形状的 fill="1A1A1A"

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

def transform(src: str) -> str:
    # <w:color w:val="1A1A1A"/> → <w:color w:val="000000"/>
    src = re.sub(r'<w:color w:val="1A1A1A"/>', '<w:color w:val="000000"/>', src)
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

# 统计
src = (ROOT / 'document.xml').read_text(encoding='utf-8')
colors = re.findall(r'w:color w:val="([0-9A-Fa-f]+)"', src)
print('document colors:', Counter(colors).most_common())
fills = re.findall(r'w:fill="([0-9A-Fa-f]+)"', src)
print('document fills:', Counter(fills).most_common())
