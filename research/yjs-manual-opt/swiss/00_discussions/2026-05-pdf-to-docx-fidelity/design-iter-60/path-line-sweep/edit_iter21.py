"""iter-21: iter-18 + reduce disclaimer HEADING char spacing val=10 → 0 too.

The heading "免责声明 DISCLAIMER" has its own rPr with spacing val=10.
Try reducing for just this one.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

# iter-18 change: body text spacing val=10 → val=0
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

# Heading: 免责声明 DISCLAIMER - reduce char spacing
HEADING_OLD = """<w:rPr>
                <w:rFonts w:ascii="Arial Black" w:hAnsi="Arial Black" w:cs="Arial Black" w:eastAsia="Microsoft YaHei"/>
                <w:b/>
                <w:sz w:val="13"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="10"/>
              </w:rPr>
              <w:t>免责声明 DISCLAIMER</w:t>"""

HEADING_NEW = """<w:rPr>
                <w:rFonts w:ascii="Arial Black" w:hAnsi="Arial Black" w:cs="Arial Black" w:eastAsia="Microsoft YaHei"/>
                <w:b/>
                <w:sz w:val="13"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="0"/>
              </w:rPr>
              <w:t>免责声明 DISCLAIMER</w:t>"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    n1 = text.count(BODY_OLD)
    n2 = text.count(HEADING_OLD)
    text = text.replace(BODY_OLD, BODY_NEW)
    text = text.replace(HEADING_OLD, HEADING_NEW)
    print(f"body={n1}, heading={n2}")
    doc.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
