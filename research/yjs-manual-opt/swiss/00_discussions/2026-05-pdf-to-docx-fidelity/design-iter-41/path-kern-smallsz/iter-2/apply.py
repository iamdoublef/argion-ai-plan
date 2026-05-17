"""iter-2: add w:kern w:val="2" to sz=14 BLACK rPr (71 sites).

Hypothesis: low-threshold kerning enables LO to apply kern pairs on body sz=14 BLACK
text — possibly tightens letter pairs slightly.
Result: 8.28/12.14 (flat) — kern val=2 is effectively inert in LO Writer.
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
    r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="14"/>(?:(?!</w:rPr>).)*?<w:color w:val="000000"/>(?:(?!</w:rPr>).)*?)(</w:rPr>)',
    re.S,
)
count = [0]
def repl(m):
    block = m.group(1)
    if '<w:kern' in block:
        return m.group(0)
    count[0] += 1
    return block + '<w:kern w:val="2"/>' + m.group(2)

new = pattern.sub(repl, xml)
print(f"Modified rPr count: {count[0]}")
doc.write_text(new, encoding="utf-8")
