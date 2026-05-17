"""iter-16: STACK iter-9 (p13+p9 line tune) ON iter-41 W33 (sz=11/12 spacing).

Base: W33 from iter-41 (8.28/12.06)
Apply: p13 271 -> 278 + p9 271 -> 264 (iter-9 winning move)
Goal: combined 8.21 mean + 12.06 max
"""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

# Reconfirm boundaries (iter-41 should not have changed paragraph counts;
# but verify sectPr lines first)
import re
sectPrs = [i for i, ln in enumerate(lines) if "<w:sectPr>" in ln]
print(f"sectPr line indices (0-based): {sectPrs}")
# Expect p13 region same as baseline: 8382..8867

P13_START, P13_END = 8382, 8867
P9_START, P9_END = 5301, 5787

n13 = 0
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
        n13 += 1
print(f"p13: 271 -> 278 x{n13}")

n9 = 0
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="264"')
        n9 += 1
print(f"p9: 271 -> 264 x{n9}")

DOC.write_text("\n".join(lines), encoding="utf-8")
