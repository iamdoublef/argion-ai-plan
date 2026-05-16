# iter-11: 在 iter-08 基础上，把整体字号微调
# - sz=13 → sz=13 保持 (6.5pt 对应 target 6.5-6.7pt)
# - 注意：iter-08 docx 中 sz=13 已经存在了，对应 winner 原始的 sz=13
# 这个 iter 改其他细节：把 page 14/15 续页"保修信息（续）" sz=24 也改 sz=27

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent / 'unpacked' / 'word'

def transform(src: str) -> str:
    # 找到"保修信息（续）"内 sz=24 改 sz=27
    src = re.sub(
        r'(<w:rPr>[^<]*(?:<[^>]+>[^<]*)*?)w:sz w:val="24"([^<]*</w:rPr>[^<]*<w:t[^>]*>保修信息（续）)',
        r'\1w:sz w:val="27"\2',
        src
    )
    src = re.sub(
        r'(<w:rPr>[^<]*(?:<[^>]+>[^<]*)*?)w:szCs w:val="24"([^<]*</w:rPr>[^<]*<w:t[^>]*>保修信息（续）)',
        r'\1w:szCs w:val="27"\2',
        src
    )
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
