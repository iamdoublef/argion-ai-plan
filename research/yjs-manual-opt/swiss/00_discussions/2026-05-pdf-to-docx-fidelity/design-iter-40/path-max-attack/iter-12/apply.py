"""iter-12: stack iter-9 + try p5 loosen 271 -> 278."""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

# iter-9 stack
P13_START, P13_END = 8382, 8867
P9_START, P9_END = 5301, 5787
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="264"')

# iter-12: p5 loosen
P5_START, P5_END = 1822, 2295
n5 = 0
for i in range(P5_START, P5_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
        n5 += 1
print(f"p5: w:line='271' -> '278' x{n5}")

DOC.write_text("\n".join(lines), encoding="utf-8")
