"""iter-11: stack iter-9 + try p14 line LOOSEN 278 -> 285."""
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

# p14 loosen 278 -> 285
P14_START, P14_END = 8867, 9834
n14 = 0
for i in range(P14_START, P14_END):
    if 'w:line="278"' in lines[i]:
        lines[i] = lines[i].replace('w:line="278"', 'w:line="285"')
        n14 += 1
print(f"p14: w:line='278' -> '285' x{n14}")

DOC.write_text("\n".join(lines), encoding="utf-8")
