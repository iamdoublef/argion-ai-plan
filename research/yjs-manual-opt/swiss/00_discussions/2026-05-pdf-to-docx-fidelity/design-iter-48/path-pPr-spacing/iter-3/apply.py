"""iter-3: line=240 -> 242 (very small LOOSEN, +0.8%).
Test sensitivity floor. iter-2 +8 regressed (-0.31); try +2 to see if there's a sweet spot.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "baseline_unpacked"
DST = ROOT / "unpacked"

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

pat = re.compile(r'(<w:spacing\b[^/]*?)w:line="240"([^/]*?/>)', re.S)
c = [0]
def repl(m):
    c[0] += 1
    return m.group(1) + 'w:line="242"' + m.group(2)
xml = pat.sub(repl, xml)
print(f"line=240 -> 242: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
