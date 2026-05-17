"""iter-5: STACKED iter-4 + sz=11 RED 2->0 (35 sites). Push RED bullets further DOWN.

sz=11 cohort is all RED Arial Black at spacing=2 (from W33). Try 2->0 (parallel to sz=12
already at 2, but sz=11 RED might want even tighter).
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

# iter-4 base
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

xml, c22 = apply_pat(xml, "22", "000000", "5", "8")
xml, c27 = apply_pat(xml, "27", "E63846", "5", "8")
xml, c13 = apply_pat(xml, "13", "000000", "5", "8")
xml, c11 = apply_pat(xml, "11", "E63846", "2", "0")

print(f"sz=22 BLACK 5->8: {c22}  sz=27 RED 5->8: {c27}  sz=13 BLACK 5->8: {c13}  sz=11 RED 2->0: {c11}")
doc.write_text(xml, encoding="utf-8")
