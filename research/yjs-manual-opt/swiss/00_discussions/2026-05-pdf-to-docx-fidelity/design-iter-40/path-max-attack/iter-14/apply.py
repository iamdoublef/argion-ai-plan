"""iter-14: stack iter-9 + p10 loosen 264 -> 271."""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

P13_START, P13_END = 8382, 8867
P9_START, P9_END = 5301, 5787
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="264"')

# p10 loosen 264 -> 271
P10_START, P10_END = 5787, 6534
n = 0
for i in range(P10_START, P10_END):
    if 'w:line="264"' in lines[i]:
        lines[i] = lines[i].replace('w:line="264"', 'w:line="271"')
        n += 1
print(f"p10: 264 -> 271 x{n}")

DOC.write_text("\n".join(lines), encoding="utf-8")
