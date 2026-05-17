"""iter-7: Stacked / extended winner — sz=13 spacing 5->2 (143) AND also flip the 24 existing
spacing=8 Arial BLACK sz=13 sites DOWN to 5 (since DOWN direction is winning for sz=13).

If iter-2 won with 143 sites, see if more aggressive coverage helps without overshooting.
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
c_52 = [0]
c_85 = [0]
def repl(m):
    b = m.group(0)
    if '<w:spacing w:val="5"/>' in b:
        c_52[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    if '<w:spacing w:val="8"/>' in b:
        c_85[0] += 1
        return b.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="5"/>')
    return b
xml = pat.sub(repl, xml)
print(f"sz=13 spacing 5->2: {c_52[0]}, sz=13 spacing 8->5: {c_85[0]}")
doc.write_text(xml, encoding="utf-8")
