"""iter-6: Stack — sz=14 body 5→9 (88 sites, winning), plus expand to sz=13 5→8 (143 sites)."""
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

count_14 = 0
count_13 = 0

def patch(m: re.Match) -> str:
    global count_14, count_13
    body = m.group(1)
    if 'w:sz w:val="14"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="9"/>')
        count_14 += 1
    elif 'w:sz w:val="13"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
        count_13 += 1
    return f"<w:rPr>{body}</w:rPr>"

new_xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", patch, xml, flags=re.DOTALL)
print(f"sz=14 patched: {count_14}, sz=13 patched: {count_13}")
doc.write_text(new_xml, encoding="utf-8")
