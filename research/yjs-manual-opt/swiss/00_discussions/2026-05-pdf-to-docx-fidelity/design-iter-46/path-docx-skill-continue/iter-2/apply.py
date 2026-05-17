"""iter-2: sz=22 BLACK Arial Black spacing 5 -> 8 (13 sites). H1 heading cohort UP.

Hypothesis: large display headings may be over-tightened by LO. Try same UP move.
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

pat = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="22"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c = [0]
def repl(m):
    b = m.group(0)
    if '<w:color w:val="000000"' in b and '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=22 BLACK spacing 5->8 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
