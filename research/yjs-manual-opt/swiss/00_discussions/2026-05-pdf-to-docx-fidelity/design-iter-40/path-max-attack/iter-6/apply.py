"""iter-6: p13 line spacing loosen 271 -> 278 (+7)."""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")
P13_START, P13_END = 8382, 8867
count = 0
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
        count += 1
print(f"Edited {count} lines with w:line='271' -> '278' in p13")
DOC.write_text("\n".join(lines), encoding="utf-8")
