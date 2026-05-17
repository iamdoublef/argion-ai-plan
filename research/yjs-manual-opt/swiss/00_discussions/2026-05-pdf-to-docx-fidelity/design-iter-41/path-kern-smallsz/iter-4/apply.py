"""iter-4: sz=12 spacing 5→8 (22 sites with existing spacing).

Hypothesis: mirror W32 winning move (sz=14 BLACK 5→8) on sz=12 cohort.
Result: 8.28/12.14 (flat). sz=12 spacing UP is wrong direction.
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
    r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="12"/>(?:(?!</w:rPr>).)*?</w:rPr>)',
    re.S,
)
count = [0]
def repl(m):
    block = m.group(0)
    if '<w:spacing w:val="5"/>' in block:
        count[0] += 1
        return block.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return block
new = pattern.sub(repl, xml)
print(f"Modified sz=12 rPr count: {count[0]}")
doc.write_text(new, encoding="utf-8")
