"""iter-12: iter-11 + sz=10 spacing 5→2 (additional 15 sites, 72 total).

Hypothesis: push the small-size-tighten lever to sz=10 too.
Result: 8.28/12.06 — same as iter-11 globally, but p4 +0.06 OVER 0.05 tolerance. ❌
Rejected: sz=10 cohort too sensitive; iter-11 is the cleanest winner.
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

for sz in [10, 11, 12]:
    pat = re.compile(rf'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="{sz}"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
    c = [0]
    def rep(m, sz=sz, c=c):
        b = m.group(0)
        if '<w:spacing w:val="5"/>' in b:
            c[0] += 1
            return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="2"/>')
        return b
    xml = pat.sub(rep, xml)
    print(f"sz={sz} modified: {c[0]}")
doc.write_text(xml, encoding="utf-8")
