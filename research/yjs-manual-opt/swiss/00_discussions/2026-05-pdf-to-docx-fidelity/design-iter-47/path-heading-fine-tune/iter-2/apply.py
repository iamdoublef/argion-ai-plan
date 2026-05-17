"""iter-2: sz=10 RED Arial Black sp=8 -> sp=11 (37 sites).

Hypothesis: extend heading-cohort UP pattern from iter-46. sz=10 RED already moved
5->8 in iter-46. Push 8->11 to test if same UP saturation pattern holds.
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


xml, c10 = apply_pat(xml, "10", "E63846", "8", "11", font="Arial Black")

print(f"sz=10 RED Arial Black 8->11: {c10}")
doc.write_text(xml, encoding="utf-8")
