"""iter-11 (WINNER): sz=11 + sz=12 spacing 5→2 stacked (57 sites total).

Hypothesis: both small-size cohorts over-spaced; combine the winning moves.
Result: 8.28/12.06 (max -0.08 vs W32 baseline 12.14). ALL gates pass.
- 35 sz=11 sites (RED Arial Black accent)
- 22 sz=12 sites (Arial Black 18 + Arial 4, with spacing=5)
- 11 sz=12 Courier sites untouched (no spacing originally)

Per-page: p5 -0.04, p14 -0.08. Regressions all ≤ +0.04.
Promoted to W33 final.
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

# A: sz=11 spacing 5→2
pat11 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="11"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c11 = [0]
def r11(m):
    b = m.group(0)
    if '<w:spacing w:val="5"/>' in b:
        c11[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat11.sub(r11, xml)

# B: sz=12 spacing 5→2
pat12 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="12"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c12 = [0]
def r12(m):
    b = m.group(0)
    if '<w:spacing w:val="5"/>' in b:
        c12[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat12.sub(r12, xml)

print(f"sz=11 modified: {c11[0]}  sz=12 modified: {c12[0]}")
doc.write_text(xml, encoding="utf-8")
