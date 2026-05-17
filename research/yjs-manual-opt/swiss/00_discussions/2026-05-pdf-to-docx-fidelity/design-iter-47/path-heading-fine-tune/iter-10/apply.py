"""iter-10: stack iter-8 (sz=13 BLACK 8->9) + try other safe levers.

iter-8 won mean -.01. Try stacking with sz=22 11->12 (was tied solo) — and explore
sz=10 RED Arial 5->8 + 1A1A1A sites which weren't touched. Goal: lock iter-8 plus
find any neutral lever that doesn't break stacking.

Conservative: just iter-8 + sz=15 GRAY/RED orphans 5->8 (1+1 sites) to test orphan UP.
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


# iter-8 cohort (the win)
xml, c1 = apply_pat(xml, "13", "000000", "8", "9", font="Arial")
xml, c2 = apply_pat(xml, "13", "000000", "8", "9", font="Arial Black")
# + orphan sz=30 single site 5->8 UP probe
xml, c30 = apply_pat(xml, "30", "000000", "5", "8", font="Arial Black")
# + orphan sz=36 single site 5->8 UP probe
xml, c36 = apply_pat(xml, "36", "1A1A1A", "5", "8", font="Arial Black")

print(f"sz=13 Arial 8->9: {c1}  Arial Black 8->9: {c2}  sz=30: {c30}  sz=36: {c36}")
doc.write_text(xml, encoding="utf-8")
