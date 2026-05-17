"""iter-1: Stack iter-40 line spacing + iter-41 small-sz spacing.

Baseline: current final/imt050-wevac-eu-cn.docx (iter-40 W33; line edits in p9/p13 already).
NOTE: at execution time, the current final was found to ALREADY contain BOTH stackings
(iter-41 sz=11/sz=12 spacing 5->2 was previously applied but the cached score.json was
stale). This apply.py reproduces iter-41's winning move on top of iter-40's baseline for
documentation. Idempotent: if spacing=5 sites are already converted, the script is a no-op
and reports c11=0, c12=0.

Inputs:
- baseline_unpacked/ = iter-40 W33 final (already pre-stacked in this session).

Outputs:
- iter-1/unpacked/  = post stacking (re-applying iter-41 winning move on iter-40 W33).
- iter-1/output.docx = packed.
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

# A: sz=11 spacing 5 -> 2 (35 sites per iter-41 analysis)
pat11 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="11"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c11 = [0]
def r11(m):
    b = m.group(0)
    if '<w:spacing w:val="5"/>' in b:
        c11[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
    return b
xml = pat11.sub(r11, xml)

# B: sz=12 spacing 5 -> 2 (22 sites: 18 Arial Black + 4 Arial; 11 Courier no spacing)
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
