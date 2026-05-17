"""iter-2: sz=13 spacing 5 -> 2 (DOWN, matching sz=11/sz=12 winning move).

Target: 143 sites = 117 Arial GRAY + 17 Arial Black BLACK + 9 Arial BLACK
NOT touched: 24 sites at spacing=8 (Arial/BLACK), 10 Courier RED no-spacing.
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
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 spacing 5->2 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
