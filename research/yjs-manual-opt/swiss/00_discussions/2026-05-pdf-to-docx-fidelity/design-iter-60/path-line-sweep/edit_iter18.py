"""iter-18: Reduce character spacing on disclaimer body to fit 1 line."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD = """<w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="14"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="10"/>
              </w:rPr>
              <w:t>如果用户不按照本手册操作产品"""

NEW = """<w:rPr>
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
    n = text.count(OLD)
    print(f"OLD count: {n}")
    new_text = text.replace(OLD, NEW)
    doc.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
