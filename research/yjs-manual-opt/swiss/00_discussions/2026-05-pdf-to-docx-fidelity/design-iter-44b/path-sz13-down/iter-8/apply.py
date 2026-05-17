"""iter-8: sz=13 GRAY-only 5->2 (117 sites). Check if pure GRAY cohort yields better
per-page balance than iter-2 (broad 143 incl. ArialBlack 17 + Arial-BLACK 9).
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
    has_gray = '<w:color w:val="1A1A1A"' in b
    has_sp5 = '<w:spacing w:val="5"/>' in b
    if has_gray and has_sp5:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat.sub(repl, xml)
print(f"sz=13 GRAY spacing 5->2 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
