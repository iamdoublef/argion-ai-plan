"""iter-5: target line=278 cohort (45 sites; heading-ish 11pt/13pt × ~1.3).
Try 278 -> 271 (mild tighten, -2.5%).
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

pat = re.compile(r'(<w:spacing\b[^/]*?)w:line="278"([^/]*?/>)', re.S)
c = [0]
def repl(m):
    c[0] += 1
    return m.group(1) + 'w:line="271"' + m.group(2)
xml = pat.sub(repl, xml)
print(f"line=278 -> 271: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
