"""iter-14: Darken the p11 right-banner text 'CH.07 - TROUBLESHOOTING' to match target.

The current color is F5F5F5 (nearly white). Target shows mid-gray. Try 808080.
Limit replacement to within p11 region.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_p11_region(text):
    positions = [m.start() for m in re.finditer(r'<w:sectPr', text)]
    if len(positions) < 12:
        return 226559, 272001
    return positions[10], positions[11]


OLD_RUN = """<w:rPr>
          <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Microsoft YaHei"/>
          <w:b w:val="0"/>
          <w:sz w:val="10"/>
          <w:color w:val="F5F5F5"/>
        </w:rPr>"""

NEW_RUN = """<w:rPr>
          <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Microsoft YaHei"/>
          <w:b w:val="0"/>
          <w:sz w:val="10"/>
          <w:color w:val="808080"/>
        </w:rPr>"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    p11s, p11e = find_p11_region(text)
    page = text[p11s:p11e]
    new_page = page.replace(OLD_RUN, NEW_RUN, 1)  # only first occurrence in p11
    n = 1 if new_page != page else 0
    print(f"replacements: {n}")
    if n == 0:
        return 1
    new_text = text[:p11s] + new_page + text[p11e:]
    doc.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
