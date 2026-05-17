"""iter-3: Sweet spot scan — try sz=14 body spacing 5→7 (between 5 and 8)."""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

VALUE = sys.argv[1] if len(sys.argv) > 1 else "7"

SRC = ROOT / "baseline_unpacked"
DST = HERE / "unpacked"

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

def patch(m: re.Match) -> str:
    body = m.group(1)
    if 'w:sz w:val="14"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', f'<w:spacing w:val="{VALUE}"/>')
        patch.count += 1
    return f"<w:rPr>{body}</w:rPr>"

patch.count = 0
new_xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", patch, xml, flags=re.DOTALL)
print(f"patched {patch.count} rPr blocks (sz=14 body) to spacing={VALUE}")

doc.write_text(new_xml, encoding="utf-8")
