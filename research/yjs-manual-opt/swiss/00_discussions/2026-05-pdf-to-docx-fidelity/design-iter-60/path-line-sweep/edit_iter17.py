"""iter-17: Reduce disclaimer cell left/right padding to fit text on 1 line."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD = """<w:tcMar>
              <w:top w:w="46" w:type="dxa"/>
              <w:start w:w="176" w:type="dxa"/>
              <w:bottom w:w="46" w:type="dxa"/>
              <w:end w:w="110" w:type="dxa"/>
            </w:tcMar>"""

NEW = """<w:tcMar>
              <w:top w:w="46" w:type="dxa"/>
              <w:start w:w="60" w:type="dxa"/>
              <w:bottom w:w="46" w:type="dxa"/>
              <w:end w:w="60" w:type="dxa"/>
            </w:tcMar>"""


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    idx = text.find("免责声明")
    if idx < 0:
        return 1
    pre = text[:idx]
    idx_m = pre.rfind(OLD)
    if idx_m < 0:
        print("OLD not found!")
        return 1
    new_text = text[:idx_m] + NEW + text[idx_m + len(OLD):]
    doc.write_text(new_text, encoding="utf-8")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
