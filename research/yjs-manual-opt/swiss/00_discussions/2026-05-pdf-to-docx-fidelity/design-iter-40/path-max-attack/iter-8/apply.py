"""iter-8: combine p13 271 -> 278 (iter-6 best) WITH p9 line tighten attempt.

iter-6 already wins on p13 (10.65). Try to find similar lever on p9 (which is 11.81).
p9 = lines 5302..5787. Let's first profile its w:line distribution.
"""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

# Apply iter-6 baseline (p13 271 -> 278)
P13_START, P13_END = 8382, 8867
n6 = 0
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
        n6 += 1
print(f"p13: w:line='271' -> '278' x{n6}")

# Now try p9: lines 5302..5787
P9_START, P9_END = 5301, 5787
n9 = 0
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
        n9 += 1
print(f"p9: w:line='271' -> '278' x{n9}")

DOC.write_text("\n".join(lines), encoding="utf-8")
