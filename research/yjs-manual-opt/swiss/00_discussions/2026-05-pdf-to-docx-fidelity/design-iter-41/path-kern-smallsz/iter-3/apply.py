"""iter-3: add w:kern w:val="14" to all sz=14 rPr (88 sites).

Hypothesis: threshold-14 exactly matches sz=14 (7pt), forcing kerning on at the
threshold itself.
Result: 8.28/12.13 (max -0.01) — kern almost completely inert in LO.
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

pattern = re.compile(
    r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="14"/>(?:(?!</w:rPr>).)*?)(</w:rPr>)',
    re.S,
)
count = [0]
def repl(m):
    block = m.group(1)
    if '<w:kern' in block:
        return m.group(0)
    count[0] += 1
    return block + '<w:kern w:val="14"/>' + m.group(2)

new = pattern.sub(repl, xml)
print(f"Modified rPr count: {count[0]}")
doc.write_text(new, encoding="utf-8")
