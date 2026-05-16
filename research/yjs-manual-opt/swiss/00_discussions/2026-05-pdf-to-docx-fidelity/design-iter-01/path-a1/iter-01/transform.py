# iter-01: P0 字体 + 字号 + 颜色（含封面威富可改黑）
# 输入：unpacked/word/document.xml
# 输出：原地修改

import re
import sys
from pathlib import Path

XML_PATH = Path(__file__).parent / 'unpacked' / 'word' / 'document.xml'

src = XML_PATH.read_text(encoding='utf-8')
orig = src

# ===== 1. 字体: 宋体/黑体 → Microsoft YaHei =====
# 中文正文用 YaHei (regular)，加粗用 YaHei + bold 标签
# 同时把 w:ascii 改为 Arial（保持），但加 w:hAnsi w:cs 一致
src = src.replace('w:eastAsia="宋体"', 'w:eastAsia="Microsoft YaHei"')
src = src.replace('w:eastAsia="黑体"', 'w:eastAsia="Microsoft YaHei"')

# ===== 2. 字号: 全面下调 =====
# 规则（基于 DESIGN_BRIEF）：
#   sz=16 (8pt)  -> 14 (7pt)    正文
#   sz=20 (10pt) -> 15 (7.5pt)  章节小标题
#   sz=24 (12pt) -> 27 (13.5pt) 章节大数字/制冰机
#   sz=28 (14pt) -> 24 (12pt)   "威富可"和"目录"（降一点）
#   sz=18 (9pt)  -> 14 (7pt)    其他
#   sz=17 (8.5pt) -> 14 (7pt)
#   sz=15 (7.5pt) 保持
#   sz=14 (7pt)  保持
#   sz=13 (6.5pt) 保持
# 用占位符避免反复替换冲突
PLACEHOLDERS = {
    '16': '__SZ16__',
    '20': '__SZ20__',
    '24': '__SZ24__',
    '28': '__SZ28__',
    '18': '__SZ18__',
    '17': '__SZ17__',
}
# 1. 先替换为占位
for v, p in PLACEHOLDERS.items():
    src = re.sub(r'w:sz w:val="' + v + r'"', f'w:sz w:val="{p}"', src)
    src = re.sub(r'w:szCs w:val="' + v + r'"', f'w:szCs w:val="{p}"', src)
# 2. 再把占位映射到目标值
TARGETS = {
    '__SZ16__': '14',
    '__SZ20__': '15',
    '__SZ24__': '27',
    '__SZ28__': '24',
    '__SZ18__': '14',
    '__SZ17__': '14',
}
for p, t in TARGETS.items():
    src = src.replace(p, t)

# ===== 3. 颜色: 灰色统一到 #8E8E93 =====
# 8A8A8A → 8E8E93
# 9A9A9A → 8E8E93
# 666666 → 8E8E93
src = src.replace('w:color w:val="8A8A8A"', 'w:color w:val="8E8E93"')
src = src.replace('w:color w:val="9A9A9A"', 'w:color w:val="8E8E93"')
src = src.replace('w:color w:val="666666"', 'w:color w:val="8E8E93"')

# ===== 4. 封面"威富可": E63946 红色 → 1A1A1A 黑色 =====
# 只改第一处，且必须是包含"威富可"的 run
# 找到 <w:t...威富可</w:t> 的位置，往前找最近的 <w:color w:val="E63946"/>
# 简单做法：替换 document.xml 中第一个 <w:r>...</w:r>，内含"威富可"
# 安全做法：匹配带"威富可"的整个 <w:r>...</w:r> 并替换其中的 color
pattern_wfk = re.compile(r'(<w:r>\s*<w:rPr>.*?)w:color w:val="E63946"(.*?威富可.*?</w:r>)', re.DOTALL)
def repl_wfk(m):
    return m.group(1) + 'w:color w:val="1A1A1A"' + m.group(2)
src_new, n = pattern_wfk.subn(repl_wfk, src, count=1)
if n == 0:
    print('WARN: 威富可 red→black 替换失败')
else:
    print(f'OK: 威富可 red→black 替换 {n} 处')
src = src_new

# ===== 写回 =====
XML_PATH.write_text(src, encoding='utf-8')

# 统计变化
import re
n_yahei = src.count('Microsoft YaHei')
print(f'YaHei count: {n_yahei}')
sizes = re.findall(r'w:sz w:val="([0-9]+)"', src)
from collections import Counter
print('after sizes:', Counter(sizes).most_common())
colors = re.findall(r'w:color w:val="([0-9A-Fa-f]+)"', src)
print('after colors:', Counter(colors).most_common())
print(f'Bytes: {len(orig)} -> {len(src)}')
