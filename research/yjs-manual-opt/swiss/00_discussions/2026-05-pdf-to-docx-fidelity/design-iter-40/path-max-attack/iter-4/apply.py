"""iter-4: p3 line spacing micro-tune +10 twips.

230 -> 240 in p3 only (24 sites).
"""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"

text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")
P3_START, P3_END = 594, 1404
count = 0
for i in range(P3_START, P3_END):
    if 'w:line="230"' in lines[i]:
        lines[i] = lines[i].replace('w:line="230"', 'w:line="240"')
        count += 1
print(f"Edited {count} lines with w:line='230' -> '240' in p3")
DOC.write_text("\n".join(lines), encoding="utf-8")
