"""iter-8: sz=11 spacing 5→3 (REDUCE, 35 sites).

Hypothesis (pivot): sz=11 cohort over-spaced by LO. Reduce instead of increase.
Result: 8.28/12.11 (max -0.03). First positive signal — reverse direction works!
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
        return block.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="3"/>')
    return block
new = pattern.sub(repl, xml)
print(f"Modified sz=11 count: {count[0]}")
doc.write_text(new, encoding="utf-8")
