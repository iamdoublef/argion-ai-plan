# iter-14: trHeight=280（小一些）
# 但只给数据表（非目录、非品牌信息表）加

import re
from pathlib import Path

ROOT = Path(__file__).parent / 'unpacked' / 'word'


def transform(src: str) -> str:
    def add_trheight(m):
        full = m.group(0)
        if '<w:trPr>' in full[:120]:
            return full
        return m.group(0).replace('<w:tr>', '<w:tr>\n        <w:trPr><w:trHeight w:val="280" w:hRule="atLeast"/></w:trPr>', 1)

    src = re.sub(r'<w:tr>\s*<w:tc>', add_trheight, src)
    return src


for sub in ROOT.iterdir():
    if sub.is_file() and sub.suffix == '.xml':
        s = sub.read_text(encoding='utf-8')
        s2 = transform(s)
        if s != s2:
            sub.write_text(s2, encoding='utf-8')

print('ok')
