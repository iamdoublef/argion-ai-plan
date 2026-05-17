"""iter-9: page-14 differential — try a LARGER bump line=240 -> 250 (+10).
iter-8 with +4 was inert. Try larger swing in same direction.
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

p_pat = re.compile(r"<w:p\b[^>]*>.*?</w:p>", re.S)
TARGET_RANGE = (277, 306)  # page 14
c = [0]

out_parts = []
prev_end = 0
for i, m in enumerate(p_pat.finditer(xml)):
    out_parts.append(xml[prev_end:m.start()])
    p_xml = m.group(0)
    if TARGET_RANGE[0] <= i <= TARGET_RANGE[1]:
        new_p = re.sub(r'(<w:spacing\b[^/]*?)w:line="240"([^/]*?/>)',
                       lambda mm: mm.group(1) + 'w:line="250"' + mm.group(2),
                       p_xml)
        if new_p != p_xml:
            c[0] += 1
        out_parts.append(new_p)
    else:
        out_parts.append(p_xml)
    prev_end = m.end()
out_parts.append(xml[prev_end:])
new_xml = "".join(out_parts)
print(f"page-14 differential line=240->250: {c[0]} sites in paras {TARGET_RANGE}")
doc.write_text(new_xml, encoding="utf-8")
