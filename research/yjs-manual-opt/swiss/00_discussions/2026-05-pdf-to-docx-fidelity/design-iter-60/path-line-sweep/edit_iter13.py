"""iter-13: Black border sz=4 + reduced right padding to single-line wrap."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD_TCB = """<w:tcBorders>
              <w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>
              <w:left w:val="nil"/>
              <w:bottom w:val="nil"/>
              <w:right w:val="nil"/>
            </w:tcBorders>"""

NEW_TCB = """<w:tcBorders>
              <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
              <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
              <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
              <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
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
    search_region = text[:idx_disc]
    idx_b = search_region.rfind(OLD_TCB)
    if idx_b < 0:
        print("OLD_TCB not found!")
        return 1
    new_text = (text[:idx_b] + NEW_TCB + text[idx_b + len(OLD_TCB):])
    doc.write_text(new_text, encoding="utf-8")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
