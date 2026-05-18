"""iter-3: w:spacing val=5 → 7 (global, 33 sites)."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    n = text.count('<w:spacing w:val="5"/>')
    text = text.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="7"/>')
    doc.write_text(text, encoding="utf-8")
    print(f"done. spacing val=5->7: {n} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
