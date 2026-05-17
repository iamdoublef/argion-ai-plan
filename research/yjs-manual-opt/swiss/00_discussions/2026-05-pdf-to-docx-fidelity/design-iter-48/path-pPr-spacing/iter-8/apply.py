"""iter-8: Differential per-page approach.
Section boundaries (sectPr-bearing paragraph indices):
[9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
So:
  page 1: paras 0..9
  page 2: 10..22
  page 3: 23..53
  page 4: 54..69
  page 5: 70..88
  page 6: 89..112
  page 7: 113..129
  page 8: 130..168
  page 9: 169..183
  page 10: 184..200
  page 11: 201..237
  page 12: 238..255
  page 13: 256..276
  page 14: 277..306
  page 15: 307..327

Worst page: p14 (11.97). Target ONLY paras 277..306. Try line=240 -> 244 (loosen +2) for this range.
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

# Walk paragraphs with index awareness.
p_pat = re.compile(r"<w:p\b[^>]*>.*?</w:p>", re.S)
TARGET_RANGE = (277, 306)  # page 14
results = []
c = [0]
def replace_line_in(p_xml):
    return re.sub(r'(<w:spacing\b[^/]*?)w:line="240"([^/]*?/>)',
                  lambda mm: mm.group(1) + 'w:line="244"' + mm.group(2),
                  p_xml)

out_parts = []
prev_end = 0
for i, m in enumerate(p_pat.finditer(xml)):
    out_parts.append(xml[prev_end:m.start()])
    p_xml = m.group(0)
    if TARGET_RANGE[0] <= i <= TARGET_RANGE[1]:
        new_p = replace_line_in(p_xml)
        if new_p != p_xml:
            c[0] += 1
        out_parts.append(new_p)
    else:
        out_parts.append(p_xml)
    prev_end = m.end()
out_parts.append(xml[prev_end:])
new_xml = "".join(out_parts)
print(f"page-14 differential line=240->244: {c[0]} sites in paras {TARGET_RANGE}")
doc.write_text(new_xml, encoding="utf-8")
