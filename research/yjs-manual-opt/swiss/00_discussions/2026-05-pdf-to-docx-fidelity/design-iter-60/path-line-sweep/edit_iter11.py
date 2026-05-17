"""iter-11: Add black border around the disclaimer table on p11.

Replace the disclaimer table's tblBorders nil block with a thin black border
on all 4 sides (matching the target PDF visual).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD_DISCLAIMER_BORDERS = """<w:tblBorders>
          <w:top w:val="nil"/>
          <w:left w:val="nil"/>
          <w:bottom w:val="nil"/>
          <w:right w:val="nil"/>
          <w:insideH w:val="nil"/>
          <w:insideV w:val="nil"/>
        </w:tblBorders>"""

NEW_DISCLAIMER_BORDERS = """<w:tblBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideH w:val="nil"/>
          <w:insideV w:val="nil"/>
        </w:tblBorders>"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")

    # Need to find the SECOND occurrence (disclaimer is the second tbl in p11)
    # First locate disclaimer
    idx_disc = text.find("免责声明")
    if idx_disc < 0:
        print("DISCLAIMER not found!")
        return 1
    # Find the most recent tblBorders nil block before disclaimer
    search_region = text[:idx_disc]
    idx_borders = search_region.rfind(OLD_DISCLAIMER_BORDERS)
    if idx_borders < 0:
        print("OLD_DISCLAIMER_BORDERS not found before disclaimer!")
        return 1
    print(f"Found disclaimer tblBorders at pos {idx_borders}")
    new_text = (text[:idx_borders] + NEW_DISCLAIMER_BORDERS +
                text[idx_borders + len(OLD_DISCLAIMER_BORDERS):])
    doc.write_text(new_text, encoding="utf-8")
    print("Wrote.")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
