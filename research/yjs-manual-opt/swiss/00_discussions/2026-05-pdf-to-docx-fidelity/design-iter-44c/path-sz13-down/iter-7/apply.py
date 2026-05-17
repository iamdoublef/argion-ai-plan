"""iter-7: GRAY-only sz=13 spacing 5 -> 3 (sub-pixel variant of iter-5 winner).

iter-3 (all 5->3) tied iter-2 (all 5->2). Test whether GRAY-only 5->3 is equal/better
than GRAY-only 5->2 (iter-5). If equal, smaller change is safer.
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
    if '<w:color w:val="1A1A1A"' in b and '<w:spacing w:val="5"/>' in b:
        c[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="3"/>')
    return b
xml = pat.sub(repl, xml)

print(f"sz=13 GRAY-only spacing 5->3 modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
