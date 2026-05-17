"""iter-5: sz=13 by color — GRAY-only spacing 5 -> 2 (117 sites, leave BLACK alone).

Hypothesis: p4 +0.04 regression in iter-2 may come from Arial Black BLACK sites (17+9=26)
clipping. GRAY (1A1A1A) Arial body text is the bulk (117). Try only GRAY.
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

pat = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="13"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c = [0]
def repl(m):
    b = m.group(0)
    # Must be GRAY (1A1A1A) AND have spacing=5
    if '<w:color w:val="1A1A1A"' in b and '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 GRAY-only spacing 5->2 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
