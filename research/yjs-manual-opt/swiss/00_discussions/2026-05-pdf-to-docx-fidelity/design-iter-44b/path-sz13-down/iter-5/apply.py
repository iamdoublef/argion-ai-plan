"""iter-5: sz=13 spacing 5->2 BLACK only (Arial+ArialBlack color=000000, 26 sites).

Test if isolating color cohort changes the curve. GRAY 117 is BIG, may be over-applied
when broad. BLACK only = 9 Arial + 17 Arial Black = 26 sites.
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

# only rPr blocks with sz=13 AND color=000000 AND spacing=5
pat = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="13"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c = [0]
def repl(m):
    b = m.group(0)
    has_black = '<w:color w:val="000000"' in b
    has_sp5 = '<w:spacing w:val="5"/>' in b
    if has_black and has_sp5:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 BLACK spacing 5->2 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
