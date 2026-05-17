"""iter-2 (MAIN TRY): sz=13 spacing 5 -> 2 (DOWN, matching sz=11/sz=12 winning move).

Cohort (from iter-1 grep):
- 143 sites at spacing=5 (target): 117 Arial GRAY + 17 Arial Black BLACK + 9 Arial BLACK
- 24 sites at spacing=8 (Arial BLACK) — NOT touched (already wide, may be intentional)
- 10 Courier NEW RED with no spacing — NOT touched

Hypothesis: sz=11/sz=12 cohorts won via 5->2 (max -0.08 in W33). sz=13 (6.5pt) is middle
small-size and should follow the same DOWN sweet spot. iter-39 (UP direction) was ruled out.

Expected: max page diff drops (W34 p14=12.06 likely tightens), mean stays ~8.20.
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
