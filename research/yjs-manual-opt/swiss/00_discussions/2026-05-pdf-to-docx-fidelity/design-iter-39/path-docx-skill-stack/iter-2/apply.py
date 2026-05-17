"""iter-2: Apply iter-35 winning move on W30 final baseline.

Change w:spacing w:val="5" → "8" inside every rPr block that contains w:sz w:val="14".
This is the +3 twip lever that worked for iter-35 (W27 baseline) — boss requested
we stack it on top of W30 final (which contains iter-36 margin + iter-37 design fixes).
"""
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

# Find every rPr block; rewrite spacing=5→8 only when sz=14 is also present.
def patch(m: re.Match) -> str:
    body = m.group(1)
    if 'w:sz w:val="14"' in body and 'w:spacing w:val="5"' in body:
        body = body.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>')
        patch.count += 1
    return f"<w:rPr>{body}</w:rPr>"

patch.count = 0
new_xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", patch, xml, flags=re.DOTALL)
print(f"patched {patch.count} rPr blocks (sz=14 body)")
assert patch.count == 88, f"expected 88, got {patch.count}"

doc.write_text(new_xml, encoding="utf-8")
print(f"Written: {doc}")
