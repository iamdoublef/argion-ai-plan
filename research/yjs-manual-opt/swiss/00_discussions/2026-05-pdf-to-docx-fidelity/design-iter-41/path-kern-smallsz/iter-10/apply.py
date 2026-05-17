"""iter-10: sz=11 spacing REMOVED entirely (35 sites, val=0 effective).

Hypothesis: maybe LO over-renders the spacing even at val=2; full removal cleanest.
Result: 8.30/12.07 mean REGRESSES (+0.02), p5 +0.20. Overshoots layout reflow.
val=2 is the sweet spot, not val=0.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "baseline_unpacked"
DST = ROOT / "unpacked"

shutil.copytree(SRC, DST, dirs_exist_ok=True)
doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

pattern = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="11"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
count = [0]
def repl(m):
    block = m.group(0)
    if '<w:spacing w:val="5"/>' in block:
        count[0] += 1
        return re.sub(r'\s*<w:spacing w:val="5"/>', '', block)
    return block
new = pattern.sub(repl, xml)
print(f"Modified sz=11 count: {count[0]}")
doc.write_text(new, encoding="utf-8")
