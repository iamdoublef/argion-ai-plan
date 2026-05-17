"""iter-8: STACKED iter-4 + push sz=22/27 further (5->11). Test heading UP saturation.

iter-3/4 confirmed sz=22 BLACK + sz=27 RED 5->8 wins. Try 5->11 (bigger UP) to see
if heading cohort has more slack.
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

def apply_pat(xml, sz, color, old_sp, new_sp):
    pat = re.compile(rf'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="{sz}"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
    c = [0]
    def repl(m):
        b = m.group(0)
        if f'<w:color w:val="{color}"' in b and f'<w:spacing w:val="{old_sp}"/>' in b:
            c[0] += 1
            return b.replace(f'<w:spacing w:val="{old_sp}"/>', f'<w:spacing w:val="{new_sp}"/>')
        return b
    return pat.sub(repl, xml), c[0]

xml, c22 = apply_pat(xml, "22", "000000", "5", "11")
xml, c27 = apply_pat(xml, "27", "E63846", "5", "11")
xml, c13 = apply_pat(xml, "13", "000000", "5", "8")

print(f"sz=22 5->11: {c22}  sz=27 5->11: {c27}  sz=13 BLACK 5->8: {c13}")
doc.write_text(xml, encoding="utf-8")
