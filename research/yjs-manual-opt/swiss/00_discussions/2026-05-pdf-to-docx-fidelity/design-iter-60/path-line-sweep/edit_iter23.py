"""iter-23: iter-22 + extend val=2→0 to p12,p13,p14 too."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_sections(text):
    return [m.start() for m in re.finditer(r'<w:sectPr', text)]


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


def apply(iter_name: str, pages_to_edit=(10, 11, 12, 13)):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")

    text = text.replace(BODY_OLD, BODY_NEW)

    sections = find_sections(text)

    # Edit val=2→0 in selected pages (sections, 0-indexed)
    # Edit from right-to-left to preserve positions
    for idx in sorted(pages_to_edit, reverse=True):
        if idx >= len(sections) - 1 or idx < 0:
            continue
        s, e = sections[idx], sections[idx+1]
        page = text[s:e]
        new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
        text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. pages edited: {pages_to_edit}")
    return 0


if __name__ == "__main__":
    pages = (10, 11, 12, 13)  # p11,p12,p13,p14 (0-indexed)
    if len(sys.argv) > 2:
        pages = tuple(int(x) for x in sys.argv[2].split(','))
    sys.exit(apply(sys.argv[1], pages))
