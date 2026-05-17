"""iter-9: stack iter-8 (sz=13 BLACK 8->9) + sz=10 RED 8->9 (37 sites).

iter-8 won mean -.01. iter-7 (sz=10 only) tied. Stack to test if they're additive.
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


def apply_pat(xml, sz, color, old_sp, new_sp, font=None):
    pat = re.compile(rf'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="{sz}"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
    c = [0]
    def repl(m):
        b = m.group(0)
        if f'<w:color w:val="{color}"' in b and f'<w:spacing w:val="{old_sp}"/>' in b:
            if font is not None and f'w:ascii="{font}"' not in b:
                return b
            c[0] += 1
            return b.replace(f'<w:spacing w:val="{old_sp}"/>', f'<w:spacing w:val="{new_sp}"/>')
        return b
    return pat.sub(repl, xml), c[0]


# iter-8 cohort
xml, c1 = apply_pat(xml, "13", "000000", "8", "9", font="Arial")
xml, c2 = apply_pat(xml, "13", "000000", "8", "9", font="Arial Black")
# + sz=10 RED 8->9
xml, c10 = apply_pat(xml, "10", "E63846", "8", "9", font="Arial Black")

print(f"sz=13 Arial 8->9: {c1}  sz=13 Arial Black 8->9: {c2}  sz=10 RED 8->9: {c10}")
doc.write_text(xml, encoding="utf-8")
