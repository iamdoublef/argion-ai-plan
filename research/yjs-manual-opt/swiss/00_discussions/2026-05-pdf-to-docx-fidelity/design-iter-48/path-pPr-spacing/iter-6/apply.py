"""iter-6: target after=27 cohort (37 sites; aligned with line=230 cohort).
Try after=27 -> after=20 (slight tighten).
This is a different lever — paragraph after-spacing rather than line height.
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

pat = re.compile(r'(<w:spacing\b[^/]*?)w:after="27"([^/]*?/>)', re.S)
c = [0]
def repl(m):
    c[0] += 1
    return m.group(1) + 'w:after="20"' + m.group(2)
xml = pat.sub(repl, xml)
print(f"after=27 -> 20: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
