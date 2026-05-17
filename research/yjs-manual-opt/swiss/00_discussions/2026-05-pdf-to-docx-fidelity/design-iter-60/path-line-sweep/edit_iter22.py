"""iter-22: iter-18 + reduce char spacing val=2 → 0 within p11 only."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_p11(text):
    positions = [m.start() for m in re.finditer(r'<w:sectPr', text)]
    if len(positions) < 12:
        return 226559, 272001
    return positions[10], positions[11]


BODY_OLD = """<w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="14"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="10"/>
              </w:rPr>
              <w:t>如果用户不按照本手册操作产品"""

BODY_NEW = """<w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="14"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="0"/>
              </w:rPr>
              <w:t>如果用户不按照本手册操作产品"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")

    # iter-18 base
    text = text.replace(BODY_OLD, BODY_NEW)

    # P11 only: val=2 → 0
    p11s, p11e = find_p11(text)
    pre = text[:p11s]; page = text[p11s:p11e]; post = text[p11e:]
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    text = pre + new_page + post
    doc.write_text(text, encoding="utf-8")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
