"""iter-3: p3 line spacing micro-tune.

p3 has 24 paragraphs with w:line="230" (WARNING bullets). Try -5 -> 225.
Localize by editing only between the p2-ending sectPr (line ~594) and the
p3-ending sectPr (line ~1404).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"

text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

# p3 region: lines 595..1404 (0-indexed: 594..1403)
P3_START = 594  # 0-indexed line 594 = file line 595
P3_END = 1404   # 0-indexed line 1403 = file line 1404 (exclusive)
# verify those bounds:
print(f"p3 start ({P3_START+1}): {lines[P3_START][:80]}")
print(f"p3 end ({P3_END}): {lines[P3_END-1][:80]}")

count = 0
for i in range(P3_START, P3_END):
    if 'w:line="230"' in lines[i]:
        lines[i] = lines[i].replace('w:line="230"', 'w:line="225"')
        count += 1
print(f"Edited {count} lines with w:line='230' -> '225' in p3")
new_text = "\n".join(lines)
DOC.write_text(new_text, encoding="utf-8")
