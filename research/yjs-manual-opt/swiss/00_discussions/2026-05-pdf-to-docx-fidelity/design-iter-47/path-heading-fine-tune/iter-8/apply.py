"""iter-8: sz=13 BLACK sp=8 -> sp=9 (50 sites).

Smaller step probe. iter-3 showed 8->11 regressed badly (+.93 on p3). Test 8->9.
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


xml, c1 = apply_pat(xml, "13", "000000", "8", "9", font="Arial")
xml, c2 = apply_pat(xml, "13", "000000", "8", "9", font="Arial Black")

print(f"sz=13 BLACK Arial 8->9: {c1}  Arial Black 8->9: {c2}")
doc.write_text(xml, encoding="utf-8")
