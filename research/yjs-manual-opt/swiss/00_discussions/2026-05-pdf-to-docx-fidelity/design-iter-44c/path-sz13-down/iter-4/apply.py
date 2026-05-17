"""iter-4: sz=13 spacing 5 -> 1 (extreme DOWN, almost zero).

Test whether reducing further than iter-2 yields gains, or overshoots wrap (like sz=11 5->0 in iter-10).
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
    if '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="1"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 spacing 5->1 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
