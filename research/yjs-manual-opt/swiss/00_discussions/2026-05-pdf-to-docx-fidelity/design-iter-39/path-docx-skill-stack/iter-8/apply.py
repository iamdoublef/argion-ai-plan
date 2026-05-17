"""iter-8: Stack iter-7 (sz=14 black 5→9) + sz=13 1A1A1A 5→8."""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
SRC = ROOT / "baseline_unpacked"
DST = HERE / "unpacked"

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

c14 = 0
c13 = 0

def patch(m: re.Match) -> str:
    global c14, c13
    body = m.group(1)
    if 'w:sz w:val="14"' in body and 'w:color w:val="000000"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="9"/>')
        c14 += 1
    elif 'w:sz w:val="13"' in body and 'w:color w:val="1A1A1A"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
        c13 += 1
    return f"<w:rPr>{body}</w:rPr>"

new_xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", patch, xml, flags=re.DOTALL)
print(f"sz=14 black: {c14}, sz=13 1A1A1A: {c13}")
doc.write_text(new_xml, encoding="utf-8")
