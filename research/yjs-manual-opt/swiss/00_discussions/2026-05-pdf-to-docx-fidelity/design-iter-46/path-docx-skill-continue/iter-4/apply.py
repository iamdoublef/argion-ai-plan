"""iter-4: STACKED iter-3 + sz=13 BLACK 5->8 (26 sites). Test UP direction on BLACK 13.

W34 noted sz=13 BLACK 5->2 was inert. Try UP instead (parallel to sz=14 W32 win).
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

# iter-3 base: sz=22 BLACK 5->8 + sz=27 RED 5->8
pat22 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="22"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c22 = [0]
def repl22(m):
    b = m.group(0)
    if '<w:color w:val="000000"' in b and '<w:spacing w:val="5"/>' in b:
        c22[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat22.sub(repl22, xml)

pat27 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="27"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c27 = [0]
def repl27(m):
    b = m.group(0)
    if '<w:color w:val="E63846"' in b and '<w:spacing w:val="5"/>' in b:
        c27[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat27.sub(repl27, xml)

# new: sz=13 BLACK 5->8
pat13 = re.compile(r'(<w:rPr>(?:(?!</w:rPr>).)*?<w:sz w:val="13"/>(?:(?!</w:rPr>).)*?</w:rPr>)', re.S)
c13 = [0]
def repl13(m):
    b = m.group(0)
    if '<w:color w:val="000000"' in b and '<w:spacing w:val="5"/>' in b:
        c13[0] += 1
        return b.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
    return b
xml = pat13.sub(repl13, xml)

print(f"sz=22 BLACK 5->8: {c22[0]}  sz=27 RED 5->8: {c27[0]}  sz=13 BLACK 5->8: {c13[0]}")
doc.write_text(xml, encoding="utf-8")
