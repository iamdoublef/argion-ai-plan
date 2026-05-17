"""iter-7: sz=14 NON-BLACK spacing 8→9 (17 sites: WHITE banner 12 + GRAY 4 + RED 1).

Hypothesis: complete W32 sz=14 BLACK move by extending to remaining sz=14 colors at slightly
higher delta (8→9 instead of 8 ceiling).
Result: 8.28/12.14 (flat). Non-BLACK runs too small/sparse to move score.
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

pattern = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="14"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
count = [0]
def repl(m):
    block = m.group(0)
    if '<w:color w:val="000000"/>' in block:
        return block  # exclude BLACK (already W32-tuned)
    if '<w:spacing w:val="8"/>' in block:
        count[0] += 1
        return block.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="9"/>')
    return block
new = pattern.sub(repl, xml)
print(f"Modified non-BLACK sz=14 count: {count[0]}")
doc.write_text(new, encoding="utf-8")
