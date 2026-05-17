"""iter-1: sz=15 BLACK spacing 5 -> 8 (27 sites). Direct sz=14 W32 analog UP.

Hypothesis: sz=14 BLACK won at 5->8 (W32). sz=15 BLACK Arial Black (27 sites)
is the closest heading cohort. UP direction (per LO over-tightening on display fonts).
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

pat = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="15"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c = [0]
def repl(m):
    b = m.group(0)
    if '<w:color w:val="000000"' in b and '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=15 BLACK spacing 5->8 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
