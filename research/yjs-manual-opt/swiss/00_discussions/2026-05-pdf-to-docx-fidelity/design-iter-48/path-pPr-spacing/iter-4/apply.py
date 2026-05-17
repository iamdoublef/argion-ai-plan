"""iter-4: target the line=230 cohort (37 sites; appears in BLACK 13 area).
Maybe 230 wants slight loosen to 234.
Or to test, line=230 -> 240 (align with body cohort, +10).
Go conservative first: line=230 -> 232 (+2).
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

pat = re.compile(r'(<w:spacing\b[^/]*?)w:line="230"([^/]*?/>)', re.S)
c = [0]
def repl(m):
    c[0] += 1
    return m.group(1) + 'w:line="232"' + m.group(2)
xml = pat.sub(repl, xml)
print(f"line=230 -> 232: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
