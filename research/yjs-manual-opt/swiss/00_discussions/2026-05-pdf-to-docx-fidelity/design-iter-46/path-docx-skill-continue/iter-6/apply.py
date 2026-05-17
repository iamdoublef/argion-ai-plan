"""iter-6: STACKED iter-4 + sz=15 BLACK 5->8 retry under iter-4 stack.

iter-1 alone showed sz=15 5->8 regression solo (mean 8.19->8.22). But maybe in
combination with iter-3/4 heading-cohort UP wins, it could re-tune (or confirm regression).
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

xml, c22 = apply_pat(xml, "22", "000000", "5", "8")
xml, c27 = apply_pat(xml, "27", "E63846", "5", "8")
xml, c13 = apply_pat(xml, "13", "000000", "5", "8")
xml, c15 = apply_pat(xml, "15", "000000", "5", "8")

print(f"sz=22 BLACK 5->8: {c22}  sz=27 RED 5->8: {c27}  sz=13 BLACK 5->8: {c13}  sz=15 BLACK 5->8: {c15}")
doc.write_text(xml, encoding="utf-8")
