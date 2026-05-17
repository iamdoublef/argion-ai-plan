"""iter-6: sz=13 BLACK-only (Arial+ArialBlack) spacing 5 -> 2 (26 sites, leave GRAY alone).

Complement to iter-5 (GRAY-only). Tests whether BLACK cohort alone has any signal,
or whether p4 +0.04 came from BLACK and isolating it helps.
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
    # BLACK 000000 with spacing=5 (not the 24 sites at spacing=8)
    if '<w:color w:val="000000"' in b and '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 BLACK-only spacing 5->2 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
