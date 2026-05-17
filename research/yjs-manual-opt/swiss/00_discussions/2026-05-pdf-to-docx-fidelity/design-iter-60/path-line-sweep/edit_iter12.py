"""iter-12: Add black border on the disclaimer cell (tcBorders) on p11.

Replace the disclaimer's tcBorders block with thin black border on all 4 sides.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD_DISCLAIMER_TCBORDERS = """<w:tcBorders>
              <w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>
              <w:left w:val="nil"/>
              <w:bottom w:val="nil"/>
              <w:right w:val="nil"/>
            </w:tcBorders>"""

NEW_DISCLAIMER_TCBORDERS = """<w:tcBorders>
              <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
              <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
              <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
              <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            </w:tcBorders>"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    idx_disc = text.find("免责声明")
    if idx_disc < 0:
        print("DISCLAIMER not found!")
        return 1
    search_region = text[:idx_disc]
    idx_b = search_region.rfind(OLD_DISCLAIMER_TCBORDERS)
    if idx_b < 0:
        print("OLD_DISCLAIMER_TCBORDERS not found!")
        return 1
    print(f"Found at pos {idx_b}")
    new_text = (text[:idx_b] + NEW_DISCLAIMER_TCBORDERS +
                text[idx_b + len(OLD_DISCLAIMER_TCBORDERS):])
    doc.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
