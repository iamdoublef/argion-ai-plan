"""iter-9: iter-8 + push sz=22/27 even further (5->14). Heading saturation test.

iter-8 (5->11) won marginal. Try 5->14 to find the local max on heading cohort.
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

xml, c22 = apply_pat(xml, "22", "000000", "5", "14")
xml, c27 = apply_pat(xml, "27", "E63846", "5", "14")
xml, c13 = apply_pat(xml, "13", "000000", "5", "8")

print(f"sz=22 5->14: {c22}  sz=27 5->14: {c27}  sz=13 BLACK 5->8: {c13}")
doc.write_text(xml, encoding="utf-8")
