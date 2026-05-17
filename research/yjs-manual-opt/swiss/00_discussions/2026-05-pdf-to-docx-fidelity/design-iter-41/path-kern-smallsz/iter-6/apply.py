"""iter-6: sz=12 spacing 5→8 + kern val=14 on all sz>=12 rPr (327 sites).

Hypothesis: stacked spacing + universal kern enable.
Result: 8.28/12.14 (flat). Stacking inert levers gives inert outcome.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "baseline_unpacked"
DST = ROOT / "unpacked"

shutil.copytree(SRC, DST, dirs_exist_ok=True)
doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

# A: sz=12 spacing 5→8
pat12 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="12"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c12 = [0]
def r12(m):
    b = m.group(0)
    if '<w:spacing w:val="5"/>' in b:
        c12[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat12.sub(r12, xml)

# B: kern val=14 on all sz>=12 rPr blocks
pat_all = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="(1[2-5])"/>(?:(?!</w:rPr>).)*?)(</w:rPr>)', re.S)
ck = [0]
def rk(m):
    block = m.group(1)
    if '<w:kern' in block:
        return m.group(0)
    ck[0] += 1
    return block + '<w:kern w:val="14"/>' + m.group(3)
xml = pat_all.sub(rk, xml)

print(f"sz=12 spacing: {c12[0]}  kern added: {ck[0]}")
doc.write_text(xml, encoding="utf-8")
