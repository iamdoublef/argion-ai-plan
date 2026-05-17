"""iter-5: sz=11 spacing 5→8 (35 sites, all RED Arial Black accent).

Hypothesis: mirror W32 winning move on sz=11 cohort.
Result: 8.29/12.17 (REGRESSION). sz=11 spacing UP is wrong direction.
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
    r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="11"/>(?:(?!</w:rPr>).)*?</w:rPr>)',
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
print(f"Modified sz=11 rPr count: {count[0]}")
doc.write_text(new, encoding="utf-8")
