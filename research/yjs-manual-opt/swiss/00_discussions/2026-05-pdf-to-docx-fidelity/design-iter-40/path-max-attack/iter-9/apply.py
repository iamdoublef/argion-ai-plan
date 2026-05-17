"""iter-9: stack iter-6 (p13 278) + try p9 tighten 271 -> 264 (-7).

Also try p11 and p14 in opposite directions to explore optimum direction.
"""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

# iter-6 baseline (p13)
P13_START, P13_END = 8382, 8867
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')

# p9 tighten 271 -> 264
P9_START, P9_END = 5301, 5787
n = 0
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="264"')
        n += 1
print(f"p9 tighten x{n}")
DOC.write_text("\n".join(lines), encoding="utf-8")
