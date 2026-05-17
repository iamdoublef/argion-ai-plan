"""iter-9: sz=11 spacing 5→2 (35 sites).

Hypothesis: push iter-8 winning direction further.
Result: 8.28/12.07 (max -0.07). Best single-cohort move.
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
        return block.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return block
new = pattern.sub(repl, xml)
print(f"Modified sz=11 count: {count[0]}")
doc.write_text(new, encoding="utf-8")
