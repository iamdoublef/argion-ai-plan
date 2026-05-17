"""iter-1: probe line=240 cohort (175 sites, body 12pt × 1.2).
Try line=240 -> line=232 (slight tighten, -3.3%). If wins, scan further.

This is the dominant cohort; even 1px gain × 175 sites could push the mean.
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

# Match pPr w:spacing with line="240"; rewrite line value only.
pat = re.compile(r'(<w:spacing\b[^/]*?)w:line="240"([^/]*?/>)', re.S)
c = [0]
def repl(m):
    c[0] += 1
    return m.group(1) + 'w:line="232"' + m.group(2)
xml = pat.sub(repl, xml)
print(f"line=240 -> 232: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
