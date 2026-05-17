"""iter-10: iter-8 (5->11 22/27, BLACK 13 5->8) + sz=10 RED 5->8 (13 sites).

Last untested small-size lever. sz=10 RED Arial Black (small accent text) at sp=5.
Parallel to BLACK 14 UP win, try same UP direction.
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
xml, c10 = apply_pat(xml, "10", "E63846", "5", "8")

print(f"sz=22: {c22}  sz=27: {c27}  sz=13: {c13}  sz=10 RED 5->8: {c10}")
doc.write_text(xml, encoding="utf-8")
