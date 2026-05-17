"""iter-10: Stack iter-7 (sz=14 black 5→9) + sz=14 white 5→7 (gentler since titles are wider letters)."""
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

cb = 0
cw = 0
def patch(m: re.Match) -> str:
    global cb, cw
    body = m.group(1)
    if 'w:sz w:val="14"' in body and 'w:color w:val="000000"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
        cb += 1
    elif 'w:sz w:val="14"' in body and 'w:color w:val="FFFFFF"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="7"/>')
        cw += 1
    return f"<w:rPr>{body}</w:rPr>"

new_xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", patch, xml, flags=re.DOTALL)
print(f"sz=14 black: {cb}, sz=14 white: {cw}")
doc.write_text(new_xml, encoding="utf-8")
